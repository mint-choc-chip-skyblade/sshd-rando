from PySide6.QtCore import QThread, Signal


class ThreadCancelled(Exception):
    def __str__(self):
        return "Some QThread was cancelled."


class RandomizationThread(QThread):
    dialog_value_update = Signal(int)
    dialog_label_update = Signal(str)

    update_progress = Signal(str, int)
    error_abort = Signal(str, str)
    randomization_complete = Signal()

    callback = None

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        try:
            # Import here to prevent circular dependency
            from randomizer.randomize import randomize

            RandomizationThread.callback = self
            randomize()
        except Exception as e:
            import traceback

            self.error_abort.emit(str(e), traceback.format_exc())

            import multiprocessing as mp

            for child in mp.active_children():
                child.kill()

            return

        self.randomization_complete.emit()

        RandomizationThread.callback = None


class VerificationThread(QThread):
    dialog_value_update = Signal(int)
    dialog_label_update = Signal(str)

    update_progress = Signal(str, int)
    error_abort = Signal(str, str)
    verification_complete = Signal()

    cancelled = False
    callback = None

    def __init__(self, verify_all: bool = False):
        QThread.__init__(self)
        self.verify_all = verify_all

    def set_verify_all(self, should_verify_all: bool):
        self.verify_all = should_verify_all

    def run(self):
        try:
            # Import here to prevent circular dependency
            from randomizer.verify_extract import verify_extract

            VerificationThread.callback = self
            verify_extract(verify_all_files=self.verify_all)
        except Exception as e:
            import traceback

            self.error_abort.emit(str(e), traceback.format_exc())

        self.verification_complete.emit()

        VerificationThread.callback = None
