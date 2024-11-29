from logic.location import *
from logic.entrance import *
from logic.requirements import TOD

from typing import TYPE_CHECKING
import logging
import random

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
        self.id = LocationAccess.id_counter
        LocationAccess.id_counter += 1


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
        self.hard_assigned_region: str = None
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

    # Will return which provinces an area is a part of
    # TODO: This isn't used anywhere and wasn never tested, so be
    # careful if you decide to try it out
    def get_provinces(self) -> set[str]:
        provinces: set[str] = set()
        already_checked: set["Area"] = set()
        area_queue: list["Area"] = [self]

        while len(area_queue) > 0:
            area = area_queue.pop(0)
            already_checked.add(area)

            prev_num_provinces = len(provinces)

            if "Sky" in area.hint_regions:
                provinces.add("Sky")
            if "Skyloft" in area.hint_regions:
                provinces.add("Skyloft")
            if area.name == "Faron Pillar":
                provinces.add("Faron")
            if area.name == "Eldin Pillar":
                provinces.add("Eldin")
            if area.name == "Lanayru Pillar":
                provinces.add("Lanayru")

            # Only continue searching if no provinces were found
            if prev_num_provinces == len(provinces):
                for entrance in area.entrances:
                    if entrance.parent_area not in already_checked:
                        area_queue.append(entrance.parent_area)

        return provinces

    # Performs a breadth first search to find all the shuffled entrances
    # within a given area. The area must have a defined hint region.
    # Returns the shuffled entrances in the order they were discovered by
    # shuffled entrance spheres.
    def find_shuffled_entrances(self, starting_queue: list["Area"] = []):
        if not self.hard_assigned_region:
            return

        shuffled_entrances: list[list[Entrance]] = []
        already_checked_areas: set["Area"] = set()
        already_checked_entrances: set[Entrance] = set()
        area_queue: list["Area"] = starting_queue
        if not area_queue:
            area_queue.append(self)

        entrances_to_try: list[Entrance] = []
        first_iteration = True
        while entrances_to_try or first_iteration:
            first_iteration = False
            entrances_to_try.clear()

            for area in area_queue:
                for entrance in area.exits:
                    if entrance in already_checked_entrances:
                        continue

                    # Only add entrances which fit the following criteria
                    # - The entrance is shuffled and not impossible
                    # - The entrance is decoupled or the entrance isn't connected or the entrance's replaced reverse hasn't been added yet
                    if (
                        entrance.shuffled
                        and entrance.requirement.type != RequirementType.IMPOSSIBLE
                    ):
                        if (
                            entrance.decoupled
                            or entrance.replaces is None
                            or entrance.replaces.reverse
                            not in already_checked_entrances
                        ):
                            entrances_to_try.append(entrance)
                    # Else, append this entrances connected area to the area queue
                    else:
                        connected_area = entrance.connected_area
                        if connected_area:
                            if connected_area not in already_checked_areas and (
                                self.hard_assigned_region in connected_area.hint_regions
                                or not connected_area.hint_regions
                            ):
                                area_queue.append(connected_area)
                                already_checked_areas.add(connected_area)

                    already_checked_entrances.add(entrance)

            # Clear the area queue and append the list of entrances to try
            # if there were any
            area_queue.clear()
            if entrances_to_try:
                shuffled_entrances.append(entrances_to_try.copy())

            # Gather all the new areas we can find to try for shuffled entrances
            for entrance in entrances_to_try:
                connected_area = entrance.connected_area
                if connected_area:
                    if connected_area not in already_checked_areas and (
                        self.hard_assigned_region in connected_area.hint_regions
                        or not connected_area.hint_regions
                    ):
                        area_queue.append(connected_area)
                        already_checked_areas.add(connected_area)

        return shuffled_entrances


# Will perform a search from the starting area until all
# possibly connected hint regions have been found.
# These hint regions will be assigned to the starting area,
# General hint regions will have priority over dungeons.
# I.e. If an area is connected to a general hint region and
# a dungeon it will only be assigned to the general hint region.
def assign_hint_regions_and_dungeon_locations(starting_area: Area):
    hint_regions: set[str] = set()
    already_checked: set[Area] = set()
    area_queue: list[Area] = [starting_area]

    while len(area_queue) > 0:
        area = area_queue.pop(0)
        already_checked.add(area)

        if area.hard_assigned_region or area.name == "Root":
            if area.hard_assigned_region not in ["None", None]:
                hint_regions.add(area.hard_assigned_region)
            continue

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

    # Assign the found hint regions to the area
    starting_area.hint_regions = hint_regions
    logging.getLogger("").debug(
        f"{starting_area} has been assigned hint region(s): {hint_regions}"
    )
    # Also assign any locations in this area to the dungeon
    # if there are any dungeon regions
    for region in hint_regions:
        if region in dungeon_regions:
            locations = [
                la.location for area in already_checked for la in area.locations
            ]
            dungeon = area.world.get_dungeon(region)
            for loc in locations:
                if loc not in dungeon.locations:
                    dungeon.locations.append(loc)
                    logging.getLogger("").debug(
                        f"{loc} has been assigned to dungeon {region}"
                    )
