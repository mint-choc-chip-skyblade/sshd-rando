# Allow keyboard interrupts on the command line to instantly close the program.
import signal
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

from constants.randoconstants import VERSION
from filepathconstants import ICON_PATH
from gui.ui.ui_main import Ui_MainWindow


signal.signal(signal.SIGINT, signal.SIG_DFL)


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(
            "The Legend of Zelda: Skyward Sword HD Randomizer " + VERSION
        )

        self.setWindowIcon(QIcon(ICON_PATH.as_posix()))

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
