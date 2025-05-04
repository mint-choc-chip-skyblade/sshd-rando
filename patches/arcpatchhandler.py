from pathlib import Path
import time
from filepathconstants import (
    ENDROLL_SOURCE_PATH,
    OBJECTPACK_FILENAME,
    OBJECTPACK_PATH,
    CACHE_OARC_PATH,
    RANDO_ROOT_PATH,
    ROMFS_EXTRACT_PATH,
    TITLE2D_SOURCE_PATH,
)
from gui.dialogs.dialog_header import (
    get_progress_value_from_range,
    print_progress_text,
    update_progress_value,
)
from sslib.utils import write_bytes_create_dirs
from sslib.u8file import U8File
from .othermods import get_cache_oarc_path


def patch_object_folder(object_folder_output_path: Path, other_mods: list[str] = []):
    print_progress_text("Moving arcs to Object folder")
    start_move_arcs_time = time.process_time()

    objectpack_arc = U8File.get_parsed_U8_from_path(OBJECTPACK_PATH)
    objectpack_arc_names = [
        path.split("/")[-1] for path in objectpack_arc.get_all_paths()
    ]

    cache_oarc_paths = list(CACHE_OARC_PATH.glob("*"))

    # Move oarc cache models to romfs/Object/NX or the ObjectPack as is appropriate.
    # Patches made previously to the ARCN arrays in the room bzs files allow these models to be found by the game.
    for current_arc_num, arc in enumerate(cache_oarc_paths):
        # Only deal with .arc files
        if not arc.name.endswith(".arc"):
            continue

        arc_data_path = get_cache_oarc_path(arc.name, other_mods)
        if not arc_data_path.exists():
            raise Exception(f"ERROR: {arc.name} not found in oarc cache.")

        # Replace arcs in objectpack. If an arc doesn't belong there, add it to the Object/NX folder.
        if arc.name in objectpack_arc_names:
            objectpack_arc.add_file_data(f"oarc/{arc.name}", arc_data_path.read_bytes())
        else:
            oarc = U8File.get_parsed_U8_from_path(CACHE_OARC_PATH / arc.name)

            write_bytes_create_dirs(
                object_folder_output_path / (arc.name + ".LZ"),
                oarc.build_and_compress_U8(),
            )

        update_progress_value(
            get_progress_value_from_range(57, 7, current_arc_num, len(cache_oarc_paths))
        )

    print(f"Moving arcs took {(time.process_time() - start_move_arcs_time)} seconds")
    start_objectpack_rebuilding_time = time.process_time()

    update_progress_value(57)
    print_progress_text("Rebuilding ObjectPack")

    write_bytes_create_dirs(
        object_folder_output_path / OBJECTPACK_FILENAME,
        objectpack_arc.build_and_compress_U8(),
    )

    end_objectpack_patching_time = time.process_time()
    print(
        f"Rebuilding ObjectPack took {(end_objectpack_patching_time - start_objectpack_rebuilding_time)} seconds"
    )
    print(
        f"Total Object folder patching took {(end_objectpack_patching_time - start_move_arcs_time)} seconds"
    )


def create_shop_rupee_arcs():
    print_progress_text("Creating Rupee arcs for shops")

    cache_oarc_names = [arc.name for arc in list(CACHE_OARC_PATH.glob("*"))]
    shop_rupee_arc_names = (
        "GetBlueRupee.arc",
        "GetRedRupee.arc",
        "GetSilverRupee.arc",
        "GetGoldRupee.arc",
        "GetRupoor.arc",
    )
    shop_rupee_arc_offsets = (0x1000, 0x1E00, 0x2C00, 0x3A00, 0x4800)

    data_size = 0x2C0
    green_data_start = 0x200
    green_data_end = green_data_start + data_size

    for rupee_index, rupee_arc in enumerate(shop_rupee_arc_names):
        if rupee_arc in cache_oarc_names:
            print(f"{rupee_arc} already exists")
            continue

        print(f"Creating {rupee_arc}")

        # Don't check other mods for this.
        # If another mod *did* change the rupee model, this method of patching
        # the model to work in shops would almost certainly cause a crash.
        rupee_arc_path = get_cache_oarc_path("GetRupee.arc", [])
        if not rupee_arc_path.exists():
            raise Exception(f"ERROR: GetRupee.arc not found in oarc cache.")

        rupee_arc = U8File.get_parsed_U8_from_path(rupee_arc_path)

        if model_xtx := rupee_arc.get_file_data("g3d/model.xtx"):
            new_data_start = shop_rupee_arc_offsets[rupee_index]
            new_data_end = new_data_start + data_size
            new_texture_data = bytearray(model_xtx)[new_data_start:new_data_end]

            model_xtx = bytearray(model_xtx)
            model_xtx[green_data_start:green_data_end] = new_texture_data
            rupee_arc.set_file_data("g3d/model.xtx", model_xtx)

        write_bytes_create_dirs(
            CACHE_OARC_PATH / shop_rupee_arc_names[rupee_index], rupee_arc.build_U8()
        )


