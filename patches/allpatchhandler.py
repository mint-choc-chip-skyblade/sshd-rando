from filepathconstants import OUTPUT_PATH
from logic.world import World
from patches.asmpatchhandler import ASMPatchHandler
from patches.conditionalpatchhandler import ConditionalPatchHandler
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
        self.world = world

        self.asm_patch_handler = ASMPatchHandler()
        self.conditional_patch_handler = ConditionalPatchHandler(self.world)
        self.event_patch_handler = EventPatchHandler()
        self.stage_patch_handler = StagePatchHandler()

    def do_all_patches(self):
        print("Patching started")

        if OUTPUT_PATH.exists() and OUTPUT_PATH.is_dir():
            print("Removing previous output")
            rmtree(OUTPUT_PATH)

        self.stage_patch_handler.create_oarc_cache()
        self.stage_patch_handler.set_oarc_add_remove_from_patches()

        determine_check_patches(
            self.world.location_table,
            self.stage_patch_handler,
            self.event_patch_handler,
        )

        append_dungeon_item_patches(self.event_patch_handler)
        determine_entrance_patches(
            self.world.get_shuffled_entrances(), self.stage_patch_handler
        )

        patch_object_pack()

        self.stage_patch_handler.handle_stage_patches(self.conditional_patch_handler)
        self.stage_patch_handler.patch_title_screen_logo()

        self.event_patch_handler.handle_event_patches(self.conditional_patch_handler)

        self.asm_patch_handler.patch_all_asm(self.world, self.conditional_patch_handler)

        print("Patching completed")
