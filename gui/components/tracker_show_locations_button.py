from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal


class TrackerShowLocationsButton(QPushButton):

    show_area_locations = Signal(str)

    def __init__(self, area_name_: str):
        super().__init__()
        self.area_name = area_name_
        self.setText("Show Locations")

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        self.show_area_locations.emit(self.area_name)
        return super().mouseReleaseEvent(e)
