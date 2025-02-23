from pathlib import Path
from filepathconstants import (
    OBJECTPACK_PATH,
    OARC_CACHE_PATH,
)
from sslib.utils import write_bytes_create_dirs
from sslib.u8file import U8File
from .stagepatchhandler import get_oarc_cache_path


def patch_object_pack(object_pack_output_path: Path, other_mods: list[str] = []):
    objectpack_arc = U8File.get_parsed_U8_from_path(OBJECTPACK_PATH)

    for path in objectpack_arc.get_all_paths():
        arc_name = path.split("/")[-1]
        oarc_path = get_oarc_cache_path(arc_name, other_mods)

        if oarc_path.exists():
            objectpack_arc.add_file_data(f"oarc/{arc_name}", oarc_path.read_bytes())
        else:
            raise Exception(f"ERROR: {arc_name} not found in oarc cache.")

    write_bytes_create_dirs(
        object_pack_output_path, objectpack_arc.build_and_compress_U8()
    )
