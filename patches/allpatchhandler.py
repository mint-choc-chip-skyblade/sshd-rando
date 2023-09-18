from filepathconstants import OUTPUT_PATH
from logic.world import World
from patches.asmpatchhandler import ASMPatchHandler
from patches.eventpatchhandler import EventPatchHandler
from filepathconstants import OUTPUT_PATH
from patches.checkpatchhandler import (
    determine_check_patches,
    append_dungeon_item_patches,
)
from patches.entrancepatchhandler import determine_entrance_patches
from patches.objectpackpatchhandler import patch_object_pack
from patches.stagepatchhandler import StagePatchHandler
from patches.eventpatchhandler import EventPatchHandler
from filepathconstants import OUTPUT_PATH
from shutil import rmtree


class AllPatchHandler:
    def __init__(self, world: World):
        self.asmPatchHandler = ASMPatchHandler()
        self.eventPatchHandler = EventPatchHandler()
        self.stagePatchHandler = StagePatchHandler()
        self.eventPatchHandler = EventPatchHandler()
        self.world = world

    def do_all_patches(self):
        if OUTPUT_PATH.exists() and OUTPUT_PATH.is_dir():
            print("Removing previous output")
            rmtree(OUTPUT_PATH)

        self.stagePatchHandler.create_oarc_cache()
        self.stagePatchHandler.set_oarc_add_remove_from_patches()

        determine_check_patches(
            self.world.location_table, self.stagePatchHandler, self.eventPatchHandler
        )

        append_dungeon_item_patches(self.eventPatchHandler)
        determine_entrance_patches(
            self.world.get_shuffled_entrances(), self.stagePatchHandler
        )

        patch_object_pack()

        self.stagePatchHandler.handle_stage_patches(self.world)
        self.stagePatchHandler.patch_title_screen_logo()

        self.eventPatchHandler.handle_event_patches()

        self.asmPatchHandler.patch_all_asm()
