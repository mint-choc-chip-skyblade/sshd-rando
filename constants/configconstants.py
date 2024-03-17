from collections import Counter
import platform
import random

import yaml
from constants.itemnames import *
from filepathconstants import DEFAULT_OUTPUT_PATH, WORDS_PATH


def get_new_seed() -> str:
    with open(WORDS_PATH, "r", encoding="utf-8") as words_file:
        words = yaml.safe_load(words_file)
        new_seed = ""

        for _ in range(0, 4):
            new_seed += random.choice(words)

        return new_seed


CONFIG_FIELDS = (
    "seed",
    "generate_spoiler_log",
    "use_plandomizer",
    "plandomizer_file",
)


PREFERENCE_FIELDS = (
    "output_dir",
    "theme_mode",
    "theme_presets",
    "use_custom_theme",
    "font_family",
    "font_size",
)


SETTINGS_NOT_IN_SETTINGS_LIST = (
    "excluded_locations",
    "excluded_hint_locations",
    "starting_inventory",
    "mixed_entrance_pools",
)


ENTRANCE_TYPES = (
    # "Spawn",
    # "Bird Statue",
    "Dungeon",
    "Door",
    "Interior",
    "Overworld",
    "Trial Gate",
)


DEFAULT_SETTINGS = {
    "output_dir": DEFAULT_OUTPUT_PATH,
    "seed": get_new_seed(),
    "use_plandomizer": False,
    "plandomizer_file": "None",
    "generate_spoiler_log": True,
    "theme_mode": "Auto",
    "theme_presets": "Default",
    "use_custom_theme": False,
    "font_family": "Figtree",
    "font_size": 10,
    "starting_inventory": Counter(
        [
            PROGRESSIVE_POUCH,
            SCRAPPER,
            SV_MAP,
            ET_MAP,
            LMF_MAP,
            AC_MAP,
            SSH_MAP,
            FS_MAP,
            SK_MAP,
        ]
        # + [
        #     "Group of Tadtones",
        # ]
        # * 17
    ),
    "excluded_locations": [
        "Knight Academy - Owlan's Crystals",
        "Upper Skyloft - Pumpkin Archery -- 600 Points",
        "Central Skyloft - Peater/Peatrice's Crystals",
        "Batreaux - 70 Crystals",
        "Batreaux - 70 Crystals Second Reward",
        "Batreaux - 80 Crystals",
        "Lumpy Pumpkin - Harp Minigame",
        "Lumpy Pumpkin - Kina's Crystals",
        "Fun Fun Island - Minigame -- 500 Rupees",
        "The Sky - Form a Squirrel Ring above Volcanic Island",
        "The Sky - Form a Squirrel Ring above Lumpy Pumpkin",
        "The Sky - Form a Squirrel Ring above Bamboo Island",
        "The Thunderhead - Song from Levias",
        "Bug Heaven - Minigame -- 10 Bugs in 3 Minutes",
        "Shipyard - Rickety Coaster -- Heart Stopping Track in 1'05",
        "The Goddess's Silent Realm - Collect all Tears Reward",
        "Farore's Silent Realm - Collect all Tears Reward",
        "Nayru's Silent Realm - Collect all Tears Reward",
        "Din's Silent Realm - Collect all Tears Reward",
    ],
    "excluded_hint_locations": [
        "Shipyard - Gossip Stone",
    ],
    "mixed_entrance_pools": [],
}

if platform.system() != "Windows":
    DEFAULT_SETTINGS["font_size"] = 13


def get_default_setting(setting_name: str):
    # Edge case to allow this function to return None without
    # causing the type checking to complain
    if setting_name == "plandomizer_file":
        return DEFAULT_SETTINGS["plandomizer_file"]

    if (setting_value := DEFAULT_SETTINGS.get(setting_name)) is None:
        raise Exception(
            f"Setting with name '{setting_name}' does not have a defined default value.\nTry adding an entry to /constants/configdefaults.py to fix."
        )

    return setting_value


LOCATION_ALIASES = {
    "Sealed Temple - Slingshot above Doors to Sealed Grounds Whirlpool": "Sealed Temple - Slingshot above Doors to Sealed Grounds Spiral",
    "Skyloft Village - Stamina Fruit": "Skyloft Village - Stamina Fruit above Mallara's House",
    "Deep Woods - Stamina Fruit": "Deep Woods - Stamina Fruit on Hanging Ledge",
    "Great Tree - Blow Small Yellow Mushroom after Vines": "Inside the Great Tree - Blow Small Yellow Mushroom after Vines",
    "Great Tree - Blow Large Yellow Mushroom after Vines": "Inside the Great Tree - Blow Large Yellow Mushroom after Vines",
    "Great Tree - Blow Red Mushroom after Swinging Platforms West": "Inside the Great Tree - Blow Red Mushroom after Swinging Platforms West",
    "Great Tree - Blow Tall Blue Mushroom after Swinging Platforms South": "Inside the Great Tree - Blow Tall Blue Mushroom after Swinging Platforms South",
    "Great Tree - Chest": "Inside the Great Tree - Chest guarded by Deku Baba",
    "Great Tree - Blow Tree Spiral on Highest Pathway": "Inside the Great Tree - Blow Tree Spiral on Highest Pathway",
}

SETTING_ALIASES = {
    "fs_lava_flow": "shortcut_fs_lava_flow",
}
