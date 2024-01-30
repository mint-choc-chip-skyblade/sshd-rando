from typing_extensions import override
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QCheckBox


class RandoTriStateCheckBox(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTristate(True)

    @override
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return

        # Change tristate order
        # Usually: off -> mid -> on
        # Now:     off -> on  -> mid
        if self.checkState() == Qt.CheckState.Checked:
            self.setCheckState(Qt.CheckState.Unchecked)
        elif self.checkState() == Qt.CheckState.PartiallyChecked:
            self.setCheckState(Qt.CheckState.Checked)
        else:
            self.setCheckState(Qt.CheckState.PartiallyChecked)

        return super().mouseReleaseEvent(event)
