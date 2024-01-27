from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QAbstractButton,
    QLabel,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import Main
    from gui.ui.ui_main import Ui_main_window

ENTRANCE_TYPES = (
    # "Spawn",
    # "Bird Statue",
    "Dungeon",
    "Door",
    "Interior",
    "Overworld",
    "Trial Gate",
)


class MixedEntrancePools(QObject):
    mixedEntrancePoolsChanged = Signal(QObject, list)

    def __init__(
        self,
        main: "Main",
        ui: "Ui_main_window",
        config_mixed_entrance_pools: list[list[str]],
    ):
        super().__init__()
        self.main = main
        self.ui = ui

        self.pools_label: QLabel = self.ui.mixed_entrance_pools_list_label
        self.mixed_entrance_pools: list[list[str]] = [
            list() for _ in range(1, len(ENTRANCE_TYPES))
        ]

        self.selected_pool_combo: QComboBox = (
            self.ui.highlighted_entrance_pool_combo_box
        )
        self.selected_pool_combo.addItems(
            [f"Pool {num}" for num in range(1, len(ENTRANCE_TYPES))]
        )
        self.selected_pool_combo.currentTextChanged.connect(self.update_pools_label)

        self.selected_type_combo: QComboBox = self.ui.selected_entrance_type_combo_box
        self.selected_type_combo.addItems(ENTRANCE_TYPES)

        self.add_button: QAbstractButton = self.ui.add_entrance_type_button
        self.add_button.clicked.connect(self.add_entrance_type)

        self.remove_button: QAbstractButton = self.ui.remove_entrance_type_button
        self.remove_button.clicked.connect(self.remove_entrance_type)

        self.reset_button: QAbstractButton = self.ui.mixed_entrance_pools_reset_button
        self.reset_button.clicked.connect(self.reset)

        self.update_from_config(config_mixed_entrance_pools)

    def update_from_config(self, config_entrances: list[list[str]]):
        for pool_index, pool in enumerate(config_entrances):
            self.mixed_entrance_pools[pool_index] = pool

        self.update_pools_label()

    def update_pools_label(self):
        pools_text = "<b>Defined Entrance Pools:</b><br>"

        for pool_number in range(1, len(ENTRANCE_TYPES)):
            if (
                is_selected := self.selected_pool_combo.currentText()
                == f"Pool {pool_number}"
            ):
                pools_text += "<b>"

            pools_text += (
                f"<br>Pool {pool_number}: {self.mixed_entrance_pools[pool_number - 1]}"
            )

            if is_selected:
                pools_text += "</b>"

        self.pools_label.setText(pools_text)

    def add_entrance_type(self):
        entrance_type = self.selected_type_combo.currentText()

        if entrance_type in self.pools_label.text():
            self.show_invalid_dialog(
                f"Could not add entrance type '{entrance_type}' as it is already added.\n\nTry removing the entrance type first."
            )
            return

        self.mixed_entrance_pools[self.selected_pool_combo.currentIndex()].append(
            entrance_type
        )
        self.mixedEntrancePoolsChanged.emit(self, self.mixed_entrance_pools)
        self.update_pools_label()

    def remove_entrance_type(self):
        entrance_type = self.selected_type_combo.currentText()

        if entrance_type not in self.pools_label.text():
            self.show_invalid_dialog(
                f"Could not remove entrance type '{entrance_type}' as it has not been added."
            )
            return

        for pool in self.mixed_entrance_pools:
            if entrance_type in pool:
                pool.remove(entrance_type)
                break

        self.mixedEntrancePoolsChanged.emit(self, self.mixed_entrance_pools)
        self.update_pools_label()

    def reset(self):
        self.mixed_entrance_pools: list[list[str]] = [
            list() for _ in range(1, len(ENTRANCE_TYPES))
        ]
        self.mixedEntrancePoolsChanged.emit(self, self.mixed_entrance_pools)
        self.update_pools_label()

    def show_invalid_dialog(self, invalid_text: str):
        self.main.fi_info_dialog.show_dialog(
            title="Invalid Entrance Pool Action", text=invalid_text
        )
