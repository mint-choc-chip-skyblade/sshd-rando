from PySide6.QtCore import QThread, Signal
from randomize import randomize


class RandomizationThread(QThread):
    # update_progress = Signal(str, int)
    # error_abort = Signal(str)
    # randomization_complete = Signal()

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        try:
            randomize()
        except Exception as e:
            self.error_abort.emit(str(e))
            import traceback

            print(traceback.format_exc())
            return

        # self.randomization_complete.emit()
