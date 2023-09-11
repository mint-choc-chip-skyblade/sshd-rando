from pathlib import Path
import os

TITLE_ID = "01002DA013484000"

RANDO_ROOT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))

OUTPUT_PATH = RANDO_ROOT_PATH / "output"
OUTPUT_STAGE_PATH = OUTPUT_PATH / "romfs" / "Stage"
OUTPUT_EVENT_PATH = OUTPUT_PATH / "romfs" / "US" / "Object" / "en_US"
OUTPUT_MAIN_NSO = OUTPUT_PATH / "exefs" / "main"
OUTPUT_ADDITIONAL_SUBSDK = OUTPUT_PATH / "exefs" / "subsdk8"

OARC_CACHE_PATH = RANDO_ROOT_PATH / "oarccache"

STAGE_PATCHES_PATH = RANDO_ROOT_PATH / "patches" / "data" / "stagepatches.yaml"
EVENT_PATCHES_PATH = RANDO_ROOT_PATH / "patches" / "data" / "eventpatches.yaml"
OBJECTPACK_PATCHES_PATH = (
    RANDO_ROOT_PATH / "patches" / "data" / "objectpackpatches.yaml"
)
EXTRACTS_PATH = RANDO_ROOT_PATH / "patches" / "data" / "extracts.yaml"
ITEMS_PATH = RANDO_ROOT_PATH / "data" / "items.yaml"
LOCATIONS_PATH = RANDO_ROOT_PATH / "data" / "locations.yaml"

STAGE_FILES_PATH = RANDO_ROOT_PATH / "title" / TITLE_ID / "romfs" / "Stage"
EVENT_FILES_PATH = (
    RANDO_ROOT_PATH / "title" / TITLE_ID / "romfs" / "US" / "Object" / "en_US"
)

OBJECTPACK_PATH = (
    RANDO_ROOT_PATH
    / "title"
    / TITLE_ID
    / "romfs"
    / "Object"
    / "NX"
    / "ObjectPack.arc.LZ"
)

MODIFIED_OBJECTPACK_PATH = OUTPUT_PATH / "romfs" / "Object" / "NX" / "ObjectPack.arc.LZ"

TITLE2D_SOURCE_PATH = (
    RANDO_ROOT_PATH / "title" / TITLE_ID / "romfs" / "Layout" / "Title2D.arc"
)

TITLE2D_OUTPUT_PATH = OUTPUT_PATH / "romfs" / "Layout" / "Title2D.arc"

# asm
ASM_PATCHES_DIFFS_PATH = RANDO_ROOT_PATH / "asm" / "patches" / "diffs"
ASM_ADDITIONS_DIFFS_PATH = RANDO_ROOT_PATH / "asm" / "additions" / "diffs"

MAIN_NSO_FILE_PATH = RANDO_ROOT_PATH / "title" / TITLE_ID / "exefs" / "main"
SUBSDK1_FILE_PATH = RANDO_ROOT_PATH / "title" / TITLE_ID / "exefs" / "subsdk1"
