import platform
from PySide6.QtWidgets import QLabel, QToolTip
from PySide6.QtGui import (
    QCursor,
    QMouseEvent,
    QPaintEvent,
    QPixmap,
    QFontMetrics,
    QPainter,
)
from PySide6 import QtCore
from PySide6.QtCore import Signal, QPoint

from constants.guiconstants import TRACKER_LOCATION_TOOLTIP_STYLESHEET
from constants.itemnames import PROGRESSIVE_SWORD
from logic.location import Location
from logic.search import Search

from filepathconstants import TRACKER_ASSETS_PATH
from logic.tooltips.tooltips import get_tooltip_text


class TrackerLocationLabel(QLabel):

    default_stylesheet = "border-width: 1px; border-color: gray;"
    icon_stylesheet = f"{default_stylesheet} padding-left: PADDINGpx;"
    clicked = Signal(str, Location)

    def __init__(
        self,
        location_: Location,
        search: Search,
        world,
        parent_area_button_,
        allow_sphere_tracking_,
    ) -> None:
        super().__init__()
        self.location = location_
        self.world = world
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.setMargin(10)
        self.setMinimumHeight(30)
        self.setMaximumWidth(273)
        self.setWordWrap(True)
        self.setMouseTracking(True)
        self.recent_search: Search = search
        self.parent_area_button = parent_area_button_
        self.allow_sphere_tracking: bool = allow_sphere_tracking_

        # Chop off the location's area in the name if it's the same
        # as the region it's in
        if self.location.name.startswith(self.parent_area_button.area):
            self.setText(
                (
                    f"[{'?' if self.location.sphere == None else self.location.sphere}] "
                    if self.allow_sphere_tracking
                    else ""
                )
                + self.location.name.replace(f"{self.parent_area_button.area} - ", "")
            )
        elif self.parent_area_button.alias and self.location.name.startswith(
            self.parent_area_button.alias
        ):
            self.setText(
                (
                    f"[{'?' if self.location.sphere == None else self.location.sphere}] "
                    if self.allow_sphere_tracking
                    else ""
                )
                + self.location.name.replace(f"{self.parent_area_button.alias} - ", "")
            )
        else:
            self.setText(
                (
                    f"[{'?' if self.location.sphere == None else self.location.sphere}] "
                    if self.allow_sphere_tracking
                    else ""
                )
                + self.location.name
            )

        # Add padding and crystal/goddess cube/gossip stone icon if necessary
        self.icon_width = QFontMetrics(self.font()).height()
        self.pixmap = QPixmap()
        has_icon = True
        if self.location.has_vanilla_gratitude_crystal():
            self.pixmap.load(
                (TRACKER_ASSETS_PATH / "side_quests" / "crystal.png").as_posix()
            )
        elif self.location.has_vanilla_goddess_cube():
            self.pixmap.load(
                (TRACKER_ASSETS_PATH / "side_quests" / "goddess_cube.png").as_posix()
            )
        elif self.location.is_gossip_stone():
            self.pixmap.load(
                (TRACKER_ASSETS_PATH / "side_quests" / "gossip_stone.png").as_posix()
            )
        elif self.location.has_vanilla_dungeon_key():
            self.pixmap.load(
                (TRACKER_ASSETS_PATH / "dungeons" / "small_key.png").as_posix()
            )
        elif (
            image := self.location.tracked_item_image
        ) is not None and self.allow_sphere_tracking:
            self.pixmap.load((TRACKER_ASSETS_PATH / image).as_posix())
        else:
            has_icon = False
            self.icon_height = self.icon_width
            self.styling = TrackerLocationLabel.default_stylesheet
        if has_icon:
            self.icon_height = (
                self.icon_width * self.pixmap.height() / self.pixmap.width()
            )
            if self.location.tracked_item is not None:
                if self.location.tracked_item.name == PROGRESSIVE_SWORD:
                    # Swords are a bit too tall
                    self.icon_height *= 0.8
            self.styling = TrackerLocationLabel.icon_stylesheet.replace(
                "PADDING", f"{self.icon_width + 2}"
            )

        self.update_color(search)

    def update_color(self, search: Search) -> None:
        self.recent_search = search
        if self.location.marked:
            self.setStyleSheet(
                f"QLabel{{{self.styling} color: gray; text-decoration: line-through;}}"
                + TRACKER_LOCATION_TOOLTIP_STYLESHEET
            )
        elif self.location in search.visited_locations:
            self.setStyleSheet(
                f"QLabel{{{self.styling} color: dodgerblue;}}"
                + TRACKER_LOCATION_TOOLTIP_STYLESHEET
            )
        elif self.location.in_semi_logic:
            self.setStyleSheet(
                f"QLabel{{{self.styling} color: orange;}}"
                + TRACKER_LOCATION_TOOLTIP_STYLESHEET
            )
        else:
            self.setStyleSheet(
                f"QLabel{{{self.styling} color: red;}}"
                + TRACKER_LOCATION_TOOLTIP_STYLESHEET
            )

    def paintEvent(self, arg__1: QPaintEvent) -> None:
        # Draw icon pixmap in the alloted space
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        draw_x = self.margin()
        draw_y = int((self.height() / 2) - (self.icon_height / 2) + 1)

        painter.drawPixmap(
            draw_x, draw_y, self.icon_width, self.icon_height, self.pixmap
        )
        return super().paintEvent(arg__1)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:

        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            self.location.marked = not self.location.marked
            self.update_color(self.recent_search)
            self.clicked.emit(self.parent_area_button.area, self.location)

        return super().mouseReleaseEvent(ev)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        coords = self.mapToGlobal(QPoint(-2, self.height() - 15))
        # For whatever reason, MacOS calculates this position differently,
        # so we must offset the height to compensate
        if platform.system() == "Darwin":
            coords.setY(coords.y() - 18)
        QToolTip.showText(
            coords, get_tooltip_text(self, self.location.computed_requirement), self
        )

        return super().mouseMoveEvent(ev)
