import logging
from filepathconstants import LOCATIONS_PATH
from logic.location import Location
from logic.settings import SettingMap

from sslib.yaml import yaml_load

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import World


def build_location_table(world: "World | None" = None) -> dict[str, Location]:
    logging.getLogger("").debug(f"Building Location Table for {world}")
    location_data = yaml_load(LOCATIONS_PATH)
    location_id_counter = 0

    location_table: dict[str, Location] = {}

    for location_node in location_data:
        # Check to make sure all required fields exist
        for field in ["name", "original_item", "types"]:
            if field not in location_node:
                raise Exception(
                    f"location \"{location_node['name']}\" is missing the \"{field}\" field in locations.yaml"
                )

        name: str = location_node["name"]
        original_item = location_node["original_item"]

        if world is not None:
            original_item = world.get_item(location_node["original_item"])

        types: list[str] = location_node.get("types", [])
        is_gui_excluded_location: bool = location_node.get(
            "is_gui_excluded_location", True
        )
        patch_paths: list[str] = location_node.get("Paths", [])
        goal_location: bool = location_node.get("goal_location", False)
        hint_priority: str = location_node.get("hint", "never")
        hint_textfile: str = location_node.get("textfile", "")
        hint_textindex: int = location_node.get("textindex", -1)
        eventflowindex: int = location_node.get("eventflowindex", -1)
        location_id = location_id_counter
        location_id_counter += 1

        location_table[name] = Location(
            location_id,
            name,
            types,
            is_gui_excluded_location,
            world,
            original_item,
            patch_paths,
            goal_location,
            hint_priority,
            hint_textfile,
            hint_textindex,
            eventflowindex,
        )
        logging.getLogger("").debug(
            f"Processing new location {name}\tid: {location_id}\toriginal item: {original_item}"
        )

    return location_table


def get_disabled_shuffle_locations(
    location_table: dict[str, Location],
    settings_map: SettingMap,
    ui_mode: bool = False,
) -> list[Location]:
    settings = settings_map.settings

    non_vanilla_locations = [
        location
        for location in location_table.values()
        if location.types is not None
        and "Hint Location" not in location.types
        and (
            (
                settings["beedle_shop_shuffle"].value == "vanilla"
                and "Beedle's Airshop" in location.types
            )
            or (
                settings["gratitude_crystal_shuffle"].value == "off"
                and "Gratitude Crystals" in location.types
            )
            or (
                settings["goddess_chest_shuffle"].value == "off"
                and "Goddess Chests" in location.types
            )
            or (
                (
                    settings["stamina_fruit_shuffle"].value == "off"
                    or (
                        not ui_mode and location.name in settings_map.excluded_locations
                    )
                )
                and "Stamina Fruits" in location.types
            )
            or (
                settings["npc_closet_shuffle"].value == "vanilla"
                and "Closets" in location.types
            )
            or (
                settings["hidden_item_shuffle"].value == "off"
                and "Hidden Items" in location.types
            )
            or (
                settings["rupee_shuffle"].value == "vanilla"
                and "Freestanding Rupees" in location.types
            )
            or (
                settings["rupee_shuffle"].value == "beginner"
                and (
                    "Intermediate Rupees" in location.types
                    or "Advanced Rupees" in location.types
                )
            )
            or (
                settings["rupee_shuffle"].value == "intermediate"
                and "Advanced Rupees" in location.types
            )
            or (
                settings["underground_rupee_shuffle"].value == "off"
                and "Underground Rupees" in location.types
            )
            # Split off the relic number for the check name and compare it to the number of treasures being allowed.
            # If it's higher than the trial treasuresanity number it'll be a vanilla location
            or (
                "Dusk Relic" in location.types
                and settings["trial_treasuresanity"].value != "random"
                and int(location.name.split(" ")[-1], 0)
                > int(settings["trial_treasuresanity"].value, 0)
            )
        )
    ]

    return non_vanilla_locations
