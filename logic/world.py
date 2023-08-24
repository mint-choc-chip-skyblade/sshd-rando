from .config import Config
from .settings import *
from .item import Item
from .location import Location
from .area import *
from .requirements import *
from .item_pool import *
from .dungeon import *

from collections import Counter
from typing import TYPE_CHECKING
import logging
import yaml
import os

if TYPE_CHECKING:
    from .search import Search


class MissingInfoError(RuntimeError):
    pass


class WrongInfoError(RuntimeError):
    pass


class World:
    event_id_counter: int = 0
    area_id_counter: int = 0

    def __init__(self, id_: int) -> None:
        self.id = id_
        self.config: Config = None
        self.num_worlds: int = 0

        self.setting_map: SettingMap = SettingMap()

        self.item_table: dict[str, Item] = {}
        self.location_table: dict[str, Location] = {}
        self.areas: dict[int, Area] = {}
        self.macros: dict[str, Requirement] = {}
        self.dungeons: dict[str, Dungeon] = {}

        # Map event names to ids and ids to names
        self.events: dict[str, int] = {}
        self.reverse_events: dict[int, str] = {}

        # Map area names to ids
        self.area_ids: dict[str, int] = {}
        # Maps area ids to their possible times of day
        self.area_time_cache: dict[int, int] = {}
        # Maps area ids to their possible times of day
        self.exit_time_cache: dict[Entrance, int] = {}

        self.item_pool: Counter[Item] = Counter()
        self.starting_item_pool: Counter[Item] = Counter()
        self.root: Area = None

        self.playthrough_spheres: list[set[Location]] = None
        self.entrance_spheres: list[list[Entrance]] = None

        self.plandomizer_locations: dict[Location, Item] = {}
        self.plandomizer_entrances: dict[str, str] = {}

    def __str__(self) -> str:
        return f"World {self.id + 1}"

    def build(self) -> None:
        self.build_item_table()
        self.build_location_table()
        self.load_logic_macros()
        self.load_world_graph()
        self.place_hardcoded_items()
        self.build_item_pools()

    # Read items.yaml and store all necessary data in a dict
    # for this world
    def build_item_table(self) -> None:
        logging.getLogger("").debug(f"Building Item Table for {self}")
        with open("data/items.yaml", "r") as item_data_file:
            item_data = yaml.safe_load(item_data_file)
            for item_node in item_data:
                # Check to make sure all neccesary fields exist
                for field in ["id", "name", "oarc"]:
                    if field not in item_node:
                        raise MissingInfoError(
                            f"item \"{item_node['name']}\" is missing the \"{field}\" field in items.yaml"
                        )

                item_id = int(item_node["id"])
                name = item_node["name"]
                oarcs = item_node["oarc"]
                major_item = (
                    item_node["advancement"] if "advancement" in item_node else False
                )
                game_winning_item = (
                    item_node["game_winning_item"]
                    if "game_winning_item" in item_node
                    else False
                )

                # TODO: Load the rest of the data

                stripped_name = name.replace("'", "")
                self.item_table[stripped_name] = Item(
                    item_id, name, oarcs, self, major_item, game_winning_item
                )
                logging.getLogger("").debug(
                    f"Processing new item {name}\tid: {item_id}"
                )

    # Read locations.yaml and store all necessary data in a dict
    # for this world
    def build_location_table(self) -> None:
        logging.getLogger("").debug(f"Building Location Table for {self}")
        with open("data/locations.yaml", "r") as item_data_file:
            location_id_counter = 0
            location_data = yaml.safe_load(item_data_file)
            for location_node in location_data:
                # Check to make sure all required fields exist
                for field in ["name", "original_item"]:
                    if field not in location_node:
                        raise MissingInfoError(
                            f"location \"{location_node['name']}\" is missing the \"{field}\" field in items.yaml"
                        )

                name = location_node["name"]
                original_item = self.get_item(location_node["original_item"])
                types = location_node["type"] if "type" in location_node else []
                if types == None:
                    types = []
                patch_paths = location_node["Paths"] if "Paths" in location_node else []
                location_id = location_id_counter
                location_id_counter += 1

                # TODO: Load the rest of the data

                self.location_table[name] = Location(
                    location_id, name, types, self, original_item, patch_paths
                )
                logging.getLogger("").debug(
                    f"Processing new location {name}\tid: {location_id}\toriginal item: {original_item}"
                )

    def load_logic_macros(self) -> None:
        logging.getLogger("").debug(f"Loading macros for {self}")
        with open("data/macros.yaml", "r") as macros_data_file:
            macros_data = yaml.safe_load(macros_data_file)
            for macro_name, req_str in macros_data.items():
                self.macros[macro_name] = parse_requirement_string(req_str, self)

    def load_world_graph(self) -> None:
        logging.getLogger("").debug(f"Loading world graph for {self}")

        # Make sure all used events and areas are defined
        defined_events: set[str] = set()
        defined_areas: set[Area] = set()

        directory = "data/world"

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            # Skip over any non-yaml files
            if not filepath.endswith(".yaml"):
                continue

            with open(filepath, "r") as world_data_file:
                world_data = yaml.safe_load(world_data_file)
                for area_node in world_data:
                    # Check to make sure all required fields exist
                    for field in ["name"]:
                        if field not in area_node:
                            raise MissingInfoError(
                                f"An area node is missing the name field"
                            )

                    area_name = area_node["name"]
                    self.add_area(area_name)
                    new_area = self.areas[self.area_ids[area_name]]
                    new_area.name = area_name
                    new_area.world = self
                    defined_areas.add(new_area)

                    if (
                        "allowed_time_of_day" in area_node
                        and self.setting("natural_night_connections") == "on"
                    ):
                        new_area.allowed_tod = (
                            TOD.DAY
                            if area_node["allowed_time_of_day"] == "Day Only"
                            else TOD.ALL
                        )

                    if "can_sleep" in area_node:
                        new_area.can_sleep = True

                    if "dungeon" in area_node:
                        dungeon_name = area_node["dungeon"]
                        self.add_dungeon(dungeon_name)
                        new_area.hint_regions.add(dungeon_name)
                        if "dungeon_starting_area" in area_node:
                            self.get_dungeon(dungeon_name).starting_area = new_area
                    elif "hint_region" in area_node:
                        hint_region = area_node["hint_region"]
                        new_area.hint_regions.add(hint_region)

                    if "events" in area_node:
                        for event_name, req_str in area_node["events"].items():
                            # Replace spaces with underscores to match logic syntax
                            event_name = event_name.replace(" ", "_")
                            defined_events.add(event_name)
                            self.add_event(event_name)
                            event_req = parse_requirement_string(req_str, self)
                            new_area.events.append(
                                EventAccess(
                                    self.events[event_name], event_req, new_area
                                )
                            )

                    if "locations" in area_node:
                        for location_name, req_str in area_node["locations"].items():
                            location_req = parse_requirement_string(req_str, self)
                            new_area.locations.append(
                                LocationAccess(
                                    self.get_location(location_name),
                                    location_req,
                                    new_area,
                                )
                            )
                            # Add the LocationAccess to the list of access points for the location
                            self.get_location(location_name).loc_access_list.append(
                                new_area.locations[-1]
                            )
                            # Add the location to the dungeon if this area is part of one
                            if "dungeon" in area_node:
                                self.get_dungeon(area_node["dungeon"]).locations.append(
                                    self.get_location(location_name)
                                )

                    if "exits" in area_node:
                        for connected_area_name, req_str in area_node["exits"].items():
                            exit_req = parse_requirement_string(req_str, self)
                            self.add_area(connected_area_name)
                            connected_area = self.areas[
                                self.area_ids[connected_area_name]
                            ]
                            connected_area.name = connected_area_name
                            new_area.exits.append(
                                Entrance(new_area, connected_area, exit_req, self)
                            )

        # Check to make sure all events were properly defined
        for event in self.events:
            if event not in defined_events:
                raise MissingInfoError(f'Event "{event}" is used, but never defined')

        # Same for areas
        for area in self.areas.values():
            if area not in defined_areas:
                raise MissingInfoError(f'Area "{area}" is used, but never defined')

        # Check that root area exists
        if self.root == None:
            raise MissingInfoError(f"Missing Root area in {self}")

        # Set all entrances for each area
        for area_id, area in self.areas.items():
            for exit_ in area.exits:
                exit_.connected_area.entrances.append(exit_)

    def build_item_pools(self) -> None:
        generate_item_pool(self)
        generate_starting_item_pool(self)

    def place_hardcoded_items(self) -> None:
        self.location_table["Hylia's Realm - Defeat Demise"].set_current_item(
            self.get_item("Game Beatable")
        )

    def place_plandomizer_items(self) -> None:
        for location, item in self.plandomizer_locations.items():
            location.set_current_item(item)
            self.item_pool[item] -= 1

    def perform_pre_entrance_shuffle_tasks(self) -> None:
        # Plandomizer items and vanilla items must
        # be placed before entrances are shuffled
        # to ensure we create a valid world graph
        # with the pre-planned item placements
        self.place_plandomizer_items()
        self.place_vanilla_items()
        # TODO: Initial entrance time cache

    def place_vanilla_items(self) -> None:
        for location in self.location_table.values():
            item = location.original_item

            if item == None:
                continue

            # Small Keys, Boss Keys, Maps, Caves Key
            if (
                (
                    self.setting("small_keys") == "vanilla"
                    and item.is_dungeon_small_key
                    and location
                    != self.get_location("Skyview Temple - Digging Spot in Crawlspace")
                )
                or (self.setting("boss_keys") == "vanilla" and item.is_boss_key)
                or (self.setting("map_mode") == "vanilla" and item.is_dungeon_map)
                or (
                    self.setting("lanayru_caves_key") == "vanilla"
                    and item == self.get_item("Lanayru Caves Small Key")
                )
            ):
                location.set_current_item(item)
                location.has_known_vanilla_item = True
                self.item_pool[item] -= 1

            # Scrap Shop Upgrades
            if "Scrap Shop" in location.types:
                if self.setting("scrap_shop_upgrades") == "off":
                    location.set_current_item(item)
                    self.item_pool[item] -= 1
                else:
                    location.set_current_item(self.get_item("Green Rupee"))

    def shuffle_entrances(self, worlds: list["World"]) -> None:
        # TODO: Actually shuffle entrances
        for area in self.areas.values():
            # Assign hint regions to all areas which don't
            # have them at this point. This will also finalize
            # dungeon locations.
            assign_hint_regions(area)

            # Also assign dungeons their entrance properties
            # so we can lookup their region later if necessary
            for exit_ in area.exits:
                exit_regions = exit_.parent_area.hint_regions
                if None not in exit_regions and not exit_regions.intersection(
                    self.dungeons.keys()
                ):
                    for dungeon in self.dungeons.values():
                        if exit_.connected_area == dungeon.starting_area:
                            dungeon.starting_entrance = exit_

    # Remove or add junk to the item pool until the total number of
    # items is equal to the number of currently empty locations
    def sanitize_item_pool(self) -> None:
        num_empty_locations = len(
            [l for l in self.get_all_item_locations() if l.is_empty()]
        )
        while self.item_pool.total() < num_empty_locations:
            junk_item = self.get_item(get_random_junk_item_name())
            logging.getLogger("").debug(f"Added {junk_item} to item pool in {self}")
            self.item_pool[junk_item] += 1

        if self.item_pool.total() > num_empty_locations:
            junk_to_remove = []
            for junk in all_junk_items:
                junk_item = self.get_item(junk)
                junk_to_remove.extend([junk_item] * self.item_pool[junk_item])

            # Make sure there's enough junk to remove
            if self.item_pool.total() - len(junk_to_remove) > num_empty_locations:
                raise ItemPoolError(
                    f"Not enough junk to remove from {self}'s item pool.\nEmpty Locations: {num_empty_locations} item_pool.total(): {self.item_pool.total()} junk_to_remove: {len(junk_to_remove)}"
                )

            while self.item_pool.total() > num_empty_locations:
                random.shuffle(junk_to_remove)
                junk_item = junk_to_remove.pop()
                logging.getLogger("").debug(
                    f"Removing {junk_item} from item pool in {self}"
                )
                self.item_pool[junk_item] -= 1

    # Adds a new event if one with the current name doesn't exist
    def add_event(self, event_name: str) -> None:
        if event_name not in self.events:
            event_id = World.event_id_counter
            World.event_id_counter += 1
            self.events[event_name] = event_id
            self.reverse_events[event_id] = event_name

    # Adds a new area if one with the current name doesn't exist
    # Just creates the entry and doesn't set any of its properties except the id
    def add_area(self, area_name: str) -> None:
        if area_name not in self.area_ids:
            area_id = World.area_id_counter
            World.area_id_counter += 1
            self.area_ids[area_name] = area_id
            self.areas[area_id] = Area()
            self.areas[area_id].id = area_id
            if area_name == "Root":
                self.root = self.areas[area_id]

    def add_dungeon(self, dungeon_name: str) -> None:
        if dungeon_name not in self.dungeons:
            self.dungeons[dungeon_name] = Dungeon()
            self.dungeons[dungeon_name].name = dungeon_name

    def get_item(self, item_name: str) -> Item:
        item_name = item_name.replace("_", " ").replace("'", "")
        if item_name == "Nothing":
            return None
        if item_name not in self.item_table:
            raise WrongInfoError(
                f'Item "{item_name}" is not defined in the item table for {self}'
            )
        return self.item_table[item_name]

    def get_location(self, location_name: str) -> Location:
        if location_name not in self.location_table:
            raise WrongInfoError(
                f'Location "{location_name}" is not defined in location table for {self}'
            )
        return self.location_table[location_name]

    def get_all_item_locations(self) -> list[Location]:
        return [
            location
            for location in self.location_table.values()
            if "Hint Location" not in location.types
        ]

    def get_dungeon(self, dungeon_name: str) -> Dungeon:
        if dungeon_name not in self.dungeons:
            raise WrongInfoError(f'Dungeon "{dungeon_name}" is not defined for {self}')
        return self.dungeons[dungeon_name]

    def get_macro(self, macro_name: str) -> Requirement:
        macro_name = macro_name.replace("_", " ")
        if macro_name not in self.macros:
            raise WrongInfoError(
                f'Macro "{macro_name}" was not previously not defined for {self}'
            )
        return self.macros[macro_name]

    def setting(self, setting_name: str) -> SettingGet:
        if setting_name not in self.setting_map.settings:
            raise SettingInfoError(
                f'No Setting named "{setting_name}" in settings for {self}'
            )
        return SettingGet(setting_name, self.setting_map.settings[setting_name])

    def set_search_starting_properties(self, search: "Search"):
        # Set the root to have daytime
        # TODO: Change if we ever have an option to start at night
        search.area_time[self.root.id] = TOD.DAY
