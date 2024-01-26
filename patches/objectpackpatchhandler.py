from pathlib import Path
from filepathconstants import (
    OBJECTPACK_PATH,
    OBJECTPACK_PATCHES_PATH,
    OARC_CACHE_PATH,
)
from sslib.utils import write_bytes_create_dirs
from sslib.yaml import yaml_load
from sslib.u8file import U8File


def patch_object_pack(object_pack_output_path: Path):
    patches = yaml_load(OBJECTPACK_PATCHES_PATH)
    objectpack_arc = None

    if "AddArc" in patches:
        objectpack_arc = U8File.get_parsed_U8_from_path(OBJECTPACK_PATH, True)

        for arc in patches["AddArc"]:
            arc_name = f"{arc}.arc"
            oarc_path = OARC_CACHE_PATH / arc_name
            if oarc_path.exists():
                objectpack_arc.add_file_data(f"oarc/{arc_name}", oarc_path.read_bytes())
            else:
                print(f"ERROR: {arc_name} not found in oarc cache")

    if objectpack_arc is not None:
        write_bytes_create_dirs(
            object_pack_output_path, objectpack_arc.build_and_compress_U8()
        )
