from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QCloseEvent, QDesktopServices, QKeyEvent, QIcon, QPixmap
from PySide6.QtWidgets import QMessageBox, QProgressDialog

from filepathconstants import ICON_PATH

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import Main


class RandomizerProgressDialog(QProgressDialog):
    def __init__(self, main: "Main"):
        QProgressDialog.__init__(self, main)
        self.main = main
        self.setWindowTitle("Randomizing...")
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setLabelText("Initializing")
        self.setWindowIcon(QIcon(ICON_PATH.as_posix()))
        self.setCancelButton(None)  # type: ignore
        self.setValue(0)
        self.setMinimumWidth(250)
        self.setVisible(True)
        self.canceled.connect(self.close)

        self.should_show_done = True

    def exec(self):
        QProgressDialog.exec(self)

        if self.should_show_done:
            done_dialog = QMessageBox(self)
            done_dialog.setWindowTitle("Randomization Completed")
            done_dialog.setText("Seed successfully generated!")

            open_output_button = done_dialog.addButton(
                "Open Output Folder", QMessageBox.ButtonRole.NoRole
            )
            open_output_button.clicked.connect(self.open_output_folder)

            done_dialog.addButton("OK", QMessageBox.ButtonRole.NoRole)

            done_dialog.setWindowIcon(QIcon(ICON_PATH.as_posix()))
            icon_pixmap = QPixmap(ICON_PATH.as_posix()).scaled(
                QSize(80, 80),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            done_dialog.setIconPixmap(icon_pixmap)
            done_dialog.exec()

    def open_output_folder(self):
        QDesktopServices.openUrl(
            QUrl(self.main.config.output_dir.as_posix(), QUrl.ParsingMode.TolerantMode)
        )

    def keyPressEvent(self, e: QKeyEvent):
        # Prevent the escape key from closing the progress dialog
        if e.key() == Qt.Key.Key_Escape:
            e.ignore()

    def closeEvent(self, e: QCloseEvent):
        self.should_show_done = False
        # Close the entire program if the progress dialog is closed
        self.main.close()
