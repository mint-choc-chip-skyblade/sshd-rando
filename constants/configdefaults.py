from collections import Counter
from pathlib import Path
import random

import yaml
from filepathconstants import WORDS_PATH


def get_new_seed() -> str:
    with open(WORDS_PATH, "r") as words_file:
        words = yaml.safe_load(words_file)
        new_seed = ""

        for _ in range(0, 4):
            new_seed += random.choice(words)

        return new_seed


DEFAULT_SETTINGS = {
    "output_dir": Path("./output"),
    "input_dir": Path("./title"),
    "seed": get_new_seed(),
    "plandomizer": False,
    "plandomizer_file": "None",
    "generate_spoiler_log": True,
    "theme_mode": "Auto",
    "theme_presets": "Default",
    "use_custom_theme": False,
    "font_family": "Lato",
    "font_size": 10,
    "starting_inventory": Counter(
        [
            "Scrapper",
        ]
        + [
            "Group of Tadtones",
        ]
        * 17
    ),
    "excluded_locations": [
        "Skyloft Silent Realm - Collect all Tears Reward",
        "Faron Silent Realm - Collect all Tears Reward",
        "Lanayru Silent Realm - Collect all Tears Reward",
        "Eldin Silent Realm - Collect all Tears Reward",
    ],
    "mixed_entrance_pools": [],
}


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
