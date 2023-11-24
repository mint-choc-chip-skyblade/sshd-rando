from pathlib import Path
import os

TITLE_ID = "01002DA013484000"

RANDO_ROOT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))

# Outputs
OUTPUT_PATH = RANDO_ROOT_PATH / "output"
OUTPUT_STAGE_PATH = OUTPUT_PATH / "romfs" / "Stage"
OUTPUT_EVENT_PATH = OUTPUT_PATH / "romfs" / "US" / "Object" / "en_US"
OUTPUT_MAIN_NSO = OUTPUT_PATH / "exefs" / "main"
OUTPUT_ADDITIONAL_SUBSDK = OUTPUT_PATH / "exefs" / "subsdk8"

# Config
CONFIG_PATH = RANDO_ROOT_PATH / "config.yaml"

# GUI Stuff
THEME_INFO_PATH = RANDO_ROOT_PATH / "gui" / "custom_themes" / "default_theme_info.yaml"

DEFAULT_THEME_PATH = RANDO_ROOT_PATH / "gui" / "custom_themes" / "default_theme.json"
HIGH_CONTRAST_THEME_PATH = (
    RANDO_ROOT_PATH / "gui" / "custom_themes" / "high_contrast_theme.json"
)
READABILITY_THEME_PATH = (
    RANDO_ROOT_PATH / "gui" / "custom_themes" / "readability_theme.json"
)
CUSTOM_THEME_PATH = RANDO_ROOT_PATH / "custom_theme.json"

LATO_FONT_PATH = RANDO_ROOT_PATH / "assets" / "Lato-Regular.ttf"
DYSLEXIC_FONT_PATH = RANDO_ROOT_PATH / "assets" / "OpenDyslexic3-Regular.ttf"

# Stage and event stuff
OARC_CACHE_PATH = RANDO_ROOT_PATH / "oarccache"

STAGE_PATCHES_PATH = RANDO_ROOT_PATH / "data" / "patches" / "stagepatches.yaml"
EVENT_PATCHES_PATH = RANDO_ROOT_PATH / "data" / "patches" / "eventpatches.yaml"
OBJECTPACK_PATCHES_PATH = (
    RANDO_ROOT_PATH / "data" / "patches" / "objectpackpatches.yaml"
)
EXTRACTS_PATH = RANDO_ROOT_PATH / "data" / "patches" / "extracts.yaml"
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

# Logo, Icon, and Words
ICON_PATH = RANDO_ROOT_PATH / "assets" / "icon.png"

TITLE2D_SOURCE_PATH = (
    RANDO_ROOT_PATH / "title" / TITLE_ID / "romfs" / "Layout" / "Title2D.arc"
)

ENDROLL_SOURCE_PATH = (
    RANDO_ROOT_PATH / "title" / TITLE_ID / "romfs" / "Layout" / "EndRoll.arc"
)

TITLE2D_OUTPUT_PATH = OUTPUT_PATH / "romfs" / "Layout" / "Title2D.arc"

ENDROLL_OUTPUT_PATH = OUTPUT_PATH / "romfs" / "Layout" / "EndRoll.arc"

WORDS_PATH = RANDO_ROOT_PATH / "data" / "skyward_sword_words.yaml"

# ASM
ASM_PATCHES_DIFFS_PATH = RANDO_ROOT_PATH / "asm" / "patches" / "diffs"
ASM_ADDITIONS_DIFFS_PATH = RANDO_ROOT_PATH / "asm" / "additions" / "diffs"

MAIN_NSO_FILE_PATH = RANDO_ROOT_PATH / "title" / TITLE_ID / "exefs" / "main"
SUBSDK1_FILE_PATH = RANDO_ROOT_PATH / "title" / TITLE_ID / "exefs" / "subsdk1"

STARTFLAGS_FILE_PATH = RANDO_ROOT_PATH / "data" / "patches" / "startflags.yaml"
