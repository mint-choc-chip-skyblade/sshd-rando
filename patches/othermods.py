from filepathconstants import OTHER_MODS_PATH, OARC_CACHE_PATH, STAGE_FILES_PATH

from pathlib import Path

def get_resolved_game_file_path(
    base_game_path: Path, other_mods: list[str] = [], specific_mod: str = ""
) -> tuple[Path, str]:
    game_path = None

    # Get the part of the path which just involves the game folders
    for i, part in enumerate(reversed(base_game_path.parts)):
        if part in ("romfs", "exefs"):
            game_path = "/".join(base_game_path.parts[-1 - i :])
            break

    # Some mods don't recompress their files, so we have to check for both compressed and noncompressed variations
    game_path_2 = get_other_file_path(game_path)

    for mod in other_mods:
        # If we're looking for the file from a specific mod, continue if this isn't that mod
        if specific_mod and mod != specific_mod:
            continue

        mod_dir = OTHER_MODS_PATH / mod
        for path in (game_path, game_path_2):
            final_path = mod_dir / path
            if final_path.exists():
                print(f'Found {path} from mod "{mod}"')
                return final_path, mod

    return base_game_path, ""


def get_oarc_cache_path(oarc_file: str, other_mods: list[str] = []):
    for mod in other_mods:
        path = OARC_CACHE_PATH / mod / oarc_file
        if path.exists():
            print(f'Found {oarc_file} from mod "{mod}"')
            return path

    return OARC_CACHE_PATH / oarc_file


# Some mods don't recompress their files, so in a bunch of instances we have to check if both the compressed or uncompressed
# ones exist
def get_other_file_path(path: str):
    return path[:-3] if path.endswith(".LZ") else f"{path}.LZ"
