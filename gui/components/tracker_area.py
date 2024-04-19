from PySide6.QtWidgets import QLabel, QSizePolicy, QToolTip
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6 import QtCore
from PySide6.QtCore import Signal, QPoint

from logic.search import Search
from logic.location import Location


class TrackerArea(QLabel):

    show_locations = Signal(str)
    change_map_area = Signal(str)

    default_stylesheet = f"background-color: COLOR; border-image: none; border-color: black; border-radius: RADIUSpx; color: black; qproperty-alignment: {int(QtCore.Qt.AlignCenter)};"

    def __init__(
        self,
        area_: str = "",
        image_filename_: str = "",
        children_: list[str] = [],
        x_: int = -1,
        y_: int = -1,
        parent_=None,
        border_radius_="6",
        alias_: str = "",
    ):
        super().__init__(parent=parent_)
        self.area = area_
        self.image_filename = image_filename_
        self.tracker_children: list["TrackerArea"] = children_
        self.tracker_x = x_
        self.tracker_y = y_
        self.area_parent: "TrackerArea" = None
        self.locations: list = []
        self.recent_search: Search = None
        self.border_radius = border_radius_
        self.alias = alias_

        self.setStyleSheet(
            TrackerArea.default_stylesheet.replace("COLOR", "gray").replace(
                "RADIUS", self.border_radius
            )
        )
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.setFixedSize(30, 30)
        self.move(self.tracker_x, self.tracker_y)
        self.setVisible(False)
        self.tooltip = f"{self.area} (0/0)"
        self.setMouseTracking(True)

    # Recursively iterate through all this area's locations and children and return all locations
    def get_all_locations(self) -> list[Location]:
        all_locations = list(self.locations)
        locations_set = set(self.locations)
        for child in self.tracker_children:
            for loc in child.get_all_locations():
                if loc not in locations_set:
                    all_locations.append(loc)
                    locations_set.add(loc)
        return all_locations

    def get_included_locations(self) -> list[Location]:
        return [
            loc
            for loc in self.get_all_locations()
            if loc.progression and loc.eud_progression
            # should probably be a special location type eventually
            and "Goddess Cube" not in loc.types
        ]

    def get_unmarked_locations(self) -> list[Location]:
        return [loc for loc in self.get_included_locations() if not loc.marked]

    def get_available_locations(self) -> list[Location]:
        return [
            loc
            for loc in self.get_unmarked_locations()
            if loc in self.recent_search.visited_locations
        ]

    def update(self, search: "Search" = None) -> None:
        if search is not None:
            self.recent_search = search

        # Don't bother trying to update areas with no locations
        if (
            len(self.locations) + len(self.tracker_children) == 0
            or self.recent_search is None
        ):
            return

        all_unmarked_locations = self.get_unmarked_locations()
        # If we don't have any possible locations at all then change to gray
        if not all_unmarked_locations:
            self.setStyleSheet(
                TrackerArea.default_stylesheet.replace("COLOR", "gray").replace(
                    "RADIUS", self.border_radius
                )
            )
            self.setText("")
            self.tooltip = f"{self.area} (0/0)"
            return

        num_available_locations = len(self.get_available_locations())
        if num_available_locations == 0:
            self.setStyleSheet(
                TrackerArea.default_stylesheet.replace("COLOR", "red").replace(
                    "RADIUS", self.border_radius
                )
            )
            self.setText("")
        elif num_available_locations == len(all_unmarked_locations):
            self.setStyleSheet(
                TrackerArea.default_stylesheet.replace("COLOR", "dodgerblue").replace(
                    "RADIUS", self.border_radius
                )
            )
            self.setText(str(num_available_locations))
        else:
            self.setStyleSheet(
                TrackerArea.default_stylesheet.replace("COLOR", "orange").replace(
                    "RADIUS", self.border_radius
                )
            )
            self.setText(str(num_available_locations))

        self.tooltip = (
            f"{self.area} ({num_available_locations}/{len(all_unmarked_locations)})"
        )

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:

        if ev.button() == QtCore.Qt.LeftButton:
            if self.image_filename != "":
                self.change_map_area.emit(self.area)
            else:
                self.show_locations.emit(self.area)

        return super().mouseReleaseEvent(ev)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:

        QToolTip.showText(QCursor.pos() + QPoint(-15, 50), self.tooltip, self)

        return super().mouseMoveEvent(ev)
