from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QMainWindow,
    QComboBox,
    QAbstractButton,
    QLabel,
    QMessageBox,
)

from filepathconstants import FI_ICON_PATH

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

    def __init__(self, parent, ui, config_mixed_entrance_pools: list[list[str]]):
        super().__init__()
        self.parent: QMainWindow = parent
        self.ui = ui

        self.pools_label: QLabel = self.ui.mixed_entrance_pools_list_label
        self.mixed_entrance_pools: list[list[str]] = [
            list() for _ in range(1, len(ENTRANCE_TYPES))
        ]

        for pool_index, pool in enumerate(config_mixed_entrance_pools):
            self.mixed_entrance_pools[pool_index] = pool

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

    def show_invalid_dialog(self, invalid_text: str):
        invalid_dialog = QMessageBox(self.parent)
        invalid_dialog.setWindowIcon(QIcon(FI_ICON_PATH.as_posix()))
        invalid_dialog.setIconPixmap(QPixmap(FI_ICON_PATH.as_posix()))
        invalid_dialog.setWindowTitle("Invalid Entrance Pool Action")
        invalid_dialog.setText(invalid_text)
        invalid_dialog.exec()
