from functools import partial
from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QLineEdit,
    QMessageBox,
    QMainWindow,
    QSpinBox,
    QWidget,
)
from constants.configdefaults import get_new_seed

from filepathconstants import CONFIG_PATH, FI_ICON_PATH
from logic.config import load_config_from_file, write_config_to_file
from logic.settings import Setting


OPTION_PREFIX = "&nbsp;&nbsp;➜ "


class Options:
    def __init__(self, parent, ui):
        self.parent: QMainWindow = parent
        self.ui = ui

        self.config = load_config_from_file(CONFIG_PATH, create_if_blank=True)
        self.settings = self.config.settings[0].settings

        self.set_setting_descriptions(None)

        # Init seed
        seed_widget: QLineEdit = getattr(self.ui, "setting_seed")
        seed_widget.setText(self.config.seed)
        seed_widget.textChanged.connect(self.update_seed)

        self.ui.new_seed_button.clicked.connect(self.new_seed)
        self.ui.reset_button.clicked.connect(self.reset)

        # Init other settings
        for setting_name, setting_info in self.settings.items():
            current_option_value = setting_info.value

            widget = None  # type: ignore
            label = None  # type: ignore

            try:
                widget: QWidget = getattr(self.ui, "setting_" + setting_name)
            except:
                print(f"Could not find widget for setting: {setting_name}.")
                continue

            # Used to change the settings description when mousing over a setting
            widget.installEventFilter(self.parent)

            try:
                label = getattr(self.ui, setting_name + "_label")
                label.installEventFilter(self.parent)
            except:
                pass

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

                widget.clicked.connect(partial(self.update_settings, widget))
            elif isinstance(widget, QComboBox):  # pick one option
                for option in setting_info.info.pretty_options:
                    widget.addItem(option)

                widget.setCurrentIndex(
                    setting_info.info.options.index(setting_info.value)
                )
                widget.currentIndexChanged.connect(
                    partial(self.update_settings, widget)
                )
            elif isinstance(widget, QSpinBox):  # pick a value
                widget.setMinimum(
                    int(setting_info.info.options[0]) - 1
                )  # -1 for special value
                widget.setMaximum(int(setting_info.info.options[-2]))
                widget.setSpecialValueText("Random")

                if current_option_value == "random":
                    widget.setValue(widget.minimum())
                else:
                    widget.setValue(int(current_option_value))

                widget.valueChanged.connect(partial(self.update_settings, widget))

        # Force descriptions to update before changing any setting
        self.update_settings()

    def update_settings(self, from_widget=None, from_reset=False, _=None):
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
                # Makes tristate buttons cycle: off, on, random
                # instead of off, random, on
                # but only when manually changed
                if widget == from_widget and not from_reset:
                    if widget.checkState() == Qt.CheckState.Checked:
                        widget.setCheckState(Qt.CheckState.Unchecked)
                        new_option = "off"
                    elif widget.checkState() == Qt.CheckState.PartiallyChecked:
                        widget.setCheckState(Qt.CheckState.Checked)
                        new_option = "on"
                    else:
                        widget.setCheckState(Qt.CheckState.PartiallyChecked)
                        new_option = "random"
                else:
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

            widget.setToolTip(
                "➜ Right-click to view all options.\n➜ Middle-click to reset to default."
            )

        self.config.settings[0].settings = self.settings

        write_config_to_file(CONFIG_PATH, self.config)
        self.update_descriptions(from_widget)

    def get_updated_setting(self, setting: Setting, value: str) -> Setting:
        if value == "":
            raise ValueError(
                f"Cannot update setting '{setting.name}' value as value is empty."
            )

        new_setting = setting

        if ((value.startswith("-") and value[1:].isdigit()) or value.isdigit()) and int(
            value
        ) == int(setting.info.options[0]) - 1:
            option_index = setting.info.options.index("random")
            new_setting.value = "random"
        else:
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

    def reset_single(self, setting: Setting | None) -> bool:
        if setting is None:
            return False

        setting_name = setting.info.name
        widget = None  # type: ignore

        try:
            widget: QWidget = getattr(self.ui, "setting_" + setting_name)
        except:
            # print(f"Cannot find attribute for '{setting_name}', ignoring.")
            return False

        if not widget:
            return False

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
            widget.setValue(int(default_option))

        self.update_settings(from_widget=widget, from_reset=True)
        return True

    def reset(self):
        confirm_choice = QMessageBox.question(
            self.parent,
            "Are you sure?",
            "Are you sure you want to reset EVERY option?",
        )

        if confirm_choice != QMessageBox.Yes:  # type: ignore (Qt is stupid)
            return

        for setting_name, setting in self.settings.items():
            self.reset_single(setting)

    def get_setting_from_widget(self, widget: QObject | None) -> Setting | None:
        if widget is None:
            return None

        widget_name = widget.objectName()
        setting_name = widget_name.removeprefix("setting_")
        setting_name = setting_name.removesuffix("_label")

        if self.settings.get(setting_name):
            return self.settings[setting_name]
        else:
            return None

    def set_setting_descriptions(self, setting: Setting | None):
        if setting is None:
            default_description = (
                OPTION_PREFIX
                + "Hover over a setting to see a description of the current and default options.<br>"
            )
            default_description += (
                OPTION_PREFIX
                + "Right click a setting to see a full description of all the options.<br>"
            )
            default_description += (
                OPTION_PREFIX + "Middle click a setting to reset it to default."
            )

            self.ui.settings_current_option_description_label.setText(
                default_description
            )
            self.ui.settings_default_option_description_label.setText("")
            # self.ui.settings_current_option_description_label.setStyleSheet("color: grey;")
        else:
            current_option_description = (
                "<b>Current Option</b> (<i>Right-click to see all the options</i>):<br>"
            )
            current_option_description += self.format_description(
                setting, setting.current_option_index
            )
            default_option_description = "<b>Default Option</b>:<br>"
            default_option_description += self.format_description(
                setting, setting.info.default_option_index
            )

            self.ui.settings_current_option_description_label.setText(
                current_option_description
            )
            self.ui.settings_default_option_description_label.setText(
                default_option_description
            )
            # self.ui.settings_current_option_description_label.setStyleSheet("")

    def format_description(self, setting: Setting, setting_index: int) -> str:
        formatted_description = (
            "<b>"
            + OPTION_PREFIX
            + setting.info.pretty_options[setting_index]
            + "</b>: "
        )
        formatted_description += setting.info.descriptions[setting_index]
        return formatted_description

    def update_descriptions(self, target: QObject | None) -> bool:
        if setting := self.get_setting_from_widget(target):
            self.set_setting_descriptions(setting)
        else:
            self.set_setting_descriptions(None)

        return True

    def show_full_descriptions(self, target: QWidget | None) -> bool:
        if target is None or not (setting := self.get_setting_from_widget(target)):
            return True

        description_dialog = QMessageBox(target)
        description_dialog.setTextFormat(Qt.TextFormat.RichText)
        target.setWindowIcon(QIcon(FI_ICON_PATH.as_posix()))

        description_text = "<b>Current Option</b>:<br>"
        description_text += self.format_description(
            setting, setting.current_option_index
        )
        description_text += "<br><br><b>Default Option</b>:<br>"
        description_text += self.format_description(
            setting, setting.info.default_option_index
        )
        description_text += "<br><br><b>All Options</b>:<br>"

        for option_index in range(0, len(setting.info.options)):
            description_text += self.format_description(setting, option_index) + "<br>"

        dialog_title = setting.info.pretty_name + " Options"
        description_dialog.about(target, dialog_title, description_text)
        return True
