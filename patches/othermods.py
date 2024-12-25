from filepathconstants import (
    OTHER_MODS_PATH,
    COMBINED_MODS_FOLDER,
    COMBINED_MODS_PATH,
    OARC_CACHE_PATH,
    SSHD_EXTRACT_PATH,
)
from gui.dialogs.dialog_header import print_progress_text
from sslib.u8file import U8File
from sslib.utils import write_bytes_create_dirs

from pathlib import Path
from shutil import rmtree
from collections import defaultdict
import copy
import os


def get_resolved_game_file_path(
    base_game_path: Path, other_mods: list[str] = [], specific_mod: str | None = None
) -> tuple[Path, str]:

    if specific_mod == "":
        return base_game_path, ""

    game_path = None

    # Get the part of the path which just involves the game folders
    for i, part in enumerate(reversed(base_game_path.parts)):
        if part in ("romfs", "exefs"):
            game_path = "/".join(base_game_path.parts[-1 - i :])
            break

    # Some mods don't recompress their files, so we have to check for both compressed and noncompressed variations
    game_path_2 = get_other_file_path(game_path)

    # Check the combined mods folder first before individual mods
    mod_folders = [COMBINED_MODS_FOLDER] + other_mods

    for mod in mod_folders:
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


# Verifies that all included mods can be used together. If mods can't be used together because they modify the same
# files that we can't resolve the differences between, then an error will be thrown
def verify_other_mods(other_mods: list[str]) -> bool:

    # Keep track of which files are modified by which mods
    mod_files: dict[str, list[str]] = defaultdict(list)

    for mod in other_mods:
        # Don't allow patching if we can't find the other mod
        if not (OTHER_MODS_PATH / mod).exists():
            raise Exception(
                f'Could not find mod "{mod}". Please make sure it\'s in the "other_mods" folder.'
            )

        if not (OTHER_MODS_PATH / mod / "romfs").exists():
            raise Exception(
                f'Mod "{mod}" does not contain a romfs folder. Please make sure the romfs folder is directly within the mod folder.'
            )

        # Find all the individual game files that each mod modifies
        for root, dirs, files in os.walk(OTHER_MODS_PATH / mod):
            for file in files:
                file_path = os.path.join(root, file)

                # Get the part of the path which just involves the game folders
                for i, part in enumerate(reversed(Path(file_path).parts)):
                    if part in ("romfs", "exefs"):
                        file_path = "/".join(Path(file_path).parts[-1 - i :])
                        break

                # Store the modded file path (and it's potential counterpart)
                mod_files[file_path].append(mod)
                mod_files[get_other_file_path(file_path)].append(mod)

    # For all files that the mods modify
    for file_path, mods in mod_files.items():
        # If more than 1 mod modifies this file and it's not the objectpack, then attempt to build a combined version
        # of the file if it's an archive file
        if (
            len(mods) > 1
            and (SSHD_EXTRACT_PATH / file_path).exists()
            and "ObjectPack.arc" not in file_path
        ):
            if not file_path.endswith(".arc") and not file_path.endswith(".LZ"):
                raise RuntimeError(
                    f"Unable to combine mods {mods} due to conflicts in file {file_path}"
                )
            build_combined_mod_file(file_path, other_mods)


# Attempts to combine two archive files from different mods. If multiple mods modify the same files within the archive
# then an error is thrown
def build_combined_mod_file(game_path: str, other_mods: list[str] = []):

    # Get all the mods which modify this file
    files_to_combine: list[U8File] = []
    for mod in other_mods:
        path_to_file = OTHER_MODS_PATH / mod / game_path
        if path_to_file.exists():
            files_to_combine.append((U8File.get_parsed_U8_from_path(path_to_file), mod))
        else:
            other_path = Path(get_other_file_path(path_to_file.as_posix()))
            if other_path.exists():
                files_to_combine.append(
                    (U8File.get_parsed_U8_from_path(other_path), mod)
                )

    print(
        f"Attempting to combine {game_path} from mods: {[t[1] for t in files_to_combine]}"
    )

    new_file = combine_mod_files(
        U8File.get_parsed_U8_from_path(SSHD_EXTRACT_PATH / game_path), files_to_combine
    )

    # Only compress if the original game file ends with .LZ, otherwise the game might throw a fit
    if game_path.endswith(".LZ"):
        new_file = new_file.build_and_compress_U8()
    else:
        new_file = new_file.build_U8()

    write_bytes_create_dirs(COMBINED_MODS_PATH / game_path, new_file)


# Combine the data from different mod files into the base file. base_file is expected to be the base game file
def combine_mod_files(
    base_file: U8File, files_to_combine: list[tuple[U8File, str]]
) -> U8File:
    for path in base_file.get_all_paths():
        base_game_data = base_file.get_file_data(path)
        modded_files: list[tuple[bytes, str]] = []
        for mod_file, mod in files_to_combine:

            mod_file_path = copy.deepcopy(path)
            # Some mods have an extra directory named "." in their archive files for some reason. Account for this
            if next(mod_file.get_all_paths()).startswith("/."):
                mod_file_path = f"/.{mod_file_path}"

            mod_data = mod_file.get_file_data(mod_file_path)
            if mod_data != base_game_data:
                modded_files.append((mod_data, mod))

        if len(modded_files) == 1:
            modded_data, mod = modded_files[0]
            base_file.set_file_data(path, modded_data)
            # print(f"Using {path} from mod {mod}")
        elif len(modded_files) > 1:
            raise RuntimeError(
                f"Unable to combine mods {[m[1] for m in modded_files]} due to conflicts in {path}"
            )

    return base_file


# If any active mods modify extra files not touched by the randomizer, then copy them over here
def copy_extra_mod_files(other_mods: list[str], output_dir: Path):

    if not other_mods:
        return

    print_progress_text(f"Copying Extra Mod Files")

    # Check the combined mods folder first before any individual mods
    mod_folders = [COMBINED_MODS_FOLDER] + other_mods

    for mod in mod_folders:
        for root, dirs, files in os.walk(OTHER_MODS_PATH / mod):
            for file in files:
                file_path = os.path.join(root, file)
                # Get the part of the path which just involves the game folders
                for i, part in enumerate(reversed(Path(file_path).parts)):
                    if part in ("romfs", "exefs"):
                        file_path = "/".join(Path(file_path).parts[-1 - i :])
                        break

                path = output_dir / file_path
                other_path = (
                    output_dir / f"{file_path[:-3]}"
                    if file_path.endswith(".LZ")
                    else output_dir / f"{file_path}.LZ"
                )

                if not path.exists() and not other_path.exists():
                    print(f"Copying {mod}/{file_path} to output")
                    write_bytes_create_dirs(
                        path, (OTHER_MODS_PATH / mod / file_path).read_bytes()
                    )

    # Since this is the last step in the process, we can delete the temporary combined mods folder here
    if Path(COMBINED_MODS_PATH).exists():
        rmtree(COMBINED_MODS_PATH)
