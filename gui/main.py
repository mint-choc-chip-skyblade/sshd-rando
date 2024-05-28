import sys
from types import TracebackType

from PySide6.QtCore import QEvent, Qt, QSize, QUrl
from PySide6.QtGui import QDesktopServices, QIcon, QMouseEvent, QPixmap
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget

from constants.randoconstants import VERSION
from filepathconstants import (
    CONFIG_PATH,
    DEFAULT_OUTPUT_PATH,
    EXEFS_EXTRACT_PATH,
    ICON_PATH,
    ROMFS_EXTRACT_PATH,
)

from gui.accessibility import Accessibility
from gui.advanced import Advanced
from gui.dialogs.dialog_header import print_progress_text
from gui.tracker import Tracker
from gui.dialogs.error_dialog import error, error_from_str
from gui.dialogs.fi_info_dialog import FiInfoDialog
from gui.dialogs.fi_question_dialog import FiQuestionDialog
from gui.guithreads import RandomizationThread
from gui.settings import Settings
from gui.dialogs.randomize_progress_dialog import RandomizerProgressDialog
from gui.ui.ui_main import Ui_main_window
from logic.config import load_config_from_file, write_config_to_file


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        print_progress_text("Initializing GUI")

        self.randomize_thread = RandomizationThread()
        self.randomize_thread.error_abort.connect(self.thread_error)

        self.progress_dialog = None

        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        self.setWindowTitle(
            f"The Legend of Zelda: Skyward Sword HD Randomizer (Ver. {VERSION})"
        )

        self.setWindowIcon(QIcon(ICON_PATH.as_posix()))

        # Always open on the getting started tab
        self.ui.tab_widget.setCurrentIndex(0)

        self.fi_info_dialog = FiInfoDialog(self)
        self.fi_question_dialog = FiQuestionDialog(self)

        self.config = load_config_from_file(CONFIG_PATH, create_if_blank=True)

        print_progress_text("Initializing GUI: accessibility")
        self.accessibility = Accessibility(self, self.ui)
        print_progress_text("Initializing GUI: settings")
        self.settings = Settings(self, self.ui)
        print_progress_text("Initializing GUI: advanced")
        self.advanced = Advanced(self, self.ui)
        print_progress_text("Initializing GUI: tracker")
        self.tracker = Tracker(self, self.ui)

        self.ui.randomize_button.setDisabled(True)
        self.ui.randomize_button.clicked.connect(self.randomize)
        self.ui.about_button.clicked.connect(self.about)
        print_progress_text("GUI initialized")

    def randomize(self):
        if not self.check_output_dir():
            return

        self.progress_dialog = RandomizerProgressDialog(self, self.cancel_callback)

        self.randomize_thread.dialog_value_update.connect(self.progress_dialog.setValue)
        self.randomize_thread.dialog_label_update.connect(
            self.progress_dialog.setLabelText
        )

        self.randomize_thread.setTerminationEnabled(True)
        self.randomize_thread.start()
        self.progress_dialog.exec()

        if self.progress_dialog is None:
            self.fi_info_dialog.show_dialog(
                "Randomization Failed",
                "The randomization was unable to be completed and has been cancelled.",
            )
            return

        done_dialog = QMessageBox(self)
        done_dialog.setWindowTitle("Randomization Completed")
        done_dialog.setText(
            f"Seed successfully generated!\n\nHash: {self.config.get_hash()}"
        )

        open_output_button = done_dialog.addButton(
            "Open", QMessageBox.ButtonRole.NoRole
        )
        open_output_button.clicked.disconnect()  # Prevent from closing the done message
        open_output_button.clicked.connect(self.open_output_folder)

        done_dialog.addButton("OK", QMessageBox.ButtonRole.NoRole)

        done_dialog.setWindowIcon(QIcon(ICON_PATH.as_posix()))
        icon_pixmap = QPixmap(ICON_PATH.as_posix()).scaled(
            QSize(80, 80),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        done_dialog.setIconPixmap(icon_pixmap)
        done_dialog.exec()

        # Prevents old progress dialogs reappearing when generating another
        # seed without reopening the entire program
        self.progress_dialog.deleteLater()

    def cancel_callback(self):
        RandomizationThread.cancelled = True

    def open_output_folder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.config.output_dir.as_posix()))

    def check_output_dir(self) -> bool:
        output_dir = self.config.output_dir

        if output_dir != DEFAULT_OUTPUT_PATH and (
            not output_dir.exists() or not output_dir.is_dir()
        ):
            output_not_exists_dialog = self.fi_question_dialog.show_dialog(
                "Cannot find output folder",
                f"""
The output folder you have specified cannot be found.
<br>Would you like to continue and use the default output path?
<br>
<br>Your output path:
<br>{output_dir.as_posix()}
<br>
<br>Default output folder:
<br>{DEFAULT_OUTPUT_PATH.as_posix()}""",
            )

            if output_not_exists_dialog != QMessageBox.StandardButton.Yes:
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
                        <a href=\"https://github.com/Kuonino\">Kuonino</a>,
                        <a href=\"https://github.com/gymnast86\">Gymnast86</a>,
                        <a href=\"https://github.com/tbpixel\">tbpixel</a>, and
                        <a href=\"https://github.com/YourAverageLink\">YourAverageLink</a><br><br>

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
        if self.progress_dialog is not None:
            self.progress_dialog.deleteLater()
            self.progress_dialog = None

        if "ThreadCancelled" in traceback:
            print(exception, "This should be ignored.")
        else:
            error_from_str(exception, traceback)


