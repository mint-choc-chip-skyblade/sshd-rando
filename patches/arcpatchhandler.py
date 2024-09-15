from pathlib import Path
import time
from filepathconstants import (
    CACHE_OARC_PATH,
    OBJECTPACK_PATH,
)
from gui.dialogs.dialog_header import print_progress_text
from sslib.utils import write_bytes_create_dirs
from sslib.u8file import U8File


def patch_object_pack(object_pack_output_path: Path) -> list[str]:
    print_progress_text("Creating ObjectPack patches")
    start_objectpack_creation_time = time.process_time()

    objectpack_arc = U8File.get_parsed_U8_from_path(OBJECTPACK_PATH, True)

    for arc in CACHE_OARC_PATH.glob("*"):
        arc_name = f"{arc.name}"
        oarc_path = CACHE_OARC_PATH / arc_name

        objectpack_arc.add_file_data(f"oarc/{arc_name}", oarc_path.read_bytes())
    
    print(f"Creating ObjectPack took {(time.process_time() - start_objectpack_creation_time)} seconds")
    start_objectpack_rebuilding_time = time.process_time()

    print_progress_text("Rebuilding ObjectPack")
    write_bytes_create_dirs(
        object_pack_output_path, objectpack_arc.build_and_compress_U8()
    )

    end_objectpack_patching_time = time.process_time()
    print(f"Rebuilding ObjectPack took {(end_objectpack_patching_time - start_objectpack_rebuilding_time)} seconds")
    print(f"Total ObjectPack creation took {(end_objectpack_patching_time - start_objectpack_creation_time)} seconds")

    return [arc_name[6:-4] for arc_name in objectpack_arc.get_all_paths()]
