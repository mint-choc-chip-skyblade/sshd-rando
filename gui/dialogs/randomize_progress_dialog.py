from typing_extensions import override

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QCloseEvent, QKeyEvent, QIcon
from PySide6.QtWidgets import QProgressDialog

from filepathconstants import ICON_PATH

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.main import Main


class RandomizerProgressDialog(QProgressDialog):
    def __init__(self, main: "Main", cancel=None):
        QProgressDialog.__init__(self, main)
        self.main = main
        self.setWindowTitle("Randomizing...")
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setLabelText("Initializing")
        self.setWindowIcon(QIcon(ICON_PATH.as_posix()))
        self.setCancelButton(None)  # type: ignore
        self.setValue(0)
        self.setMinimumWidth(250)

        self.installEventFilter(self)

        if cancel:
            # This is a bit awkward but we cannot use the builtin self.canceled signal,
            # single the dialog will always automatically close when the signal
            # is triggered. So if our owner can handle cancellation, we trigger our own callback.
            self.user_cancel = cancel
        else:
            # Otherwise cancellation is not allowed.
            self.user_cancel = lambda: None

        self.setVisible(True)

    def exec(self):
        QProgressDialog.exec(self)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj == self:
            if event.type() in (
                QEvent.Type.KeyPress,
                QEvent.Type.ShortcutOverride,
                QEvent.Type.KeyRelease,
            ):
                if isinstance(event, QKeyEvent) and event.key() in (
                    Qt.Key.Key_Return,
                    Qt.Key.Key_Escape,
                    Qt.Key.Key_Enter,
                ):
                    self.user_cancel()
                    # Always prevent attempts to cancel the dialog via ESC - the owner
                    # is responsible for closing this dialog when progress is done or
                    # cancellation has explicitly been handled.
                    event.accept()
                    return True

        return super(QProgressDialog, self).eventFilter(obj, event)

    @override
    def closeEvent(self, close_event: QCloseEvent):
        self.user_cancel()
        close_event.ignore()
