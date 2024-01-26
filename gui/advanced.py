from functools import partial
from pathlib import Path
import sys

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QAbstractButton,
    QCheckBox,
    QComboBox,
    QLineEdit,
    QFileDialog,
)

from filepathconstants import CONFIG_PATH, DEFAULT_OUTPUT_PATH, PLANDO_PATH
from gui.dialogs.error_dialog import error_from_str
from gui.dialogs.verify_files_progress_dialog import VerifyFilesProgressDialog
from gui.guithreads import VerificationThread
from logic.config import Config, write_config_to_file

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import Main
    from gui.ui.ui_main import Ui_main_window

NO_PLANDO_FILE = "~~ No Plandomizer File ~~"


class Advanced:
    def __init__(self, main: "Main", ui: "Ui_main_window"):
        self.main = main
        self.ui = ui
        self.config: Config = main.config

        # TODO: Add configs for these
        self.ui.random_settings_group_box.setTitle("")
        self.ui.randomization_settings_group_box.setTitle("")

        self.output_dir_line_edit: QLineEdit = self.ui.config_output
        self.output_dir_line_edit.setText(self.config.output_dir.as_posix())

        self.reset_output_button: QAbstractButton = self.ui.reset_output_button
        self.reset_output_button.clicked.connect(self.reset_output_dir)

        self.browse_output_button: QAbstractButton = self.ui.browse_output_button
        self.browse_output_button.clicked.connect(self.open_file_picker)

        self.spoiler_log_check_box: QCheckBox = self.ui.config_generate_spoiler_log
        self.spoiler_log_check_box.setChecked(self.config.generate_spoiler_log)
        self.spoiler_log_check_box.stateChanged.connect(self.toggle_spoiler_log)

        self.verify_thread = VerificationThread()
        self.verify_thread.error_abort.connect(self.thread_error)

        self.verify_important_button = self.ui.verify_important_extract_button
        self.verify_important_button.clicked.connect(self.verify_extract)

        self.verify_all_button = self.ui.verify_all_extract_button
        self.verify_all_button.clicked.connect(
            partial(self.verify_extract, verify_all=True)
        )

        self.use_plando_button: QCheckBox = self.ui.config_use_plandomizer
        self.use_plando_button.stateChanged.connect(self.toggle_plando)
        self.toggle_plando()

        self.selected_plando_file_combo: QComboBox = (
            self.ui.selected_plandomizer_file_combo_box
        )

        if not PLANDO_PATH.exists():
            PLANDO_PATH.mkdir()

        plando_filenames = [
            file.name
            for file in PLANDO_PATH.glob("*.yaml")
            if file.name.endswith(".yaml")
        ]
        self.selected_plando_file_combo.addItems([NO_PLANDO_FILE] + plando_filenames)
        self.selected_plando_file_combo.currentTextChanged.connect(
            self.change_plando_file
        )
        self.change_plando_file()

        self.open_plando_folder_button: QAbstractButton = (
            self.ui.open_plandomizer_folder_button
        )
        self.open_plando_folder_button.clicked.connect(self.open_plando_folder)

    def update_config(self):
        write_config_to_file(CONFIG_PATH, self.config)

    def open_file_picker(self):
        if output_dir := QFileDialog.getExistingDirectory(
            self.main, "Select output folder", self.config.output_dir.as_posix()
        ):
            self.output_dir_line_edit.setText(output_dir)
            self.config.output_dir = Path(output_dir)
            self.update_config()

    def reset_output_dir(self):
        self.config.output_dir = DEFAULT_OUTPUT_PATH
        self.output_dir_line_edit.setText(self.config.output_dir.as_posix())
        self.update_config()

    def toggle_spoiler_log(self):
        generate_spoiler_log: Qt.CheckState = self.spoiler_log_check_box.checkState()
        self.config.generate_spoiler_log = False

        if generate_spoiler_log == Qt.CheckState.Checked:
            self.config.generate_spoiler_log = True

        self.update_config()

    def toggle_plando(self):
        use_plando_state: Qt.CheckState = self.use_plando_button.checkState()
        self.config.use_plandomizer = False

        if use_plando_state == Qt.CheckState.Checked:
            self.config.use_plandomizer = True

        self.update_config()

    def change_plando_file(self):
        self.config.plandomizer_file = self.selected_plando_file_combo.currentText()

        if self.config.plandomizer_file == NO_PLANDO_FILE:
            self.config.plandomizer_file = None

        self.update_config()

    def open_plando_folder(self):
        try:
            if not PLANDO_PATH.exists():
                PLANDO_PATH.mkdir()

            QDesktopServices.openUrl(
                QUrl(PLANDO_PATH.as_posix(), QUrl.ParsingMode.TolerantMode)
            )
        except:
            self.show_file_error_dialog(
                "Could not open or create the 'plandomizers' folder.\n\nThe 'plandomizers' folder should be in the same folder as this randomizer program."
            )

    def verify_extract(self, verify_all: bool = False):
        verify_dialog = VerifyFilesProgressDialog(self.main)
        self.verify_thread.dialog_value_update.connect(verify_dialog.setValue)
        self.verify_thread.dialog_label_update.connect(verify_dialog.setLabelText)

        self.verify_thread.set_verify_all(verify_all)
        self.verify_thread.setTerminationEnabled(True)
        self.verify_thread.start()
        verify_dialog.exec()

        # Prevents old progress dialogs reappearing when verifying multiple
        # times without reopening the entire program
        verify_dialog.deleteLater()

    def show_file_error_dialog(self, file_text: str):
        self.main.fi_info_dialog.show_dialog(title="File not found!", text=file_text)

    def thread_error(self, exception: str, traceback: str):
        error_from_str(exception, traceback)
        sys.exit()