def start_gui(app: QApplication):
    try:
        main = Main()
        main.show()

        if not main.config.verified_extract:
            get_extract_text = "Before you can begin, you will need to provide an extract of The Legend of Zelda: Skyward Sword HD"
            get_extract_text += "<br><br>Instructions for how to do this can be found here: <a href='https://docs.google.com/document/d/1HHQRXND0n-ZrmhEl4eXjzMANQ-xHK3pKKXPQqSbwXwY'>The Legend of Zelda: Skyward Sword HD Randomizer - Setup Guide</a>"
            get_extract_text += '<br><br>Once you are ready, click "OK" and the extract folder will open. Copy your extract of the base game into this folder'
            get_extract_text += "<br><br>(If you just wish to look around, you can skip this step but you will be unable to randomize the game)."
            main.fi_info_dialog.show_dialog(
                title="Getting Started", text=get_extract_text
            )

            main.advanced.open_extract_folder()

            confirm_first_time_verify_dialog = main.fi_question_dialog.show_dialog(
                "Perform Full Verification?",
                f'Would you like to verify your extract (required for the randomizer to work)?<br><br>Answering "No" will prevent you from randomizing the game but you will still be able to look around.',
            )

            if confirm_first_time_verify_dialog == QMessageBox.StandardButton.Yes:
                if main.advanced.verify_extract(verify_all=True):
                    main.ui.randomize_button.setDisabled(False)
                    main.config.verified_extract = True
                    main.settings.update_from_config()
        else:
            main.ui.randomize_button.setDisabled(False)

        sys.exit(app.exec())
    except Exception as e:
        error(e)
        sys.exit()


old_excepthook = sys.excepthook


def excepthook(source, exception, traceback: TracebackType):
    old_excepthook(source, exception, traceback)

    traceback_str = "Qt caught and ignored exception:\n"
    current_traceback = traceback

    while current_traceback.tb_next is not None:
        traceback_str += f"\n{current_traceback.tb_frame}"
        current_traceback = current_traceback.tb_next

    traceback_str += f"\n\n{source}: {exception}"
    error_from_str(exception, traceback_str)


sys.excepthook = excepthook

if __name__ == "__main__":
    start_gui(QApplication([]))
