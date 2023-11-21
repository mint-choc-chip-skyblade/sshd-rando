import argparse

from logic.generate import generate
from patches.allpatchhandler import AllPatchHandler

parser = argparse.ArgumentParser(
    description="A randomizer for The Legend of Zelda: Skyward Sword HD."
)

parser.add_argument(
    "--with-gui",
    dest="with_gui",
    action="store_true",
    help="Runs the randomizer through a gui.",
)

# parser.print_help()
args = parser.parse_args()


if args.with_gui:
    from gui.main import start_gui
    start_gui()
else:
    worlds = generate("config.yaml")

    patch_handler = AllPatchHandler(worlds[0])
    patch_handler.do_all_patches()
