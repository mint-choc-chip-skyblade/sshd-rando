from collections import defaultdict
from dataclasses import dataclass

from constants.configconstants import TRACKER_NOTE_EVENTS
from ..item_pool import get_complete_item_pool
from ..search import Search, SearchMode
from ..requirements import (
    Requirement,
    RequirementType,
    ALL_TODS,
    evaluate_requirement_at_time,
    visit_requirement,
)
from typing import Callable
from constants.trackerprettyitems import PRETTY_ITEM_NAMES
from ..world import World, TOD, LocationAccess
from ..entrance import Entrance
from ..area import EventAccess, Area
from .bits import BitIndex, DNF
from .simplify_algebraic import dnf_to_expr


@dataclass
class TrackerNoteEvent:
    id: int
    name: str
    internal_name: str
    known_unreachable: bool


class TooltipsSearch:
    """
    A variant of the Search class that computes tooltip expressions instead
    of boolean logical state.

    Instead of exploring the area graph until no new things are in logic,
    we explore the area graph until tooltip requirements don't change,
    at which point we have closed-form logical expressions.
    """

    def __init__(
        self,
        world_: "World",
    ) -> None:
        self.world = world_

        # figure out if we can possibly reach the bazaar, to provide more helpful
        # tooltips for stuff that depends on item check access or shield purchases
        item_pool = get_complete_item_pool([self.world])
        search = Search(SearchMode.ACCESSIBLE_LOCATIONS, [self.world], item_pool)
        search.search_worlds()

        self.note_event_ids: dict[int, TrackerNoteEvent] = {}
        for internal_name, name in TRACKER_NOTE_EVENTS.items():
            id = self.world.events[internal_name]
            self.note_event_ids[id] = TrackerNoteEvent(
                id, name, internal_name, id not in search.owned_events
            )

        self.bitindex = BitIndex()

        # partially computed requirements for areas at a
        # given time of day and for events
        self.event_exprs: dict[int, DNF] = defaultdict(DNF.false)
        self.area_exprs_tod: dict[int, dict[int, DNF]] = {
            TOD.DAY: defaultdict(DNF.false),
            TOD.NIGHT: defaultdict(DNF.false),
        }

        # nodes we haven't looked at we don't even need to bother with
        self.exits_to_try: set[Entrance] = set()
        self.events_to_try: set[EventAccess] = set()
        self.areas_to_try: set[Area] = set()

        # we only re-check an exit or an event if its dependencies changed.
        # dependencies can be the implicit parent area (for events and exits),
        # the opposite-TOD area (for sleeping), and "remote" requirements arising
        # from the expression itself mentioning an event or an area via can_access
        self.recently_updated_areas: set[int] = set()
        self.recently_updated_events: set[int] = set()

        self.newly_updated_areas: set[int] = set()
        self.newly_updated_events: set[int] = set()

        self.remote_requirements: dict[str, dict[Entrance | EventAccess, set[int]]] = {
            "event": defaultdict(lambda: set()),
            "area": defaultdict(lambda: set()),
        }

        for area in self.world.areas.values():

            def visitor(thing):
                def handler(req: Requirement):
                    if req.type == RequirementType.EVENT:
                        self.remote_requirements["event"][thing].add(req.args[0])
                    elif req.type == RequirementType.CAN_ACCESS:
                        self.remote_requirements["area"][thing].add(req.args[0])

                return handler

            for exit in area.exits:
                visit = visitor(exit)
                visit_requirement(exit.requirement, visit)

            for event in area.events:
                visit = visitor(event)
                visit_requirement(event.req, visit)

        # we start with the starting exit, both day and night following
        # the comment in Search
        self.area_exprs_tod[TOD.DAY][self.world.root.id] = DNF.true()
        self.area_exprs_tod[TOD.NIGHT][self.world.root.id] = DNF.true()
        self.newly_updated_areas.add(self.world.root.id)
        self.new_things_found = True

        for exit in self.world.root.exits:
            if exit.connected_area is not None:
                self.exits_to_try.add(exit)
                assert exit.parent_area == self.world.root

    def do_search(self):
        # This algorithm works in three stages:
        # 1. Compute area and event requirements -> DNFs
        # 2. Compute location requirement -> DNF
        # 3. Simplify location requirement -> Requirement
        import time

        start = time.time()
        # This is step 1. This computes everything that requirements
        # can depend on in a fixpoint algorithm - namely, areas at given
        # times-of-day and events.
        self.new_things_found = True
        while self.new_things_found:
            self.recently_updated_areas = self.newly_updated_areas
            self.recently_updated_events = self.newly_updated_events
            self.newly_updated_areas = set()
            self.newly_updated_events = set()
            self.new_things_found = False
            # try to reach areas in new ways through exits
            self.try_exits()
            # try to acquire events in new ways
            self.try_events()
            # try to reach areas in new ways by sleeping
            self.try_sleep()

        print("area/event requirements search", time.time() - start)

        start = time.time()

        item_locations: dict[int, list[LocationAccess]] = {}
        for area in self.world.areas.values():
            for loc_access in area.locations:
                if not loc_access.location.id in item_locations:
                    item_locations[loc_access.location.id] = []
                item_locations[loc_access.location.id].append(loc_access)

        # TODO this immediately combines the "local" requirements with the implicit
        # area requirement. It has been hypothesized that converting them
        # separately may produce better tooltips, but at that point you need the
        # TWWR-Tracker boolean-expression multi-level simplification code

        # step 2: for every location, OR all the ways to access it
        for access_list in item_locations.values():
            expr = DNF.false()
            for access in access_list:
                expr = expr.or_(
                    self.try_access_at_time(access, TOD.DAY).or_(
                        self.try_access_at_time(access, TOD.NIGHT)
                    )
                )
            # step 3: simplify
            access.location.computed_requirement = dnf_to_expr(self.bitindex, expr)

        # same thing for exits
        for area in self.areas_to_try:
            for exit in area.exits:
                if not exit.shuffled:
                    # only shuffled entrances are shown in the tracker UI
                    continue
                expr = DNF.false()
                for tod in ALL_TODS:
                    valid_tods = self.world.exit_time_cache.get(exit, TOD.ALL)
                    if not (valid_tods & tod):
                        continue
                    expr = expr.or_(self.try_exit_at_time(exit, tod))

                exit.computed_requirement = dnf_to_expr(self.bitindex, expr)

        print("location requirements search and simplification", time.time() - start)

    def was_updated(self, area: Area, thing: "Entrance|EventAccess"):
        """Check for a thing in area whether its logical dependencies
        have recently been updated.
        """
        if area.id in self.recently_updated_areas:
            # if the parent area's computed requirements changed,
            # this thing's computed requirements may change too
            return True
        remote_event_req = self.remote_requirements["event"][thing]
        if self.recently_updated_events & remote_event_req:
            # if the expression mentions an event and that event's computed
            # requirements changed, this thing's requirements may change
            return True
        remote_area_req = self.remote_requirements["area"][thing]
        if self.recently_updated_areas & remote_area_req:
            # if the expression requires can_access(area) and that area's computed
            # requirements changed, this thing's requirements may change
            return True

        return False

    def try_exits(self):
        for exit in [*self.exits_to_try]:
            if not self.was_updated(exit.parent_area, exit):
                continue

            for tod in ALL_TODS:
                valid_tods = self.world.exit_time_cache.get(exit, TOD.ALL)
                if not (valid_tods & tod & exit.connected_area.allowed_tod):
                    continue

                old_expr = self.area_exprs_tod[tod][exit.connected_area.id]
                new_partial = self.try_exit_at_time(exit, tod)
                useful, new_expr = old_expr.or_useful(new_partial)
                if useful:
                    self.newly_updated_areas.add(exit.connected_area.id)
                    self.new_things_found = True
                    self.area_exprs_tod[tod][exit.connected_area.id] = new_expr.dedup()
                    self.events_to_try.update(exit.connected_area.events)
                    self.exits_to_try.update(
                        [
                            e
                            for e in exit.connected_area.exits
                            if e.connected_area is not None
                        ]
                    )
                    self.areas_to_try.add(exit.connected_area)

    def try_events(self):
        for event in self.events_to_try:
            if not self.was_updated(event.area, event):
                continue

            old_expr = self.event_exprs[event.id]
            new_partial = self.try_access_at_time(event, TOD.DAY).or_(
                self.try_access_at_time(event, TOD.NIGHT)
            )
            useful, new_expr = old_expr.or_useful(new_partial)
            if useful:
                self.newly_updated_events.add(event.id)
                self.new_things_found = True
                self.event_exprs[event.id] = new_expr.dedup()

    def try_sleep(self):
        for area in self.areas_to_try:
            if area.can_sleep:
                if not area.id in self.recently_updated_areas:
                    continue
                for tod in ALL_TODS:
                    # NB no need to check allowed_tod since can_sleep should
                    # imply that both TODs are valid
                    old_expr = self.area_exprs_tod[tod][area.id]
                    opposite_tod = TOD.DAY if tod == TOD.NIGHT else TOD.NIGHT
                    new_partial = self.area_exprs_tod[opposite_tod][area.id]
                    if not new_partial.is_trivially_false():
                        useful, new_expr = old_expr.or_useful(new_partial)
                        if useful:
                            self.newly_updated_areas.add(area.id)
                            self.new_things_found = True
                            self.area_exprs_tod[tod][area.id] = new_expr.dedup()

    def try_access_at_time(
        self, access: "EventAccess | LocationAccess", tod: int
    ) -> DNF:
        return self.area_exprs_tod[tod][access.area.id].and_(
            evaluate_partial_requirement(self.bitindex, access.req, self, tod)
        )

    def try_exit_at_time(
        self,
        exit: Entrance,
        tod: int,
    ):
        return self.area_exprs_tod[tod][exit.parent_area.id].and_(
            evaluate_partial_requirement(self.bitindex, exit.requirement, self, tod)
        )


