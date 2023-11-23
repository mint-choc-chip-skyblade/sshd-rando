from pathlib import Path
from .world import *

import yaml


class PlandomizerError(RuntimeError):
    pass


def load_plandomizer_data(worlds: list[World], filepath: Path):
    if filepath == None:
        return
    if not filepath.is_file():
        raise PlandomizerError(f"Could not find plandomizer file: {filepath}")

    with open(filepath, "r") as plando_file:
        plando = yaml.safe_load(plando_file)

        # Load plando data for all worlds
        for world in worlds:
            world_str = f"{world}"
            if world_str not in plando:
                continue
            world_data = plando[world_str]

            if "locations" in world_data:
                for location, item in world_data["locations"].items():
                    # If the item is a string, use it directly
                    if type(item) is str:
                        world.plandomizer_locations[
                            world.get_location(location)
                        ] = world.get_item(item)
                    else:
                        # If the item isn't a string, then it should have world and item specifications
                        for field in ["world", "item"]:
                            if field not in item:
                                raise PlandomizerError(
                                    f"The item being plandomized at {location} in {world} is missing the {field} field"
                                )

                        # Throw an error if the specified world number doesn't exist
                        if item["world"] > len(worlds):
                            raise PlandomizerError(
                                f'Incorrect world number "{item["world"]}". Only {len(worlds)} world(s) are being generated.'
                            )

                        world.plandomizer_locations[
                            world.get_location(location)
                        ] = worlds[item["world"] - 1].get_item(item["item"])

            if "entrances" in world_data:
                for entrance_name, target_name in world_data["entrances"].items():
                    target_connected, target_parent = target_name.split(" from ")

                    entrance = world.get_entrance(entrance_name)
                    target = world.get_entrance(
                        f"{target_parent} -> {target_connected}"
                    )

                    world.plandomizer_entrances[entrance] = target
