from gui.guithreads import ThreadCancelled
from util.arguments import get_program_args
import logging

args = get_program_args()


def get_progress_value_from_range(
    end_value: int, range_size: int, current_step: int, total_steps: int
) -> int:
    # final_value - ( ((total_tasks - current_tast)/total_tasks) * value_range_to_fill)
    progress_left_to_make = total_steps - current_step
    progress_made_ratio = progress_left_to_make / total_steps

    return int(end_value - (progress_made_ratio * range_size))


if not args.nogui:
    from gui.guithreads import RandomizationThread, VerificationThread

    def update_progress_value(value: int):
        if RandomizationThread.cancelled:
            RandomizationThread.cancelled = False
            raise ThreadCancelled

        if RandomizationThread.callback:
            RandomizationThread.callback.dialog_value_update.emit(value)

    def print_progress_text(label_text: str):
        if RandomizationThread.cancelled:
            RandomizationThread.cancelled = False
            raise ThreadCancelled

        logging.getLogger("").debug(label_text)
        print(label_text)

        if RandomizationThread.callback:
            RandomizationThread.callback.dialog_label_update.emit(label_text)

    def update_verify_value(value: int):
        if VerificationThread.cancelled:
            VerificationThread.cancelled = False
            raise ThreadCancelled

        if VerificationThread.callback:
            VerificationThread.callback.dialog_value_update.emit(value)

    def print_verify_text(label_text: str):
        if VerificationThread.cancelled:
            VerificationThread.cancelled = False
            raise ThreadCancelled

        logging.getLogger("").debug(label_text)

        if VerificationThread.callback:
            VerificationThread.callback.dialog_label_update.emit(label_text)

else:  # Don't actually do anything since there's no gui to update

    def update_progress_value(value: int):
        pass

    def print_progress_text(label_text: str):
        logging.getLogger("").debug(label_text)
        print(label_text)

    def update_verify_value(value: int):
        pass

    def print_verify_text(label_text: str):
        logging.getLogger("").debug(label_text)
