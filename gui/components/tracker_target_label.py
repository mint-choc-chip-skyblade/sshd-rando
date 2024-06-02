from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6 import QtCore
from PySide6.QtCore import Signal

from logic.entrance import Entrance


class TrackerTargetLabel(QLabel):

    default_stylesheet = "border-width: 1px; border-color: gray; color: dodgerblue"
    clicked = Signal(Entrance, Entrance, str)

    def __init__(
        self, entrance_: Entrance, target_: Entrance, parent_area_name_: str
    ) -> None:
        super().__init__()
        self.entrance = entrance_
        self.target = target_
        self.parent_area_name = parent_area_name_
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet(TrackerTargetLabel.default_stylesheet)
        self.setMargin(10)
        self.setMinimumHeight(30)
        self.setMaximumWidth(273)
        self.setWordWrap(True)

        self.setText(self.target.replaces.original_name.split(" -> ")[1])

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit(self.entrance, self.target, self.parent_area_name)
        return super().mouseReleaseEvent(ev)