def print_req(req: Requirement) -> str:
    """Debugging function for tests."""
    match req.type:
        case RequirementType.IMPOSSIBLE:
            return "Impossible"
        case RequirementType.NOTHING:
            return "Nothing"
        case RequirementType.ITEM:
            return f"{req.args[0]}"
        case RequirementType.COUNT:
            return f"{req.args[1]} x {req.args[0]}"
        case RequirementType.WALLET_CAPACITY:
            return "Wallet >= " + str(req.args[0])
        case RequirementType.GRATITUDE_CRYSTALS:
            return "Gratitude Crystals >= " + str(req.args[0])
        case RequirementType.TRACKER_NOTE:
            return req.args[2]
        case RequirementType.OR:
            return "(" + " or ".join([print_req(a) for a in req.args]) + ")"

        case RequirementType.AND:
            return "(" + " and ".join([print_req(a) for a in req.args]) + ")"

        case _:
            raise ValueError("unreachable")


def evaluate_partial_requirement(
    bit_index: BitIndex, req: Requirement, search: "TooltipsSearch", time: int
) -> DNF:
    """Turns the requirement `req` at a given time of day into a DNF expression
    that depends only on items. can_access and event requirements are inlined
    from the computed requirements in `search`.
    """
    match req.type:
        case RequirementType.IMPOSSIBLE:
            return DNF.false()
        case RequirementType.NOTHING:
            return DNF.true()
        case (
            RequirementType.ITEM
            | RequirementType.WALLET_CAPACITY
            | RequirementType.GRATITUDE_CRYSTALS
        ):
            return DNF([1 << bit_index.req_bit(req)])

        case RequirementType.COUNT:
            # count requirements frequently have to unify with weaker terms,
            # so a count requirement always requires all lesser item counts too.
            # this ensures redundant terms can be eliminated
            [count, item] = req.args
            bits = 0
            for i in range(1, count + 1):
                if i == 1:
                    new_req = Requirement(RequirementType.ITEM, [item])
                else:
                    new_req = Requirement(RequirementType.COUNT, [i, item])
                bits |= 1 << bit_index.req_bit(new_req)
            return DNF([bits])

        case RequirementType.OR:
            d = DNF.false()
            for r in req.args:
                d = d.or_(evaluate_partial_requirement(bit_index, r, search, time))
            return d

        case RequirementType.AND:
            d = DNF.true()
            for r in req.args:
                d = d.and_(evaluate_partial_requirement(bit_index, r, search, time))
            return d

        case RequirementType.NOT:
            raise ValueError("NOT is unsound and logic cannot model it")

        case RequirementType.EVENT:
            id = req.args[0]
            expr = search.event_exprs[id]
            if id in search.note_event_ids:
                note = search.note_event_ids[id]
                # for the item check (and similar), we adjust the
                # displayed logic by creating an opaque wrapper
                # requirement for this event
                bazaar_req = Requirement(
                    RequirementType.TRACKER_NOTE, [id, req, note.name]
                )
                bazaar_dnf = DNF([1 << bit_index.req_bit(bazaar_req)])
                if note.known_unreachable:
                    # If the user cannot reach the item check ever, simply return
                    # an "item check" requirement that will ensure the path
                    # isn't discarded entirely with "Impossible"
                    # Double check that there really is no path
                    assert expr.is_trivially_false()
                    return bazaar_dnf
                else:
                    # otherwise add an *additional* requirement that
                    # won't be useful but will be shown in tooltips
                    expr = expr.and_(bazaar_dnf)
            return expr

        case RequirementType.CAN_ACCESS:
            area_id = req.args[0]
            return search.area_exprs_tod[TOD.DAY][area_id].or_(
                search.area_exprs_tod[TOD.NIGHT][area_id]
            )

        case RequirementType.CUSTOM_FUNCTION:
            # TODO
            raise NotImplementedError("not implemented")

        case RequirementType.DAY:
            return DNF.true() if time & TOD.DAY else DNF.false()

        case RequirementType.NIGHT:
            return DNF.true() if time & TOD.NIGHT else DNF.false()


def num_terms(req: Requirement):
    if req.type == RequirementType.AND or req.type == RequirementType.OR:
        return sum(map(num_terms, req.args))
    return 1


def sort_requirement(req: Requirement):
    def by_length(req: Requirement):
        if req.type == RequirementType.AND or req.type == RequirementType.OR:
            return num_terms(req)
        return -1

    def by_item(req: Requirement):
        if req.type == RequirementType.ITEM:
            return pretty_name(req.args[0].name, 1)
        elif req.type == RequirementType.COUNT:
            return pretty_name(req.args[1].name, req.args[0])
        elif req.type == RequirementType.AND or req.type == RequirementType.OR:
            return by_item(req.args[0])
        elif req.type == RequirementType.TRACKER_NOTE:
            return req.args[2]
        return ""

    def sort_key(req: Requirement):
        return (by_length(req), by_item(req))

    if req.type == RequirementType.AND or req.type == RequirementType.OR:
        for expr in req.args:
            sort_requirement(expr)
        req.args.sort(key=sort_key)


def pretty_name(item, count):
    if (pretty_name := PRETTY_ITEM_NAMES.get((item, count), None)) is not None:
        return pretty_name

    if count > 1:
        return f"{item} x {count}"
    else:
        return item
