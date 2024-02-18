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
