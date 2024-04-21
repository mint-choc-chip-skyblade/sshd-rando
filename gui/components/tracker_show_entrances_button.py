from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal


class TrackerShowEntrancesButton(QPushButton):

    show_area_entrances = Signal(str)

    def __init__(self, area_name_: str, label_text: str = "Show Entrances"):
        super().__init__()
        self.area_name = area_name_
        self.setText(label_text)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        self.show_area_entrances.emit(self.area_name)
        return super().mouseReleaseEvent(e)
