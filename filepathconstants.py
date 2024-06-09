import appdirs
import os
import platform

from pathlib import Path

TITLE_ID = "01002DA013484000"

userdata_path = "."

try:
    from sys import _MEIPASS  # @IgnoreException

    RANDO_ROOT_PATH = Path(_MEIPASS)

except ImportError:
    RANDO_ROOT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))

if platform.system() == "Darwin":
    userdata_path = appdirs.user_data_dir("Skyward Sword HD Randomizer", "SSHD Rando")

    if not os.path.isdir(userdata_path):
        os.mkdir(userdata_path)

    print(
        f"You are running from source on macOS. Currently, macOS builds cannot reliably access data from the local directory, so, to keep things consistent, your data, such as all default paths and config, can be found at {userdata_path}"
    )

SSHD_EXTRACT_PATH = Path(userdata_path) / "sshd_extract"
EXEFS_EXTRACT_PATH = SSHD_EXTRACT_PATH / "exefs"
ROMFS_EXTRACT_PATH = SSHD_EXTRACT_PATH / "romfs"

# Outputs
DEFAULT_OUTPUT_PATH = Path(userdata_path) / "sshdr_output"
SPOILER_LOGS_PATH = Path(userdata_path) / "logs"

# Config
CONFIG_PATH = Path(userdata_path) / "config.yaml"
PREFERENCES_PATH = Path(userdata_path) / "preferences.yaml"
SETTINGS_LIST_PATH = RANDO_ROOT_PATH / "data" / "settings_list.yaml"
PLANDO_PATH = Path(userdata_path) / "plandomizers"
PRESETS_PATH = Path(userdata_path) / "presets"
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
CUSTOM_THEME_PATH = Path(userdata_path) / "custom_theme.json"

RANDO_FONT_PATH = RANDO_ROOT_PATH / "assets" / "Figtree-Regular.ttf"
DYSLEXIC_FONT_PATH = RANDO_ROOT_PATH / "assets" / "OpenDyslexic3-Regular.ttf"

TRACKER_AREAS_PATH = RANDO_ROOT_PATH / "data" / "tracker_areas.yaml"
TRACKER_AUTOSAVE_PATH = Path(userdata_path) / "tracker_autosave_RANDOMIZER_VERSION.yaml"

# Stage and event stuff
OARC_CACHE_PATH = Path(userdata_path) / "oarccache"

STAGE_PATCHES_PATH = RANDO_ROOT_PATH / "data" / "patches" / "stagepatches.yaml"
EVENT_PATCHES_PATH = RANDO_ROOT_PATH / "data" / "patches" / "eventpatches.yaml"
OBJECTPACK_PATCHES_PATH = (
    RANDO_ROOT_PATH / "data" / "patches" / "objectpackpatches.yaml"
)
EXTRACTS_PATH = RANDO_ROOT_PATH / "data" / "patches" / "extracts.yaml"
ITEMS_PATH = RANDO_ROOT_PATH / "data" / "items.yaml"
LOCATIONS_PATH = RANDO_ROOT_PATH / "data" / "locations.yaml"

STAGE_FILES_PATH = ROMFS_EXTRACT_PATH / "Stage"

EVENT_FILE_PATH_TAILS = [
    Path("romfs") / "CN" / "Object" / "zh_CN",
    Path("romfs") / "EU" / "Object" / "de_DE",
    Path("romfs") / "EU" / "Object" / "en_GB",
    Path("romfs") / "EU" / "Object" / "es_ES",
    Path("romfs") / "EU" / "Object" / "fr_FR",
    Path("romfs") / "EU" / "Object" / "it_IT",
    Path("romfs") / "EU" / "Object" / "nl_NL",
    Path("romfs") / "JP" / "Object" / "ja_JP",
    Path("romfs") / "KR" / "Object" / "ko_KR",
    Path("romfs") / "RU" / "Object" / "ru_RU",
    Path("romfs") / "TW" / "Object" / "zh_TW",
    Path("romfs") / "US" / "Object" / "en_US",
    Path("romfs") / "US" / "Object" / "es_US",
    Path("romfs") / "US" / "Object" / "fr_US",
]
VANILLA_EVENT_FILE_PATHS = {
    tail.name: SSHD_EXTRACT_PATH / tail for tail in EVENT_FILE_PATH_TAILS
}

OBJECTPACK_PATH_TAIL = Path("romfs") / "Object" / "NX" / "ObjectPack.arc.LZ"
OBJECTPACK_PATH = SSHD_EXTRACT_PATH / OBJECTPACK_PATH_TAIL

TEXT_DATA_PATH = RANDO_ROOT_PATH / "data" / "text_data"
ENTRANCE_SHUFFLE_DATA_PATH = RANDO_ROOT_PATH / "data" / "entrance_shuffle_data.yaml"
BIRD_STATUE_DATA_PATH = RANDO_ROOT_PATH / "data" / "bird_statue_data.yaml"
WORLD_DATA_PATH = RANDO_ROOT_PATH / "data" / "world"
MACROS_DATA_PATH = RANDO_ROOT_PATH / "data" / "macros.yaml"

# Logo, Icon, and Words
ICON_PATH = RANDO_ROOT_PATH / "assets" / "icon.png"
FI_ICON_PATH = RANDO_ROOT_PATH / "assets" / "fi.png"
ERROR_ICON_PATH = RANDO_ROOT_PATH / "assets" / "error.png"
TRACKER_ASSETS_PATH = RANDO_ROOT_PATH / "assets" / "tracker"

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
