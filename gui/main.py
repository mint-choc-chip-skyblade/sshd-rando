# Allow keyboard interrupts on the command line to instantly close the program.
import signal
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from gui.ui.ui_main import Ui_MainWindow


signal.signal(signal.SIGINT, signal.SIG_DFL)

# TODO: Replace with a proper version
TEMP_VERSION = "-1"


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(
            "The Legend of Zelda: Skyward Sword HD Randomizer " + TEMP_VERSION
        )

        # TODO: Replace with path from constants file
        self.setWindowIcon(QIcon("../assets/icon.png"))

        self.ui.randomize_button.clicked.connect(self.randomize)

    def randomize(self):
        print("Randomize")


def start_gui():
    app = QApplication([])

    widget = Main()
    widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    start_gui()
