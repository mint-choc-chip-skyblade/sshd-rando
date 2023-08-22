from patches.checkpatchhandler import determine_check_patches
from patches.objectpackpatchhandler import patch_object_pack
from patches.stagepatches import StagePatchHandler
from patches.eventpatches import EventPatchHandler
from filepathconstants import OUTPUT_PATH
from shutil import rmtree
import os


class AllPatchHandler:
    def __init__(self, world):
        self.stagePatchHandler = StagePatchHandler()
        self.eventPatchHandler = EventPatchHandler()
        self.world = world

    def do_all_patches(self):
        if os.path.exists(OUTPUT_PATH) and os.path.isdir(OUTPUT_PATH):
            rmtree(OUTPUT_PATH)

        self.stagePatchHandler.create_oarc_cache()
        self.stagePatchHandler.set_oarc_add_remove_from_patches()
        determine_check_patches(
            self.world.location_table, self.stagePatchHandler, self.eventPatchHandler
        )
        patch_object_pack()
        self.stagePatchHandler.handle_stage_patches()
        self.stagePatchHandler.patch_title_screen_logo()
        self.eventPatchHandler.handle_event_patches()
