import random
import struct
import tempfile
import time

from io import BytesIO
from pathlib import Path
from collections import Counter
from lz4.block import compress, decompress

from constants.asmconstants import *
from constants.itemconstants import (
    ITEM_ITEMFLAGS,
    ITEM_STORYFLAGS,
    ITEM_DUNGEONFLAGS,
    ITEM_COUNTS,
    PROGRESSIVE_POUCH,
)
from constants.itemnames import *
from constants.musicconstants import VANILLA_MUSIC_DATA
from filepathconstants import (
    ASM_ADDITIONS_DIFFS_PATH,
    ASM_PATCHES_DIFFS_PATH,
    ASM_SDK_DIFFS_PATH,
    MAIN_NSO_FILE_PATH,
    SDK_FILE_PATH,
    STARTFLAGS_FILE_PATH,
    SUBSDK1_FILE_PATH,
    BIRD_STATUE_DATA_PATH,
)

from gui.dialogs.dialog_header import print_progress_text, update_progress_value

from logic.world import World

from patches.asmpatchhelper import NsoOffsets, SegmentHeader
from patches.conditionalpatchhandler import ConditionalPatchHandler

from sslib.fs_helpers import write_bytes, write_str, write_u32, write_u8
from sslib.utils import write_bytes_create_dirs
from sslib.yaml import yaml_load, yaml_write

# Adds a patch to nnSdk to route all vfprintf calls to the debug output
# These will be printed to the console on yuzu
# Only prints that start with "> " will be printed to the console on yuzu
# This variable disables this functionality if desired (mainly just leftover
# from when this would print *everything* to the console ^^')
ASM_DEBUG_PRINT = True


