from filepathconstants import ENTRANCE_SHUFFLE_DATA_PATH
from pathlib import Path
from typing import TYPE_CHECKING
import yaml

from .world import *
from .location import Location
from .entrance import Entrance

if TYPE_CHECKING:
    from .world import *


class PlandomizerError(RuntimeError):
    pass


class Plandomizer:
    def __init__(self) -> None:
        self.locations: dict[Location, Item] = {}
        self.entrances: dict[Entrance, Entrance] = {}
        self.shop_prices: dict[Location, int] = {}
        self.custom_messages: dict[Location, str] = {}


def load_plandomizer_data(worlds: list["World"], filepath: Path):
    if filepath == None:
        return
    if not filepath.is_file():
        raise PlandomizerError(f"Could not find plandomizer file: {filepath}")

    with open(filepath, "r", encoding="utf-8") as plando_file:
        plando = yaml.safe_load(plando_file)

        # Load plando data for all worlds
        for world in worlds:
            world_str = f"{world}"
            if world_str not in plando:
                continue
            world_data = plando[world_str]

            if "locations" in world_data:
                for location_name, item in world_data["locations"].items():
                    location = world.get_location(location_name)
                    # If the item is a string, use it directly
                    if type(item) is str:
                        world.plandomizer.locations[location] = world.get_item(item)
                    else:
                        # If any field is unrecognized, throw an error
                        for field in item:
                            if field not in ["item", "world", "price"]:
                                raise PlandomizerError(
                                    f"Unknown field for location {location} in plandomizer file."
                                )

                        # Set item if the field is there
                        if item["item"]:
                            # Get world id for item if specified
                            item_world = item.get("world", world.id)

                            # Throw an error if the specified world number doesn't exist
                            if item_world >= len(worlds):
                                raise PlandomizerError(
                                    f'Incorrect world number "{item["world"]}". Only {len(worlds)} world(s) are being generated.'
                                )

                            world.plandomizer.locations[location] = worlds[
                                item_world
                            ].get_item(item["item"])

                        # Set price if it's there
                        if item["price"]:
                            if "Price" not in location.types:
                                raise PlandomizerError(
                                    f"Location {location} does not have a price associated with it."
                                )
                            if item["price"] < 0:
                                raise PlandomizerError(
                                    f"Shop price must not be negative"
                                )
                            world.plandomizer.shop_prices[location] = item["price"]

            if "entrances" in world_data:
                alias_dict = load_entrance_aliases()
                for entrance_name, target_name in world_data["entrances"].items():
                    # Get proper names if aliases were used
                    if entrance_name in alias_dict:
                        entrance_name = alias_dict[entrance_name]
                    if target_name in alias_dict:
                        target_name = alias_dict[target_name]
                        target_parent, target_connected = target_name.split(" -> ")
                    else:
                        target_connected, target_parent = target_name.split(" from ")

                    entrance = world.get_entrance(entrance_name)
                    target = world.get_entrance(
                        f"{target_parent} -> {target_connected}"
                    )

                    world.plandomizer.entrances[entrance] = target

            if "sometimes_hint_locations" in world_data:
                # Clear previous sometimes locations
                for location in world.get_all_item_locations():
                    if location.hint_priority == "sometimes":
                        location.hint_priority = "never"

                for location_name in world_data["sometimes_hint_locations"]:
                    location = world.get_location(location_name)
                    location.hint_priority = "sometimes"

            if "always_hint_locations" in world_data:
                # Clear previous always locations
                for location in world.get_all_item_locations():
                    if location.hint_priority == "always":
                        location.hint_priority = "never"

                for location_name in world_data["always_hint_locations"]:
                    location = world.get_location(location_name)
                    location.hint_priority = "always"

            if "custom_messages" in world_data:
                for location_name, message in world_data["custom_messages"].items():
                    location = world.get_location(location_name)
                    if "Hint Location" not in location.types:
                        raise PlandomizerError(
                            f"{location} does not have a custom message associated with it."
                        )
                    world.plandomizer.custom_messages[location] = message


# Helper function to load entrance aliases since they aren't normally loaded until setting entrance data
def load_entrance_aliases() -> dict[str, str]:
    alias_dict: dict[str, str] = {}

    with open(ENTRANCE_SHUFFLE_DATA_PATH, encoding="utf-8") as entrance_data_file:
        entrance_shuffle_list = yaml.safe_load(entrance_data_file)

        for entrance_data in entrance_shuffle_list:
            original_name = entrance_data["forward"]["connection"]

            if alias := entrance_data["forward"].get("alias", None):
                alias_reverse_format = " from ".join(reversed(alias.split(" -> ")))
                alias_dict[alias] = original_name
                alias_dict[alias_reverse_format] = original_name

            if "return" in entrance_data:
                return_name = entrance_data["return"]["connection"]

                if alias := entrance_data["return"].get("alias", None):
                    alias_reverse_format = " from ".join(reversed(alias.split(" -> ")))
                    alias_dict[alias] = return_name
                    alias_dict[alias_reverse_format] = return_name

    return alias_dict
