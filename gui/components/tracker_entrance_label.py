import platform
from PySide6.QtWidgets import QLabel, QToolTip
from PySide6.QtGui import QCursor, QMouseEvent, QFontMetrics, QTextDocumentFragment
from PySide6 import QtCore
from PySide6.QtCore import Signal, QPoint

from logic.entrance import Entrance
from logic.search import Search
from logic.requirements import *

from constants.guiconstants import TRACKER_LOCATION_TOOLTIP_STYLESHEET
from logic.tooltips.tooltips import pretty_name, sort_requirement


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

        self.update_color(recent_search_)

    def update_color(self, recent_search_: Search | None = None) -> None:
        if recent_search_ is not None:
            self.recent_search = recent_search_
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
        QToolTip.showText(coords, self.get_tooltip_text(), self)

        return super().mouseMoveEvent(ev)

    def get_tooltip_text(self) -> str:
        req = self.entrance.computed_requirement
        sort_requirement(req)
        match req.type:
            case RequirementType.AND:
                # Computed requirements have a top-level AND requirement
                # We display them as a list of bullet points to the user
                # This fetches a list of the terms ANDed together
                text = [self.format_requirement(a) for a in req.args]
            case _:
                # The requirement is just one term, so format the requirement
                text = [self.format_requirement(req)]

        tooltip_font_metrics = QFontMetrics(QToolTip.font())
        # Find the width of the longest requirement description, adding a 16px buffer for the bullet point
        max_line_width = (
            max(
                [
                    tooltip_font_metrics.horizontalAdvance(
                        QTextDocumentFragment.fromHtml(line).toPlainText()
                    )
                    for line in text + ["Item Requirements:"]
                ]
            )
            + 16
        )
        # Set the tooltip's min and max width to ensure the tooltip is the right size and line-breaks properly
        self.setStyleSheet(
            self.styleSheet()
            .replace("MINWIDTH", str(min(max_line_width, self.width() - 3)))
            .replace("MAXWIDTH", str(self.width() - 3))
        )
        return (
            "Item Requirements:"
            + '<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 8px; margin-right: 0px; -qt-list-indent:0;"><li>'
            + "</li><li>".join(text)
            + "</li></ul>"
        )

    def format_requirement(self, req: Requirement, is_top_level=True) -> str:
        match req.type:
            case RequirementType.IMPOSSIBLE:
                return '<span style="color:red">Impossible (please discover an entrance first)</span>'
            case RequirementType.NOTHING:
                return '<span style="color:dodgerblue">Nothing</span>'
            case RequirementType.ITEM:
                # Determine if the user has marked this item
                color = (
                    "dodgerblue"
                    if evaluate_requirement_at_time(
                        req, self.recent_search, TOD.ALL, self.world
                    )
                    else "red"
                )
                # Get a pretty name for the item if it is the first stage of a progressive item
                name = pretty_name(req.args[0].name, 1)
                return f'<span style="color:{color}">{name}</span>'
            case RequirementType.COUNT:
                # Determine if the user has enough of this item marked
                color = (
                    "dodgerblue"
                    if evaluate_requirement_at_time(
                        req, self.recent_search, TOD.ALL, self.world
                    )
                    else "red"
                )
                # Get a pretty name for the progressive item
                name = pretty_name(req.args[1].name, req.args[0])
                return f'<span style="color:{color}">{name}</span>'
            case RequirementType.WALLET_CAPACITY:
                # Determine if the user has enough wallet capacity for this requirement
                color = (
                    "dodgerblue"
                    if evaluate_requirement_at_time(
                        req, self.recent_search, TOD.ALL, self.world
                    )
                    else "red"
                )
                # TODO: Properly expand into wallet combinations
                return f'<span style="color:{color}">Wallet >= {req.args[0]}</span>'
            case RequirementType.GRATITUDE_CRYSTALS:
                # Determine if the user has enough gratitude crystals marked
                color = (
                    "dodgerblue"
                    if evaluate_requirement_at_time(
                        req, self.recent_search, TOD.ALL, self.world
                    )
                    else "red"
                )
                return f'<span style="color:{color}">{req.args[0]} Gratitude Crystals</span>'
            case RequirementType.OR:
                # Recursively join requirements with "or"
                # Only include parentheses if not at the top level (where they'd be redundant)
                return (
                    ("" if is_top_level else "(")
                    + " or ".join([self.format_requirement(a, False) for a in req.args])
                    + ("" if is_top_level else ")")
                )
            case RequirementType.AND:
                # Recursively join requirements with "and"
                # Only include parentheses if not at the top level (where they'd be redundant)
                return (
                    ("" if is_top_level else "(")
                    + " and ".join(
                        [self.format_requirement(a, False) for a in req.args]
                    )
                    + ("" if is_top_level else ")")
                )
            case _:
                raise ValueError("unreachable")
