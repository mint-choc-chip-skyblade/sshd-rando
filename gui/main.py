import sys

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget

from constants.randoconstants import VERSION
from filepathconstants import CONFIG_PATH, DEFAULT_OUTPUT_PATH, ICON_PATH

from gui.accessibility import Accessibility
from gui.advanced import Advanced
from gui.dialogs.error_dialog import error, error_from_str
from gui.dialogs.fi_info_dialog import FiInfoDialog
from gui.guithreads import RandomizationThread
from gui.settings import Settings
from gui.dialogs.randomize_progress_dialog import RandomizerProgressDialog
from gui.ui.ui_main import Ui_main_window
from logic.config import load_config_from_file, write_config_to_file


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.randomize_thread = RandomizationThread()
        self.randomize_thread.error_abort.connect(self.thread_error)

        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        self.setWindowTitle(
            f"The Legend of Zelda: Skyward Sword HD Randomizer (Ver. {VERSION})"
        )

        self.setWindowIcon(QIcon(ICON_PATH.as_posix()))

        # Always open on the getting started tab
        self.ui.tab_widget.setCurrentIndex(0)

        self.fi_info_dialog = FiInfoDialog(self)

        self.config = load_config_from_file(CONFIG_PATH, create_if_blank=True)

        self.settings = Settings(self, self.ui)
        self.accessibility = Accessibility(self, self.ui)
        self.advanced = Advanced(self, self.ui)

        self.ui.randomize_button.clicked.connect(self.randomize)
        self.ui.about_button.clicked.connect(self.about)

    def randomize(self):
        if not self.check_output_dir():
            return

        progress_dialog = RandomizerProgressDialog(self)

        self.randomize_thread.dialog_value_update.connect(progress_dialog.setValue)
        self.randomize_thread.dialog_label_update.connect(progress_dialog.setLabelText)

        self.randomize_thread.setTerminationEnabled(True)
        self.randomize_thread.start()
        progress_dialog.exec()

        # Prevents old progress dialogs reappearing when generating another
        # seed without reopening the entire program
        progress_dialog.deleteLater()

    def check_output_dir(self) -> bool:
        output_dir = self.config.output_dir

        if output_dir != DEFAULT_OUTPUT_PATH and (
            not output_dir.exists() or not output_dir.is_dir()
        ):
            output_not_exists_dialog = QMessageBox.question(
                self,
                "Cannot find output folder",
                f"""
The output folder you have specified cannot be found.
Would you like to continue and use the default output path?

Your output path:
{output_dir.as_posix()}

Default output folder:
{DEFAULT_OUTPUT_PATH.as_posix()}""",
            )

            if output_not_exists_dialog != QMessageBox.Yes:  # type: ignore (Qt is stupid)
                return False

            self.config.output_dir = DEFAULT_OUTPUT_PATH
            self.advanced.output_dir_line_edit.setText(
                self.config.output_dir.as_posix()
            )
            write_config_to_file(CONFIG_PATH, self.config)

        return True

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
            return self.settings.update_descriptions(target)
        elif event.type() == QEvent.Type.Leave:
            return self.settings.update_descriptions(None)
        elif event.type() == QEvent.Type.ContextMenu:
            return self.settings.show_full_descriptions(target)
        elif (
            isinstance(event, QMouseEvent)
            and event.button() == Qt.MouseButton.MiddleButton
        ):
            return self.settings.reset_single(
                self.settings.get_setting_from_widget(target)
            )

        return QMainWindow.eventFilter(self, target, event)

    def thread_error(self, exception: str, traceback: str):
        error_from_str(exception, traceback)
        sys.exit()


def start_gui(app: QApplication):
    try:
        widget = Main()
        widget.show()

        sys.exit(app.exec())
    except Exception as e:
        error(e)
        sys.exit()


if __name__ == "__main__":
    start_gui(QApplication([]))
