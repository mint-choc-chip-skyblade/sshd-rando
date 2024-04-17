from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QFontDatabase, QCursor, QMouseEvent
from PySide6 import QtCore
from PySide6.QtCore import Signal

from filepathconstants import TRACKER_ASSETS_PATH

class TrackerDungeonLabel(QLabel):

    hylia_font_id: int = -1
    default_style = f"color: COLOR; font-size: 30pt; font-family: Hylia Serif Beta; text-align: center; qproperty-alignment: {int(QtCore.Qt.AlignCenter)};"

    clicked = Signal(str)

    def __init__(self, abbreviation: str) -> None:

        if TrackerDungeonLabel.hylia_font_id == -1:
            TrackerDungeonLabel.hylia_font_id = QFontDatabase.addApplicationFont((TRACKER_ASSETS_PATH / "HyliaSerifBeta-Regular.otf").as_posix())
            if TrackerDungeonLabel.hylia_font_id == -1:
                print("Could not load Hylia Serif Font")

        super().__init__()
        self.setText(abbreviation)
        self.setStyleSheet(TrackerDungeonLabel.default_style)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.active: bool = False
        self.setStyleSheet(TrackerDungeonLabel.default_style.replace("COLOR", "gray"))

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if ev.button() in [QtCore.Qt.LeftButton, QtCore.Qt.RightButton]:
            if self.active:
                self.setStyleSheet(TrackerDungeonLabel.default_style.replace("COLOR", "gray"))
            else:
                self.setStyleSheet(TrackerDungeonLabel.default_style.replace("COLOR", "blue"))
            self.active = not self.active
            self.clicked.emit(self.text())
        return super().mouseReleaseEvent(ev)