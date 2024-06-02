from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6 import QtCore
from PySide6.QtCore import Signal


class TrackerBackButton(QLabel):

    clicked = Signal()

    def __init__(self, text_: str, parent_) -> None:
        super().__init__(text_, parent_)
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit()
        return super().mouseReleaseEvent(ev)
