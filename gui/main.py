# Allow keyboard interrupts on the command line to instantly close the program.
import signal
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from ui.ui_main import Ui_MainWindow


signal.signal(signal.SIGINT, signal.SIG_DFL)

# TODO: Replace with a proper version
TEMP_VERSION = "-1"

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("The Legend of Zelda: Skyward Sword HD Randomizer " + TEMP_VERSION)

def start_gui():
    app = QApplication([])

    widget = Main()
    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    start_gui()
