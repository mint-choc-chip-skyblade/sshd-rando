from filepathconstants import OUTPUT_PATH
from gui.dialog_header import print_progress_text, update_progress_value
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
from patches.dynamictextpatches import add_dynamic_text_patches
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
        update_progress_value(14)
        print_progress_text("Patching started")

        if OUTPUT_PATH.exists() and OUTPUT_PATH.is_dir():
            print_progress_text("Removing previous output")
            rmtree(OUTPUT_PATH)

        update_progress_value(16)
        self.stage_patch_handler.create_oarc_cache()
        self.stage_patch_handler.set_oarc_add_remove_from_patches()

        determine_check_patches(
            self.world.location_table,
            self.stage_patch_handler,
            self.event_patch_handler,
        )

        update_progress_value(18)
        append_dungeon_item_patches(self.event_patch_handler)

        update_progress_value(20)
        determine_entrance_patches(
            self.world.get_shuffled_entrances(), self.stage_patch_handler
        )

        patch_object_pack()

        self.stage_patch_handler.handle_stage_patches(self.conditional_patch_handler)

        update_progress_value(90)
        self.stage_patch_handler.patch_logo()

        update_progress_value(91)
        add_dynamic_text_patches(self.world, self.event_patch_handler)

        update_progress_value(92)
        self.event_patch_handler.handle_event_patches(self.conditional_patch_handler)

        update_progress_value(99)
        self.asm_patch_handler.patch_all_asm(self.world, self.conditional_patch_handler)

        print_progress_text("Patching completed")
        update_progress_value(100)
