from PySide6.QtWidgets import QLabel, QSizePolicy, QToolTip
from PySide6.QtGui import *
from PySide6 import QtCore
from PySide6.QtCore import QEvent, QPoint, Signal


from constants.itemnames import (
    GRATITUDE_CRYSTAL,
    GRATITUDE_CRYSTAL_PACK,
    TRIFORCE_OF_COURAGE,
    TRIFORCE_OF_POWER,
    TRIFORCE_OF_WISDOM,
)
from filepathconstants import TRACKER_ASSETS_PATH
from constants.guiconstants import TRACKER_TOOLTIP_STYLESHEET
from gui.components.outlined_label import OutlinedLabel

from logic.world import World, Counter, Location
from logic.item import Item
import platform

import math


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
        self.minimum_state: int = 0
        self.world: World = None
        self.sphere_tracked_items: dict[Location, str] = {}
        self.inventory: Counter[Item]
        self.allow_sphere_tracking: bool = False
        self.number_label: OutlinedLabel = None
        self.label_offset_x_ratio: float = 0
        self.label_offset_y_ratio: float = 0
        self.label_scale: float = 1.0
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

    def create_number_label(self) -> None:
        self.number_label = OutlinedLabel(self)
        self.number_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.update_number_label_font_size()

    def set_label_offset_ratios(self, x: float, y: float) -> None:
        self.label_offset_x_ratio = x
        self.label_offset_y_ratio = y

    def set_label_scale(self, scale: float) -> None:
        self.label_scale = scale

    def get_number_label_font_size(self) -> float:
        # Keep the font size reasonable. e scales well for whatever reason
        return (min(self.width(), self.height()) // math.e) * self.label_scale

    def update_number_label_font_size(self) -> None:
        if self.number_label is not None:
            pt_size = self.get_number_label_font_size()
            self.number_label.setStyleSheet(f"font-size: {pt_size}pt;")

    def resizeEvent(self, arg__1: QResizeEvent) -> None:
        self.update_number_label_font_size()
        return super().resizeEvent(arg__1)

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

        # Adjust the label if it exists
        if self.number_label is not None:
            # If count is 0, don't display the number
            if self.state == 0:
                self.number_label.setBrush(Qt.transparent)
                self.number_label.setPen(Qt.transparent)
            # If the count is maxed, set the number as green
            elif self.state == len(self.items) - 1:
                self.number_label.setBrush(Qt.green)
                self.number_label.setPen(Qt.black)
            # Otherwise, set it as white
            else:
                self.number_label.setBrush(Qt.white)
                self.number_label.setPen(Qt.black)
            # Set the proper text
            self.number_label.setText(str(self.state))

            # Now we have to do some math to properly center the number regardless of font
            pt_size = self.get_number_label_font_size()
            font = self.number_label.font()
            font.setPointSize(pt_size)
            # This is the *font* width of the characters in the string added together
            number_advance = QFontMetrics(font).horizontalAdvance(str(self.state))
            # This is the *actual* pixel width of the individual number string
            number_width = QFontMetrics(font).boundingRect(str(self.state)).width()
            # Keep the label centered and adjusted by the offset
            x_offset = int(self.label_offset_x_ratio * self.width()) + int(
                self.width() / 2 - (number_advance - number_width / 2)
            )
            y_offset = int(self.label_offset_y_ratio * self.height())
            self.number_label.setGeometry(
                x_offset - 10, 9 + y_offset, number_advance + 20, self.height() - 20
            )

        return super().paintEvent(arg__1)

    def get_current_item(self) -> Item:
        if self.items[self.state] == "Nothing" or self.world is None:
            return None
        return self.world.get_item(self.items[self.state])

    def remove_current_item(self) -> None:
        current_item = self.get_current_item()
        if current_item is not None and self.state - 1 >= self.minimum_state:
            self.inventory[current_item] -= 1
            if self.inventory[current_item] < 0:
                self.inventory[current_item] = 0

    def add_current_item(self) -> None:
        current_item = self.get_current_item()
        if current_item is not None and self.state - 1 >= self.minimum_state:
            self.inventory[current_item] += 1

    def remove_all_items(self) -> None:
        current_state = self.state
        for i in range(self.minimum_state, len(self.items)):
            self.state = i
            self.remove_current_item()
        self.state = current_state

    def add_all_items(self) -> None:
        current_state = self.state
        for i in range(self.minimum_state, len(self.items)):
            self.state = i
            self.add_current_item()
        self.state = current_state

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        should_sphere_track = self.allow_sphere_tracking
        must_be_five_pack = (
            self.world.setting("gratitude_crystal_shuffle") == "off"
            and self.items[-1] == GRATITUDE_CRYSTAL
        )
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            if must_be_five_pack:
                for _ in range(5):
                    original_state = self.state
                    should_sphere_track &= self.increment_item_state()
                    # Stop adding crystals once the count overflows
                    if original_state == len(self.items) - 1:
                        break
            else:
                should_sphere_track &= self.increment_item_state()
        elif ev.button() == QtCore.Qt.MouseButton.RightButton:
            if must_be_five_pack:
                for _ in range(5):
                    should_sphere_track = self.decrement_item_state()
                    # Stop removing crystals once the count is congruent
                    # to the number of tracked loose crystals mod 5
                    # That way, the number of manually tracked crystals
                    # is still divisble by 5, to line up with tracked
                    # crystal packs.
                    if self.state == 76 + (self.minimum_state - 1) % 5:
                        break
            else:
                should_sphere_track = self.decrement_item_state()

        # don't try to sphere-track when removing an item or resetting an item all the way
        if should_sphere_track:
            self.clicked.emit(
                (
                    self.world.get_item(GRATITUDE_CRYSTAL_PACK)
                    if must_be_five_pack
                    else self.get_current_item()
                ),
                (
                    "sidequests/crystal_pack.png"
                    if must_be_five_pack
                    else self.filenames[self.state]
                ),
            )
        else:
            self.clicked.emit(None, None)

        self.update_icon()
        self.update_hover_text()
        return super().mouseReleaseEvent(ev)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        if self.allow_sphere_tracking:
            self.calculate_tooltip()
            coords = self.mapToGlobal(QPoint(-60, self.height() * 3 // 4))
            # For whatever reason, MacOS calculates this position differently,
            # so we must offset the height to compensate
            if platform.system() == "Darwin":
                coords.setY(coords.y() - 18)
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
        matching_item_names = self.items[-1:]
        # Add special cases for Triforces and Gratitude Crystals
        if matching_item_names[0] == TRIFORCE_OF_POWER:
            matching_item_names.extend([TRIFORCE_OF_WISDOM, TRIFORCE_OF_COURAGE])
        elif matching_item_names[0] == GRATITUDE_CRYSTAL:
            matching_item_names.append(GRATITUDE_CRYSTAL_PACK)
        locations = [
            loc
            for loc, item_name in self.sphere_tracked_items.items()
            if item_name in matching_item_names
        ]

        if any(locations):
            self.tooltip = "Locations found at:"
            locations.sort(
                key=lambda loc: loc.sphere if loc.sphere is not None else 1000000
            )
            for loc in locations:
                self.tooltip += (
                    "\n"
                    + f"[{loc.sphere if loc.sphere is not None else '?'}] {'(5 Pack) ' if loc.tracked_item.name == GRATITUDE_CRYSTAL_PACK else ''}{loc.name}"
                )

    # The following functions return whether or not sphere tracking should initiate

    def increment_item_state(self) -> bool:
        first_iteration = True
        should_sphere_track = True
        while first_iteration or self.state < self.minimum_state:
            first_iteration = False
            self.state += 1
            if self.state >= len(self.items):
                self.state = self.minimum_state
                self.remove_all_items()
                should_sphere_track = False
            self.add_current_item()
        # sphere tracking should start only if the user didn't overflow the item counter
        return should_sphere_track

    def decrement_item_state(self) -> bool:
        first_iteration = True
        while first_iteration or self.state < self.minimum_state:
            first_iteration = False
            self.remove_current_item()
            self.state -= 1
            if self.state < self.minimum_state:
                self.state = len(self.items) - 1
                self.add_all_items()
        # sphere tracking shouldn't start when decrementing
        return False
