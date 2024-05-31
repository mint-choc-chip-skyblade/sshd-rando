from PySide6.QtWidgets import QPushButton, QSizePolicy, QToolTip
from PySide6.QtGui import QFontDatabase, QCursor, QMouseEvent
from PySide6 import QtCore
from PySide6.QtCore import Signal, QPoint

from filepathconstants import TRACKER_ASSETS_PATH


class TrackerToggleSTButton(QPushButton):

    left_clicked = Signal()
    right_clicked = Signal()

    def __init__(self, parent_) -> None:
        super().__init__(parent_)
        self.setText("Enable Sphere Tracking")
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.setStyleSheet(
            "QToolTip { color: white; background-color: black; border-image: none; border-color: white; }"
        )
        self.setMouseTracking(True)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        coords = self.mapToGlobal(QPoint(0, 0)) + QPoint(100, self.height() / 4)
        QToolTip.showText(coords, "Right-click for info", self)

        return super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == QtCore.Qt.LeftButton:
            self.left_clicked.emit()
        elif ev.button() == QtCore.Qt.RightButton:
            self.right_clicked.emit()

        return super().mouseReleaseEvent(ev)
