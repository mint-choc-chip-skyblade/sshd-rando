from PySide6.QtCore import QThread, Signal


class RandomizationThread(QThread):
    dialog_value_update = Signal(int)
    dialog_label_update = Signal(str)

    update_progress = Signal(str, int)
    error_abort = Signal(str)
    randomization_complete = Signal()

    callback = None

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        try:
            # Import here to prevent circular dependency
            from randomize import randomize

            RandomizationThread.callback = self
            randomize()
        except Exception as e:
            self.error_abort.emit(str(e))

            import multiprocessing as mp

            for child in mp.active_children():
                child.kill()

            import traceback

            print(traceback.format_exc())

            return

        self.randomization_complete.emit()

        RandomizationThread.callback = None
