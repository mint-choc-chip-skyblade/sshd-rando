from .world import *

import logging


class SearchMode:
    ACCESSIBLE_LOCATIONS: int = 0
    GAME_BEATABLE: int = 1
    ALL_LOCATIONS_REACHABLE: int = 2
    GENERATE_PLAYTHROUGH: int = 3


class Search:
    def __init__(
        self,
        search_mode_: int,
        worlds_: list[World],
        items_: list[Item] = [],
        world_to_search_: int = -1,
    ) -> None:
        self.search_mode: int = search_mode_
        self.worlds: list[World] = worlds_
        self.world_to_search: int = world_to_search_

        # Search variables
        self.sphere_num: int = 0
        self.new_things_found: bool = True
        self.is_beatable: bool = False
        self.collect_items: bool = True
        self.owned_events: set[int] = set()
        self.owned_items: Counter[Item] = Counter(items_)

        self.events_to_try: list[EventAccess] = []
        self.exits_to_try: list[Entrance] = []
        self.visited_locations: set[Location] = set()
        self.visited_areas: set[Area] = set()
        self.successful_exits: set[Entrance] = set()
        self.playthrough_entrances: set[Entrance] = set()

        self.playthrough_spheres: list[list[Location]] = []
        self.entrance_spheres: list[list[Entrance]] = []

        self.area_time: dict[int, int] = {}

        # Add starting inventory items for each world
        for world in self.worlds:
            if world.id == self.world_to_search or self.world_to_search == -1:
                for item, count in world.starting_item_pool.items():
                    self.owned_items[item] += count

        # Set search starting properties and add each world's root to exits_to_try
        for world in self.worlds:
            if world.id == self.world_to_search or self.world_to_search == -1:
                root = world.root
                self.visited_areas.add(root)
                world.set_search_starting_properties(self)
                for root_exit in root.exits:
                    if not root_exit.disabled:
                        self.exits_to_try.append(root_exit)

    def search_worlds(self) -> None:
        # Get all locations which fit criteria to test on each iteration
        item_locations: list[LocationAccess] = []
        for world in self.worlds:
            for area in world.areas.values():
                for loc_access in area.locations:
                    if not loc_access.location.is_empty() or self.search_mode in [
                        SearchMode.ACCESSIBLE_LOCATIONS,
                        SearchMode.ALL_LOCATIONS_REACHABLE,
                    ]:
                        item_locations.append(loc_access)

        # Main Searching Loop
        # Keep iterating while new things are being found, but
        # if the search is beatable and we're either generating
        # the playthrough or checking for beatability, exit early
        self.new_things_found = True
        while self.new_things_found and not (
            self.is_beatable
            and self.search_mode
            in [SearchMode.GENERATE_PLAYTHROUGH, SearchMode.GAME_BEATABLE]
        ):
            # Variable to keep track of making logical progress. We want to keep
            # looping as long as we're finding new things on each iteration
            self.new_things_found = False

            # Add an empty sphere if we're generating the playthrough
            if self.search_mode == SearchMode.GENERATE_PLAYTHROUGH:
                self.playthrough_spheres.append([])
                self.entrance_spheres.append([])

            self.process_events()
            self.process_exits()

            # For proper sphere calculation based on item locations
            # we need to keep looping over exits and events until
            # nothing new is found in them (and then process locations)
            while (
                self.search_mode == SearchMode.GENERATE_PLAYTHROUGH
                and self.new_things_found
            ):
                self.new_things_found = False
                self.process_events()
                self.process_exits()

            self.process_locations(item_locations)

            self.sphere_num += 1

    # Explore the given area, and recursively explore the area's connected to it as
    # well if they haven't been visited yet.
    def explore(self, area: Area) -> None:
        for event in area.events:
            self.events_to_try.append(event)

        for exit_ in area.exits:
            eval_success = evaluate_exit_requirement(self, exit_)
            match eval_success:
                case EvalSuccess.COMPLETE:
                    self.successful_exits.add(exit_)
                    self.add_exit_to_entrance_spheres(exit_)
                    if exit_.connected_area not in self.visited_areas:
                        self.visited_areas.add(exit_.connected_area)
                        self.explore(exit_.connected_area)
                case EvalSuccess.PARTIAL:
                    self.exits_to_try.append(exit_)
                    self.add_exit_to_entrance_spheres(exit_)
                    if exit_.connected_area not in self.visited_areas:
                        self.visited_areas.add(exit_.connected_area)
                        self.explore(exit_.connected_area)
                case EvalSuccess.NONE:
                    self.exits_to_try.append(exit_)
                case _:
                    pass

    def process_exits(self) -> None:
        # Search each exit in the exitsToTry list and explore any new areas found as well.
        # For any exits which we try and don't meet the requirements for, put them
        # into exitsToTry for the next iteration.
        for exit_ in self.exits_to_try:
            # Ignore the exit if it we've already completed it, or we're not searching
            # its world at the moment
            if exit_ in self.successful_exits or (
                self.world_to_search != -1 and self.world_to_search != exit_.world.id
            ):
                continue

            eval_success = evaluate_exit_requirement(self, exit_)
            if eval_success == EvalSuccess.UNNECESSARY:
                self.successful_exits.add(exit_)
            elif eval_success in [EvalSuccess.COMPLETE, EvalSuccess.PARTIAL]:
                self.add_exit_to_entrance_spheres(exit_)
                if eval_success == EvalSuccess.COMPLETE:
                    self.successful_exits.add(exit_)

                self.new_things_found = True

                # If this exit's connected region hasn't been explored yet, then explore it
                if exit_.connected_area not in self.visited_areas:
                    self.visited_areas.add(exit_.connected_area)
                    self.explore(exit_.connected_area)

    # Loop through and see if there are any events that are now accessible.
    # Add them to the ownedEvents list if they are.
    def process_events(self) -> None:
        for event in self.events_to_try:
            # Ignore the event if it isn't part of the world we're searching or we already found it
            if event.id in self.owned_events or (
                self.world_to_search != -1
                and event.area.world.id != self.world_to_search
            ):
                continue

            if evaluate_event_requirement(self, event) == EvalSuccess.COMPLETE:
                self.new_things_found = True
                self.owned_events.add(event.id)

    def process_locations(self, item_locations: list[LocationAccess]) -> None:
        accessible_this_iteration: list[Location] = []
        for loc_access in item_locations:
            loc = loc_access.location
            world = loc_access.area.world

            if (
                loc in self.visited_locations
                or loc_access.area not in self.visited_areas
                or (self.world_to_search != -1 and world.id != self.world_to_search)
            ):
                continue

            if evaluate_location_requirement(self, loc_access) == EvalSuccess.COMPLETE:
                self.visited_locations.add(loc)
                self.new_things_found = True
                if self.search_mode == SearchMode.GENERATE_PLAYTHROUGH:
                    accessible_this_iteration.append(loc)
                else:
                    self.process_location(loc)

        for location in accessible_this_iteration:
            self.process_location(location)
            if self.is_beatable:
                return

    def process_location(self, location: Location) -> None:
        if not self.collect_items:
            return

        self.owned_items[location.current_item] += 1
        if (
            self.search_mode == SearchMode.GENERATE_PLAYTHROUGH
            and location.current_item.is_major_item
        ):
            self.playthrough_spheres[-1].append(location)

        # If we're generating a playthrough or just checking for beatability then we can
        # stop searching early by checking if we've found all game beating items for each
        # world
        if (
            self.search_mode
            in [SearchMode.GENERATE_PLAYTHROUGH, SearchMode.GAME_BEATABLE]
            and location.current_item.is_game_winning_item
        ):
            if len(
                [item for item in self.owned_items if item.is_game_winning_item]
            ) == len(self.worlds):
                # If this is the playthrough, and we've found all game winning items, clear the current sphere
                # except for the last game winning items
                if self.search_mode == SearchMode.GENERATE_PLAYTHROUGH:
                    self.playthrough_spheres[-1] = [
                        loc
                        for loc in self.playthrough_spheres[-1]
                        if loc.current_item.is_game_winning_item
                    ]
                self.is_beatable = True

    def add_exit_to_entrance_spheres(self, exit_: Entrance) -> None:
        if self.search_mode == SearchMode.GENERATE_PLAYTHROUGH and exit_.shuffled:
            if exit_ not in self.playthrough_entrances:
                self.entrance_spheres[-1].append(exit_)
                self.playthrough_entrances.add(exit_)
                if not exit_.decoupled and exit_.replaces.reverse:
                    self.playthrough_entrances.add(exit_.replaces.reverse)

    def remove_empty_spheres(self) -> None:
        spheres_to_remove = []
        for i in range(len(self.playthrough_spheres)):
            if (
                len(self.playthrough_spheres[i]) == 0
                and len(self.entrance_spheres[i]) == 0
            ):
                spheres_to_remove.append(i)

        # Remove spheres from higher indices first so we the lower
        # indices stay the same
        for index in reversed(spheres_to_remove):
            self.playthrough_spheres.pop(index)
            self.entrance_spheres.pop(index)

    # Will dump a file which can be turned into a visual graph using graphviz
    # https://graphviz.org/download/
    # Use this command to generate the graph: dot -Tsvg <filename> -o world.svg
    # Then, open world.svg in a browser and CTRL + F to find the area of interest
    def dump_world_graph(self, world_num: int = 0, filename: str = "World"):
        world = self.worlds[world_num]
        with open(filename + ".gv", "w") as world_graph:
            world_graph.write("digraph {\n\tcenter=true;\n")

            for area_id, area in world.areas.items():
                color = '"black"' if area in self.visited_areas else '"red"'
                tod_str = ":<br/>"
                if area_id in self.area_time:
                    if self.area_time[area_id] & TOD.DAY:
                        tod_str += " Day"
                    if self.area_time[area_id] & TOD.NIGHT:
                        tod_str += " Night"

                world_graph.write(
                    f'\t"{area}"[label=<{area}{tod_str}> shape="plain" fontcolor={color}];\n'
                )

                # Make edge connections defined by events
                for event in area.events:
                    color = '"blue"' if event.id in self.owned_events else '"red"'
                    event_name = world.reverse_events[event.id]
                    world_graph.write(
                        f'\t"{event_name}"[label=<{event_name}> shape="plain" fontcolor={color}];'
                    )
                    world_graph.write(
                        f'\t"{area}" -> "{event_name}"[dir=forward color={color}]'
                    )

                # Make edge connections defined by exits
                for exit_ in area.exits:
                    if exit_.connected_area != None:
                        color = '"black"' if exit_ in self.successful_exits else '"red"'
                        world_graph.write(
                            f'\t"{area}" -> "{exit_.connected_area}"[dir=forward color={color}]'
                        )

                # Make edge connections between areas and their locations:
                for loc_access in area.locations:
                    loc = loc_access.location
                    color = '"black"' if loc in self.visited_locations else '"red"'
                    world_graph.write(
                        f'\t"{loc}"[label=<{loc}:<br/>{loc.current_item}> shape="plain" fontcolor={color}];'
                    )
                    world_graph.write(
                        f'\t"{area}" -> "{loc}"[dir=forward color={color}]'
                    )

            world_graph.write("}")


