from pathlib import Path
import os

TITLE_ID = "01002DA013484000"

RANDO_ROOT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))

OUTPUT_PATH = RANDO_ROOT_PATH / "output"
OUTPUT_STAGE_PATH = OUTPUT_PATH / "romfs" / "Stage"
OUTPUT_EVENT_PATH = OUTPUT_PATH / "romfs" / "US" / "Object" / "en_US"
OUTPUT_MAIN_NSO = OUTPUT_PATH / "exefs" / "main"

OARC_CACHE_PATH = RANDO_ROOT_PATH / "oarccache"

STAGE_PATCHES_PATH = RANDO_ROOT_PATH / "patches" / "data" / "stagepatches.yaml"
EVENT_PATCHES_PATH = RANDO_ROOT_PATH / "patches" / "data" / "eventpatches.yaml"
EXTRACTS_PATH = RANDO_ROOT_PATH / "patches" / "data" / "extracts.yaml"
ITEMS_PATH = RANDO_ROOT_PATH / "patches" / "data" / "items.yaml"
CHECKS_PATH = RANDO_ROOT_PATH / "patches" / "data" / "checks.yaml"

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

TITLE2D_SOURCE_PATH = (
    RANDO_ROOT_PATH / "title" / TITLE_ID / "romfs" / "Layout" / "Title2D.arc"
)
TITLE2D_OUTPUT_PATH = OUTPUT_PATH / "romfs" / "Layout" / "Title2D.arc"

ASM_PATCHES_PATH = RANDO_ROOT_PATH / "patches"
ASM_PATCHES_DIFFS_PATH = RANDO_ROOT_PATH / "asm" / "patches" / "diffs"

MAIN_NSO_FILE_PATH = RANDO_ROOT_PATH / "title" / TITLE_ID / "exefs" / "main"
