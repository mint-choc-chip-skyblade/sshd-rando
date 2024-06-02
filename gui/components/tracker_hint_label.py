from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6 import QtCore
from PySide6.QtCore import Signal

from gui.components.tracker_area import TrackerArea


class TrackerHintLabel(QLabel):

    default_stylesheet = "border-width: 1px; border-color: gray; color: dodgerblue"
    clicked = Signal(str, TrackerArea)

    def __init__(self, hint_: str, area_: TrackerArea) -> None:
        super().__init__()
        self.hint = hint_
        self.area = area_
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet(TrackerHintLabel.default_stylesheet)
        self.setMargin(10)
        self.setMinimumHeight(30)
        self.setMaximumWidth(273)
        self.setWordWrap(True)

        self.setText(self.hint)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit(self.hint, self.area)
        return super().mouseReleaseEvent(ev)
