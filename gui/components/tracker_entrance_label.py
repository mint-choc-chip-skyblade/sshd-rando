import platform
from PySide6.QtWidgets import QLabel, QToolTip
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6 import QtCore
from PySide6.QtCore import Signal, QPoint

from logic.entrance import Entrance
from logic.search import Search
from logic.requirements import *

from constants.guiconstants import TRACKER_LOCATION_TOOLTIP_STYLESHEET
from .tooltip_formatting import get_tooltip_text


class TrackerEntranceLabel(QLabel):

    default_stylesheet = (
        "QLabel { border-width: 1px; border-color: gray; color: COLOR; }"
    )
    choose_target = Signal(Entrance, str)
    disconnect_entrance = Signal(Entrance, str)

    def __init__(
        self,
        entrance_: Entrance,
        parent_area_name_: str,
        recent_search_: Search,
        world_,
        show_full_connection_: bool,
    ) -> None:
        super().__init__()
        self.entrance = entrance_
        self.parent_area_name = parent_area_name_
        self.recent_search = recent_search_
        self.world = world_
        self.show_full_connection = show_full_connection_
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.setMargin(10)
        self.setMinimumHeight(30)
        self.setMaximumWidth(273)
        self.setWordWrap(True)
        self.setMouseTracking(True)
        self.update_text()

    def entrance_is_accessible(self) -> bool:
        if (
            self.recent_search is not None
            and self.entrance.parent_area in self.recent_search.visited_areas
        ):
            for tod in ALL_TODS:
                if evaluate_requirement_at_time(
                    self.entrance.requirement,
                    self.recent_search,
                    tod,
                    self.entrance.world,
                ):
                    return True
        return False

    def update_text(self, recent_search_: Search | None = None) -> None:
        if recent_search_ is not None:
            self.recent_search = recent_search_

        # Take the name of the connected area to start (or just "?" if it isn't connected)
        connected_area_name = "?"
        # If this entrance has a replacement, then use the second part of the replacement's
        # original name (this takes into account undecoupled double door names)
        if self.entrance.replaces:
            connected_area_name = self.entrance.replaces.alias.split(" -> ")[1]

        original_parent, original_connected = self.entrance.alias.split(" -> ")
        first_part = (
            f"{original_parent} to "
            if self.parent_area_name
            not in (
                self.entrance.parent_area.hard_assigned_region,
                self.entrance.alias_parent_area(),
            )
            or self.show_full_connection
            else ""
        )
        self.setText(f"{first_part}{original_connected} -> {connected_area_name}")

        self.update_color(recent_search_)

    def update_color(self, recent_search_: Search | None = None) -> None:
        if recent_search_ is not None:
            self.recent_search = recent_search_
        # Set the color as blue if accessible, or red if not
        color = "red"
        if self.entrance_is_accessible():
            color = "dodgerblue"

        self.setStyleSheet(
            TrackerEntranceLabel.default_stylesheet.replace("COLOR", color)
            + TRACKER_LOCATION_TOOLTIP_STYLESHEET
        )

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            self.choose_target.emit(self.entrance, self.parent_area_name)
        elif ev.button() == QtCore.Qt.MouseButton.RightButton:
            self.disconnect_entrance.emit(self.entrance, self.parent_area_name)
            self.update_text()
        return super().mouseReleaseEvent(ev)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        coords = self.mapToGlobal(QPoint(-2, self.height() - 15))
        # For whatever reason, MacOS calculates this position differently,
        # so we must offset the height to compensate
        if platform.system() == "Darwin":
            coords.setY(coords.y() - 18)
        QToolTip.showText(
            coords, get_tooltip_text(self, self.entrance.computed_requirement), self
        )

        return super().mouseMoveEvent(ev)
