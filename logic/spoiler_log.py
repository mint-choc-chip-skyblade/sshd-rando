from .world import *


def spoiler_format_location(location: Location, longest_name_length: int) -> str:
    spaces = longest_name_length - len(f"{location}")
    return f"{location}: {spaces * ' '}{location.current_item}"


def generate_spoiler_log(worlds: list[World]) -> None:
    filepath = "Spoiler Log.txt"
    with open(filepath, "w") as spoiler_log:
        # Get name lengths for pretty formating
        longest_name_length = 0
        for sphere in worlds[0].playthrough_spheres:
            for location in sphere:
                longest_name_length = max(longest_name_length, len(f"{location}"))

        # Print playthrough
        sphere_num = 1
        spoiler_log.write("Playthrough:\n")
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

        # Recalculate longest name length for all locations
        for location in worlds[0].location_table.values():
            longest_name_length = max(longest_name_length, len(f"{location}"))

        spoiler_log.write("\nAll Locations:\n")
        for world in worlds:
            spoiler_log.write(f"    {world}:\n")
            for location in world.location_table.values():
                if "Hint Location" not in location.types:
                    spoiler_log.write(
                        "        "
                        + spoiler_format_location(location, longest_name_length)
                        + "\n"
                    )

    print(f"Generated Spoiler Log at {filepath}")
