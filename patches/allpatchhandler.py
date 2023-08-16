from filepathconstants import OUTPUT_PATH
from patches.asmpatches import ASMPatchHandler
from patches.eventpatches import EventPatchHandler
from patches.stagepatches import StagePatchHandler
from shutil import rmtree

from sslib.utils import mask_shift_set


class AllPatchHandler:
    def __init__(self):
        self.asmPatchHandler = ASMPatchHandler()
        self.eventPatchHandler = EventPatchHandler()
        self.stagePatchHandler = StagePatchHandler()

    def do_all_patches(self):
        if OUTPUT_PATH.exists() and OUTPUT_PATH.is_dir():
            rmtree(OUTPUT_PATH)

        # print(hex(mask_shift_set(0xFFFFFFF3, 0x3, 4, 0x02)))

        self.stagePatchHandler.create_oarc_cache()
        self.stagePatchHandler.set_oarc_add_remove()
        self.stagePatchHandler.handle_stage_patches()
        self.eventPatchHandler.handle_event_patches()

        self.asmPatchHandler.do_asm_patches()
