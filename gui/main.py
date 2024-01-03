import sys

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget

from constants.randoconstants import VERSION
from filepathconstants import ICON_PATH

from gui.accessibility import Accessibility
from gui.guithreads import RandomizationThread
from gui.options import Options
from gui.dialogs.randomize_progress_dialog import RandomizerProgressDialog
from gui.ui.ui_main import Ui_main_window


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.randomize_thread = RandomizationThread()

        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        self.setWindowTitle(
            "The Legend of Zelda: Skyward Sword HD Randomizer " + VERSION
        )

        self.setWindowIcon(QIcon(ICON_PATH.as_posix()))

        # Always open on the getting started tab
        self.ui.tab_widget.setCurrentIndex(0)

        self.options = Options(self, self.ui)
        self.accessibility = Accessibility(self, self.ui)

        self.ui.randomize_button.clicked.connect(self.randomize)
        self.ui.about_button.clicked.connect(self.about)

    def randomize(self):
        progress_dialog = RandomizerProgressDialog(self)

        self.randomize_thread.dialog_value_update.connect(progress_dialog.setValue)
        self.randomize_thread.dialog_label_update.connect(progress_dialog.setLabelText)

        self.randomize_thread.setTerminationEnabled(True)
        self.randomize_thread.start()
        progress_dialog.exec()

    def about(self):
        about_dialog = QMessageBox(self)
        about_dialog.setTextFormat(Qt.TextFormat.RichText)

        about_text = f"""
                        <b>The Legend of Zelda: Skyward Sword HD Randomizer</b><br>
                        Version: {VERSION}<br><br>

                        Created by:
                        <a href=\"https://github.com/covenesme\">CovenEsme</a>,
                        <a href=\"https://github.com/muzugalium\">Muzugalium</a>,
                        <a href=\"https://github.com/gymnast86\">Gymnast86</a>, and
                        <a href=\"https://github.com/tbpixel\">tbpixel</a><br><br>

                        <a href=\"https://github.com/mint-choc-chip-skyblade/sshd-rando/issues\">Report issues</a>
                        or view the 
                        <a href=\"https://github.com/mint-choc-chip-skyblade/sshd-rando\">Source code</a>
        """

        about_dialog.about(self, "About", about_text)

    def eventFilter(self, target: QWidget, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Enter:
            return self.options.update_descriptions(target)
        elif event.type() == QEvent.Type.Leave:
            return self.options.update_descriptions(None)
        elif event.type() == QEvent.Type.ContextMenu:
            return self.options.show_full_descriptions(target)
        elif (
            isinstance(event, QMouseEvent)
            and event.button() == Qt.MouseButton.MiddleButton
        ):
            return self.options.reset_single(
                self.options.get_setting_from_widget(target)
            )

        return QMainWindow.eventFilter(self, target, event)


def start_gui():
    app = QApplication([])

    widget = Main()
    widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    start_gui()
