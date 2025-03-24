from pathlib import Path
from filepathconstants import (
    OBJECTPACK_FILENAME,
    OBJECTPACK_PATH,
    CACHE_OARC_PATH,
)
from sslib.utils import write_bytes_create_dirs
from sslib.u8file import U8File
from .othermods import get_cache_oarc_path


def patch_object_folder(object_folder_output_path: Path, other_mods: list[str] = []):
    objectpack_arc = U8File.get_parsed_U8_from_path(OBJECTPACK_PATH)

    for path in objectpack_arc.get_all_paths():
        arc_name = path.split("/")[-1]
        oarc_path = get_cache_oarc_path(arc_name, other_mods)

        if oarc_path.exists():
            objectpack_arc.add_file_data(f"oarc/{arc_name}", oarc_path.read_bytes())
        else:
            raise Exception(f"ERROR: {arc_name} not found in oarc cache.")

    write_bytes_create_dirs(
        object_folder_output_path / OBJECTPACK_FILENAME,
        objectpack_arc.build_and_compress_U8(),
    )

    # Move oarc cache models to romfs/Object/NX
    # Patches to the ARCN arrays in the room bzs files allow these models to be found by the game
    for arc in CACHE_OARC_PATH.glob("*"):
        # TODO: actually deal with other mod support :p
        if not arc.name.endswith(".arc"):
            continue

        arc_name = f"{arc.name}"
        oarc = U8File.get_parsed_U8_from_path(CACHE_OARC_PATH / arc_name)

        write_bytes_create_dirs(
            object_folder_output_path / (arc_name + ".LZ"), oarc.build_and_compress_U8()
        )
