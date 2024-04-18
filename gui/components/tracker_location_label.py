from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6 import QtCore
from PySide6.QtCore import Signal

from logic.location import Location
from logic.search import Search


class TrackerLocationLabel(QLabel):

    default_stylesheet = "border-width: 1px; border-color: gray;"

    def __init__(
        self, location_: Location, search: Search, parent_area_button_
    ) -> None:
        super().__init__()
        self.location = location_
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.setStyleSheet(TrackerLocationLabel.default_stylesheet)
        self.setMargin(10)
        self.setMinimumHeight(30)
        self.setMaximumWidth(273)
        self.setWordWrap(True)
        self.recent_search: Search = search
        self.parent_area_button = parent_area_button_

        if self.location.name.startswith(self.parent_area_button.area):
            self.setText(
                self.location.name.replace(f"{self.parent_area_button.area} - ", "")
            )
        else:
            self.setText(self.location.name)

        self.update_color(search)

    def update_color(self, search: Search) -> None:
        self.recent_search = search
        if self.location.marked:
            self.setStyleSheet(
                f"{TrackerLocationLabel.default_stylesheet} color: gray; text-decoration: line-through;"
            )
        elif self.location in search.visited_locations:
            self.setStyleSheet(
                f"{TrackerLocationLabel.default_stylesheet} color: dodgerblue;"
            )
        else:
            self.setStyleSheet(f"{TrackerLocationLabel.default_stylesheet} color: red;")

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:

        if ev.button() == QtCore.Qt.LeftButton:
            self.location.marked = not self.location.marked
            self.update_color(self.recent_search)
            self.parent_area_button.update(self.recent_search)

        return super().mouseReleaseEvent(ev)
