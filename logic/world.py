from logic.config import Config
from logic.settings import *
from logic.item import Item
from logic.location import Location
from logic.area import *
from logic.requirements import *
from logic.item_pool import *

from collections import Counter
import logging
import yaml
import os

class MissingInfoError(RuntimeError):
    pass

class WrongInfoError(RuntimeError):
    pass

class World:
    def __init__(self, id_ : int) -> None:
        self.id = id_
        self.config: Config = None

        self.setting_map: SettingMap = SettingMap()

        self.item_table: dict[str, Item] = {}
        self.location_table: dict[str, Location] = {}
        self.areas: dict[int, Area] = {}
        self.macros: dict[str, Requirement] = {}

        # Map event names to ids and ids to names
        self.events: dict[str, int] = {}
        self.reverse_events: dict[int, str] = {}

        # Map area names to ids
        self.area_ids: dict[str, int] = {}

        self.item_pool: Counter[Item] = Counter()
        self.starting_item_pool: Counter[Item] = Counter()
        self.root: Area = None

        self.playthrough_spheres: list[set[Location]] = None

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
        logging.getLogger('').debug(f"Building Item Table for {self}")
        with open("data/items.yaml", "r") as item_data_file:

            item_data = yaml.safe_load(item_data_file)
            for item_node in item_data:

                # Check to make sure all neccesary fields exist
                for field in ["id", "name"]:
                    if field not in item_node:
                        raise MissingInfoError(f"item \"{item_node['name']}\" is missing the \"{field}\" field in items.yaml")

                item_id = int(item_node["id"])
                name = item_node["name"]
                major_item = item_node["advancement"] if "advancement" in item_node else False
                game_winning_item = item_node["game_winning_item"] if "game_winning_item" in item_node else False
                
                # TODO: Load the rest of the data

                stripped_name = name.replace('\'', '')
                self.item_table[stripped_name] = Item(item_id, name, self, major_item, game_winning_item)
                logging.getLogger('').debug(f"Processing new item {name}\tid: {item_id}")


    # Read checks.yaml and store all necessary data in a dict
    # for this world
    def build_location_table(self) -> None:
        logging.getLogger('').debug(f"Building Location Table for {self}")
        with open("data/locations.yaml", "r") as item_data_file:

            location_id_counter = 0
            location_data = yaml.safe_load(item_data_file)
            for location_node in location_data:

                # Check to make sure all required fields exist
                for field in ["name", "original_item"]:
                    if field not in location_node:
                        raise MissingInfoError(f"location \"{location_node['name']}\" is missing the \"{field}\" field in items.yaml")

                name = location_node["name"]
                original_item = self.get_item(location_node["original_item"])
                types = location_node["type"] if "type" in location_node else []
                if types == None:
                    types = []
                location_id = location_id_counter
                location_id_counter += 1

                # TODO: Load the rest of the data

                self.location_table[name] = Location(location_id, name, types, self, original_item)
                logging.getLogger('').debug(f"Processing new location {name}\tid: {location_id}\toriginal item: {original_item}")


    def load_logic_macros(self) -> None:
        logging.getLogger('').debug(f"Loading macros for {self}")
        with open("data/macros.yaml", "r") as macros_data_file:
            macros_data = yaml.safe_load(macros_data_file)
            for macro_name, req_str in macros_data.items():
                self.macros[macro_name] = parse_requirement_string(req_str, self)


    def load_world_graph(self) -> None:
        logging.getLogger('').debug(f"Loading world graph for {self}")

        # Make sure all used events are defined
        defined_events = []
        defined_areas = set()
        
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
                            raise MissingInfoError(f"An area node is missing the name field")
                    
                    area_name = area_node["name"]
                    self.add_area(area_name)
                    new_area = self.areas[self.area_ids[area_name]]
                    new_area.name = area_name
                    new_area.world = self
                    defined_areas.add(new_area)

                    if "allowed_time_of_day" in area_node and self.setting("natural_night_connections") == "on":
                        new_area.allowed_tod = TOD.DAY if area_node["allowed_time_of_day"] == "Day Only" else TOD.ALL
                    
                    if "can_sleep" in area_node:
                        new_area.can_sleep = True

                    if "events" in area_node:
                        for event_name, req_str in area_node["events"].items():
                            # Replace spaces with underscores to match logic syntax
                            event_name = event_name.replace(' ', '_')
                            defined_events.append(event_name)
                            self.add_event(event_name)
                            event_req = parse_requirement_string(req_str, self)
                            new_area.events.append(EventAccess(self.events[event_name], event_req, new_area))
                    
                    if "locations" in area_node:
                        for location_name, req_str in area_node["locations"].items():
                            location_req = parse_requirement_string(req_str, self)
                            new_area.locations.append(LocationAccess(self.get_location(location_name), location_req, new_area))
                            # Add the LocationAccess to the list of access points for the location
                            self.get_location(location_name).loc_access_list.append(new_area.locations[-1])

                    if "exits" in area_node:
                        for connected_area_name, req_str in area_node["exits"].items():
                            exit_req = parse_requirement_string(req_str, self)
                            self.add_area(connected_area_name)
                            connected_area = self.areas[self.area_ids[connected_area_name]]
                            connected_area.name = connected_area_name
                            new_area.exits.append(Entrance(new_area, connected_area, exit_req, self))
        
        # Check to make sure all events were properly defined
        # Uncomment when world graph is finished
        # for event in self.events:
        #     if event not in defined_events:
        #         raise MissingInfoError(f"Event \'{event}\' is used, but never defined")

        # Same for areas

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
        self.location_table["Hylia's Realm - Defeat Demise"].set_current_item(self.get_item("Game Beatable"))


    # Adds a new event if one with the current name doesn't exist
    def add_event(self, event_name: str) -> None:
        if event_name not in self.events:
            id = len(self.events) + (100000 * self.id) # Should be fine as long as never need more than 100000 events per world
            self.events[event_name] = id
            self.reverse_events[id] = event_name

    # Adds a new area if one with the current name doesn't exist
    # Just creates the entry and doesn't set any of its properties except the id
    def add_area(self, area_name: str) -> None:
        if area_name not in self.area_ids:
            area_id = len(self.area_ids) + (100000 * self.id) # Should be fine as long as we never need more than 100000 areas per world
            self.area_ids[area_name] = area_id
            self.areas[area_id] = Area()
            self.areas[area_id].id = area_id
            if area_name == "Root":
                self.root = self.areas[area_id]


    def get_item(self, item_name: str) -> Item:
        item_name = item_name.replace('_', ' ').replace('\'', '')
        if item_name == "Nothing":
            return None
        if item_name not in self.item_table:
            raise WrongInfoError(f"Item \"{item_name}\" is not defined in the item table for {self}")
        return self.item_table[item_name]
    

    def get_location(self, location_name: str) -> Location:
        if location_name not in self.location_table:
            raise WrongInfoError(f"Location \"{location_name}\" is not defined in location table for {self}")
        return self.location_table[location_name]


    def get_macro(self, macro_name: str) -> Requirement:
        macro_name = macro_name.replace('_', ' ')
        if macro_name not in self.macros:
            raise WrongInfoError(f"Macro \"{macro_name}\" was not previously not defined for {self}")
        return self.macros[macro_name]


    def setting(self, setting_name: str) -> SettingGet:
        if setting_name not in self.setting_map.settings:
            raise SettingInfoError(f"No Setting named \"{setting_name}\" in settings for {self}")
        return SettingGet(setting_name, self.setting_map.settings[setting_name])
    

    def set_search_starting_properties(self, search):
        # Set the root to have daytime
        # TODO: Change if we ever have an option to start at night
        search.area_time[self.root.id] = TOD.DAY