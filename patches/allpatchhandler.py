from filepathconstants import OUTPUT_PATH
from patches.asmpatches import ASMPatchHandler
from patches.eventpatches import EventPatchHandler

# from patches.checkpatchhandler import determine_check_patches
from filepathconstants import OUTPUT_PATH
from patches.stagepatches import StagePatchHandler
from shutil import rmtree


class AllPatchHandler:
    def __init__(self):
        self.asmPatchHandler = ASMPatchHandler()
        self.eventPatchHandler = EventPatchHandler()
        self.stagePatchHandler = StagePatchHandler()

    def do_all_patches(self):
        if OUTPUT_PATH.exists() and OUTPUT_PATH.is_dir():
            print("Removing previous output")
            rmtree(OUTPUT_PATH)

        self.stagePatchHandler.create_oarc_cache()
        self.stagePatchHandler.set_oarc_add_remove_from_patches()
        # Commented since TEMP_PLACEMENT_LIST doesn't (and shouldn't) exist.
        # determine_check_patches(self.stagePatchHandler, self.eventPatchHandler)
        self.stagePatchHandler.handle_stage_patches()
        self.stagePatchHandler.patch_title_screen_logo()
        self.eventPatchHandler.handle_event_patches()

        self.asmPatchHandler.patch_all_asm()
