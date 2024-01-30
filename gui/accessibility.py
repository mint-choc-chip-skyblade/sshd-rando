import json
import qdarktheme

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QAbstractButton,
    QComboBox,
    QFontComboBox,
    QSpinBox,
)
from constants.configconstants import DEFAULT_SETTINGS

from filepathconstants import (
    CONFIG_PATH,
    CUSTOM_THEME_PATH,
    DEFAULT_THEME_PATH,
    DYSLEXIC_FONT_PATH,
    HIGH_CONTRAST_THEME_PATH,
    RANDO_FONT_PATH,
    READABILITY_THEME_PATH,
)
from gui.dialogs.custom_theme_dialog import CustomThemeDialog
from logic.config import Config, write_config_to_file

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import Main
    from gui.ui.ui_main import Ui_main_window

# Add stylesheet overrides here.
BASE_STYLE_SHEET_OVERRIDES = ""

THEME_MODE_OPTIONS = ("Light", "Dark", "Auto")
THEME_PRESETS_OPTIONS = ("Default", "High Contrast", "Readability")


class Accessibility:
    def __init__(self, main: "Main", ui: "Ui_main_window"):
        self.main = main
        self.ui = ui
        self.config: Config = main.config

        QFontDatabase.addApplicationFont(RANDO_FONT_PATH.as_posix())
        QFontDatabase.addApplicationFont(DYSLEXIC_FONT_PATH.as_posix())

        # Accessibility setup.
        self.custom_theme_path = CUSTOM_THEME_PATH
        match self.config.theme_presets:
            case "Default":
                self.default_theme_path = DEFAULT_THEME_PATH
            case "High Contrast":
                self.default_theme_path = HIGH_CONTRAST_THEME_PATH
            case "Readability":
                self.default_theme_path = READABILITY_THEME_PATH
            case _:
                raise ValueError(
                    f"Invalid option for gui-theme-preset option. Expected one of ('Default', 'High Contrast', 'Readability') but found {self.config.theme_presets}."
                )

        if not self.custom_theme_path.is_file():
            with open(self.default_theme_path) as f:
                default_theme_json = json.load(f)
            with open(self.custom_theme_path, "w") as f:
                json.dump(default_theme_json, f)

        self.ui.customize_theme_button.clicked.connect(self.open_custom_theme_picker)
        self.ui.font_reset_button.clicked.connect(self.reset_font)

        # Init accessibility options
        theme_mode_widget: QComboBox = getattr(self.ui, "theme_mode_combo_box")
        theme_mode_widget.addItems(THEME_MODE_OPTIONS)
        theme_mode_widget.currentTextChanged.connect(self.update_theme)
        theme_mode_widget.setCurrentIndex(
            THEME_MODE_OPTIONS.index(self.config.theme_mode)
        )

        theme_presets_widget: QComboBox = getattr(self.ui, "theme_presets_combo_box")
        theme_presets_widget.addItems(THEME_PRESETS_OPTIONS)
        theme_presets_widget.currentTextChanged.connect(self.update_theme_preset)
        theme_presets_widget.setCurrentIndex(
            THEME_PRESETS_OPTIONS.index(self.config.theme_presets)
        )

        use_custom_theme_widget: QAbstractButton = getattr(
            self.ui, "use_custom_theme_check_box"
        )
        self.ui.use_custom_theme_check_box.stateChanged.connect(
            self.toggle_custom_theme
        )

        if self.config.use_custom_theme:
            use_custom_theme_widget.setChecked(True)
            self.enable_theme_interface()
        else:
            use_custom_theme_widget.setChecked(False)
            self.disable_theme_interface()

        font_family_widget: QFontComboBox = getattr(self.ui, "font_family_combo_box")
        font_family_widget.setCurrentIndex(
            font_family_widget.findText(self.config.font_family)
        )
        font_family_widget.currentFontChanged.connect(self.update_font)

        font_size_widget: QSpinBox = getattr(self.ui, "font_size_spin_box")
        font_size_widget.valueChanged.connect(self.update_font)
        font_size_widget.setValue(self.config.font_size)

        self.update_font()
        self.update_theme()

    def toggle_custom_theme(self, state: int):
        self.config.use_custom_theme = bool(state)

        if state:
            self.enable_theme_interface()
        else:
            self.disable_theme_interface()

        self.update_theme()

    def update_theme(self):
        theme_mode: QComboBox = getattr(self.ui, "theme_mode_combo_box")
        self.config.theme_mode = theme_mode.currentText()

        write_config_to_file(CONFIG_PATH, self.config)

        if self.config.use_custom_theme:
            with open(self.custom_theme_path) as f:
                theme = json.load(f)
        else:
            with open(self.default_theme_path) as f:
                theme = json.load(f)

        qdarktheme.setup_theme(
            self.config.theme_mode.lower(), custom_colors=theme, corner_shape="sharp"
        )

    def update_theme_preset(self, preset: str):
        if preset == "Default":
            self.default_theme_path = DEFAULT_THEME_PATH
        elif preset == "High Contrast":
            self.default_theme_path = HIGH_CONTRAST_THEME_PATH
        elif preset == "Readability":
            self.default_theme_path = READABILITY_THEME_PATH

            font_index = self.ui.font_family_combo_box.findText("OpenDyslexic3")
            self.ui.font_family_combo_box.setCurrentIndex(font_index)
            self.ui.font_size_spin_box.setValue(10)

        self.config.theme_presets = preset
        write_config_to_file(CONFIG_PATH, self.config)

        self.update_theme()

    def open_custom_theme_picker(self):
        custom_theme_picker = CustomThemeDialog(
            self.default_theme_path, self.custom_theme_path, self.main.styleSheet()
        )

        custom_theme_picker.themeSaved.connect(self.update_custom_theme)
        custom_theme_picker.exec()

    def update_custom_theme(self, theme: dict):
        with open(self.custom_theme_path, "w") as f:
            json.dump(theme, f)

        self.update_theme()

    def enable_theme_interface(self):
        getattr(self.ui, "customize_theme_button").setEnabled(True)

    def disable_theme_interface(self):
        getattr(self.ui, "customize_theme_button").setEnabled(False)

    def update_font(self):
        font_family_widget: QFontComboBox = getattr(self.ui, "font_family_combo_box")
        self.config.font_family = font_family_widget.currentText()

        font_size_widget: QSpinBox = getattr(self.ui, "font_size_spin_box")
        self.config.font_size = font_size_widget.value()

        write_config_to_file(CONFIG_PATH, self.config)

        self.main.setStyleSheet(
            BASE_STYLE_SHEET_OVERRIDES
            + f"QWidget {{ font-family: { self.config.font_family }; font-size: { self.config.font_size }pt }}"
        )

    def reset_font(self):
        font_index = self.ui.font_family_combo_box.findText(
            DEFAULT_SETTINGS["font_family"]
        )
        self.ui.font_family_combo_box.setCurrentIndex(font_index)
        self.ui.font_size_spin_box.setValue(10)
