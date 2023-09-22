from logic.location import *
from logic.entrance import *
from logic.requirements import TOD

from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from .world import World


# Helper class to link locations with their requirements
# in a specific area. We don't want to tie requirements
# to the Location class directly since some locations can
# be accessed from multiple areas
class LocationAccess:
    id_counter: int = 0

    def __init__(self, location_: Location, req_: Requirement, area_: "Area") -> None:
        self.location: Location = location_
        self.req: Requirement = req_
        self.area: "Area" = area_
        self.id = self.id_counter
        self.id_counter += 1


# Same for events
class EventAccess:
    def __init__(self, id_: int, req_: Requirement, area_: "Area") -> None:
        self.id: int = id_
        self.req: Requirement = req_
        self.area: "Area" = area_


class Area:
    def __init__(self) -> None:
        self.id: int = None
        self.name: str = None
        self.hint_regions: set[str] = set()
        self.events: list[EventAccess] = []
        self.locations: list[LocationAccess] = []
        self.exits: list[Entrance] = []
        self.entrances: list[Entrance] = []
        self.world: "World" = None
        self.allowed_tod: int = (
            TOD.ALL
        )  # All by default, will set to day only if natural night connections are enforced
        self.can_sleep: bool = False

    def __str__(self) -> str:
        return self.name

    def __lt__(self, other: "Area"):
        return self.id < other.id

    # Will return the currently connected hint regions, if none are assigned
    # but will not assign the found hint regions. This is meant to be called
    # in the entrance randomization algorithm
    def get_regions(self) -> set[str]:
        if self.hint_regions:
            return self.hint_regions

        hint_regions: set[str] = set()
        already_checked: set["Area"] = set()
        area_queue: list["Area"] = [self]

        while len(area_queue) > 0:
            area = area_queue.pop(0)
            already_checked.add(area)

            if len(area.hint_regions) > 0:
                for region in area.hint_regions:
                    # Don't add None if we come across it
                    if region != "None":
                        hint_regions.add(region)
                continue

            # If this area isn't assigned any hint regions
            # add its entrances' parent areas to the queue
            # as long as they haven't been checked yet
            for entrance in area.entrances:
                if entrance.parent_area not in already_checked:
                    area_queue.append(entrance.parent_area)

        return hint_regions


# Will perform a search from the starting area until all
# possibly connected hint regions have been found.
# These hint regions will be assigned to the starting area,
# as well as any areas along the way that don't have an
# assigned hint region. General hint regions will have priority
# over dungeons. I.e. If an area is connected to a general
# hint region and a dungeon it will only be assigned to the
# general hint region.
def assign_hint_regions_and_dungeon_locations(starting_area: Area):
    hint_regions: set[str] = set()
    already_checked: set[Area] = set()
    unassigned_areas: set[Area] = set()
    area_queue: list[Area] = [starting_area]

    while len(area_queue) > 0:
        area = area_queue.pop(0)
        already_checked.add(area)

        if len(area.hint_regions) > 0:
            for region in area.hint_regions:
                # Don't add None if we come across it
                if region != "None":
                    hint_regions.add(region)
            continue

        unassigned_areas.add(area)
        # If this area isn't assigned any hint regions
        # add its entrances' parent areas to the queue
        # as long as they haven't been checked yet
        for entrance in area.entrances:
            if entrance.parent_area not in already_checked:
                area_queue.append(entrance.parent_area)

    # Filter out dungeon regions if there are any general hint regions
    dungeon_regions: set[str] = set(
        [region for region in hint_regions if region in starting_area.world.dungeons]
    )
    if len(dungeon_regions) < len(hint_regions):
        hint_regions = set(
            [region for region in hint_regions if region not in dungeon_regions]
        )

    # Assign the found hint regions to all unassigned areas
    for area in unassigned_areas:
        area.hint_regions = hint_regions
        logging.getLogger("").debug(
            f"{area} has been assigned hint region(s): {hint_regions}"
        )
        # Also assign any locations in this area to the dungeon
        # if there are any dungeon regions
        for region in hint_regions:
            if region in dungeon_regions:
                locations = [la.location for la in area.locations]
                area.world.get_dungeon(region).locations.extend(locations)
                logging.getLogger("").debug(
                    f"{[l.name for l in locations]} have been assigned to dungeon {region}"
                )

                # Also assign goal locations
                goal_locations = [loc for loc in locations if loc.is_goal_location]
                area.world.get_dungeon(region).goal_locations.extend(goal_locations)
