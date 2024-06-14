from PySide6.QtWidgets import QPushButton, QToolTip
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6 import QtCore
from PySide6.QtCore import Signal, QPoint
from constants.guiconstants import TRACKER_TOOLTIP_STYLESHEET
import platform


class TrackerToggleSTButton(QPushButton):

    left_clicked = Signal()
    right_clicked = Signal()

    def __init__(self, parent_) -> None:
        super().__init__(parent_)
        self.setText("Enable Sphere Tracking")
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.setMouseTracking(True)
        self.setStyleSheet(TRACKER_TOOLTIP_STYLESHEET)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        coords = self.mapToGlobal(QPoint(100, self.height() // 2))
        # For whatever reason, MacOS calculates this position differently,
        # so we must offset the height to compensate
        if platform.system() == "Darwin":
            coords.setY(coords.y() - 18)
        QToolTip.showText(coords, "Right-click for info", self)

        return super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            self.left_clicked.emit()
        elif ev.button() == QtCore.Qt.MouseButton.RightButton:
            self.right_clicked.emit()

        return super().mouseReleaseEvent(ev)
