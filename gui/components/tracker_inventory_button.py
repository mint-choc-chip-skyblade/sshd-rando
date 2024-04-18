from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QCursor, QMouseEvent, QImageReader
from PySide6 import QtCore
from PySide6.QtCore import Signal

from pathlib import Path
from typing import TYPE_CHECKING

from filepathconstants import TRACKER_ASSETS_PATH

from logic.world import World, Counter
from logic.item import Item


class TrackerInventoryButton(QLabel):

    clicked = Signal()

    def __init__(
        self, items_: list[str] = [], filenames_: list[Path] = [], parent_=None
    ) -> None:
        super().__init__(parent=parent_)
        self.items: list[str] = items_
        self.filenames: list[str] = filenames_
        self.forbidden_states: set[int] = set()
        self.world: World = None
        self.inventory: Counter[Item]
        assert len(self.items) == len(self.filenames)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.max_width = 0
        self.max_height = 0
        for filename in self.filenames:
            image = QImageReader(f"{(TRACKER_ASSETS_PATH / filename).as_posix()}")
            image = image.read()
            width = image.rect().width()
            height = image.rect().height()
            if height > self.max_height:
                self.max_height = height
            if width > self.max_width:
                self.max_width = width

        self.setMinimumHeight(self.max_height)
        self.setMinimumWidth(self.max_width)

        self.state: int = 0
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.update_icon()

    def update_icon(self) -> None:
        if self.state >= len(self.filenames):
            print(f"Out of range for {self.items[-1]} {self.state}")
            self.state = len(self.filenames) - 1

        self.setStyleSheet(
            f'background-image: url("{(TRACKER_ASSETS_PATH / self.filenames[self.state]).as_posix()}");'
            + "background-repeat: none;"
            + "background-position: center;"
            + "background-color: rgba(0, 0, 0, 0);"
        )

    def get_current_item(self) -> Item:
        if self.items[self.state] == "Nothing" or self.world is None:
            return None
        return self.world.get_item(self.items[self.state])

    def remove_current_item(self) -> None:
        current_item = self.get_current_item()
        if current_item is not None and self.state - 1 not in self.forbidden_states:
            self.inventory[current_item] -= 1
            if self.inventory[current_item] < 0:
                self.inventory[current_item] = 0

    def add_current_item(self) -> None:
        current_item = self.get_current_item()
        if current_item is not None and self.state - 1 not in self.forbidden_states:
            self.inventory[current_item] += 1

    def remove_all_items(self) -> None:
        current_state = self.state
        for i in range(len(self.items)):

            if i - 1 in self.forbidden_states:
                continue

            self.state = i
            self.remove_current_item()
        self.state = current_state

    def add_all_items(self) -> None:
        current_state = self.state
        for i in range(len(self.items)):

            if i - 1 in self.forbidden_states:
                continue

            self.state = i
            self.add_current_item()
        self.state = current_state

    def add_forbidden_state(self, state: int) -> None:
        self.forbidden_states.add(state)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == QtCore.Qt.LeftButton:
            first_iteration = True
            while first_iteration or self.state in self.forbidden_states:
                first_iteration = False
                self.state += 1
                if self.state >= len(self.items):
                    self.state = 0
                    self.remove_all_items()
                self.add_current_item()
        elif ev.button() == QtCore.Qt.RightButton:
            first_iteration = True
            while first_iteration or self.state in self.forbidden_states:
                first_iteration = False
                self.remove_current_item()
                self.state -= 1
                if self.state < 0:
                    self.state = len(self.items) - 1
                    self.add_all_items()

        self.update_icon()
        self.clicked.emit()
        return super().mouseReleaseEvent(ev)
