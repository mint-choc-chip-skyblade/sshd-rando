from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QCursor, QMouseEvent, QPaintEvent, QPixmap, QFontMetrics, QPainter
from PySide6 import QtCore
from PySide6.QtCore import Signal

from logic.location import Location
from logic.search import Search

from filepathconstants import TRACKER_ASSETS_PATH
from constants.itemconstants import GRATITUDE_CRYSTAL

class TrackerLocationLabel(QLabel):

    default_stylesheet = "border-width: 1px; border-color: gray;"
    icon_stylesheet = f"{default_stylesheet} padding-left: PADDINGpx;"
    clicked = Signal(str)

    def __init__(
        self, location_: Location, search: Search, parent_area_button_
    ) -> None:
        super().__init__()
        self.location = location_
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.setMargin(10)
        self.setMinimumHeight(30)
        self.setMaximumWidth(273)
        self.setWordWrap(True)
        self.recent_search: Search = search
        self.parent_area_button = parent_area_button_

        # Chop off the location's area in the name if it's the same
        # as the region it's in
        if self.location.name.startswith(self.parent_area_button.area):
            self.setText(
                self.location.name.replace(f"{self.parent_area_button.area} - ", "")
            )
        elif self.parent_area_button.alias and self.location.name.startswith(
            self.parent_area_button.alias
        ):
            self.setText(
                self.location.name.replace(f"{self.parent_area_button.alias} - ", "")
            )
        else:
            self.setText(self.location.name)

        # Add padding and crystal/goddess cube/gossip stone icon if necessary
        self.icon_size = QFontMetrics(self.font()).height()
        self.pixmap = QPixmap()
        self.styling = TrackerLocationLabel.icon_stylesheet.replace("PADDING", f"{self.icon_size + 2}")
        if self.location.has_vanilla_gratitude_crystal():
            self.pixmap.load((TRACKER_ASSETS_PATH / "sidequests" / "crystal.png").as_posix())
        elif self.location.has_vanilla_goddess_cube():
            self.pixmap.load((TRACKER_ASSETS_PATH / "sidequests" / "goddess_cube.png").as_posix())
        elif self.location.is_gossip_stone():
            self.pixmap.load((TRACKER_ASSETS_PATH / "sidequests" / "gossip_stone.png").as_posix())
        elif self.location.has_vanilla_dungeon_key():
            self.pixmap.load((TRACKER_ASSETS_PATH / "dungeons" / "small_key.png").as_posix())
        else:
            self.styling = TrackerLocationLabel.default_stylesheet

        self.update_color(search)

    def update_color(self, search: Search) -> None:
        self.recent_search = search
        if self.location.marked:
            self.setStyleSheet(
                f"{self.styling} color: gray; text-decoration: line-through;"
            )
        elif self.location in search.visited_locations:
            self.setStyleSheet(f"{self.styling} color: dodgerblue;")
        elif self.location.in_semi_logic:
            self.setStyleSheet(f"{self.styling} color: orange;")
        else:
            self.setStyleSheet(f"{self.styling} color: red;")

    def paintEvent(self, arg__1: QPaintEvent) -> None:
        # Draw icon pixmap in the alloted space
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        draw_x = self.margin()
        draw_y = (self.height() / 2) - (self.icon_size / 2) + 1

        painter.drawPixmap(draw_x, draw_y, self.icon_size, self.icon_size, self.pixmap)
        return super().paintEvent(arg__1)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:

        if ev.button() == QtCore.Qt.LeftButton:
            self.location.marked = not self.location.marked
            self.update_color(self.recent_search)
            self.clicked.emit(self.parent_area_button.area)

        return super().mouseReleaseEvent(ev)
