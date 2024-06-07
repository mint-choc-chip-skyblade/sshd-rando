from PySide6.QtWidgets import QLabel, QSizePolicy, QToolTip
from PySide6.QtGui import (
    QCursor,
    QMouseEvent,
    QPaintEvent,
    QPainter,
    QPixmap,
)
from PySide6 import QtCore
from PySide6.QtCore import QEvent, QPoint, Signal


from filepathconstants import TRACKER_ASSETS_PATH
from constants.guiconstants import TRACKER_TOOLTIP_STYLESHEET

from logic.world import World, Counter, Location
from logic.item import Item


class TrackerInventoryButton(QLabel):

    clicked = Signal(Item, str)
    mouse_hover = Signal(str)

    def __init__(
        self,
        items_: list[str] = [],
        filenames_: list[str] = [],
        parent_=None,
        item_names_: list[str] = [],
    ) -> None:
        super().__init__(parent=parent_)
        self.items: list[str] = items_
        self.filenames: list[str] = filenames_
        self.item_names: list[str] = item_names_
        self.forbidden_states: set[int] = set()
        self.world: World = None
        self.sphere_tracked_items: dict[Location, str] = {}
        self.inventory: Counter[Item]
        self.allow_sphere_tracking: bool = False
        assert len(self.items) == len(self.filenames)

        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )

        self.setMinimumHeight(10)
        self.setMinimumWidth(10)

        self.state: int = 0
        self.pixmap = QPixmap()
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet(
            "QLabel {background-color: rgba(0, 0, 0, 0);}" + TRACKER_TOOLTIP_STYLESHEET
        )
        self.update_icon()
        self.setMouseTracking(True)
        self.tooltip = ""
        self.installEventFilter(self)

    def update_icon(self) -> None:
        if self.state >= len(self.filenames):
            print(f"Out of range for {self.items[-1]} {self.state}")
            self.state = len(self.filenames) - 1

        if not self.pixmap.load(
            f"{(TRACKER_ASSETS_PATH / self.filenames[self.state]).as_posix()}"
        ):
            print(f"Could not load pixmap for {self.items[-1]}")
            print(
                f"File: {(TRACKER_ASSETS_PATH / self.filenames[self.state]).as_posix()}"
            )

        self.update()  # Calls paintEvent

    def paintEvent(self, arg__1: QPaintEvent) -> None:

        # Paint the appropriate image scaled to fit inside
        # of the widget
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        pixmap_ratio = self.pixmap.width() / self.pixmap.height()
        widget_ratio = self.width() / self.height()

        if pixmap_ratio < widget_ratio:
            new_width = int(self.height() * pixmap_ratio)
            offset = int((new_width - self.width()) / -2)
            painter.drawPixmap(offset, 0, new_width, self.height(), self.pixmap)
        else:
            new_height = int(self.width() / pixmap_ratio)
            offset = int((new_height - self.height()) / -2)
            painter.drawPixmap(0, offset, self.width(), new_height, self.pixmap)

        return super().paintEvent(arg__1)

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
        should_sphere_track = self.allow_sphere_tracking
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            first_iteration = True
            while first_iteration or self.state in self.forbidden_states:
                first_iteration = False
                self.state += 1
                if self.state >= len(self.items):
                    self.state = 0
                    self.remove_all_items()
                    should_sphere_track = False
                self.add_current_item()
        elif ev.button() == QtCore.Qt.MouseButton.RightButton:
            should_sphere_track = False
            first_iteration = True
            while first_iteration or self.state in self.forbidden_states:
                first_iteration = False
                self.remove_current_item()
                self.state -= 1
                if self.state < 0:
                    self.state = len(self.items) - 1
                    self.add_all_items()

        # don't try to sphere-track when removing an item or resetting an item all the way
        if should_sphere_track:
            self.clicked.emit(self.get_current_item(), self.filenames[self.state])
        else:
            self.clicked.emit(None, None)

        self.update_icon()
        self.update_hover_text()
        return super().mouseReleaseEvent(ev)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        if self.allow_sphere_tracking:
            self.calculate_tooltip()
            coords = self.mapToGlobal(QPoint(0, 0)) + QPoint(
                -60, int(self.height() * 3 / 4)
            )
            QToolTip.showText(coords, self.tooltip, self)

        self.update_hover_text()

        return super().mouseMoveEvent(ev)

    def update_hover_text(self) -> None:
        if any(self.item_names):
            self.mouse_hover.emit(f"{self.item_names[self.state]}")
        else:
            self.mouse_hover.emit(f"{self.items[-1]}")

    def eventFilter(self, target: QLabel, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Leave:
            self.mouse_hover.emit("")

        return super().eventFilter(target, event)

    def calculate_tooltip(self) -> None:
        self.tooltip = ""
        locations = [
            loc
            for loc, item_name in self.sphere_tracked_items.items()
            if item_name in self.items[1:]
        ]

        if any(locations):
            self.tooltip = "Locations found at:"
            locations.sort(
                key=lambda loc: loc.sphere if loc.sphere is not None else 1000000
            )
            for loc in locations:
                self.tooltip += (
                    "\n"
                    + f"[{loc.sphere if loc.sphere is not None else '?'}] {loc.name}"
                )
