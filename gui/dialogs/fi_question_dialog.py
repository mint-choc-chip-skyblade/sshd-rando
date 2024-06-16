from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMessageBox

from filepathconstants import FI_ICON_PATH


class FiQuestionDialog:
    def __init__(self, parent):
        self.parent = parent

    def show_dialog(self, title: str, text: str, yes_text: str = "", no_text: str = ""):
        dialog = QMessageBox(self.parent)
        dialog.setTextFormat(Qt.TextFormat.RichText)
        dialog.setWindowIcon(QIcon(FI_ICON_PATH.as_posix()))
        dialog.setIconPixmap(QPixmap(FI_ICON_PATH.as_posix()))
        dialog.setWindowTitle(title)
        dialog.setText(text)

        self.dialog_yes_button = dialog.addButton(QMessageBox.StandardButton.Yes)
        self.dialog_no_button = dialog.addButton(QMessageBox.StandardButton.No)

        if yes_text:
            self.dialog_yes_button.setText(yes_text)
        if no_text:
            self.dialog_no_button.setText(no_text)

        return dialog.exec()
