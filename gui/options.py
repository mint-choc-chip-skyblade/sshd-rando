from PySide6.QtWidgets import QAbstractButton, QComboBox, QSpinBox
from filepathconstants import CONFIG_PATH
from logic.config import load_config_from_file


class Options:
    def __init__(self, ui):
        self.ui = ui

        config = load_config_from_file(CONFIG_PATH, create_if_blank=True)

        for setting_name, setting_info in config.settings[0].settings.items():
            current_option_value = setting_info.value

            widget = None

            try:
                widget = getattr(self.ui, "setting_" + setting_name)
            except:
                pass
                print(f"Could not find widget for setting: {setting_name}.")

            if isinstance(widget, QAbstractButton):  # on or off
                if current_option_value == "on":
                    widget.setChecked(True)
                elif current_option_value == "off":
                    widget.setChecked(False)
                else:
                    raise TypeError(
                        f"Setting '{setting_name}' has value '{current_option_value}' which is invalid for a QAbstractButton. Expected either 'on' or 'off'."
                    )

                widget.clicked.connect(self.update_settings)
            elif isinstance(widget, QComboBox):  # pick one option
                widget.setCurrentIndex(setting_info.current_option)
                widget.currentIndexChanged.connect(self.update_settings)
            elif isinstance(widget, QSpinBox):  # pick a value
                widget.setMinimum(int(setting_info.info.options[0]))
                widget.setMaximum(int(setting_info.info.options[-1]))
                widget.setValue(int(current_option_value))
                widget.valueChanged.connect(self.update_settings)

    def update_settings(self):
        pass
