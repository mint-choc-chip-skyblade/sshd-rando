from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMessageBox

from filepathconstants import FI_ICON_PATH


class FiInfoDialog:
    def __init__(self, parent):
        self.parent = parent

    def show_dialog(self, title: str, text: str):
        dialog = QMessageBox(self.parent)
        dialog.setTextFormat(Qt.TextFormat.RichText)
        dialog.setWindowIcon(QIcon(FI_ICON_PATH.as_posix()))
        dialog.setIconPixmap(QPixmap(FI_ICON_PATH.as_posix()))
        dialog.setWindowTitle(title)
        dialog.setText(text)
        dialog.exec()
