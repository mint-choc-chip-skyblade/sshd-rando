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

import time
import random
import os


def generate(config_file: str) -> list[World]:
    get_all_settings_info()
    load_text_data()

    # If the config file doesn't exist, create default
    if not os.path.isfile(config_file):
        create_default_config(config_file)
    config = load_config_from_file(config_file)

    # If config has no seed, generate one
    if config.seed == "" or config.seed == "-1":
        config.seed = str(random.randint(0, 0xFFFFFFFF))
        write_config_to_file(config_file, config)

    print(f"Seed: {config.seed}")

    return generate_randomizer(config)


def generate_randomizer(config: Config) -> list[World]:
    start = time.process_time()

    # Seed RNG with combination of seed, standard settings, and plando file (if being used)
    hash_str = config.seed
    for setting_map in config.settings:
        for name, setting in setting_map.settings.items():
            if setting.info.type == SettingType.STANDARD:
                hash_str += name + setting.value

    if config.plandomizer:
        with open(config.plandomizer_file) as plando_file:
            hash_str += plando_file.read()

    if config.generate_spoiler_log:
        hash_str += "spoilerlog"

    random.seed(hash_str)

    worlds: list[World] = []

    # Build all necessary worlds
    for i in range(len(config.settings)):
        setting_map = config.settings[i]
        worlds.append(World(i))
        print(f"Building {worlds[i]}")

        # TODO: Resolve Random Settings
        # TODO: Resolve Cosmetic Choices
        # TODO: Resolve Setting Conflicts

        worlds[i].setting_map = setting_map
        worlds[i].num_worlds = len(config.settings)
        worlds[i].config = config
        worlds[i].build()

    for world in worlds:
        world.worlds = worlds

    # Process plando data for all worlds
    if config.plandomizer:
        load_plandomizer_data(worlds, config.plandomizer_file)

    # All worlds must perform pre-entrance shuffle tasks
    # before any entrance shuffling takes place
    for world in worlds:
        world.perform_pre_entrance_shuffle_tasks()

    for world in worlds:
        print(f"Shuffling entrances for {world}...")
        shuffle_world_entrances(world, worlds)

    for world in worlds:
        world.perform_post_entrance_shuffle_tasks()

    start = time.process_time()
    print("Filling Worlds...")
    fill_worlds(worlds)
    end = time.process_time()
    print(f"Fill took {(end - start)} seconds")

    generate_playthrough(worlds)
    generate_hints(worlds)
    generate_spoiler_log(worlds)
    return worlds
