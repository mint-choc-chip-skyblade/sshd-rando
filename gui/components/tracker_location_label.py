from collections import Counter
import platform
from PySide6.QtWidgets import QLabel, QToolTip
from PySide6.QtGui import (
    QCursor,
    QMouseEvent,
    QPaintEvent,
    QPixmap,
    QFontMetrics,
    QPainter,
    QTextDocumentFragment,
)
from PySide6 import QtCore
from PySide6.QtCore import Signal, QPoint

from constants.guiconstants import TRACKER_LOCATION_TOOLTIP_STYLESHEET
from constants.itemnames import PROGRESSIVE_SWORD
from constants.trackerprettyitems import PRETTY_ITEM_NAMES
from logic.item import Item
from logic.location import Location
from logic.requirements import (
    TOD,
    Requirement,
    RequirementType,
    evaluate_requirement_at_time,
)
from logic.search import Search

from filepathconstants import TRACKER_ASSETS_PATH


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
                (TRACKER_ASSETS_PATH / "sidequests" / "crystal.png").as_posix()
            )
        elif self.location.has_vanilla_goddess_cube():
            self.pixmap.load(
                (TRACKER_ASSETS_PATH / "sidequests" / "goddess_cube.png").as_posix()
            )
        elif self.location.is_gossip_stone():
            self.pixmap.load(
                (TRACKER_ASSETS_PATH / "sidequests" / "gossip_stone.png").as_posix()
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
        QToolTip.showText(coords, self.get_tooltip_text(), self)

        return super().mouseMoveEvent(ev)

    def get_tooltip_text(self) -> str:
        req = self.location.computed_requirement
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


def sort_requirement(req: Requirement):
    def by_length(req: Requirement):
        if req.type == RequirementType.AND or req.type == RequirementType.OR:
            return len(req.args)
        return -1

    def by_item(req: Requirement):
        if req.type == RequirementType.ITEM:
            return pretty_name(req.args[0].name, 1)
        elif req.type == RequirementType.COUNT:
            return pretty_name(req.args[1].name, req.args[0])
        return ""

    def sort_key(req: Requirement):
        return (by_length(req), by_item(req))

    if req.type == RequirementType.AND or req.type == RequirementType.OR:
        for expr in req.args:
            sort_requirement(expr)
        req.args.sort(key=sort_key)


def pretty_name(item, count):
    if (pretty_name := PRETTY_ITEM_NAMES.get((item, count), None)) is not None:
        return pretty_name

    if count > 1:
        return f"{item} x {count}"
    else:
        return item
