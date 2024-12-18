from filepathconstants import OBJECTPACK_PATH_TAIL, SSHD_EXTRACT_PATH, OTHER_MODS_PATH
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
from patches.stagepatchhandler import StagePatchHandler
from patches.eventpatchhandler import EventPatchHandler
from patches.dynamictextpatches import add_dynamic_text_patches
from sslib.utils import write_bytes_create_dirs
from shutil import rmtree
import os

from patches.temp_objectpack_texture_replace_hack import patch_object_pack


class AllPatchHandler:
    def __init__(self, world: World):
        self.world = world
        output_dir = self.world.config.output_dir

        asm_output_path = output_dir / "exefs"
        self.asm_patch_handler = ASMPatchHandler(asm_output_path)

        self.conditional_patch_handler = ConditionalPatchHandler(self.world)

        self.event_patch_handler = EventPatchHandler(output_dir)

        stage_output_path = output_dir / "romfs"
        self.stage_patch_handler = StagePatchHandler(
            stage_output_path, world.setting_map.other_mods
        )

    def do_all_patches(self):
        update_progress_value(14)
        print_progress_text("Patching started")

        output_dir = self.world.config.output_dir
        if output_dir == SSHD_EXTRACT_PATH:
            raise Exception(
                f"Output path cannot be the same as extract path (the randomizer cannot overwrite its own extract)."
            )

        exefs_output = output_dir / "exefs"
        romfs_output = output_dir / "romfs"

        if exefs_output.exists() and exefs_output.is_dir():
            print_progress_text("Removing Old exefs Output")
            rmtree(exefs_output.as_posix())

        if romfs_output.exists() and romfs_output.is_dir():
            print_progress_text("Removing Old romfs Output")
            rmtree(romfs_output.as_posix())

        update_progress_value(16)
        self.stage_patch_handler.verify_other_mods()
        self.stage_patch_handler.create_oarc_cache()
        self.stage_patch_handler.set_oarc_add_remove_from_patches()

        determine_check_patches(
            self.world,
            self.stage_patch_handler,
            self.event_patch_handler,
        )

        update_progress_value(18)
        append_dungeon_item_patches(self.event_patch_handler)

        update_progress_value(20)
        determine_entrance_patches(
            self.world.get_shuffled_entrances(), self.stage_patch_handler
        )

        patch_object_pack(
            self.world.config.output_dir / OBJECTPACK_PATH_TAIL,
            self.stage_patch_handler.other_mods,
        )

        print_progress_text("Patching Stages")
        patch_required_dungeon_text_trigger(self.world, self.stage_patch_handler)
        self.stage_patch_handler.handle_stage_patches(self.conditional_patch_handler)

        update_progress_value(90)
        self.stage_patch_handler.patch_logo()

        update_progress_value(91)
        add_dynamic_text_patches(self.world, self.event_patch_handler)

        update_progress_value(92)
        print_progress_text("Patching Events")
        self.event_patch_handler.handle_event_patches(
            self.conditional_patch_handler, self.world.setting("language")
        )

        update_progress_value(99)
        self.asm_patch_handler.patch_all_asm(self.world, self.conditional_patch_handler)
        self.copy_extra_mod_files(self.stage_patch_handler.other_mods)

        print_progress_text("Patching completed")

    # If any active mods modify extra files not touched by the randomizer, then copy them over here
    def copy_extra_mod_files(self, other_mods: list[str] = []):

        if not other_mods:
            return

        print_progress_text("Copying Other Mod Files")
        for mod in other_mods:
            for root, dirs, files in os.walk(OTHER_MODS_PATH / mod):
                for file in files:
                    file_path = os.path.join(root, file)
                    if "exefs" in file_path:
                        file_path = file_path[file_path.index("exefs") :]
                    elif "romfs" in file_path:
                        file_path = file_path[file_path.index("romfs") :]

                    output = self.world.config.output_dir
                    path = output / file_path
                    other_path = (
                        output / f"{file_path[:-3]}"
                        if file_path.endswith(".LZ")
                        else output / f"{file_path}.LZ"
                    )

                    if not path.exists() and not other_path.exists():
                        write_bytes_create_dirs(
                            path, (OTHER_MODS_PATH / mod / file_path).read_bytes()
                        )
