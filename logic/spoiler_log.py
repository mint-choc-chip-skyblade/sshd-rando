from logic.config import load_config_from_file
from randomizer.setting_string import setting_string_from_config
from .world import *
from .entrance_shuffle import create_entrance_pools
from filepathconstants import CONFIG_PATH, SPOILER_LOGS_PATH
from constants.randoconstants import VERSION
import os


def spoiler_format_location(
    location: Location, longest_name_length: int, override_item_name: str | None = None
) -> str:
    spaces = longest_name_length - len(f"{location}")

    if "Goddess Cube" in location.types:
        return f"{location}: {spaces * ' '}Strike Goddess Cube"

    if override_item_name == None:
        return f"{location}: {spaces * ' '}{location.current_item}"

    return f"{location}: {spaces * ' '}{override_item_name} # {location.current_item}"


def spoiler_format_entrance(entrance: Entrance, longest_name_length: int) -> str:
    spaces = longest_name_length - len(f"{entrance.alias}")
    replacement = entrance.replaces.alias
    parent, connected = replacement.split(" -> ")
    return f"{entrance.alias}: {spaces * ' '}{connected} from {parent}"


def log_basic_info(log, config: Config, worlds: list[World]) -> None:
    log.write(f"Skyward Sword HD Randomizer Version: {VERSION}\n")
    log.write(f"Seed: {config.seed}\n")

    log.write(
        f"Setting String: {setting_string_from_config(config, worlds[0].location_table)}\n"
    )
    log.write(f"Hash: {config.get_hash()}\n")


def log_settings(log, config: Config, worlds: list[World]) -> None:
    # Settings
    log.write(f"\n# Settings\n")
    log.write(f"seed: {config.seed}\n")
    log.write(
        f"generate_spoiler_log: {'true' if config.generate_spoiler_log else 'false'}\n"
    )
    log.write(f"plandomizer: {'true' if config.use_plandomizer else 'false'}\n")
    log.write(
        f"plandomizer_file: {config.plandomizer_file if config.plandomizer_file else 'null'}\n"
    )
    for world in worlds:
        log.write(f"{world}:\n")
        for setting in world.setting_map.settings.values():
            if setting.is_using_random_option:
                log.write(
                    f"    {setting.name}: '{setting.info.random_option}' # chose {setting.value}\n"
                )
            else:
                log.write(f"    {setting.name}: '{setting.value}'\n")
        log.write(
            f"    starting_inventory: {sorted(world.setting_map.starting_inventory.elements())}\n"
        )
        log.write(f"    excluded_locations: {world.setting_map.excluded_locations}\n")
        log.write(
            f"    excluded_hint_locations: {world.setting_map.excluded_hint_locations}\n"
        )
        log.write(
            f"    mixed_entrance_pools: {world.setting_map.mixed_entrance_pools}\n"
        )


