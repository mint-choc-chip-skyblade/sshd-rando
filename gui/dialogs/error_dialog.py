import getpass
import pyclip
import traceback

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QCloseEvent, QIcon, QPixmap

from filepathconstants import ERROR_ICON_PATH


def error(exception: Exception):
    error_from_str(str(exception), traceback.format_exc())


def error_from_str(exception: str, traceback: str):
    def copy_error():
        pyclip.copy(error_dialog.detailedText())

    error_dialog = QMessageBox()
    error_dialog.setWindowTitle("An error has occurred!")

    copy_error_button = error_dialog.addButton(
        "Copy Error", QMessageBox.ButtonRole.NoRole
    )
    copy_error_button.clicked.disconnect()  # Prevent this from closing the error
    copy_error_button.clicked.connect(copy_error)

    try:
        error_dialog.setWindowIcon(QIcon(ERROR_ICON_PATH.as_posix()))
        error_dialog.setIconPixmap(QPixmap(ERROR_ICON_PATH.as_posix()))
    except:
        # It's not important if the icons fail to load
        error_dialog.setIcon(QMessageBox.Icon.Critical)

    # .ljust(128) makes the window size artificially bigger.
    # Annoyingly, QMessageBox widgets can't be resized but display text
    # nicely. QErrorMessage widgets can be resized but don't display
    # text nicely. QDialog can do both but would require even more
    # setup that's a bit much for a simple error message ^^'.
    error_dialog.setTextFormat(Qt.TextFormat.RichText)
    error_text = f"ERROR: {exception}"
    error_text += """
                    <br><br>If you are unsure how to fix this problem, please copy the
                    below error message and report the issue in the
                    <a href=\"https://discord.com/invite/zkm6yncD\">Discord server</a>
                    or create an issue on
                    <a href=\"https://github.com/mint-choc-chip-skyblade/sshd-rando/issues\">GitHub</a>
    """
    error_dialog.setText(error_text.ljust(128))

    # Remove usernames for easier privacy when reporting issues
    error_dialog.setDetailedText(
        f"```\n{ traceback.replace(getpass.getuser(), '[user]') }\n```"
    )

    print(traceback)
    error_dialog.exec()