def patch_logo(output_path: Path):
    print_progress_text("Patching Title Screen Logo")
    logo_data = (RANDO_ROOT_PATH / "assets" / "sshdr-logo.tpl").read_bytes()
    rogo_03_data = (RANDO_ROOT_PATH / "assets" / "th_rogo_03.tpl").read_bytes()
    rogo_04_data = (RANDO_ROOT_PATH / "assets" / "th_rogo_04.tpl").read_bytes()

    # Write title screen logo
    title_2d_arc = U8File.get_parsed_U8_from_path(TITLE2D_SOURCE_PATH)
    title_2d_arc.set_file_data("timg/tr_wiiKing2Logo_00.tpl", logo_data)
    title_2d_arc.set_file_data("timg/th_rogo_03.tpl", rogo_03_data)
    title_2d_arc.set_file_data("timg/th_rogo_04.tpl", rogo_04_data)

    # Fix size of rogo stuff (makes the logo text shiny)
    if lyt_file := title_2d_arc.get_file_data("blyt/titleBG_00.brlyt"):
        # Changes the size of the P_loop_00, P_auraR_03, and P_auraR_00 lyt elements
        lyt_file = lyt_file.replace(
            b"\x43\xa4\xc0\x00\x43\x37", b"\x43\xa4\xc0\x00\x43\x69"
        )
        title_2d_arc.set_file_data("blyt/titleBG_00.brlyt", lyt_file)

    write_bytes_create_dirs(
        output_path / "Layout" / "Title2D.arc", title_2d_arc.build_U8()
    )

    # Write credits logo
    print_progress_text("Patching Credits Logo")
    endroll_arc = U8File.get_parsed_U8_from_path(ENDROLL_SOURCE_PATH)
    endroll_arc.set_file_data("timg/th_zeldaRogoEnd_02.tpl", logo_data)
    endroll_arc.set_file_data("timg/th_rogo_03.tpl", rogo_03_data)
    endroll_arc.set_file_data("timg/th_rogo_04.tpl", rogo_04_data)

    # Fix size of rogo stuff (makes the logo text shiny)
    if lyt_file := endroll_arc.get_file_data("blyt/endTitle_00.brlyt"):
        # Changes the size of the P_loop_00, and P_auraR_00 lyt elements
        lyt_file = lyt_file.replace(
            b"\x9a\x40\x49\x99\x9a\x43\x13\x80\x00\x42\xa2",
            b"\x99\x40\x49\x99\x99\x43\x13\x80\x00\x42\xce",
        )
        endroll_arc.set_file_data("blyt/endTitle_00.brlyt", lyt_file)

    write_bytes_create_dirs(
        output_path / "Layout" / "EndRoll.arc", endroll_arc.build_U8()
    )


def patch_tablet_ui(output_path: Path):
    print_progress_text("Patching Tablet UI")
    menu_pause_path = ROMFS_EXTRACT_PATH / "Layout" / "MenuPause.arc"
    menu_pause_arc = U8File.get_parsed_U8_from_path(menu_pause_path)
    brlan_data = (
        RANDO_ROOT_PATH / "assets" / "tablets" / "pause_00_sekiban.brlan"
    ).read_bytes()
    menu_pause_arc.add_file_data("anim/pause_00_sekiban.brlan", brlan_data)

    for suffix in ("3", "4", "5", "6"):
        name = f"tr_sekiban_0{suffix}.tpl"
        tpl_data = (RANDO_ROOT_PATH / "assets" / "tablets" / name).read_bytes()
        menu_pause_arc.add_file_data("timg/" + name, tpl_data)

    write_bytes_create_dirs(
        output_path / "Layout" / "MenuPause.arc", menu_pause_arc.build_U8()
    )