def generate_spoiler_log(worlds: list[World]) -> None:
    print_progress_text("Generating Spoiler Log")

    # Create logs folder if it doesn't exist
    os.makedirs(SPOILER_LOGS_PATH, exist_ok=True)

    config = worlds[0].config
    filepath = f"{SPOILER_LOGS_PATH}/{config.get_hash()} Spoiler Log.txt"

    with open(filepath, "w", encoding="utf-8") as spoiler_log:
        log_basic_info(spoiler_log, config, worlds)

        # Print starting inventories if there are any
        if worlds_with_starting_inventories := [
            w for w in worlds if w.starting_item_pool.total() > 0
        ]:
            spoiler_log.write("\nStarting Inventory:\n")
            for world in worlds_with_starting_inventories:
                spoiler_log.write(f"    {world}:\n")
                for item in sorted(world.starting_item_pool.elements()):
                    spoiler_log.write(f"      - {item}\n")

        # Print Required dungeons if there are any
        if worlds_with_requried_dungeons := [
            w for w in worlds if any([True for d in w.dungeons.values() if d.required])
        ]:
            spoiler_log.write("\nRequired Dungeons:\n")
            for world in worlds_with_requried_dungeons:
                spoiler_log.write(f"    {world}:\n")
                for dungeon in world.dungeons.values():
                    if dungeon.required:
                        spoiler_log.write(f"      - {dungeon.name}\n")

        # Get name lengths for pretty formating
        longest_name_length = 0
        for sphere in worlds[0].playthrough_spheres:
            for location in sphere:
                longest_name_length = max(longest_name_length, len(f"{location}"))

        # Get shop item name lengths for pretty formatting
        longest_shop_item_length = 0
        for world in worlds:
            for location in world.location_table.values():
                if (
                    location.name in VANILLA_SHOP_PRICES
                    and len(location.current_item.name) > longest_shop_item_length
                ):
                    longest_shop_item_length = len(location.current_item.name)

        # Print playthrough
        sphere_num = 0
        spoiler_log.write("\nPlaythrough:\n")
        for sphere in worlds[0].playthrough_spheres:
            sphere = sorted(sphere)
            spoiler_log.write(f"    Sphere {sphere_num}:\n")
            for location in sphere:
                override_item_name = None
                if (
                    location.current_item.name in BOTTLE_ITEMS
                    and location.current_item.name != EMPTY_BOTTLE
                ):
                    override_item_name = EMPTY_BOTTLE

                formatted_location_name = spoiler_format_location(
                    location,
                    longest_name_length,
                    override_item_name=get_item_override_name(location),
                )

                if (
                    world.setting("randomize_shop_prices") == "on"
                    and location.name in world.shop_prices
                ):
                    price_info = f" # Price: {world.shop_prices[location.name]:>4}R"
                    formatted_location_name += (
                        " "
                        * (longest_shop_item_length - len(location.current_item.name))
                    ) + price_info

                spoiler_log.write("        " + formatted_location_name + "\n")
            sphere_num += 1

        # Get name lengths for entrances for pretty formatting
        longest_name_length = 0
        for sphere in worlds[0].entrance_spheres:
            for entrance in sphere:
                longest_name_length = max(longest_name_length, len(entrance.alias))

        # Print entrance playthrough
        sphere_num = 0
        if len([e for sphere in worlds[0].entrance_spheres for e in sphere]) > 0:
            spoiler_log.write("\nEntrance Playthrough:\n")
        for sphere in worlds[0].entrance_spheres:
            sphere_num += 1
            if len(sphere) == 0:
                continue
            spoiler_log.write(f"    Sphere {sphere_num}:\n")

            for entrance in sorted(sphere):
                spoiler_log.write(
                    "        "
                    + spoiler_format_entrance(entrance, longest_name_length)
                    + "\n"
                )

        # Recalculate longest name length for all locations
        longest_name_length = 0
        for location in worlds[0].location_table.values():
            if "Goddess Cube" not in location.types:
                longest_name_length = max(longest_name_length, len(f"{location}"))

        # Output all enabled locations
        spoiler_log.write("\nEnabled Locations:\n")
        for world in worlds:
            spoiler_log.write(f"    {world}:\n")

            disabled_shuffle_locations = get_disabled_shuffle_locations(
                world.location_table, world.config.settings[0]
            )

            for location in world.location_table.values():
                if "Gratitude Crystals" in location.types or (
                    location not in disabled_shuffle_locations
                    and "Hint Location" not in location.types
                    and "Goddess Cube" not in location.types
                ):
                    formatted_location_name = spoiler_format_location(
                        location,
                        longest_name_length,
                        override_item_name=get_item_override_name(location),
                    )

                    if (
                        world.setting("randomize_shop_prices") == "on"
                        and location.name in world.shop_prices
                    ):
                        price_info = f" # Price: {world.shop_prices[location.name]:>4}R"
                        formatted_location_name += (
                            " "
                            * (
                                longest_shop_item_length
                                - len(location.current_item.name)
                            )
                        ) + price_info

                    spoiler_log.write("        " + formatted_location_name + "\n")

        # Recalculate longest name length for all shuffled entrances
        longest_name_length = 0
        for world in worlds:
            for entrance in world.get_shuffled_entrances():
                longest_name_length = max(longest_name_length, len(entrance.alias))

        if worlds_with_shuffled_entrances := [
            w for w in worlds if len(w.get_shuffled_entrances()) > 0
        ]:
            spoiler_log.write("\nAll Entrances:\n")
            for world in worlds_with_shuffled_entrances:
                spoiler_log.write(f"    {world}:\n")
                entrance_pools = create_entrance_pools(world)
                for entrance_type, pool in entrance_pools.items():
                    spoiler_log.write(f"        {entrance_type}:\n")
                    for entrance in sorted(pool):
                        # Ignore entrances that are impossible
                        if entrance.requirement.type == RequirementType.IMPOSSIBLE:
                            continue
                        spoiler_log.write(
                            "            "
                            + spoiler_format_entrance(entrance, longest_name_length)
                            + "\n"
                        )

        # Print hints if there are any
        if worlds_with_hints := [
            world
            for world in worlds
            if world.fi_hints
            or world.gossip_stone_hints
            or world.song_hints
            or world.impa_sot_hint
        ]:
            spoiler_log.write("\nHints:\n")
            for world in worlds_with_hints:
                spoiler_log.write(f"    {world}:\n")
                if world.fi_hints:
                    spoiler_log.write("        Fi Hints:\n")
                    for location in world.fi_hints:
                        spoiler_log.write(f"            {location.hint}")
                        if location.hint.type == "Path":
                            spoiler_log.write(f" ({location.current_item})")
                        spoiler_log.write("\n")
                if world.gossip_stone_hints:
                    spoiler_log.write("        Gossip Stone Hints:\n")
                    for stone, locations in world.gossip_stone_hints.items():
                        spoiler_log.write(f"            {stone}:\n")
                        for location in locations:
                            spoiler_log.write(f"                {location.hint}")
                            if location.hint.type == "Path":
                                spoiler_log.write(f" ({location.current_item})")
                            spoiler_log.write("\n")
                if world.song_hints:
                    spoiler_log.write("        Song Hints:\n")
                    for song, hint in world.song_hints.items():
                        spoiler_log.write(f"            {song}: {hint}\n")
                if world.impa_sot_hint:
                    spoiler_log.write("        Impa Hint:\n")
                    spoiler_log.write(f"            {world.impa_sot_hint}\n")

        # Recalculate longest name length for all locations
        longest_name_length = 0
        for location in worlds[0].location_table.values():
            if "Goddess Cube" not in location.types:
                longest_name_length = max(longest_name_length, len(f"{location}"))

        # Output all disabled locations
        spoiler_log.write("\nDisabled Locations:\n")
        for world in worlds:
            spoiler_log.write(f"    {world}:\n")

            disabled_shuffle_locations = get_disabled_shuffle_locations(
                world.location_table, world.config.settings[0]
            )

            for location in world.location_table.values():
                if location in disabled_shuffle_locations:
                    formatted_location_name = spoiler_format_location(
                        location,
                        longest_name_length,
                        override_item_name=get_item_override_name(location),
                    )

                    if (
                        world.setting("randomize_shop_prices") == "on"
                        and location.name in world.shop_prices
                    ):
                        price_info = f" # Price: {world.shop_prices[location.name]:>4}R"
                        formatted_location_name += (
                            " "
                            * (
                                longest_shop_item_length
                                - len(location.current_item.name)
                            )
                        ) + price_info

                    spoiler_log.write("        " + formatted_location_name + "\n")

        log_settings(spoiler_log, config, worlds)


def generate_anti_spoiler_log(worlds: list[World]) -> None:
    print_progress_text("Generating Anti-Spoiler Log")

    # Create logs folder if it doesn't exist
    os.makedirs(SPOILER_LOGS_PATH, exist_ok=True)

    config = worlds[0].config
    filepath = f"{SPOILER_LOGS_PATH}/{config.get_hash()} Anti Spoiler Log.txt"
    with open(filepath, "w", encoding="utf-8") as anti_spoiler_log:
        log_basic_info(anti_spoiler_log, config, worlds)
        log_settings(anti_spoiler_log, config, worlds)


def get_item_override_name(location: Location) -> str | None:
    if (
        location.current_item.name in BOTTLE_ITEMS
        and location.current_item.name != EMPTY_BOTTLE
    ):
        return EMPTY_BOTTLE
    return None
