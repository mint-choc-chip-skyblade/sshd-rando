import multiprocessing as mp
import os
import sys

# Required to make the multiprocessing stuff not infinitely hang when running a build
# version. See https://pyinstaller.org/en/stable/common-issues-and-pitfalls.html?highlight=multipr#multi-processing
# for more info.
mp.freeze_support()

from filepathconstants import (
    PLANDO_PATH,
    PRESETS_PATH,
    SSHD_EXTRACT_PATH,
    OTHER_MODS_PATH,
)
from util.arguments import get_program_args
import logging


args = get_program_args()

# Set specified log level
if args.debug and __name__ == "__main__":
    print("Starting Debug Log")
    logging.basicConfig(
        filename="debug.log",
        encoding="utf-8",
        level=logging.DEBUG,
        filemode="w",
    )

# Ensure the necessary directories are created
if not SSHD_EXTRACT_PATH.exists():
    SSHD_EXTRACT_PATH.mkdir()

if not PLANDO_PATH.exists():
    PLANDO_PATH.mkdir()

if not PRESETS_PATH.exists():
    PRESETS_PATH.mkdir()

if not OTHER_MODS_PATH.exists():
    OTHER_MODS_PATH.mkdir()

# Imports here to prevent circular dependency
if not args.nogui:
    from gui.main import start_gui

    if __name__ == "__main__":
        # Before starting the gui, setup exception handling
        from PySide6.QtWidgets import QApplication
        from gui.dialogs.error_dialog import error

        # Adding these lines helps fix the GUI on Retina displays
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        app = QApplication(sys.argv + ["--style", "fusion"])

        try:
            start_gui(app)
        except Exception as e:
            error(e)
else:
    from randomizer.randomize import randomize

    if __name__ == "__main__":
        randomize()
