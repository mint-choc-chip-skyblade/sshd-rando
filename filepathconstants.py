from pathlib import Path
import os

TITLE_ID = "01002DA013484000"

RANDO_ROOT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
SSHD_EXTRACT_PATH = RANDO_ROOT_PATH / "sshd_extract"
EXEFS_EXTRACT_PATH = SSHD_EXTRACT_PATH / "exefs"
ROMFS_EXTRACT_PATH = SSHD_EXTRACT_PATH / "romfs"

# Outputs
DEFAULT_OUTPUT_PATH = RANDO_ROOT_PATH / "sshdr_output"
LOGS_PATH = RANDO_ROOT_PATH / "logs"

# Config
CONFIG_PATH = RANDO_ROOT_PATH / "config.yaml"
PREFERENCES_PATH = RANDO_ROOT_PATH / "preferences.yaml"
PLANDO_PATH = RANDO_ROOT_PATH / "plandomizers"
PRESETS_PATH = RANDO_ROOT_PATH / "presets"
BASE_PRESETS_PATH = RANDO_ROOT_PATH / "data" / "presets"

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

RANDO_FONT_PATH = RANDO_ROOT_PATH / "assets" / "Figtree-Regular.ttf"
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

STAGE_FILES_PATH = ROMFS_EXTRACT_PATH / "Stage"
EVENT_FILES_PATH = ROMFS_EXTRACT_PATH / "US" / "Object" / "en_US"

OBJECTPACK_PATH_TAIL = Path("romfs") / "Object" / "NX" / "ObjectPack.arc.LZ"
OBJECTPACK_PATH = SSHD_EXTRACT_PATH / OBJECTPACK_PATH_TAIL

# Logo, Icon, and Words
ICON_PATH = RANDO_ROOT_PATH / "assets" / "icon.png"
FI_ICON_PATH = RANDO_ROOT_PATH / "assets" / "fi.png"
ERROR_ICON_PATH = RANDO_ROOT_PATH / "assets" / "error.png"

TITLE2D_SOURCE_PATH = ROMFS_EXTRACT_PATH / "Layout" / "Title2D.arc"
ENDROLL_SOURCE_PATH = ROMFS_EXTRACT_PATH / "Layout" / "EndRoll.arc"

WORDS_PATH = RANDO_ROOT_PATH / "data" / "skyward_sword_words.yaml"

# ASM
ASM_PATCHES_DIFFS_PATH = RANDO_ROOT_PATH / "asm" / "patches" / "diffs"
ASM_ADDITIONS_DIFFS_PATH = RANDO_ROOT_PATH / "asm" / "additions" / "diffs"
ASM_SDK_DIFFS_PATH = RANDO_ROOT_PATH / "asm" / "sdk" / "diffs"

MAIN_NSO_FILE_PATH = EXEFS_EXTRACT_PATH / "main"
SUBSDK1_FILE_PATH = EXEFS_EXTRACT_PATH / "subsdk1"
SDK_FILE_PATH = EXEFS_EXTRACT_PATH / "sdk"

STARTFLAGS_FILE_PATH = RANDO_ROOT_PATH / "data" / "patches" / "startflags.yaml"
