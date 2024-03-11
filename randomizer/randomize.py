from constants.verificationconstants import *
from filepathconstants import CONFIG_PATH
from logic.generate import generate
from patches.allpatchhandler import AllPatchHandler
from randomizer.verify_extract import verify_extract
from util.arguments import get_program_args
from gui.dialogs.dialog_header import update_progress_value


def randomize():
    print("Starting new randomization:")
    args = get_program_args()

    if not args.dryrun:
        verify_extract()

    worlds = generate(CONFIG_PATH)

    if not args.dryrun:
        patch_handler = AllPatchHandler(worlds[0])
        patch_handler.do_all_patches()

    print("Randomization complete!")
    update_progress_value(100)

    if not args.dryrun:
        print(
            f"\nThe randomizer patch can be found at: {worlds[0].config.output_dir.as_posix()}"
        )
