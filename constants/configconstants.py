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
        "Knight Academy - Deliver Kikwi to Owlan",
        "Upper Skyloft - 600 Points in Pumpkin Pull",
        "Central Skyloft - Peatrice's Love",
        "Batreaux - 70 Crystals",
        "Batreaux - 70 Crystals Second Reward",
        "Batreaux - 80 Crystals",
        "Lumpy Pumpkin - Harp Duet with Kina",
        "Lumpy Pumpkin - Deliver Mogma to Kina",
        "Fun Fun Island - 500 Rupees in Dodoh's High Dive",
        "The Sky - Form a Squirrel Ring above Volcanic Island",
        "The Sky - Form a Squirrel Ring above Lumpy Pumpkin",
        "The Sky - Form a Squirrel Ring above Bamboo Island",
        "Inside the Thunderhead - Song from Levias",
        "Bug Heaven - 10 Bugs in 3 Minutes",
        "Shipyard - Heart Stopping Rickety Coaster Track in 1'05",
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
    "Batreaux - 5 Crystals": "Batreaux's House - 5 Gratitude Crystals Reward",
    "Batreaux - 10 Crystals": "Batreaux's House - 10 Gratitude Crystals Reward",
    "Batreaux - 30 Crystals": "Batreaux's House - 30 Gratitude Crystals Reward",
    "Batreaux - 30 Crystals Chest": "Batreaux's House - 30 Gratitude Crystals Reward Chest",
    "Batreaux - 40 Crystals": "Batreaux's House - 40 Gratitude Crystals Reward",
    "Batreaux - 50 Crystals": "Batreaux's House - 50 Gratitude Crystals Reward",
    "Batreaux - 70 Crystals": "Batreaux's House - 70 Gratitude Crystals First Reward",
    "Batreaux - 70 Crystals Second Reward": "Batreaux's House - 70 Gratitude Crystals Second Reward",
    "Batreaux - 80 Crystals": "Batreaux's House - 80 Gratitude Crystals Reward",
    "The Thunderhead - Song from Levias": "Inside the Thunderhead - Song from Levias",
    "Bug Heaven - Nearby Gossip Stone": "Inside the Thunderhead - Gossip Stone near Bug Heaven",
    "Thunderhead East Island - Chest": "Inside the Thunderhead - East Island Chest",
    "Thunderhead East Island - Goddess Chest": "Inside the Thunderhead - East Island Goddess Chest",
    "Mogma Mitts Island - First Goddess Chest": "Inside the Thunderhead - Mogma Mitts Island First Goddess Chest",
    "Mogma Mitts Island - Second Goddess Chest": "Inside the Thunderhead - Mogma Mitts Island Second Goddess Chest",
    "Upper Skyloft - Pumpkin Archery -- 600 Points": "Upper Skyloft - 600 Points in Pumpkin Pull",
    "Lumpy Pumpkin - Harp Minigame": "Lumpy Pumpkin - Harp Duet with Kina",
    "Fun Fun Island - Minigame -- 500 Rupees": "Fun Fun Island - 500 Rupees in Dodoh's High Dive",
    "Bug Heaven - Minigame -- 10 Bugs in 3 Minutes": "Bug Heaven - 10 Bugs in 3 Minutes",
    "Shipyard - Rickety Coaster -- Heart Stopping Track in 1'05": "Shipyard - Heart Stopping Rickety Coaster Track in 1'05",
    "Knight Academy - Owlan's Crystals": "Knight Academy - Deliver Kikwi to Owlan",
    "Knight Academy - Fledge's Crystals": "Knight Academy - Help Fledge Workout",
    "Knight Academy - Ghost/Pipit's Crystals": "Knight Academy - Deliver Cawlin's Letter",
    "Central Skyloft - Wryna's Crystals": "Central Skyloft - Wryna's Gratitude",
    "Central Skyloft - Parrow's Crystals": "Central Skyloft - Parrow's Gratitude",
    "Central Skyloft - Peater/Peatrice's Crystals": "Central Skyloft - Peatrice's Love",
    "Skyloft Village - Mallara's Crystals": "Skyloft Village - Clean Mallara's House",
    "Skyloft Village - Bertie's Crystals": "Skyloft Village - Deliver Rattle to Bertie",
    "Skyloft Village - Sparrot's Crystals": "Skyloft Village - Deliver Crystal Ball to Sparrot",
    "Lumpy Pumpkin - Kina's Crystals": "Lumpy Pumpkin - Deliver Mogma to Kina",
    "Orielle's Island - Orielle's Crystals": "Orielle's Island - Heal Orielle's Loftwing",
    "Beedle's Island - Beedle's Crystals": "Beedle's Island - Deliver Beedle's Insect Cage",
    "Fun Fun Island - Dodoh's Crystals": "Fun Fun Island - Deliver Party Wheel to Dodoh",
    "Beedle's Shop - 300 Rupee Item": "Beedle's Airshop - 300 Rupee Item",
    "Beedle's Shop - 600 Rupee Item": "Beedle's Airshop - 600 Rupee Item",
    "Beedle's Shop - 1200 Rupee Item": "Beedle's Airshop - 1200 Rupee Item",
    "Beedle's Shop - 800 Rupee Item": "Beedle's Airshop - 800 Rupee Item",
    "Beedle's Shop - 1600 Rupee Item": "Beedle's Airshop - 1600 Rupee Item",
    "Beedle's Shop - First 100 Rupee Item": "Beedle's Airshop - First 100 Rupee Item",
    "Beedle's Shop - Second 100 Rupee Item": "Beedle's Airshop - Second 100 Rupee Item",
    "Beedle's Shop - Third 100 Rupee Item": "Beedle's Airshop - Third 100 Rupee Item",
    "Beedle's Shop - 50 Rupee Item": "Beedle's Airshop - 50 Rupee Item",
    "Beedle's Shop - 1000 Rupee Item": "Beedle's Airshop - 1000 Rupee Item",
}

SETTING_ALIASES = {
    "fs_lava_flow": "shortcut_fs_lava_flow",
}
