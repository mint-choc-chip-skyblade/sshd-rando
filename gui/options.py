from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QLineEdit,
    QMessageBox,
    QMainWindow,
    QSpinBox,
    QWidget,
)

from filepathconstants import CONFIG_PATH
from logic.config import get_new_seed, load_config_from_file, write_config_to_file
from logic.settings import Setting


class Options:
    def __init__(self, parent, ui):
        self.parent: QMainWindow = parent
        self.ui = ui

        self.config = load_config_from_file(CONFIG_PATH, create_if_blank=True)
        self.settings = self.config.settings[0].settings

        # Init seed
        seed_widget: QLineEdit = getattr(self.ui, "setting_seed")
        seed_widget.setText(self.config.seed)
        seed_widget.textChanged.connect(self.update_seed)

        self.ui.new_seed_button.clicked.connect(self.new_seed)
        self.ui.reset_button.clicked.connect(self.reset)

        # Init other settings
        for setting_name, setting_info in self.settings.items():
            current_option_value = setting_info.value

            widget = None

            try:
                widget = getattr(self.ui, "setting_" + setting_name)
            except:
                pass
                print(f"Could not find widget for setting: {setting_name}.")

            if isinstance(widget, QCheckBox):  # on or off
                widget.setTristate(True)

                if current_option_value == "on":
                    widget.setChecked(True)
                elif current_option_value == "random":
                    widget.setCheckState(Qt.CheckState.PartiallyChecked)
                elif current_option_value == "off":
                    widget.setChecked(False)
                else:
                    raise TypeError(
                        f"Setting '{setting_name}' has value '{current_option_value}' which is invalid for a QAbstractButton. Expected either 'on' or 'off'."
                    )

                widget.stateChanged.connect(self.update_settings)
            elif isinstance(widget, QComboBox):  # pick one option
                for option in setting_info.info.pretty_options:
                    widget.addItem(option)

                widget.setCurrentIndex(
                    setting_info.info.options.index(setting_info.value)
                )
                widget.currentIndexChanged.connect(self.update_settings)
            elif isinstance(widget, QSpinBox):  # pick a value
                widget.setMinimum(int(setting_info.info.options[0]))
                widget.setMaximum(int(setting_info.info.options[-2]))
                widget.setValue(int(current_option_value))
                widget.valueChanged.connect(self.update_settings)

    def update_settings(self):
        for setting_name, setting in self.settings.items():
            widget = None  # type: ignore

            try:
                widget: QWidget = getattr(self.ui, "setting_" + setting_name)
            except:
                # print(f"Cannot find attribute for '{setting_name}', ignoring.")
                continue

            if not widget:
                continue

            new_setting = setting
            new_option = ""

            if isinstance(widget, QCheckBox):
                if widget.checkState() == Qt.CheckState.Checked:
                    new_option = "on"
                elif widget.checkState() == Qt.CheckState.PartiallyChecked:
                    new_option = "random"
                else:
                    new_option = "off"
            elif isinstance(widget, QComboBox):
                new_option = new_setting.info.options[widget.currentIndex()]
            elif isinstance(widget, QSpinBox):
                new_option = str(widget.value())

            self.settings[setting_name] = self.get_updated_setting(
                new_setting, new_option
            )

        self.config.settings[0].settings = self.settings

        write_config_to_file(CONFIG_PATH, self.config)

    def get_updated_setting(self, setting: Setting, value: str) -> Setting:
        if value == "":
            raise ValueError(
                f"Cannot update setting '{setting.name}' value as value is empty."
            )

        new_setting = setting

        option_index = setting.info.options.index(value)
        new_setting.value = value
        new_setting.current_option_index = option_index
        new_setting.info.current_option_index = option_index

        return new_setting

    def new_seed(self):
        seed_widget: QLineEdit = getattr(self.ui, "setting_seed")
        seed_widget.setText(get_new_seed())

    def update_seed(self):
        seed_widget: QLineEdit = getattr(self.ui, "setting_seed")
        self.config.seed = seed_widget.text()

        write_config_to_file(CONFIG_PATH, self.config)

    def reset(self):
        confirm_choice = QMessageBox.question(
            self.parent,
            "Are you sure?",
            "Are you sure you want to reset EVERY option?",
        )

        if confirm_choice != QMessageBox.Yes:  # type: ignore (Qt is stupid)
            return

        for setting_name, setting in self.settings.items():
            widget = None  # type: ignore

            try:
                widget: QWidget = getattr(self.ui, "setting_" + setting_name)
            except:
                # print(f"Cannot find attribute for '{setting_name}', ignoring.")
                continue

            if not widget:
                continue

            default_option = setting.info.options[setting.info.default_option_index]

            if isinstance(widget, QCheckBox):
                if default_option == "on":
                    widget.setCheckState(Qt.CheckState.Checked)
                elif default_option == "random":
                    widget.setCheckState(Qt.CheckState.PartiallyChecked)
                elif default_option == "off":
                    widget.setCheckState(Qt.CheckState.Unchecked)
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(setting.info.default_option_index)
            elif isinstance(widget, QSpinBox):
                new_option = str(widget.value())
                widget.setValue(int(default_option))
