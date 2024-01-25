from functools import partial
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QAbstractButton,
    QCheckBox,
    QComboBox,
)

from filepathconstants import CONFIG_PATH, PLANDO_PATH
from logic.config import Config, write_config_to_file

from typing import TYPE_CHECKING

from randomizer.verify_extract import verify_extract

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

        self.verify_important_button = self.ui.verify_important_extract_button
        self.verify_important_button.clicked.connect(verify_extract)

        self.verify_all_button = self.ui.verify_all_extract_button
        self.verify_all_button.clicked.connect(
            partial(verify_extract, verify_all_files=True)
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

    def show_file_error_dialog(self, file_text: str):
        self.main.fi_info_dialog.show_dialog(title="File not found!", text=file_text)
