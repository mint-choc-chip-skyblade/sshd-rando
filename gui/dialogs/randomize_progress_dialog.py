from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QKeyEvent, QIcon
from PySide6.QtWidgets import QProgressDialog

from filepathconstants import ICON_PATH


class RandomizerProgressDialog(QProgressDialog):
    def __init__(self, parent):
        QProgressDialog.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle("Randomizing...")
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setLabelText("Initializing")
        self.setWindowIcon(QIcon(ICON_PATH.as_posix()))
        self.setCancelButton(None)  # type: ignore
        self.setValue(0)
        self.setMinimumWidth(250)
        self.setVisible(True)
        self.canceled.connect(self.close)

    def keyPressEvent(self, e: QKeyEvent):
        # Prevent the escape key from closing the progress dialog
        if e.key() == Qt.Key.Key_Escape:
            e.ignore()

    def closeEvent(self, e: QCloseEvent):
        # Close the entire program if the progress dialog is closed
        self.parent.close()
