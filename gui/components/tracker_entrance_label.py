from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6 import QtCore
from PySide6.QtCore import Signal

from logic.entrance import Entrance
from logic.search import Search
from logic.requirements import *


class TrackerEntranceLabel(QLabel):

    default_stylesheet = "border-width: 1px; border-color: gray; color: COLOR;"
    choose_target = Signal(Entrance, str)
    disconnect_entrance = Signal(Entrance, str)

    def __init__(
        self,
        entrance_: Entrance,
        parent_area_name_: str,
        recent_search_: Search,
        show_full_connection_: bool,
    ) -> None:
        super().__init__()
        self.entrance = entrance_
        self.parent_area_name = parent_area_name_
        self.recent_search = recent_search_
        self.show_full_connection = show_full_connection_
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.setMargin(10)
        self.setMinimumHeight(30)
        self.setMaximumWidth(273)
        self.setWordWrap(True)
        self.update_text()

    def update_text(self, recent_search_: Search | None = None) -> None:
        if recent_search_ is not None:
            self.recent_search = recent_search_
        connected_area = self.entrance.connected_area
        original_parent, original_connected = self.entrance.original_name.split(" -> ")
        first_part = (
            f"{original_parent} to "
            if self.entrance.parent_area.hard_assigned_region != self.parent_area_name
            or self.show_full_connection
            else ""
        )
        self.setText(
            f"{first_part}{original_connected} -> {connected_area.name if connected_area else '?'}"
        )

        # Set the color as blue if accessible, or red if not
        color = "red"
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
                    color = "dodgerblue"

        self.setStyleSheet(
            TrackerEntranceLabel.default_stylesheet.replace("COLOR", color)
        )

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            self.choose_target.emit(self.entrance, self.parent_area_name)
        elif ev.button() == QtCore.Qt.MouseButton.RightButton:
            self.disconnect_entrance.emit(self.entrance, self.parent_area_name)
            self.update_text()
        return super().mouseReleaseEvent(ev)
