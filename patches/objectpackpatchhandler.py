from filepathconstants import OBJECTPACK_PATH, MODIFIED_OBJECTPACK_PATH, OBJECTPACK_PATCHES_PATH, OARC_CACHE_PATH
from sslib.utils import write_bytes_create_dirs
from sslib.yaml import yaml_load
from sslib.u8file import U8File

def patch_object_pack():
    patches = yaml_load(OBJECTPACK_PATCHES_PATH)
    objectpackArc = None

    if "AddArc" in patches:
        objectpackArc = U8File.get_parsed_U8_from_path(OBJECTPACK_PATH, True)

        for arc in patches["AddArc"]:
            arcName = f"{arc}.arc"
            oarcPath = OARC_CACHE_PATH / arcName
            if oarcPath.exists():
                objectpackArc.add_file_data(
                    f"oarc/{arcName}", oarcPath.read_bytes()
                )
            else:
                print(f"ERROR: {arcName} not found in oarc cache")

    if objectpackArc is not None:
        write_bytes_create_dirs(MODIFIED_OBJECTPACK_PATH, objectpackArc.build_and_compress_U8())

