
from world import World
from config import *
from settings import *
from fill import fill_worlds
from search import generate_playthrough
from spoiler_log import generate_spoiler_log

import time
import random
import os
import sys, getopt
import logging



def generate():

    # Set specified log level
    opts, args = getopt.getopt(sys.argv[1:],"ll:", ["loglevel="])
    for opt, arg in opts:
      if opt in ("-ll", "--loglevel"):
         if arg == "debug":
             print("Starting Debug Log")
             logging.basicConfig(filename='debug.log', encoding='utf-8', level=logging.DEBUG)

    start = time.process_time()

    get_all_settings_info()

    # If the config file doesn't exist, create default
    if not os.path.isfile("config.yaml"):
        create_default_config("config.yaml")

    config = load_config_from_file("config.yaml")

    generate_randomizer(config)

    end = time.process_time()
    print(f"Total Generation Time: {end - start} seconds")


def generate_randomizer(config: Config):

    if config.seed == "":
        config.seed = str(random())
        # Write config back to file

    # Seed RNG with combination of seed, standard settings, and plando file (if being used)
    hash_str = config.seed
    for setting_map in config.settings:
        for name, setting in setting_map.settings.items():
            if setting.info.type == SettingType.STANDARD:
                hash_str += name + setting.value

    # TODO: Check plando file

    if config.generate_spoiler_log:
        hash_str += "spoilerlog"
    
    random.seed(hash_str)

    worlds: list[World] = []

    # Build all necessary worlds
    for i in range(len(config.settings)):
        setting_map = config.settings[i]
        print(f"Building World {i}")
        worlds.append(World(i))
        
        # TODO: Resolve Random Settings
        # TODO: Resolve Cosmetic Choices
        # TODO: Resolve Setting Conflicts

        worlds[i].setting_map = setting_map
        worlds[i].build()
        # TODO: Set Excluded Locations
        # TODO: Set Item Locations


    # TODO: Process plando data for all worlds
    # TODO: Perform Pre-Entrance Shuffle Tasks
    # TODO: Shuffle Entrances

    start = time.process_time()
    print("Filling Worlds...")
    fill_worlds(worlds)
    end = time.process_time()
    print(f"Fill took {(end - start)} seconds")

    generate_playthrough(worlds)
    # TODO: Perform Post-Fill Tasks
    generate_spoiler_log(worlds)


generate()