from pathlib import Path
import time
from filepathconstants import (
    OBJECTPACK_FILENAME,
    OBJECTPACK_PATH,
    CACHE_OARC_PATH,
)
from gui.dialogs.dialog_header import (
    get_progress_value_from_range,
    print_progress_text,
    update_progress_value,
)
from sslib.utils import write_bytes_create_dirs
from sslib.u8file import U8File
from .othermods import get_cache_oarc_path


def patch_object_folder(object_folder_output_path: Path, other_mods: list[str] = []):
    print_progress_text("Moving arcs to Object folder")
    start_move_arcs_time = time.process_time()

    objectpack_arc = U8File.get_parsed_U8_from_path(OBJECTPACK_PATH)
    objectpack_arc_names = [
        path.split("/")[-1] for path in objectpack_arc.get_all_paths()
    ]

    cache_oarc_paths = list(CACHE_OARC_PATH.glob("*"))

    # Move oarc cache models to romfs/Object/NX or the ObjectPack as is appropriate.
    # Patches made previously to the ARCN arrays in the room bzs files allow these models to be found by the game.
    for current_arc_num, arc in enumerate(cache_oarc_paths):
        # Only deal with .arc files
        if not arc.name.endswith(".arc"):
            continue

        arc_data_path = get_cache_oarc_path(arc.name, other_mods)
        if not arc_data_path.exists():
            raise Exception(f"ERROR: {arc.name} not found in oarc cache.")

        # Replace arcs in objectpack. If an arc doesn't belong there, add it to the Object/NX folder.
        if arc.name in objectpack_arc_names:
            objectpack_arc.add_file_data(f"oarc/{arc.name}", arc_data_path.read_bytes())
        else:
            oarc = U8File.get_parsed_U8_from_path(CACHE_OARC_PATH / arc.name)

            write_bytes_create_dirs(
                object_folder_output_path / (arc.name + ".LZ"),
                oarc.build_and_compress_U8(),
            )

        update_progress_value(
            get_progress_value_from_range(57, 7, current_arc_num, len(cache_oarc_paths))
        )

    print(f"Moving arcs took {(time.process_time() - start_move_arcs_time)} seconds")
    start_objectpack_rebuilding_time = time.process_time()

    update_progress_value(57)
    print_progress_text("Rebuilding ObjectPack")

    write_bytes_create_dirs(
        object_folder_output_path / OBJECTPACK_FILENAME,
        objectpack_arc.build_and_compress_U8(),
    )

    end_objectpack_patching_time = time.process_time()
    print(
        f"Rebuilding ObjectPack took {(end_objectpack_patching_time - start_objectpack_rebuilding_time)} seconds"
    )
    print(
        f"Total Object folder patching took {(end_objectpack_patching_time - start_move_arcs_time)} seconds"
    )
