import os
import shutil
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from constants.itemnames import *
from logic.generate import generate
from logic.config import *
from logic.search import all_logic_satisfied
from logic.world import World
from filepathconstants import (
    BASE_PRESETS_PATH,
    CROSS_PLATFORM_TESTS_PATH,
    SPOILER_LOGS_PATH,
)

from test_logic import config_test


def cross_platform_config_test(config_file_name: str, is_preset: bool = False) -> None:
    if is_preset:
        config_file_path = BASE_PRESETS_PATH / config_file_name
    else:
        config_file_path = CROSS_PLATFORM_TESTS_PATH / config_file_name

    shutil.copyfile(config_file_path, config_file_name)
    worlds = config_test(config_file_name, remove_spoiler=False, is_test_config=False)
    assert all_logic_satisfied(worlds)

    # Remove the anti spoiler log but keep the regular one for further testing.
    anti_spoiler_path = (
        f"{SPOILER_LOGS_PATH}/{worlds[0].config.get_hash()} Anti Spoiler Log.txt"
    )
    os.remove(anti_spoiler_path)


def test_default_settings() -> None:
    cross_platform_config_test("default_settings.yaml")


def test_default_beatable_only() -> None:
    cross_platform_config_test("default_beatable_only.yaml")


def test_beginner_preset() -> None:
    cross_platform_config_test("Beginner.yaml", is_preset=True)


def test_chestless_preset() -> None:
    cross_platform_config_test("Chestless.yaml", is_preset=True)


def test_max_settings_preset() -> None:
    cross_platform_config_test("Max Settings.yaml", is_preset=True)


def test_max_settings_tricks() -> None:
    cross_platform_config_test("max_settings_tricks.yaml")


def test_max_settings_mixed_er() -> None:
    cross_platform_config_test("max_settings_mixed_er.yaml")


def test_max_settings_mixed_er_beatable_only() -> None:
    cross_platform_config_test("max_settings_mixed_er_beatable_only.yaml")


def test_random() -> None:
    cross_platform_config_test("random.yaml")


def test_random_beatable_only() -> None:
    cross_platform_config_test("random_beatable_only.yaml")
