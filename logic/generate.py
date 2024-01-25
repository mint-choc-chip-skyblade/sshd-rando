from filepathconstants import PLANDO_PATH
from .world import World
from .config import *
from .settings import *
from .fill import fill_worlds
from .search import generate_playthrough
from .spoiler_log import generate_spoiler_log
from .plandomizer import load_plandomizer_data
from .entrance_shuffle import shuffle_world_entrances
from .hints import generate_hints
from util.text import load_text_data

from gui.dialogs.dialog_header import print_progress_text, update_progress_value
import time
import random


def generate(config_file: Path) -> list[World]:
    get_all_settings_info()
    load_text_data()

    config = load_config_from_file(config_file, create_if_blank=True)

    # If config has no seed, generate one
    if config.seed == "" or config.seed == "-1":
        config.seed = str(random.randint(0, 0xFFFFFFFF))
        # write_config_to_file(config_file, config)

    print_progress_text(f"Seed: {config.seed}")

    return generate_randomizer(config)


def generate_randomizer(config: Config) -> list[World]:
    start = time.process_time()

    # Seed RNG with combination of seed, standard settings, and plando file (if being used)
    hash_str = config.seed
    for setting_map in config.settings:
        for name, setting in setting_map.settings.items():
            if setting.info.type == SettingType.STANDARD:
                hash_str += name + setting.value
            else:
                # If any non-standard settings are random, resolve them now before seeding
                setting.resolve_if_random()

    if config.use_plandomizer:
        if config.plandomizer_file is None:
            raise ConfigError(
                f"Cannot use plandomizer file as the current plandomizer filename is invalid: {config.plandomizer_file}"
            )

        with open(PLANDO_PATH / config.plandomizer_file) as plando_file:
            hash_str += plando_file.read()

    if config.generate_spoiler_log:
        hash_str += "spoilerlog"

    random.seed(hash_str)

    worlds: list[World] = []

    update_progress_value(2)

    # Build all necessary worlds
    for i in range(len(config.settings)):
        setting_map = config.settings[i]
        worlds.append(World(i))
        print_progress_text(f"Building {worlds[i]}")
        worlds[i].setting_map = setting_map
        worlds[i].resolve_random_settings()
        worlds[i].resolve_conflicting_settings()
        worlds[i].num_worlds = len(config.settings)
        worlds[i].config = config
        worlds[i].build()

    for world in worlds:
        world.worlds = worlds

    # Process plando data for all worlds
    if config.use_plandomizer:
        if config.plandomizer_file is None:
            raise ConfigError(
                f"Cannot use plandomizer file as the current plandomizer filename is invalid: {config.plandomizer_file}"
            )

        load_plandomizer_data(worlds, PLANDO_PATH / config.plandomizer_file)

    # All worlds must perform pre-entrance shuffle tasks
    # before any entrance shuffling takes place
    for world in worlds:
        world.perform_pre_entrance_shuffle_tasks()

    update_progress_value(4)
    for world in worlds:
        print_progress_text(f"Shuffling entrances for {world}...")
        shuffle_world_entrances(world, worlds)

    for world in worlds:
        world.perform_post_entrance_shuffle_tasks()

    start = time.process_time()

    update_progress_value(6)
    print_progress_text("Filling Worlds...")

    fill_worlds(worlds)
    end = time.process_time()
    print(f"Fill took {(end - start)} seconds")

    update_progress_value(8)
    generate_playthrough(worlds)

    update_progress_value(10)
    generate_hints(worlds)

    update_progress_value(12)
    generate_spoiler_log(worlds)
    return worlds
