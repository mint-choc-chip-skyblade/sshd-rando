import argparse
import logging

from filepathconstants import CONFIG_PATH
from logic.config import create_default_config

parser = argparse.ArgumentParser(
    description="A randomizer for The Legend of Zelda: Skyward Sword HD."
)

parser.add_argument(
    "--with-gui",
    dest="with_gui",
    action="store_true",
    help="Runs the randomizer through a gui.",
)

parser.add_argument(
    "--debug",
    action="store_true",
    help="Generates a debug log when running the rando.",
)

# parser.print_help()
args = parser.parse_args()

# Set specified log level
if args.debug:
    print("Starting Debug Log")
    logging.basicConfig(
        filename="debug.log",
        encoding="utf-8",
        level=logging.DEBUG,
        filemode="w",
    )

# If the config file doesn't exist, create default
if not CONFIG_PATH.is_file():
    create_default_config(CONFIG_PATH)

# Imports here to prevent circular dependency
if args.with_gui:
    from gui.main import start_gui

    start_gui()
else:
    from randomize import randomize

    randomize()
