from constants.itemconstants import ALL_JUNK_ITEMS, TRAP_SETTING_TO_ITEM
from logic.location_table import build_location_table, get_disabled_shuffle_locations
from .config import Config
from .settings import *
from .item import Item
from .location import Location
from .area import *
from .requirements import *
from .item_pool import *
from .dungeon import *
from util.text import *

from collections import Counter, OrderedDict
from typing import TYPE_CHECKING
import logging
import yaml

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
        self.config: Config = None  # type: ignore
        self.num_worlds: int = 0
        self.worlds: list = []

        self.setting_map: SettingMap = SettingMap()

        self.item_table: dict[str, Item] = {}
        self.location_table: dict[str, Location] = {}
        self.areas: OrderedDict[int, Area] = OrderedDict()
        self.macros: dict[str, Requirement] = {}
        self.dungeons: dict[str, Dungeon] = {}

        # Map event names to ids and ids to names
        self.events: dict[str, int] = {}
        self.reverse_events: dict[int, str] = {}

        # Map area names to ids
        self.area_ids: dict[str, int] = {}
        # Maps area ids to their possible times of day
        self.area_time_cache: dict[int, int] = {}
        # Maps exits to their possible times of day
        self.exit_time_cache: dict[Entrance, int] = {}

        self.item_pool: Counter[Item] = Counter()
        self.starting_item_pool: Counter[Item] = Counter()
        self.root: Area = None  # type: ignore

        self.playthrough_spheres: list[list[Location]] = None  # type: ignore
        self.entrance_spheres: list[list[Entrance]] = None  # type: ignore

        self.plandomizer_locations: dict[Location, Item] = {}
        self.plandomizer_entrances: dict[Entrance, Entrance] = {}

        # Hint related things
        # path_locations maps a goal location to its set of path locations
        self.path_locations: dict[Location, list[Location]] = {}
        # barren_regions maps a hint region to the list of all locations in the region
        self.barren_regions: OrderedDict[str, list[Location]] = OrderedDict()
        self.fi_hints: list[Location] = []
        # gossip_stone_hints map each gossip stone location to the list of locations the stone is hinting at
        self.gossip_stone_hints: OrderedDict[Location, list[Location]] = OrderedDict()
        self.song_hints: dict[Item, Hint] = {}
        self.impa_sot_hint: Hint = None  # type: ignore

        # Save which bird statues we start with for patching and printing to spoiler log
        # Mapping of pillar to starting statue data
        self.starting_bird_statues: dict[str, dict] = {}

        # Save which bird statues we start with for patching and printing to spoiler log
        # Mapping of pillar to starting statue data
        self.starting_bird_statues: dict[str, dict] = {}

    def __str__(self) -> str:
        return f"World {self.id + 1}"

    def build(self) -> None:
        self.build_item_table()
        self.build_location_table()
        self.load_logic_macros()
        self.load_world_graph()
        self.verify_hint_data()
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
                major_item = item_node.get("advancement", False)
                game_winning_item = item_node.get("game_winning_item", False)
                chain_locations = item_node.get("chain_locations", [])

                stripped_name = name.replace("'", "")
                self.item_table[stripped_name] = Item(
                    item_id,
                    name,
                    oarcs,
                    self,
                    major_item,
                    game_winning_item,
                    chain_locations,
                )
                logging.getLogger("").debug(
                    f"Processing new item {name}\tid: {item_id}"
                )

                # Assign this item to its appropriate dungeon if it's a dungeon item
                item = self.item_table[stripped_name]
                if item.is_dungeon_small_key:
                    dungeon_name = item.name.replace(" Small Key", "")
                    self.add_dungeon(dungeon_name)
                    self.get_dungeon(dungeon_name).small_key = item
                    logging.getLogger("").debug(
                        f"Assigned {item} as small key for dungeon {dungeon_name}"
                    )
                elif item.is_boss_key:
                    dungeon_name = item.name.replace(" Boss Key", "")
                    self.add_dungeon(dungeon_name)
                    self.get_dungeon(dungeon_name).boss_key = item
                    logging.getLogger("").debug(
                        f"Assigned {item} as boss key for dungeon {dungeon_name}"
                    )
                elif item.is_dungeon_map:
                    dungeon_name = item.name.replace(" Map", "")
                    self.add_dungeon(dungeon_name)
                    self.get_dungeon(dungeon_name).map = item
                    logging.getLogger("").debug(
                        f"Assigned {item} as map for dungeon {dungeon_name}"
                    )

    # Read locations.yaml and store all necessary data in a dict
    # for this world
    def build_location_table(self) -> None:
        self.location_table = build_location_table(self)

    def load_logic_macros(self) -> None:
        logging.getLogger("").debug(f"Loading macros for {self}")
        with open("data/macros.yaml", "r") as macros_data_file:
            macros_data = yaml.safe_load(macros_data_file)
            for macro_name, req_str in macros_data.items():
                self.macros[macro_name] = parse_requirement_string(
                    req_str, self, force_logic=True
                )

    def load_world_graph(self) -> None:
        logging.getLogger("").debug(f"Loading world graph for {self}")

        # Make sure all used events and areas are defined
        defined_events: set[str] = set()
        defined_areas: set[Area] = set()

        directory = Path("data") / "world"

        for filepath in directory.iterdir():
            # Skip over any non-yaml files
            if not filepath.as_posix().endswith(".yaml"):
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

                    new_area.can_sleep = area_node.get("can_sleep", False)

                    if dungeon_name := area_node.get("dungeon", False):
                        self.add_dungeon(dungeon_name)
                        new_area.hint_regions.add(dungeon_name)
                        if "dungeon_starting_area" in area_node:
                            self.get_dungeon(dungeon_name).starting_area = new_area
                    elif hint_region := area_node.get("hint_region", False):
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
                            if dungeon_name := area_node.get("dungeon", False):
                                self.get_dungeon(dungeon_name).locations.append(
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

    def verify_hint_data(self) -> None:
        # Verify that every item, location, and hint region has text data
        for item in self.item_table.values():
            if get_text_data(item.name) is None:
                raise MissingInfoError(f'"{item}" has no associated hint data')
        for location in self.location_table.values():
            if get_text_data(location.name) is None:
                raise MissingInfoError(f'"{location}" has no associated hint data')
        for area in self.areas.values():
            for region in area.hint_regions:
                if region != "None" and get_text_data(region) is None:
                    raise MissingInfoError(f'"{region}" has no associated hint data')

    def build_item_pools(self) -> None:
        generate_item_pool(self)
        generate_starting_item_pool(self)

    def resolve_random_settings(self) -> None:
        # Use the randomness from the seed for resolving standard settings
        for setting in self.setting_map.settings.values():
            if setting.info.type == SettingType.STANDARD:
                setting.resolve_if_random()

    def resolve_conflicting_settings(self) -> None:
        # Resolve any conflicting settings here if we ever
        # find any
        pass

    def place_hardcoded_items(self) -> None:
        defeat_demise = self.get_location("Hylia's Realm - Defeat Demise")
        defeat_demise.set_current_item(self.get_item(GAME_BEATABLE))
        defeat_demise.has_known_vanilla_item = True

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
        disabled_shuffle_locations = [
            location
            for location in get_disabled_shuffle_locations(
                self.location_table, self.config
            )
        ]

        for location in self.location_table.values():
            item = location.original_item

            if item == None:
                continue

            # Small Keys, Boss Keys, Maps, Caves Key, Shop items, Single Crystals, Stamina Fruit, Rupees, Closets
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
                    self.setting("lanayru_caves_keys") == "vanilla"
                    and item == self.get_item(LC_SMALL_KEY)
                )
                or location in disabled_shuffle_locations
            ):
                location.set_current_item(item)
                location.has_known_vanilla_item = True
                location.hint_priority = "never"
                if item in self.item_pool:
                    self.item_pool[item] -= 1

            # Scrap Shop Upgrades
            if "Scrap Shop" in location.types:
                if self.setting("item_pool") == "minimum":
                    location.set_current_item(item)
                    self.item_pool[item] -= 1
                else:
                    location.set_current_item(self.get_item(GREEN_RUPEE))

            # Set Goddess Cubes as having their own item
            if "Goddess Cube" in location.types:
                location.set_current_item(item)
                location.has_known_vanilla_item = True

    def perform_post_entrance_shuffle_tasks(self) -> None:
        self.assign_all_areas_hint_regions()
        self.choose_required_dungeons()
        self.set_nonprogress_locations()

    def assign_all_areas_hint_regions(self):
        for area in self.areas.values():
            # Assign hint regions to all areas which don't
            # have them at this point. This will also finalize
            # dungeon locations.
            assign_hint_regions_and_dungeon_locations(area)

            # Also assign dungeons their entrance properties
            # so we can lookup their region later if necessary
            for exit_ in area.exits:
                exit_regions = exit_.parent_area.hint_regions
                if None not in exit_regions:
                    for dungeon in self.dungeons.values():
                        if (
                            exit_.connected_area == dungeon.starting_area
                            and dungeon.name not in exit_regions
                        ):
                            dungeon.starting_entrance = exit_

    def choose_required_dungeons(self):
        num_required_dungeons = self.setting("required_dungeons").value_as_number()

        dungeons = [
            d
            for d in self.dungeons.values()
            if d.goal_location and d.name != "Sky Keep"
        ]

        # Remove any dungeons which have non-major items plandomized to their goal locations
        # Also force require any dungeons which have a major item plandomized to their goal locations
        for dungeon in dungeons.copy():
            if (
                not dungeon.goal_location.is_empty()
                and not dungeon.goal_location.current_item.is_major_item
            ):
                dungeons.remove(dungeon)
            elif (
                not dungeon.goal_location.is_empty()
                and dungeon.goal_location.current_item.is_major_item
            ):
                dungeon.required = True
                num_required_dungeons -= 1
                if (
                    num_required_dungeons < 0
                    and self.setting("empty_unrequired_dungeons") == "on"
                ):
                    raise WrongInfoError(
                        "There are more major items plandomized at the end of dungeons than there are required dungeons. Please remove some plandomized major items at the end of dungeons"
                    )
                logging.getLogger("").debug(f"Chose {dungeons} as required dungeon")

        if num_required_dungeons > len(dungeons):
            raise WrongInfoError(
                "Not enough free goal locations to satisfy required dungeons. Please remove junk that has been plandomized at the end of dungeons"
            )

        random.shuffle(dungeons)
        for i in range(num_required_dungeons):
            dungeon = dungeons.pop()
            dungeon.required = True
            logging.getLogger("").debug(f"Chose {dungeon} as required dungeon")

    def set_nonprogress_locations(self):
        # Set excluded locations as non-progress
        for location_name in (
            self.setting_map.excluded_locations
            + self.setting_map.excluded_hint_locations
        ):
            self.get_location(location_name).progression = False

        # Sky Keep will never be a required dungeon with empty unrequired dungeons
        if self.setting("empty_unrequired_dungeons") == "on":
            self.dungeons["Sky Keep"].required = False

        # Set dungeon locations which should be barren as non-progress
        for dungeon in self.dungeons.values():
            if dungeon.should_be_barren():
                for location in dungeon.locations:
                    location.progression = False

        # Set beedle's shop items as nonprogress if they can only contain junk
        if self.setting("beedle_shop_shuffle") == "junk_only":
            for location in self.location_table.values():
                if "Beedle's Shop" in location.types:
                    location.progression = False

    # Remove or add junk to the item pool until the total number of
    # items is equal to the number of currently empty locations
    def sanitize_item_pool(self) -> None:
        # Get rid of any negative item counts. This can happen if
        # a user plandomizes an item into more locations than the
        # number of times the item appears in the pool
        for item, count in self.item_pool.items():
            if count < 0:
                self.item_pool[item] = 0

        num_empty_locations = len(
            [l for l in self.get_all_item_locations() if l.is_empty()]
        )
        while self.item_pool.total() < num_empty_locations:
            junk_item = self.get_item(get_random_junk_item_name())
            logging.getLogger("").debug(f"Added {junk_item} to item pool in {self}")
            self.item_pool[junk_item] += 1

        if self.item_pool.total() > num_empty_locations:
            junk_to_remove = []
            for junk in ALL_JUNK_ITEMS:
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

    # Replaces a portion of the non-major item pool with traps.
    def add_traps(self) -> None:
        item_pool_copy: list[Item] = []

        # Get item pool as list
        for item, count in self.item_pool.items():
            item_pool_copy.extend([item] * count)

        # Remove major items from item pool
        major_item_pool = [item for item in item_pool_copy if item.is_major_item]
        non_major_item_pool = [
            item for item in item_pool_copy if not item.is_major_item
        ]

        match self.setting("trap_mode"):
            case "trapish":
                num_traps = 10
            case "trapsome":
                num_traps = len(non_major_item_pool) // 4
            case "traps_o_plenty":
                num_traps = len(non_major_item_pool) // 2
            case "traptacular":
                num_traps = len(non_major_item_pool)
            case _:
                num_traps = 0

        possible_traps = [
            trap_name
            for trap_name in TRAP_SETTING_TO_ITEM
            if self.setting(trap_name) == "on"
        ]

        if len(possible_traps) <= 0:
            return

        # Replace non-major items with traps
        random.shuffle(non_major_item_pool)

        for replace_index in range(0, num_traps):
            if replace_index >= len(non_major_item_pool):
                break

            trap_item = TRAP_SETTING_TO_ITEM[random.choice(possible_traps)]
            non_major_item_pool[replace_index] = self.get_item(trap_item)

        new_item_pool = major_item_pool + non_major_item_pool

        assert len(item_pool_copy) == len(new_item_pool)

        self.item_pool = Counter()
        for item in new_item_pool:
            self.item_pool[item] += 1

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
            self.dungeons[dungeon_name].world = self

    def get_item(self, item_name: str) -> Item:
        item_name = item_name.replace("_", " ").replace("'", "")
        if item_name == "Nothing":
            return None  # type: ignore
        if item_name not in self.item_table:
            raise WrongInfoError(
                f'Item "{item_name}" is not defined in the item table for {self}'
            )
        return self.item_table[item_name]

    def get_game_winning_item(self) -> Item:
        for item in self.item_table.values():
            if item.is_game_winning_item:
                return item

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

    def get_gossip_stones(self) -> list[Location]:
        return [
            location
            for location in self.location_table.values()
            if "Hint Location" in location.types
            and location.name not in self.setting_map.excluded_locations
            and location.name not in self.setting_map.excluded_hint_locations
        ]

    def get_area(self, area_name) -> Area:
        if area_name not in self.area_ids:
            raise WrongInfoError(f'area "{area_name}" is not a defined area for {self}')
        return self.areas[self.area_ids[area_name]]

    def get_entrance(self, original_name: str) -> Entrance:
        parent_area_name, connected_area_name = original_name.split(" -> ")
        parent_area = self.get_area(parent_area_name)
        connected_area = self.get_area(connected_area_name)
        for exit_ in parent_area.exits:
            if exit_.original_connected_area == connected_area:
                return exit_

        raise WrongInfoError(f"There is no known entrance connection {original_name}")

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
        # Set the root to have all times of day (necessary for entrance rando)
        search.area_time[self.root.id] = TOD.ALL

    def get_shuffleable_entrances(
        self,
        entrance_type: str,
        only_primary: bool = False,
    ) -> list[Entrance]:
        entrances = []
        for area in self.areas.values():
            for exit_ in area.exits:
                if (
                    exit_.original_type != "None"
                    and (entrance_type == "All" or exit_.original_type == entrance_type)
                    and (exit_.primary or not only_primary)
                ):
                    entrances.append(exit_)
        return entrances

    def get_shuffled_entrances(
        self, entrance_type: str = "All", only_primary: bool = False
    ) -> list[Entrance]:
        entrances = self.get_shuffleable_entrances(entrance_type, only_primary)
        return [e for e in entrances if e.shuffled]