def game_beatable(worlds: list[World]) -> bool:
    search = Search(SearchMode.GAME_BEATABLE, worlds)
    search.search_worlds()
    return search.is_beatable


def all_locations_reachable(worlds: list[World], item_pool: Counter[Item] = {}) -> bool:
    total_locations = 0
    for world in worlds:
        total_locations += len(world.location_table)
    search = Search(SearchMode.ALL_LOCATIONS_REACHABLE, worlds, item_pool)
    search.search_worlds()
    return len(search.visited_locations) == total_locations


def generate_playthrough(worlds: list[World]) -> None:
    logging.getLogger("").debug("Generating Playthrough")
    # Generate initial playthrough
    playthrough_search = Search(SearchMode.GENERATE_PLAYTHROUGH, worlds)
    playthrough_search.search_worlds()

    playthrough_spheres = playthrough_search.playthrough_spheres

    # Keep track of all locations we temporarily take items away from
    # so we can give them back after playthrough calculation
    temp_empty_locations = {}
    # Keep track of all the locations that appear in the playthrough
    playthrough_locations_set: set[Location] = set(
        [l for sphere in playthrough_spheres for l in sphere]
    )

    # Remove all items from locations that are not part of the playthrough set
    for location in [l for world in worlds for l in world.location_table.values()]:
        if location not in playthrough_locations_set:
            temp_empty_locations[location] = location.current_item
            location.remove_current_item()

    print("Paring down playthrough")
    # Reverse the playthrough so we're paring it down from highest to lowest sphere
    # This way, lower sphere items will be prioritized for the playthrough
    for sphere in reversed(playthrough_spheres):
        for location in sphere:
            item_at_location = location.current_item
            location.remove_current_item()

            # If the game is beatable, temporarily take this item away and
            # discard the location to the set of playthrough locations
            if game_beatable(worlds):
                temp_empty_locations[location] = item_at_location
                playthrough_locations_set.discard(location)
            else:
                location.set_current_item(item_at_location)

    # Now generate a new playthrough search incase some spheres were flattened
    # by the previous generation having access to extra items
    new_search = Search(SearchMode.GENERATE_PLAYTHROUGH, worlds)
    new_search.search_worlds()

    # Now do the same process for entrances to pare down the entrance playthrough
    entrance_spheres = new_search.entrance_spheres
    non_required_entrances = {}

    for sphere in entrance_spheres:
        for entrance in sphere.copy():
            connected_area = entrance.disconnect()
            if game_beatable(worlds):
                # If the game is still beatable then this entrance is not required
                sphere.remove(entrance)
                non_required_entrances[entrance] = connected_area
            else:
                # If the entrance is required, reconnect it
                entrance.connect(connected_area)

    # Reconnect all non-required entrances
    for entrance, connected_area in non_required_entrances.items():
        entrance.connect(connected_area)

    # Give locations back their items
    for location, item in temp_empty_locations.items():
        location.set_current_item(item)

    # Discard all locations not in the playthrough locations set
    for sphere in new_search.playthrough_spheres:
        for location in sphere.copy():
            if location not in playthrough_locations_set:
                sphere.discard(location)

    # Now remove any empty spheres that might remain
    new_search.remove_empty_spheres()

    worlds[0].playthrough_spheres = new_search.playthrough_spheres
    worlds[0].entrance_spheres = new_search.entrance_spheres
