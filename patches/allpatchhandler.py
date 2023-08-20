from patches.eventpatches import EventPatchHandler
from patches.checkpatchhandler import determine_check_patches
from filepathconstants import OUTPUT_PATH
import os
from patches.stagepatches import StagePatchHandler
from shutil import rmtree


class AllPatchHandler:
    def __init__(self):
        self.stagePatchHandler = StagePatchHandler()
        self.eventPatchHandler = EventPatchHandler()

    def do_all_patches(self):
        if os.path.exists(OUTPUT_PATH) and os.path.isdir(OUTPUT_PATH):
            rmtree(OUTPUT_PATH)

        self.stagePatchHandler.create_oarc_cache()
        self.stagePatchHandler.set_oarc_add_remove_from_patches()
        determine_check_patches(self.stagePatchHandler, self.eventPatchHandler)
        self.stagePatchHandler.handle_stage_patches()
        self.eventPatchHandler.handle_event_patches()
