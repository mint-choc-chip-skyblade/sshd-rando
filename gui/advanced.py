from functools import partial
from pathlib import Path
import os

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QAbstractButton,
    QCheckBox,
    QComboBox,
    QLineEdit,
    QFileDialog,
    QSpacerItem,
    QSizePolicy,
)

from filepathconstants import (
    CONFIG_PATH,
    DEFAULT_OUTPUT_PATH,
    PLANDO_PATH,
    SPOILER_LOGS_PATH,
    SSHD_EXTRACT_PATH,
    OTHER_MODS_PATH,
    COMBINED_MODS_FOLDER,
)
from gui.dialogs.error_dialog import error_from_str
from gui.dialogs.verify_files_progress_dialog import VerifyFilesProgressDialog
from gui.dialogs.fi_info_dialog import FiInfoDialog
from gui.guithreads import VerificationThread
from logic.config import Config, write_config_to_file, seed_rng

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

        self.ui.refresh_mod_list_button.clicked.connect(self.generate_other_mods_list)

        self.verify_dialog = None

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

        # Open Folders buttons
        self.open_plando_folder_button: QAbstractButton = (
            self.ui.open_plandomizer_folder_button
        )
        self.open_plando_folder_button.clicked.connect(self.open_plando_folder)

        self.open_extract_folder_button: QAbstractButton = (
            self.ui.open_extract_folder_button
        )
        self.open_extract_folder_button.clicked.connect(self.open_extract_folder)

        self.open_output_folder_button: QAbstractButton = (
            self.ui.open_output_folder_button
        )
        self.open_output_folder_button.clicked.connect(self.open_output_folder)

        self.open_spoiler_logs_folder_button: QAbstractButton = (
            self.ui.open_spoiler_logs_folder_button
        )
        self.open_spoiler_logs_folder_button.clicked.connect(
            self.open_spoiler_logs_folder
        )

        # Other mods
        self.generate_other_mods_list()

    def update_config(self):
        write_config_to_file(CONFIG_PATH, self.config)
        self.update_hash()

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
        self.main.settings.update_setting_string()

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

            QDesktopServices.openUrl(QUrl.fromLocalFile(PLANDO_PATH.absolute()))
        except:
            self.show_file_error_dialog(
                "Could not open or create the 'plandomizers' folder.\n\nThe 'plandomizers' folder should be in the same folder as this randomizer program."
            )

    def open_extract_folder(self):
        # If this fails, let the error get caught normally so the user can report it.
        QDesktopServices.openUrl(QUrl.fromLocalFile(SSHD_EXTRACT_PATH.absolute()))

    def open_output_folder(self):
        if not self.config.output_dir.exists():
            self.config.output_dir.mkdir()

        QDesktopServices.openUrl(QUrl.fromLocalFile(self.config.output_dir.absolute()))

    def open_spoiler_logs_folder(self):
        if not SPOILER_LOGS_PATH.exists():
            SPOILER_LOGS_PATH.mkdir()

        QDesktopServices.openUrl(QUrl.fromLocalFile(SPOILER_LOGS_PATH.absolute()))

    def verify_extract(self, verify_all: bool = False) -> bool:
        self.verify_dialog = VerifyFilesProgressDialog(self.main, self.cancel_callback)
        self.verify_thread.dialog_value_update.connect(self.verify_dialog.setValue)
        self.verify_thread.dialog_label_update.connect(self.verify_dialog.setLabelText)

        self.verify_thread.set_verify_all(verify_all)
        self.verify_thread.setTerminationEnabled(True)
        self.verify_thread.start()
        self.verify_dialog.exec()

        completion_dialog = FiInfoDialog(self.main)

        if self.verify_dialog is None:
            completion_dialog.show_dialog(
                "Verification Failed",
                "Verification could not be completed.<br><br>Randomization will not work.",
            )
            return False

        if verify_all:
            self.main.config.verified_extract = True
            self.update_config()

            # Make sure the "Randomize" button no longer has the "Verify Extract" label
            self.main.ui.randomize_button.setText("Randomize")
            self.main.ui.randomize_button.clicked.disconnect()
            self.main.ui.randomize_button.clicked.connect(self.main.randomize)

        completion_dialog.show_dialog("Done", "Verification Complete!")

        # Prevents old progress dialogs reappearing when verifying multiple
        # times without reopening the entire program
        self.verify_dialog.deleteLater()

        return True

    def generate_other_mods_list(self):
        self.main.clear_layout(self.ui.other_mods_scroll_layout)
        found_mods = []
        for entry in os.scandir(OTHER_MODS_PATH):
            if entry.is_dir():
                mod_name = entry.name

                # Don't include the combined mods folder as a mod folder. Normally this folder is deleted, but
                # if generation fails for some reason, then it might not get deleted.
                if mod_name == COMBINED_MODS_FOLDER:
                    continue

                # Don't include the mod if it has an exefs folder. We don't support integrating other mods which modify code
                if (OTHER_MODS_PATH / mod_name / "exefs").exists():
                    continue

                mod_checkbox = QCheckBox(mod_name)
                mod_checkbox.clicked.connect(self.update_mods_in_config)
                if mod_name in self.config.settings[0].other_mods:
                    mod_checkbox.setChecked(True)
                    found_mods.append(mod_name)

                self.ui.other_mods_scroll_layout.addWidget(mod_checkbox)

        # Add a vertical spacer to push the mod list up
        self.ui.other_mods_scroll_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Remove mods from config which weren't found
        for mod_name in self.config.settings[0].other_mods.copy():
            if mod_name not in found_mods:
                print(
                    f"Removing mod {mod_name} from other_mods list as the QCheckbox for the mod could not be found"
                )
                self.config.settings[0].other_mods.remove(mod_name)

        self.update_config()

    def update_mods_in_config(self):
        other_mods = self.config.settings[0].other_mods
        other_mods.clear()
        for checkbox in self.ui.other_mods_scroll_widget.findChildren(QCheckBox):
            if checkbox.isChecked():
                other_mods.append(checkbox.text())

        self.update_config()

    def cancel_callback(self):
        VerificationThread.cancelled = True

    def show_file_error_dialog(self, file_text: str):
        self.main.fi_info_dialog.show_dialog(title="File not found!", text=file_text)

    def update_hash(self):
        self.config.hash = ""

        if self.config.seed == "":
            self.main.settings.new_seed()

        seed_rng(self.config)
        self.ui.hash_label.setText(f"Hash: {self.config.get_hash()}")

    def thread_error(self, exception: str, traceback: str):
        if self.verify_dialog is not None:
            self.verify_dialog.deleteLater()
            self.verify_dialog = None

        if "ThreadCancelled" in traceback:
            print(exception, "This should be ignored.")
        else:
            error_from_str(exception, traceback)