class ASMPatchHandler:
    def __init__(self, asm_output_path: Path) -> None:
        self.asm_output_path = asm_output_path
        self.main_nso_output_path = self.asm_output_path / "main"
        self.subsdk8_nso_path = self.asm_output_path / "subsdk8"
        self.sdk_nso_path = self.asm_output_path / "sdk"
        self.shop_data: dict = {}

    def compress(self, data: bytes) -> bytes:
        # Uses the lz4 compression.
        return compress(data)[4:]  # trims lz4 junk off the start

    def decompress(self, data: bytes, size: int) -> bytes:
        # Uses the lz4 decompression.
        return decompress(data, size)

    def get_segments(self, nso):
        size = SegmentHeader.SEGMENT_HEADER_SIZE
        nso.seek(0x10)  # Start of .text SegmentHeader
        text_header = SegmentHeader.bytes_to_segment_header(nso.read(size))
        rodata_header = SegmentHeader.bytes_to_segment_header(nso.read(size))
        data_header = SegmentHeader.bytes_to_segment_header(nso.read(size))

        return text_header, rodata_header, data_header

    def patch_asm(
        self,
        world: World,
        onlyif_handler: ConditionalPatchHandler,
        nso_path: Path,
        asm_diffs_path: Path,
        output_path: Path,
        offsets: NsoOffsets,
        extra_diffs_path: Path | None = None,
    ):
        # Get asm patch diffs.
        asm_patch_diff_paths = tuple(asm_diffs_path.glob("*-diff.yaml"))

        if extra_diffs_path is not None:
            asm_patch_diff_paths += tuple(extra_diffs_path.glob("*-diff.yaml"))

        # Get segment headers.
        nso = BytesIO(nso_path.read_bytes())
        text_header, rodata_header, data_header = self.get_segments(nso)

        nso.seek(text_header.get_file_offset())
        compressed_text = nso.read(
            rodata_header.get_file_offset() - text_header.get_file_offset()
        )
        compressed_rodata = nso.read(
            data_header.get_file_offset() - rodata_header.get_file_offset()
        )
        compressed_data = nso.read()

        # Decompress them.
        text_segment = BytesIO(
            self.decompress(compressed_text, text_header.get_decompressed_size())
        )
        rodata_segment = BytesIO(
            self.decompress(compressed_rodata, rodata_header.get_decompressed_size())
        )
        data_segment = BytesIO(
            self.decompress(compressed_data, data_header.get_decompressed_size())
        )

        for diff_file_name in asm_patch_diff_paths:
            binary_diffs = yaml_load(diff_file_name)

            # Write patch data for each segment.
            for relative_offset, data in binary_diffs.items():
                if type(relative_offset) is not int:
                    if onlyif_handler.evaluate_onlyif(relative_offset):
                        for relative_offset, data2 in data.items():
                            self.write_patch(
                                relative_offset,
                                offsets,
                                text_segment,
                                rodata_segment,
                                data_segment,
                                data2,
                            )
                else:
                    self.write_patch(
                        relative_offset,
                        offsets,
                        text_segment,
                        rodata_segment,
                        data_segment,
                        data,
                    )

                # print(f"data {bytes(data)}")

        new_compressed_text = self.compress(text_segment.getvalue())
        new_compressed_rodata = self.compress(rodata_segment.getvalue())
        new_compressed_data = self.compress(data_segment.getvalue())

        new_text_size_diff = len(new_compressed_text) - len(compressed_text)
        new_rodata_size_diff = len(new_compressed_rodata) - len(compressed_rodata)
        new_data_size_diff = len(new_compressed_data) - len(compressed_data)

        # Update NSO header.
        #
        # Each segment size can change due to the compression.
        # If the new size is smaller, don't bother updating it - there's no point.
        # The MemoryOffset and Size fields are left unchanged as this doesn't appear to cause problems.
        if new_text_size_diff > 0:
            # Update rodata and data file offsets in their segment headers.
            write_u32(
                nso,
                SegmentHeader.SEGMENT_HEADER_SIZE * 2,
                rodata_header.get_file_offset() + new_text_size_diff,
                is_little_endian=True,
            )
            write_u32(
                nso,
                SegmentHeader.SEGMENT_HEADER_SIZE * 3,
                data_header.get_file_offset() + new_text_size_diff,
                is_little_endian=True,
            )

            # Update the local segment headers in case the rodata size is different too.
            text_header, rodata_header, data_header = self.get_segments(nso)

        if new_rodata_size_diff > 0:
            # Update data file offset in its segment header.
            write_u32(
                nso,
                SegmentHeader.SEGMENT_HEADER_SIZE * 3,
                data_header.get_file_offset() + new_rodata_size_diff,
                is_little_endian=True,
            )

        # Update segment headers one final time before writing them.
        text_header, rodata_header, data_header = self.get_segments(nso)

        write_bytes(nso, text_header.get_file_offset(), new_compressed_text)
        write_bytes(nso, rodata_header.get_file_offset(), new_compressed_rodata)
        write_bytes(nso, data_header.get_file_offset(), new_compressed_data)

        # Update compressed sizes (each is 4 bytes).
        write_u32(
            nso,
            COMPRESSED_SEGMENT_NSO_OFFSET,
            len(new_compressed_text),
            is_little_endian=True,
        )
        write_u32(
            nso,
            COMPRESSED_SEGMENT_NSO_OFFSET + 4,
            len(new_compressed_rodata),
            is_little_endian=True,
        )
        write_u32(
            nso,
            COMPRESSED_SEGMENT_NSO_OFFSET + 8,
            len(new_compressed_data),
            is_little_endian=True,
        )

        # Patch nso flags to tell consoles not to check the segment hashes.
        # See https://switchbrew.org/wiki/NSO#Flags for more info.
        write_u8(nso, NSO_FLAGS_OFFSET, 0x7, is_little_endian=True)

        write_bytes_create_dirs(output_path, nso.getvalue())

    def write_patch(
        self, relative_offset, offsets, text_segment, rodata_segment, data_segment, data
    ) -> None:
        if relative_offset < offsets.get_rodata_offset():
            file_offset = relative_offset - offsets.get_text_offset()
            write_bytes(text_segment, file_offset, bytes(data))
        elif relative_offset < offsets.get_data_offset():
            file_offset = relative_offset - offsets.get_rodata_offset()
            write_bytes(rodata_segment, file_offset, bytes(data))
        else:
            file_offset = relative_offset - offsets.get_data_offset()
            write_bytes(data_segment, file_offset, bytes(data))

    # Applies both asm patches and additions.
    def patch_all_asm(self, world: World, onlyif_handler: ConditionalPatchHandler):
        asm_patching_start_time = time.process_time()

        # Apply sdk patches
        if ASM_DEBUG_PRINT:
            print_progress_text("Applying SDK asm patches")
            self.patch_asm(
                world,
                onlyif_handler,
                SDK_FILE_PATH,
                ASM_SDK_DIFFS_PATH,
                self.sdk_nso_path,
                SDK_NSO_OFFSETS,
            )

            print(
                f"Patching sdk.nso took {(time.process_time() - asm_patching_start_time)} seconds"
            )

        start_main_patching_time = time.process_time()
        temp_dir = tempfile.TemporaryDirectory()

        # Apply main patches
        # Keeps the temporary directory only within this with block.
        with temp_dir as temp_dir_name:
            temp_dir_name = Path(temp_dir_name)

            print_progress_text("Creating shop shuffle patches")
            shop_shuffle_diff_file_path = temp_dir_name / "shop-shuffle-diff.yaml"
            self.create_shop_data_patch(
                ASM_PATCHES_DIFFS_PATH / shop_shuffle_diff_file_path
            )

            print_progress_text("Creating damage multiplier patch")
            damage_multiplier_diff_file_path = (
                temp_dir_name / "damage-multiplier-diff.yaml"
            )
            self.create_damage_multiplier_patch(
                ASM_PATCHES_DIFFS_PATH / damage_multiplier_diff_file_path, world
            )

            print_progress_text("Applying asm patches")
            self.patch_asm(
                world,
                onlyif_handler,
                MAIN_NSO_FILE_PATH,
                ASM_PATCHES_DIFFS_PATH,
                self.main_nso_output_path,
                MAIN_NSO_OFFSETS,
                extra_diffs_path=temp_dir_name,
            )

        update_progress_value(93)
        print(
            f"Patching main.nso took {(time.process_time() - start_main_patching_time)} seconds"
        )
        start_subsdk8_patching_time = time.process_time()

        temp_dir = tempfile.TemporaryDirectory()

        # Apply subsdk8 patches
        # Keeps the temporary directory only within this with block.
        with temp_dir as temp_dir_name:
            temp_dir_name = Path(temp_dir_name)

            update_progress_value(94)
            print_progress_text("Creating startflag additions")
            startflags_diff_file_path = temp_dir_name / "startflags-diff.yaml"
            self.create_startflag_patches(
                startflags_diff_file_path, world, onlyif_handler
            )

            update_progress_value(95)
            print("Initializing global variables")
            global_variables_diff_file_path = (
                temp_dir_name / "global-variables-diff.yaml"
            )
            self.init_global_variables(global_variables_diff_file_path, world)

            print_progress_text("Creating starting entrance additions")
            staring_entrance_diff_file_path = (
                temp_dir_name / "starting-entrance-diff.yaml"
            )
            self.create_starting_entrance_patch(staring_entrance_diff_file_path, world)

            update_progress_value(96)
            print_progress_text("Creating music patches")
            music_diff_file_path = temp_dir_name / "music-diff.yaml"
            self.create_music_patch(music_diff_file_path, world)

            update_progress_value(97)
            print_progress_text("Applying asm additions")
            self.patch_asm(
                world,
                onlyif_handler,
                SUBSDK1_FILE_PATH,
                ASM_ADDITIONS_DIFFS_PATH,
                self.subsdk8_nso_path,
                SUBSDK_NSO_OFFSETS,
                extra_diffs_path=temp_dir_name,
            )

        asm_patching_end_time = time.process_time()
        print(
            f"Patching subsdk8.nso took {(asm_patching_end_time - start_subsdk8_patching_time)} seconds"
        )
        print(
            f"Total asm patching took {(asm_patching_end_time - asm_patching_start_time)} seconds"
        )

    def create_starting_entrance_patch(self, output_path: Path, world: World):
        try:
            spawn_info = world.get_entrance(
                "Link's Spawn -> Knight Academy"
            ).replaces.spawn_info[0]
        except:
            spawn_info = world.get_entrance(
                "Link's Spawn -> Knight Academy"
            ).spawn_info[0]

        # print(spawn_info)

        stage_name: str = spawn_info["stage"]
        layer: int = spawn_info["layer"]
        room: int = spawn_info["room"]
        entrance: int = spawn_info["entrance"]

        spawn_data = BytesIO()
        write_str(spawn_data, 0, stage_name, 8)
        write_u8(spawn_data, 8, room)
        write_u8(spawn_data, 9, layer)
        write_u8(spawn_data, 10, entrance)
        write_u8(spawn_data, 11, 0)  # night

        # print(spawn_info)
        # print(spawn_data.getvalue())

        # Convert startflags_data into a list of bytes.
        spawn_data_bytes = spawn_data.getvalue()
        assert len(spawn_data_bytes) == 12

        spawn_data_dict = {
            SUBSDK_WARP_TO_START_OFFSET: list(
                struct.unpack("B" * len(spawn_data_bytes), spawn_data_bytes)
            )
        }

        yaml_write(output_path, spawn_data_dict)

        # Write the starting entrance binary to a non-temp file.
        # yaml_write(Path("./test-starting-entrance.yaml"), spawn_data_dict)

    def create_startflag_patches(
        self, output_path: Path, world: World, onlyif_handler: ConditionalPatchHandler
    ):
        startflags = dict(yaml_load(STARTFLAGS_FILE_PATH))

        storyflags = startflags["Storyflags"]
        sceneflags = startflags["Sceneflags"]
        itemflags = startflags["Itemflags"]
        dungeonflags = startflags["Dungeonflags"]
        start_counts = Counter()

        # Handle starting bugs and treasures
        additional_starting_items = {}

        if world.setting("start_with_all_bugs") == "on":
            for bug in BUG_NAMES:
                additional_starting_items[world.get_item(bug)] = 99

        if world.setting("start_with_all_treasures") == "on":
            for treasure in TREASURE_NAMES:
                additional_starting_items[world.get_item(treasure)] = 99

        # Get flag data from starting item pool
        for item, count in (
            world.starting_item_pool.items() | additional_starting_items.items()
        ):
            item_name = item.name

            if itemflag_data := ITEM_ITEMFLAGS.get(item_name, False):
                if type(itemflag_data) == list:
                    for item_count in range(0, count):
                        itemflags.append(itemflag_data[item_count])
                elif type(itemflag_data) == tuple:
                    for flag in itemflag_data:
                        itemflags.append(flag)
                else:
                    itemflags.append(itemflag_data)

            if storyflag_data := ITEM_STORYFLAGS.get(item_name, False):
                if type(storyflag_data) == list:
                    for item_count in range(count):
                        storyflags.append(storyflag_data[item_count])
                elif type(storyflag_data) == tuple:
                    for flag in storyflag_data:
                        storyflags.append(flag)
                else:
                    storyflags.append(storyflag_data)

            if dungeonflag_data := ITEM_DUNGEONFLAGS.get(item_name, False):
                scene, flag = dungeonflag_data
                if scene not in dungeonflags:
                    dungeonflags[scene] = []
                dungeonflags[scene].append(flag)

            if start_count_data := ITEM_COUNTS.get(item_name, False):
                counter, amount, maximum = start_count_data
                final_count = min(maximum, count)
                if item_name == PROGRESSIVE_POUCH:
                    final_count -= 1
                start_counts[counter] += amount * final_count

        # Set flags for random starting statues
        bird_statue_data = yaml_load(BIRD_STATUE_DATA_PATH)
        faron_starting_statue = world.get_entrance(
            "Faron Region Entrance -> Sealed Grounds Statue"
        ).connected_area.name
        eldin_starting_statue = world.get_entrance(
            "Eldin Region Entrance -> Volcano Entrance Statue"
        ).connected_area.name
        lanayru_starting_statue = world.get_entrance(
            "Lanayru Region Entrance -> Lanayru Mine Entry Statue"
        ).connected_area.name
        for statue in (
            faron_starting_statue,
            eldin_starting_statue,
            lanayru_starting_statue,
        ):
            flag = bird_statue_data[statue]["flag"]
            if bird_statue_data[statue]["flag_space"] == "Story":
                storyflags.append(flag)
            else:
                scene = bird_statue_data[statue]["flag_space"]
                if scene not in sceneflags:
                    sceneflags[scene] = []
                sceneflags[scene].append(flag)

        # Each section is delimited by 0xFFFF
        startflags_data = BytesIO()

        # Storyflags
        for flag in self._get_flags(storyflags, onlyif_handler):
            startflags_data.write(struct.pack("<H", flag))

        startflags_data.write(bytes.fromhex("FFFF"))

        # Sceneflags
        for scene in sceneflags:
            for flag in self._get_flags(sceneflags[scene], onlyif_handler):
                startflags_data.write(
                    struct.pack("<BB", SCENE_NAME_TO_SCENE_INDEX[scene], flag)
                )

        startflags_data.write(bytes.fromhex("FFFF"))

        # Itemflags
        itemflags.sort()  # Forces Hylian Shield to always be the top slot of the pouch wheel

        for flag in self._get_flags(itemflags, onlyif_handler):
            startflags_data.write(struct.pack("<H", flag))

        startflags_data.write(bytes.fromhex("FFFF"))

        # Dungeonflags
        for scene in dungeonflags:
            for flag in self._get_flags(dungeonflags[scene], onlyif_handler):
                startflags_data.write(
                    struct.pack("<BB", SCENE_NAME_TO_SCENE_INDEX[scene], flag)
                )

        startflags_data.write(bytes.fromhex("FFFF"))

        start_counts_data = BytesIO()

        # Start counts
        for counter, amount in start_counts.items():
            start_counts_data.write(struct.pack("<HH", counter, amount))

        start_counts_data.write(bytes.fromhex("FFFFFFFF"))

        # Convert startflags_data into a list of bytes.
        startflags_data_bytes = startflags_data.getvalue()
        startflags_data_dict = {
            SUBSDK_STARTFLAG_OFFSET: list(
                struct.unpack("B" * len(startflags_data_bytes), startflags_data_bytes)
            )
        }

        # Same with start_counts_data
        start_counts_data_bytes = start_counts_data.getvalue()
        start_counts_data_dict = {
            SUBSDK_START_COUNTS_OFFSET: list(
                struct.unpack(
                    "B" * len(start_counts_data_bytes), start_counts_data_bytes
                )
            )
        }

        startflags_data_dict.update(start_counts_data_dict)

        yaml_write(output_path, startflags_data_dict)

        # Write the startflag binary to a non-temp file.
        # yaml_write(Path("./test-startflags.yaml"), startflags_data_dict)

        # If this fails, the rust struct size will need increasing
        assert len(startflags_data_bytes) < MAX_STARTFLAGS

    def init_global_variables(self, output_path: Path, world: World):

        daytime_sky_color_index = world.setting_map.settings[
            "daytime_sky_color"
        ].current_option_index
        nighttime_sky_color_index = world.setting_map.settings[
            "nighttime_sky_color"
        ].current_option_index
        daytime_cloud_color_index = world.setting_map.settings[
            "daytime_cloud_color"
        ].current_option_index
        nighttime_cloud_color_index = world.setting_map.settings[
            "nighttime_cloud_color"
        ].current_option_index

        skip_harp_playing = world.setting("skip_harp_playing").value_index()
        cutoff_game_over_music = world.setting("cutoff_game_over_music").value_index()

        sky_keep_goal = world.get_dungeon("Sky Keep").goal_location
        if sky_keep_goal == None:
            sky_keep_beaten_sceneflag = -1
        elif sky_keep_goal.name.endswith("Din"):
            sky_keep_beaten_sceneflag = 61
        elif sky_keep_goal.name.endswith("Nayru"):
            sky_keep_beaten_sceneflag = 62
        elif sky_keep_goal.name.endswith("Farore"):
            sky_keep_beaten_sceneflag = 64

        init_rw_globals_dict = {
            0x712E54B6BC: [
                daytime_sky_color_index,
                nighttime_sky_color_index,
                daytime_cloud_color_index,
                nighttime_cloud_color_index,
            ],  # SKY_CLOUD_COLORS
            0x712E54B6C0: [
                skip_harp_playing,
                sky_keep_beaten_sceneflag,
                cutoff_game_over_music,
                0xFF,
            ],  # RANDOMIZER_SETTINGS
            0x712E5FF020: [
                0xFF,
                0xFF,
                0xFF,
                0xFF,
            ],  # NEXT_TRAP_ID
            0x712E5FF024: [
                0xFF,
                0xFF,
                0xFF,
                0xFF,
            ],  # TRAP_ID
            0x712E5FF028: [
                0x00,
                0x00,
                0x00,
                0x00,
            ],  # TRAP_DURATION
            0x712E5FF02C: [
                random.randint(0, 0xFF),
                random.randint(0, 0xFF),
                random.randint(0, 0xFF),
                random.randint(0, 0xFF),
            ],  # RNG_SEED
            0x712E5FF034: [
                0x00,
                0x00,
                0x00,
                0x00,
            ],  # COLOR_CHANGE_DELAY
            0x712E5FF058: [0x00] * 16,  # BOSS_RUSH_SCENEFLAG_BKP
            0x712E5FF068: [0x00] * 16,  # BOSS_RUSH_DUNGEONFLAG_BKP
            0x712E5FF078: [
                0xFF,
                0xFF,
            ],  # BOSS_RUSH_CURRENT_SCENEINDEX
            0x712E5FF07A: [
                0x00,
                0x0,
            ],  # BOSS_RUSH_STORYFLAG_STATES
        }

        yaml_write(output_path, init_rw_globals_dict)

        # Write the global variables binary to a non-temp file.
        # yaml_write(Path("./test-global-variables.yaml"), init_globals_dict)

    def create_damage_multiplier_patch(self, output_path: Path, world: World):
        multiplier = world.setting("damage_multiplier").value_as_number()
        # bytes for instruction: mov w8, damage_multiplier
        bytes = 0x52800008 | (multiplier << 5)

        # Reverse order for proper endianess
        damage_multiplier_dict = {
            0x7100A6CD84: [
                bytes & 0x000000FF,
                (bytes & 0x0000FF00) >> 8,
                (bytes & 0x00FF0000) >> 16,
                (bytes & 0xFF000000) >> 24,
            ]
        }

        yaml_write(output_path, damage_multiplier_dict)

    def add_shop_data(
        self,
        shop_index: int,
        buy_decide_scale: float,
        put_scale: float,
        target_arrow_height_offset: float,
        itemid: int,
        price: int,
        event_entrypoint: int,
        next_shop_index: int,
        spawn_storyflag: int,
        shop_arc_name: str,
        shop_model_name: str,
        display_height_offset: float,
        trapbits: int,
        sold_out_storyflag: int,
    ):
        self.shop_data[shop_index] = (
            buy_decide_scale,
            put_scale,
            target_arrow_height_offset,
            itemid,
            price,
            event_entrypoint,
            next_shop_index,
            spawn_storyflag,
            shop_arc_name,
            shop_model_name,
            display_height_offset,
            trapbits,
            sold_out_storyflag,
        )

    def create_shop_data_patch(self, output_path: Path):
        shop_item_table_start_address = 0x710164043C
        shop_item_size = 0x54
        shop_data_dict = {}

        for shop_index in self.shop_data:
            item_start_address = shop_item_table_start_address + (
                shop_item_size * shop_index
            )

            for value_index, value in enumerate(self.shop_data[shop_index]):
                if value != -1:
                    if (format := SHOP_ITEM_DATA_FORMATS[value_index]) is not None:
                        value = list(struct.pack(format, value))
                    else:  # must be a string
                        value = list(bytes(value + "\0", "ascii"))

                    shop_data_dict[
                        item_start_address + SHOP_ITEM_DATA_OFFSETS[value_index]
                    ] = value

        yaml_write(output_path, shop_data_dict)

        # Write the shop data binary to a non-temp file.
        # yaml_write(Path("./test-shop-data.yaml"), shop_data_dict)

    def create_music_patch(self, output_path: Path, world: World):
        music_rando_setting = world.setting("randomize_music")
        music_data = VANILLA_MUSIC_DATA.copy()
        music_pool: dict[int, list[str]] = {}

        for music_name, music_type in music_data:
            # Shuffle type 2 with type 1
            if music_type == 2:
                music_type = 1

            # Tadtones Melody
            # Add it to type 3 so it can show up in random places but ensure
            # it's also added to type 11 so the vanilla tadtone melody remains
            # unchanged (as non-vanilla tadtone music softlocks).
            if music_name == "F63D5DB51DE748A3729628C659397A49":
                music_pool[11].append(music_name)  # the pool for type 11 already exists
                music_type = 3

            if music_type not in music_pool:
                music_pool[music_type] = [music_name]
            else:
                music_pool[music_type].append(music_name)

        if music_rando_setting != "vanilla":
            for music_type, music_name_list in music_pool.items():
                # Don't shuffle types 10 and 11
                if music_type not in (10, 11) and len(music_name_list) > 1:
                    if music_rando_setting == "shuffle_music_limit_vanilla":
                        derangement = self._get_derangement(len(music_name_list))
                        shuffled_music_name_list = []

                        for track_index in range(len(music_name_list)):
                            shuffled_music_name_list.append(
                                music_name_list[derangement[track_index]]
                            )
                    else:
                        shuffled_music_name_list = music_name_list
                        random.shuffle(shuffled_music_name_list)

                    music_pool[music_type] = shuffled_music_name_list

        shuffled_names = []
        music_type_counter: dict[int, int] = {}

        for music_name, music_type in music_data:
            if music_type == 2:
                music_type = 1

            if music_type not in music_type_counter:
                music_type_counter[music_type] = 0

            music_type_counter[music_type] += 1

            shuffled_music_name = music_pool[music_type][
                music_type_counter[music_type] - 1
            ]

            # print(music_name, shuffled_music_name)
            for char in shuffled_music_name:
                shuffled_names.append(ord(char))

        music_data_dict = {0x712E54C000: shuffled_names}

        yaml_write(output_path, music_data_dict)

        # Write the shop data binary to a non-temp file.
        # yaml_write(Path("./test-music.yaml"), music_data_dict)

    def _is_derangement(self, l: list[int]) -> bool:
        for i, n in enumerate(l):
            if i == n:
                return False
        return True

    def _get_derangement(self, music_list_length: int) -> list[int]:
        # Generates a list of the range [0, music_list_length],
        # shuffled such that no number is at its original index.
        if music_list_length <= 1:
            raise ValueError("Length of music list needs to be at least 2.")

        music_index_list = list(range(music_list_length))
        random.shuffle(music_index_list)

        while not self._is_derangement(music_index_list):
            random.shuffle(music_index_list)

        return music_index_list

    def _get_flags(
        self, startflag_section, onlyif_handler: ConditionalPatchHandler
    ) -> tuple:
        flags = []

        for flag in startflag_section:
            if type(flag) is not int:
                condition = tuple(flag.keys())[0]

                if onlyif_handler.evaluate_onlyif(condition):
                    for onlyif_flag in flag[condition]:
                        flags.append(onlyif_flag)
            else:
                flags.append(flag)

        return tuple(flags)
