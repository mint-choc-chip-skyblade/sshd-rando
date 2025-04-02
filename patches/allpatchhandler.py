import time
from filepathconstants import (
    OBJECT_PATH_TAIL,
    SSHD_EXTRACT_PATH,
)
from gui.dialogs.dialog_header import print_progress_text, update_progress_value
from logic.world import World
from patches.asmpatchhandler import ASMPatchHandler
from patches.conditionalpatchhandler import ConditionalPatchHandler
from patches.eventpatchhandler import EventPatchHandler
from patches.checkpatchhandler import (
    determine_check_patches,
    append_dungeon_item_patches,
)
from patches.entrancepatchhandler import (
    determine_entrance_patches,
    patch_required_dungeon_text_trigger,
)
from patches.stagepatchhandler import (
    StagePatchHandler,
    create_shuffled_trial_object_patches,
)
from patches.eventpatchhandler import EventPatchHandler
from patches.dynamictextpatches import add_dynamic_text_patches
from patches.othermods import verify_other_mods, copy_extra_mod_files
from shutil import rmtree

from patches.arcpatchhandler import patch_object_folder


class AllPatchHandler:
    def __init__(self, world: World):
        self.world = world
        output_dir = self.world.config.output_dir

        asm_output_path = output_dir / "exefs"
        self.asm_patch_handler = ASMPatchHandler(asm_output_path)

        self.conditional_patch_handler = ConditionalPatchHandler(self.world)

        self.event_patch_handler = EventPatchHandler(
            output_dir, world.setting_map.other_mods
        )

        stage_output_path = output_dir / "romfs"
        self.stage_patch_handler = StagePatchHandler(
            stage_output_path, world.setting_map.other_mods
        )

    def do_all_patches(self):
        update_progress_value(25)
        print_progress_text("Patching started")

        output_dir = self.world.config.output_dir
        if output_dir == SSHD_EXTRACT_PATH:
            raise Exception(
                f"Output path cannot be the same as extract path (the randomizer cannot overwrite its own extract)."
            )

        exefs_output = output_dir / "exefs"
        romfs_output = output_dir / "romfs"

        update_progress_value(27)
        if exefs_output.exists() and exefs_output.is_dir():
            print_progress_text("Removing Old exefs Output")
            rmtree(exefs_output.as_posix())

        update_progress_value(28)
        if romfs_output.exists() and romfs_output.is_dir():
            print_progress_text("Removing Old romfs Output")
            rmtree(romfs_output.as_posix())

        update_progress_value(29)
        verify_other_mods(self.world.setting_map.other_mods)

        update_progress_value(30)
        self.stage_patch_handler.create_cache()

        update_progress_value(45)
        determine_check_patches(
            self.world,
            self.stage_patch_handler,
            self.event_patch_handler,
            self.asm_patch_handler,
        )

        update_progress_value(47)
        append_dungeon_item_patches(self.event_patch_handler)

        update_progress_value(48)
        determine_entrance_patches(
            self.world.get_shuffled_entrances(), self.stage_patch_handler
        )

        update_progress_value(50)
        patch_object_folder(
            self.world.config.output_dir / OBJECT_PATH_TAIL,
            self.stage_patch_handler.other_mods,
        )

        update_progress_value(59)
        create_shuffled_trial_object_patches(self.world, self.stage_patch_handler)

        update_progress_value(60)
        print_progress_text("Patching Stages")
        patch_required_dungeon_text_trigger(self.world, self.stage_patch_handler)
        self.stage_patch_handler.handle_stage_patches(self.conditional_patch_handler)

        update_progress_value(80)
        self.stage_patch_handler.patch_logo()

        update_progress_value(82)
        add_dynamic_text_patches(self.world, self.event_patch_handler)

        update_progress_value(84)
        print_progress_text("Patching Events")

        start_event_patching_time = time.process_time()

        self.event_patch_handler.handle_event_patches(
            self.conditional_patch_handler, self.world.setting("language")
        )

        print(
            f"Patching events took {(time.process_time() - start_event_patching_time)} seconds"
        )

        update_progress_value(90)
        self.asm_patch_handler.patch_all_asm(self.world, self.conditional_patch_handler)
        copy_extra_mod_files(
            self.world.setting_map.other_mods, self.world.config.output_dir
        )

        print_progress_text("Patching completed")
