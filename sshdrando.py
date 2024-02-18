import argparse
import logging


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
if args.debug and __name__ == "__main__":
    print("Starting Debug Log")
    logging.basicConfig(
        filename="debug.log",
        encoding="utf-8",
        level=logging.DEBUG,
        filemode="w",
    )

# Imports here to prevent circular dependency
if args.with_gui:
    from gui.main import start_gui

    if __name__ == "__main__":
        # Before starting the gui, setup exception handling
        from PySide6.QtWidgets import QApplication
        from gui.dialogs.error_dialog import error

        app = QApplication([])

        try:
            start_gui(app)
        except Exception as e:
            error(e)
else:
    from randomizer.randomize import randomize

    if __name__ == "__main__":
        randomize()
