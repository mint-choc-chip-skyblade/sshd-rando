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
    "verified_extract",
    "tutorial_random_settings",
    "first_time_seed_gen_text",
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
    "verified_extract": False,
    "tutorial_random_settings": False,
    "first_time_seed_gen_text": False,
    "starting_inventory": Counter(
        [
            HYLIAN_SHIELD,
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
        "Batreaux's House - 70 Gratitude Crystals First Reward",
        "Batreaux's House - 70 Gratitude Crystals Second Reward",
        "Batreaux's House - 80 Gratitude Crystals Reward",
        "Lumpy Pumpkin - Harp Duet with Kina",
        "Lumpy Pumpkin - Deliver Mogma to Kina",
        "Fun Fun Island - 500 Rupees in Dodoh's High Dive",
        "The Sky - Form a Swirrell Ring above Volcanic Island",
        "The Sky - Form a Swirrell Ring above Lumpy Pumpkin",
        "The Sky - Form a Swirrell Ring above Bamboo Island",
        "Inside the Thunderhead - Song from Levias",
        "Bug Heaven - 10 Bugs in 3 Minutes",
        "Flooded Faron Woods - Water Dragon's Reward",
        "Shipyard - Heart Stopping Rickety Coaster Track in 1'05",
        "The Goddess's Silent Realm - Collect all Tears Reward",
        "Farore's Silent Realm - Collect all Tears Reward",
        "Nayru's Silent Realm - Collect all Tears Reward",
        "Din's Silent Realm - Collect all Tears Reward",
    ],
    "excluded_hint_locations": [
        "Shipyard - Gossip Stone after First Minecart Track",
    ],
    "mixed_entrance_pools": [],
    "other_mods": [],
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
    # Since v1.0
    "Faron Woods - Stamina Fruit after Kiwki in Clearing": "Faron Woods - Stamina Fruit after Kikwi in Clearing",
    "Flooded Faron Woods - Rupee behind West Breakable Rocks 1": "Inside the Flooded Great Tree - Rupee behind Breakable Rocks near Dragon's Tail 1",
    "Flooded Faron Woods - Rupee behind West Breakable Rocks 2": "Inside the Flooded Great Tree - Rupee behind Breakable Rocks near Dragon's Tail 2",
    "Lanayru Mine - Goddess Cube": "Lanayru Mine - Goddess Cube behind First Landing Robot",
    "Lanayru Mine - Chest behind First Landing": "Lanayru Mine - Chest behind First Landing Robot",
    "Temple of Time - Goddess Cube": "Temple of Time - Goddess Cube on High Platform North of Tree",
    "Lanayru Gorge - Life Tree Digging Spot": "Lanayru Gorge - Life Tree Digging Spot near Sandfalls",
    "Lanayru Gorge - Goddess Cube": "Lanayru Gorge - Goddess Cube near Sandfalls",
    "Ancient Harbour - Goddess Cube": "Ancient Harbour - Goddess Cube in North Cave",
    "Skipper's Retreat - Goddess Cube": "Skipper's Retreat - Goddess Cube on Southwest Pillar",
    "Skipper's Retreat - Chest on Cacti Pillar": "Skipper's Retreat - Chest on North Cacti Pillar",
    "Pirate Stronghold - Goddess Cube": "Pirate Stronghold - Goddess Cube on top of Shark Head",
    "Skyview Spring - Goddess Cube": "Skyview Spring - Goddess Cube behind Crest",
    "Temple of Time - Bonk Northeast Pillar": "Temple of Time - Bonk Northeast Bird Pillar near Gate of Time",
    "Temple of Time - Bonk Southeast Pillar": "Temple of Time - Bonk Southeast Bird Pillar near Gate of Time",
    "Sealed Grounds - Blow Bushes in Corner Left of Gossip Stone": "Sealed Grounds - Blow High Bushes in Corner Left of Gossip Stone",
    "Lanayru Mine - Blow Digging Robot before Side Room near First Timeshift Stone": "Lanayru Mine - Blow Digging Robot's Wall before Side Room near First Timeshift Stone",
    "Lanayru Mine - Blow Left Digging Robot in Side Room near First Timeshift Stone": "Lanayru Mine - Blow Left Digging Robot's Wall in Side Room near First Timeshift Stone",
    "Lanayru Mine - Blow Right Digging Robot in Side Room near First Timeshift Stone": "Lanayru Mine - Blow Right Digging Robot's Wall in Side Room near First Timeshift Stone",
    "Lanayru Mine - Blow Left Digging Robot after First Minecart Ride": "Lanayru Mine - Blow Left Digging Robot's Wall after First Minecart Ride",
    "Lanayru Mine - Blow Right Digging Robot after First Minecart Ride": "Lanayru Mine - Blow Right Digging Robot's Wall after First Minecart Ride",
    "Lanayru Mine - Blow Digging Robot near Mine Exit": "Lanayru Mine - Blow Digging Robot's Wall near Mine Exit",
    "Lanayru Mine - Blow Digging Robot near Last Mine Timeshift Stone": "Lanayru Mine - Blow Digging Robot's Wall near Last Mine Timeshift Stone",
    # Since v1.1
    "Sealed Grounds - Slingshot Mouth in Wall Drawing of Beast": "Sealed Grounds - Slingshot Open Mouth in Wall Drawing of Beast",
    "Sealed Grounds - Bonk Wall Drawing of Hylia Raising Skyloft": "Sealed Grounds - Bonk Wall Drawing of Hylia Raising Sword and Harp",
    "Sealed Grounds - Slingshot Sun in Wall Drawing of Worshippers": "Sealed Grounds - Slingshot Light of Ultimate Power in Wall Drawing of Worshippers",
}

TRACKER_NOTE_EVENTS = {
    "Access_Item_Check": "Access Item Check",
    "Purchase_Shield": "Purchase Shield",
}

SETTING_ALIASES = {
    "shortcut_fs_lava_flow": "fs_lava_flow",
}
