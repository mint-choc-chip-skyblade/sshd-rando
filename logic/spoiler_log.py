from .world import *
from .entrance_shuffle import create_entrance_pools


def spoiler_format_location(location: Location, longest_name_length: int) -> str:
    spaces = longest_name_length - len(f"{location}")
    if "Goddess Cube" in location.types:
        return f"{location}"
    return f"{location}: {spaces * ' '}{location.current_item}"


def spoiler_format_entrance(entrance: Entrance, longest_name_length: int) -> str:
    spaces = longest_name_length - len(f"{entrance}")
    replacement = entrance.replaces.original_name
    parent, connected = replacement.split(" -> ")
    return f"{entrance}: {spaces * ' '}{connected} from {parent}"


def generate_spoiler_log(worlds: list[World]) -> None:
    filepath = "Spoiler Log.txt"
    with open(filepath, "w") as spoiler_log:
        spoiler_log.write(f"Seed: {worlds[0].config.seed}\n")
        # Print starting inventories if there are any
        if any([True for world in worlds if world.starting_item_pool.total() > 0]):
            spoiler_log.write("\nStarting Inventory:\n")
            for world in worlds:
                spoiler_log.write(f"    {world}:\n")
                for item, count in world.starting_item_pool.items():
                    for _ in range(count):
                        spoiler_log.write(f"      - {item}\n")

        # Print Required dungeons if there are any
        if any([True for w in worlds for d in w.dungeons.values() if d.required]):
            spoiler_log.write("\nRequired Dungeons:\n")
            for world in worlds:
                spoiler_log.write(f"    {world}:\n")
                for dungeon in world.dungeons.values():
                    if dungeon.required:
                        spoiler_log.write(f"      - {dungeon.name}\n")

        # Get name lengths for pretty formating
        longest_name_length = 0
        for sphere in worlds[0].playthrough_spheres:
            for location in sphere:
                longest_name_length = max(longest_name_length, len(f"{location}"))

        # Print playthrough
        sphere_num = 1
        spoiler_log.write("\nPlaythrough:\n")
        for sphere in worlds[0].playthrough_spheres:
            sphere = sorted(sphere)
            spoiler_log.write(f"    Sphere {sphere_num}:\n")
            for location in sphere:
                spoiler_log.write(
                    "        "
                    + spoiler_format_location(location, longest_name_length)
                    + "\n"
                )
            sphere_num += 1

        # Get name lengths for entrances for pretty formatting
        longest_name_length = 0
        for sphere in worlds[0].entrance_spheres:
            for entrance in sphere:
                longest_name_length = max(longest_name_length, len(f"{entrance}"))

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

        spoiler_log.write("\nAll Locations:\n")
        for world in worlds:
            spoiler_log.write(f"    {world}:\n")
            for location in world.location_table.values():
                if (
                    "Hint Location" not in location.types
                    and "Goddess Cube" not in location.types
                ):
                    spoiler_log.write(
                        "        "
                        + spoiler_format_location(location, longest_name_length)
                        + "\n"
                    )

        # Recalculate longest name length for all shuffled entrances
        longest_name_length = 0
        for world in worlds:
            for entrance in world.get_shuffled_entrances():
                longest_name_length = max(longest_name_length, len(f"{entrance}"))

        if any([len(world.get_shuffled_entrances()) for world in worlds]):
            spoiler_log.write("\nAll Entrances:\n")
            for world in worlds:
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

    print_progress_text(f"Generated Spoiler Log at {filepath}")
