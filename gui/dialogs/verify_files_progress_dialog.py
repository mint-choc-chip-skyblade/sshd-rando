from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QProgressDialog

from filepathconstants import ICON_PATH


class VerifyFilesProgressDialog(QProgressDialog):
    def __init__(self, parent):
        QProgressDialog.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle("Verifying Files...")
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setLabelText("Initializing...")
        self.setWindowIcon(QIcon(ICON_PATH.as_posix()))
        self.setCancelButton(None)  # type: ignore
        self.setValue(0)
        self.setMinimumWidth(500)
        self.setAutoClose(False)
        self.setVisible(True)

    def exec(self):
        QProgressDialog.exec(self)

    def setValue(self, value: int):
        super().setValue(value)

        if value == 100:
            self.setLabelText("Verification complete!")
            print("Verification complete!")
