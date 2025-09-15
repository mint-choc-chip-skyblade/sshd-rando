import hashlib
import shutil
import time
from constants.verificationconstants import BZS_FILE_HASHES
from patches.stagepatchhelper import patch_additional_properties
from util.arguments import get_program_args
from gui.dialogs.dialog_header import (
    get_progress_value_from_range,
    print_progress_text,
    update_progress_value,
)
from patches.conditionalpatchhandler import ConditionalPatchHandler
from patches.othermods import (
    get_resolved_game_file_path,
)
from sslib.bzs import parse_bzs, build_bzs, get_entry_from_bzs, get_highest_object_id
from sslib.utils import mask_shift_set, write_bytes_create_dirs
from sslib.yaml import yaml_load
from sslib.u8file import U8File
from logic.world import World

from collections import defaultdict
from pathlib import Path
import json
import os
import random

from constants.tboxsubtypes import VANILLA_TBOX_SUBTYPES
from constants.patchconstants import (
    DEFAULT_PATH,
    DEFAULT_PNT,
    DEFAULT_SOBJ,
    DEFAULT_OBJ,
    DEFAULT_SCEN,
    DEFAULT_PLY,
    DEFAULT_AREA,
    STAGE_OBJECT_NAMES,
    VALID_STAGE_PATCH_TYPES,
)

from filepathconstants import (
    BZS_TEMPLATE_PATH,
    CACHE_BZS_PATH,
    CACHE_OARC_PATH,
    CACHE_PATH,
    OTHER_MODS_PATH,
    STAGE_FILES_PATH,
    STAGE_PATCHES_PATH,
    EXTRACTS_PATH,
    OBJECTPACK_PATH,
)

args = get_program_args()


def patch_tbox(
    bzs: dict, itemid: int, object_id_str: str, trapid: int, tbox_subtype: int
):
    id = int(object_id_str)
    tbox: dict | None = next(
        filter(lambda x: x["name"] == "TBox" and (x["anglez"] >> 9) == id, bzs["OBJS"]),
        None,
    )

    if tbox is None:
        raise Exception(f"No TBox with id '{id}' found to patch.")

    # Need to check this as itemid is the itemid of the fake item model when trapid > 0
    if trapid:
        trapbits = 254 - trapid
        # Unsets bit 0xF0000000 of params2
        tbox["params2"] = mask_shift_set(tbox["params2"], 0xF, 28, trapbits)
    else:
        # Makes sure the bit is set if not a trap
        tbox["params2"] = mask_shift_set(tbox["params2"], 0xF, 28, 0xF)

    original_itemid = tbox["anglez"] & 0x1FF

    # Patch chest subtype
    #
    ## 0 = Big Blue Chest
    ## 1 = Small Brown Chest
    ## 2 = Fancy Boss Key Chest
    ## 3 = Goddess Chest
    vanilla_tbox_subtype = VANILLA_TBOX_SUBTYPES[original_itemid]

    if vanilla_tbox_subtype == 3:
        # Goddess Chests (subtype 0x03) expect the signed negative number of
        # the item id for the item they have (for some reason)
        # 9 bits means 2^9 - 1 = 511
        itemid = 511 - itemid
        tbox_subtype = 3
    elif tbox_subtype == -1:
        tbox_subtype = vanilla_tbox_subtype

    tbox["params1"] = mask_shift_set(tbox["params1"], 0x3, 4, tbox_subtype)

    # Patch itemid
    tbox["anglez"] = mask_shift_set(tbox["anglez"], 0x1FF, 0, itemid)


def patch_freestanding_item(
    bzs: dict,
    itemid: int,
    object_id_str: str,
    trapid: int,
    custom_flag: int,
    original_itemid: int,
):
    id = int(object_id_str, 0)
    freestanding_item: dict | None = next(
        filter(
            lambda x: x["name"] == "Item"
            and (((x["params1"] >> 10) & 0xFF) == id or x["id"] == id),
            bzs["OBJ "],
        ),
        None,
    )
    if freestanding_item is None:
        raise Exception(
            f"No freestanding item with id '{id}({hex(id)})' found to patch."
        )

    # Need to check this as itemid is the itemid of the fake item model when trapid > 0
    if trapid:
        trapbits = 254 - trapid
        # Unsets bit 0x000000F0 of params2
        freestanding_item["params2"] = mask_shift_set(
            freestanding_item["params2"], 0xF, 4, trapbits
        )
    else:
        # Makes sure the bit is set if not a trap
        freestanding_item["params2"] = mask_shift_set(
            freestanding_item["params2"], 0xF, 4, 0xF
        )

    freestanding_item["params1"] = mask_shift_set(
        freestanding_item["params1"], 0xFF, 0, itemid
    )

    # Unset 9th bit of param1 to force a textbox for freestanding items.
    freestanding_item["params1"] = mask_shift_set(
        freestanding_item["params1"], 0x1, 9, 0
    )

    if custom_flag != -1:
        freestanding_item["params2"] = mask_shift_set(
            freestanding_item["params2"], 0x3FF, 8, custom_flag
        )
        freestanding_item["params2"] = mask_shift_set(
            freestanding_item["params2"], 0x3F, 18, original_itemid
        )


def patch_dusk_relic(
    bzs: dict,
    itemid: int,
    object_id_and_scene_flag_str: str,
    trapid: int,
) -> None:

    # Don't change anything if this is a dusk relic
    if itemid == 168:
        return

    object_id_str, sceneflag_str = object_id_and_scene_flag_str.split("-")
    id = int(object_id_str, 0)
    scene_flag = int(sceneflag_str, 0)

    freestanding_item: dict | None = next(
        filter(
            lambda x: x["name"] == "AncJwls" and x["id"] == id,
            bzs["OBJ "],
        ),
        None,
    )
    if freestanding_item is None:
        raise Exception(
            f"No freestanding item with id '{id}({hex(id)})' found to patch."
        )

    # Need to check this as itemid is the itemid of the fake item model when trapid > 0
    if trapid:
        trapbits = 254 - trapid
        # Unsets bit 0x000000F0 of params2
        freestanding_item["params2"] = mask_shift_set(
            freestanding_item["params2"], 0xF, 4, trapbits
        )
    else:
        # Makes sure the bit is set if not a trap
        freestanding_item["params2"] = mask_shift_set(
            freestanding_item["params2"], 0xF, 4, 0xF
        )

    # Change the actor into an Item instead of AncJwls
    freestanding_item["name"] = "Item"

    # Set the scene flag and item id to use in the params
    params1 = 0xFF9C0200
    params1 = mask_shift_set(params1, 0xFF, 0, itemid)
    params1 = mask_shift_set(params1, 0xFF, 10, scene_flag)
    # Unset 9th bit of param1 to force a textbox for freestanding items.
    params1 = mask_shift_set(params1, 0x1, 9, 0)

    freestanding_item["params1"] = params1


def patch_bucha(bzs: dict, itemid: int, object_id_str: str, trapid: int):
    id = int(object_id_str, 16)
    bucha: dict | None = next(
        filter(lambda x: x["name"] == "NpcKyuE" and x["id"] == id, bzs["OBJ "]), None
    )

    if bucha is None:
        raise Exception(f"Bucha's id '{id}' not found. Cannot patch this check.")

    # Need to check this as itemid is the itemid of the fake item model when trapid > 0
    if trapid:
        trapbits = 254 - trapid
        # Unsets bit 0x000000F0 of params2
        bucha["params2"] = mask_shift_set(bucha["params2"], 0xF, 4, trapbits)
    else:
        # Makes sure the bit is set if not a trap
        bucha["params2"] = mask_shift_set(bucha["params2"], 0xF, 4, 0xF)

    bucha["params2"] = mask_shift_set(bucha["params2"], 0xFF, 0x8, itemid)


def patch_closet(
    bzs: dict, itemid: int, object_id_str: str, trapid: int, room: int, stage: str
):
    id = int(object_id_str, 16)
    closet: dict | None = next(
        filter(lambda x: x["name"] == "chest" and x["id"] == id, bzs["OBJ "]),
        None,
    )

    if closet is None:
        raise Exception(f"No closet with id '{id}' found to patch.")

    # Need to check this as itemid is the itemid of the fake item model when trapid > 0
    if trapid:
        trapbits = 254 - trapid
        # Unsets bit 0x000000F0 of params2
        closet["params2"] = mask_shift_set(closet["params2"], 0xF, 4, trapbits)
    else:
        # Makes sure the bit is set if not a trap
        closet["params2"] = mask_shift_set(closet["params2"], 0xF, 4, 0xF)

    # Mapping of each closet (scene, roomid, objectid) to the local scene flag we'll use
    unused_scene_flags: dict[tuple[str, int, int], int] = {
        ("F001r", 1, 0xFC08): 12,  # Link's Closet            0x10
        ("F001r", 1, 0xFC07): 24,  # Fledge's Closet          2x01
        ("F001r", 6, 0xFC07): 32,  # Zelda's Closet           5x01 (vanilla scene flag)
        ("F001r", 2, 0xFC03): 48,  # Groose's Closet          7x01
        ("F001r", 5, 0xFC05): 50,  # Owlan's Closet           7x04
        ("F001r", 4, 0xFC03): 57,  # Horwell's Closet         6x02
        ("F001r", 6, 0xFC06): 61,  # Karane's Closet          6x20
        ("F005r", 0, 0xFC0E): 81,  # O&P's Closet             Bx02
        ("F006r", 0, 0xFC16): 82,  # Kukiel's Closet          Bx04
        ("F013r", 0, 0xFC0E): 100,  # Sparrot's Closet        Dx10
        ("F014r", 0, 0xFC12): 101,  # Luv and Bertie's Closet Dx20
        ("F015r", 0, 0xFC10): 105,  # Gondo's Closet          Cx02
        ("F016r", 0, 0xFC28): 107,  # Pipit's Closet          Cx04
        ("F017r", 0, 0xFC1E): 116,  # Rupin's Closet          Fx10
        ("F018r", 0, 0xFC11): 117,  # Peater's Closet         Fx20
        ("F018r", 0, 0xFC12): 118,  # Peatrice's Closet       Fx40
        ("F011r", 0, 0xFC3B): 3,  # Pumm and Kina's Closet    1x08
        ("F301_5", 0, 0xFC0C): 0,  # Skipper's Closet         2x01
    }

    # Specify which scene flag to use
    closet["params1"] = mask_shift_set(
        closet["params1"], 0xFF, 0, unused_scene_flags[(stage, room, id)]
    )
    # Patch in the item
    closet["params1"] = mask_shift_set(closet["params1"], 0xFF, 8, itemid)
    # Tell the closet to interpret the flag as a local scene flag
    closet["params1"] = mask_shift_set(closet["params1"], 0x1, 16, 1)


def patch_ac_key_boko(bzs: dict, itemid: int, object_id_str: str, trapid: int):
    id = int(object_id_str, 16)
    boko: dict | None = next(
        filter(lambda x: x["name"] == "EBc" and x["id"] == id, bzs["OBJ "]), None
    )

    if boko is None:
        raise Exception(f"No Bokoblin (EBc) with id '{id}' found to patch.")

    # Need to check this as itemid is the itemid of the fake item model when trapid > 0
    if trapid:
        trapbits = 254 - trapid
        # Unsets bit 0x000000F0 of params2
        boko["params2"] = mask_shift_set(boko["params2"], 0xF, 8, trapbits)
    else:
        # Makes sure the bit is set if not a trap
        boko["params2"] = mask_shift_set(boko["params2"], 0xF, 8, 0xF)

    boko["params2"] = mask_shift_set(boko["params2"], 0xFF, 0x0, itemid)


def patch_heart_container(bzs: dict, itemid: int, trapid: int):
    heart_container: dict | None = next(
        filter(lambda x: x["name"] == "HeartCo", bzs["OBJ "]), None
    )

    if heart_container is None:
        raise Exception(f"No heart container found to patch.")

    # Need to check this as itemid is the itemid of the fake item model when trapid > 0
    if trapid:
        trapbits = 254 - trapid
        # Unsets bit 0x000000F0 of params2
        heart_container["params2"] = mask_shift_set(
            heart_container["params2"], 0xF, 8, trapbits
        )
    else:
        # Makes sure the bit is set if not a trap
        heart_container["params2"] = mask_shift_set(
            heart_container["params2"], 0xF, 8, 0xF
        )

    heart_container["params1"] = mask_shift_set(
        heart_container["params1"], 0xFF, 16, itemid
    )


def patch_chandelier_item(bzs: dict, itemid: int, trapid: int):
    chandelier: dict | None = next(
        filter(lambda x: x["name"] == "Chandel", bzs["OBJ "]), None
    )

    if chandelier is None:
        raise Exception(f"No chandelier found to patch.")

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = 34  # rupoor

    chandelier["params1"] = mask_shift_set(chandelier["params1"], 0xFF, 8, itemid)


def patch_tree_of_life(bzs: dict, itemid: int, trapid: int):
    tree: dict | None = next(
        filter(lambda x: x["name"] == "FrtTree", bzs["OBJ "]), None
    )

    if tree is None:
        raise Exception(f"No FrtTree (Tree of Life) found to patch.")

    # Need to check this as itemid is the itemid of the fake item model when trapid > 0
    if trapid:
        trapbits = 254 - trapid
        # Unsets bit 0x000000F0 of params2
        tree["params2"] = mask_shift_set(tree["params2"], 0xF, 4, trapbits)
    # No need for other checks as params2 is always 0xFFFFFFFF

    tree["params1"] = mask_shift_set(tree["params1"], 0xFF, 24, itemid)


def patch_digspot_item(bzs: dict, itemid: int, object_id_str: str, trapid: int):
    id = int(object_id_str)
    digspot: dict | None = next(
        filter(
            lambda x: x["name"] == "Soil" and ((x["params1"] >> 4) & 0xFF) == id,
            bzs["OBJ "],
        ),
        None,
    )

    if digspot is None:
        raise Exception(f"No digspot with id '{id}' found to patch.")

    # Need to check this as itemid is the itemid of the fake item model when trapid > 0
    if trapid:
        trapbits = 254 - trapid
        # Unsets bit 0x000000F0 of params2
        digspot["params2"] = mask_shift_set(digspot["params2"], 0xF, 8, trapbits)
    else:
        # Makes sure the bit is set if not a trap
        digspot["params2"] = mask_shift_set(digspot["params2"], 0xF, 8, 0xF)

    # patch digspot to be the same as key piece digspots in all ways except it keeps it's initial sceneflag
    digspot["params1"] = (digspot["params1"] & 0xFF0) | 0xFF0B1004
    digspot["params2"] = mask_shift_set(digspot["params2"], 0xFF, 0x18, itemid)


def patch_goddess_crest(bzs: dict, itemid: int, index: str, trapid: int):
    crest: dict | None = next(filter(lambda x: x["name"] == "SwSB", bzs["OBJ "]), None)

    if crest is None:
        raise Exception(f"No goddess crest found to patch.")

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = 34  # rupoor

    # 3 items patched into same object at different points in the params
    if index == "0":
        crest["params1"] = mask_shift_set(crest["params1"], 0xFF, 0x18, itemid)
    elif index == "1":
        crest["params1"] = mask_shift_set(crest["params1"], 0xFF, 0x10, itemid)
    elif index == "2":
        crest["params2"] = mask_shift_set(crest["params2"], 0xFF, 0x18, itemid)


def patch_squirrels(bzs: dict, itemid: int, object_id_str: str, trapid: int):
    id = int(object_id_str, 16)

    squirrel_tag: dict | None = next(
        filter(lambda x: x["name"] == "MssbTag" and x["id"] == id, bzs["STAG"]), None
    )

    if squirrel_tag is None:
        raise Exception(f"No squirrel tag (MssbTag) found to patch.")

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = 34  # rupoor

    squirrel_tag["params2"] = mask_shift_set(squirrel_tag["params2"], 0xFF, 0, itemid)

    squirrel_id_to_sceneflag = {
        0xFCC8: 88,  # 0xA 01
        0xFC9C: 89,  # 0xA 02
        0xFCA0: 90,  # 0xA 04
    }
    squirrel_tag["params2"] = mask_shift_set(
        squirrel_tag["params2"], 0xFF, 8, squirrel_id_to_sceneflag[id]
    )


def patch_tadtone_group(bzs: dict, itemid: int, groupid_str: str, trapid: int):
    groupid = int(groupid_str, 0)
    clefs = filter(
        lambda x: x["name"] == "Clef" and ((x["params1"] >> 3) & 0x1F) == groupid,
        bzs["OBJ "],
    )

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = 34  # rupoor

    for clef in clefs:
        clef["anglez"] = mask_shift_set(clef["anglez"], 0xFFFF, 0, itemid)


def patch_trial_gate(bzs: dict, itemid: int, trapid: int):
    trial_gate: dict | None = next(
        filter(lambda x: x["name"] == "WarpObj", bzs["OBJ "]), None
    )

    if trial_gate is None:
        raise Exception(f"No WarpObj found to patch.")

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = 34  # rupoor

    trial_gate["params1"] = mask_shift_set(trial_gate["params1"], 0xFF, 0x18, itemid)


def patch_tgreact(
    bzs: dict, itemid: int, object_id_str: str, trapid: int, custom_flag: int
):
    id = int(object_id_str, 16)

    tgreact: dict | None = next(
        filter(lambda x: x["name"] == "TgReact" and x["id"] == id, bzs["SOBJ"]), None
    )

    if tgreact is None:
        raise Exception(
            f"No tag reaction (TgReact) with id '{hex(id)}' found to patch."
        )

    # Need to check this as itemid is the itemid of the fake item model when trapid > 0
    if trapid:
        trapbits = 254 - trapid
        # Unsets bit 0x00780000 of params2
        tgreact["params2"] = mask_shift_set(tgreact["params2"], 0xF, 19, trapbits)
    else:
        # Makes sure the bit is set if not a trap
        tgreact["params2"] = mask_shift_set(tgreact["params2"], 0xF, 19, 0xF)

    # Move vanilla velocity type indicator to free space in params2
    if (tgreact["params1"] >> 8) & 0xFF == 0:
        tgreact["params2"] = mask_shift_set(tgreact["params2"], 1, 18, 1)
    else:
        tgreact["params2"] = mask_shift_set(tgreact["params2"], 1, 18, 0)

    # THEN, patch item id
    tgreact["params1"] = mask_shift_set(tgreact["params1"], 0xFF, 8, itemid)

    if custom_flag != -1:
        tgreact["params2"] = mask_shift_set(tgreact["params2"], 0x3FF, 8, custom_flag)
    else:
        tgreact["params2"] = mask_shift_set(tgreact["params2"], 0x3FF, 8, 0x3FF)


def patch_academy_bell(bzs: dict, itemid: int, trapid: int):

    academy_bell: dict | None = next(
        filter(lambda x: x["name"] == "Bell", bzs["OBJ "]), None
    )

    if academy_bell is None:
        raise Exception(f"No Bell found to patch.")

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = 34  # rupoor

    academy_bell["params1"] = mask_shift_set(academy_bell["params1"], 0xFF, 0, itemid)


def patch_hrphint(bzs: dict, itemid: int, object_id_str: str, trapid: int):
    id = int(object_id_str, 16)

    hrphint: dict | None = next(
        filter(lambda x: x["name"] == "HrpHint" and x["id"] == id, bzs["OBJ "]), None
    )

    if hrphint is None:
        raise Exception(
            f"No gossip stone (HrpHint) with id '{hex(id)}' found to patch."
        )

    # Need to check this as itemid is the itemid of the fake item model when trapid > 0
    if trapid:
        trapbits = 254 - trapid
        # Unsets bit 0x000000F0 of params2
        hrphint["params2"] = mask_shift_set(hrphint["params2"], 0xF, 0, trapbits)
    else:
        # Makes sure the bit is set if not a trap
        hrphint["params2"] = mask_shift_set(hrphint["params2"], 0xF, 0, 0xF)

    hrphint["params2"] = mask_shift_set(hrphint["params2"], 0xFF, 4, itemid)


def object_add(bzs: dict, object_add: dict, nextid: int) -> int:
    layer = object_add.get("layer", None)
    object_type: str = object_add["objtype"].ljust(4)
    obj: dict = object_add["object"]
    return_nextid_increment = 0

    # populate with default object as a base
    if object_type in ["SOBS", "SOBJ", "STAS", "STAG", "SNDT"]:
        new_object = DEFAULT_SOBJ.copy()
    elif object_type in ["OBJS", "OBJ ", "DOOR"]:
        new_object = DEFAULT_OBJ.copy()
    elif object_type == "SCEN":
        new_object = DEFAULT_SCEN.copy()
    elif object_type == "PLY ":
        new_object = DEFAULT_PLY.copy()
    elif object_type == "AREA":
        new_object = DEFAULT_AREA.copy()
    else:
        raise Exception(
            f"Cannot add object with unknown objtype: {object_type}.\nObject: {obj}\nPatch: {object_add}"
        )

    # check index to verify new index is the next available index
    if "index" in obj:
        if layer is None:
            object_list = bzs.get(object_type, [])
        else:
            object_list = bzs["LAY "][f"l{layer}"].get(object_type, [])

        if len(object_list) != obj["index"]:
            raise Exception(
                f"Cannot use wrong index on added object: {json.dumps(object_add)}"
            )

    # Assign the name first so additional properties can be listed in any order
    if obj_name := obj.get("name"):
        new_object["name"] = obj_name

    # populate provided properties
    for prop, value in obj.items():
        if prop in new_object:
            new_object[prop] = value

            if prop == "id":
                new_object["id"] = (new_object["id"] & ~0x3FF) | (
                    nextid + return_nextid_increment
                )
                return_nextid_increment += 1
        # Allow creating new objects that *need* a known id
        elif prop == "hardcoded_id":
            new_object["id"] = value
        else:
            patch_additional_properties(obj=new_object, prop=prop, value=value)

    if new_object.get("id") == 0:
        new_object["id"] = nextid + return_nextid_increment
        return_nextid_increment += 1

    # Prevent ammo pots getting ids that collide with viewclip indexes
    if new_object.get("name") == "Tubo":
        id = new_object.get("id", -1)

        if id != -1 and id < 0xF000:
            new_object["id"] = id | 0xF000

    # creates list for object types if don't already exist in bzs
    if layer is None:
        if object_type not in bzs:  # check
            bzs[object_type] = []

        object_list = bzs[object_type]
    else:
        if object_type not in bzs["LAY "][f"l{layer}"]:
            bzs["LAY "][f"l{layer}"][object_type] = []

        object_list = bzs["LAY "][f"l{layer}"][object_type]

    # add object name to objn if it's some type of actor
    if object_type in STAGE_OBJECT_NAMES:
        # Add layer if it doesn't already exist
        if not bzs["LAY "].get(f"l{layer}"):
            bzs["LAY "][f"l{layer}"] = []

        if not "OBJN" in bzs["LAY "][f"l{layer}"]:
            bzs["LAY "][f"l{layer}"]["OBJN"] = []

        objn = bzs["LAY "][f"l{layer}"]["OBJN"]

        if (obj_name := obj.get("name")) is None:
            raise Exception(
                f"Cannot add an object without a name field (actor name).\nObject: {obj}\nPatch: {object_add}"
            )

        if not obj_name in objn:
            objn.append(obj_name)

    object_list.append(new_object)
    return return_nextid_increment


def object_handle_list_props(object: dict, ids: list, current_id_index: int) -> dict:
    new_object = object.copy()
    new_object["ids"] = []
    new_object["id"] = ids[current_id_index]

    # Allows batch handling of objects across multiple layers
    if len(layers := object.get("layers", [])) > 0:
        if not isinstance(layers, list):
            raise Exception(
                f"Cannot handle object as property 'layers' is not a list: {object}."
            )

        if len(layers) != len(ids):
            raise Exception(
                f"Cannot handle object as number of layers is different to number of ids: {object}."
            )

        new_object["layers"] = []
        new_object["layer"] = layers[current_id_index]

    # Allows batch handling of objects across multiple rooms
    if len(rooms := object.get("rooms", [])) > 0:
        assert isinstance(rooms, list)

        if len(rooms) != len(ids):
            raise Exception(
                f"Cannot handle object as number of rooms is different to number of ids: {object}."
            )

        new_object["rooms"] = []
        new_object["room"] = rooms[current_id_index]

    # Allows batch handling of objects of different types
    if len(objtypes := object.get("objtypes", [])) > 0:
        assert isinstance(objtypes, list)

        if len(objtypes) != len(ids):
            raise Exception(
                f"Cannot handle object as number of rooms is different to number of ids: {object}."
            )

        new_object["objtypes"] = []
        new_object["objtype"] = objtypes[current_id_index]

    if not isinstance(new_object["layer"], int):
        raise Exception(
            f"Cannot handle object with a non-integer layer ({new_object['layer']}).\nObject: {new_object}\nPatch: {object}"
        )

    if not isinstance(new_object["room"], int):
        raise Exception(
            f"Cannot handle object with a non-integer room ({new_object['room']}).\nObject: {new_object}\nPatch: {object}"
        )

    if not isinstance(new_object["objtype"], str):
        raise Exception(
            f"Cannot handle object with a non-string objtype ({new_object['objtype']}).\nObject: {new_object}\nPatch: {object}"
        )

    return new_object


def object_delete(bzs: dict, object_delete: dict):
    ids: list = object_delete.get("ids", [])
    start_obj_id = object_delete.get("startid")
    end_obj_id = object_delete.get("endid")

    if id := object_delete.get("id"):
        ids.append(id)

    if start_obj_id and end_obj_id:
        if start_obj_id > end_obj_id:
            raise Exception(
                f"Cannot perform objdelete because startid ({start_obj_id}) is bigger than endid ({end_obj_id})."
            )

        for obj_id in range(start_obj_id, end_obj_id + 1):
            ids.append(obj_id)

    for id_index in range(len(ids)):
        object_to_delete = object_handle_list_props(object_delete, ids, id_index)
        obj = get_entry_from_bzs(bzs=bzs, object_def=object_to_delete, remove=True)

        if obj is None:
            raise Exception(
                f"Cannot find object:\nObject {obj}\nPatch: {object_delete}"
            )


def object_patch(bzs: dict, object_patch: dict):
    obj = get_entry_from_bzs(bzs=bzs, object_def=object_patch)

    if obj is not None:
        for prop, value in object_patch["object"].items():
            if prop in obj:
                obj[prop] = value
            else:
                patch_additional_properties(obj=obj, prop=prop, value=value)


def object_move(bzs: dict, object_move: dict, nextid: int) -> int:
    ids: list = object_move.get("ids", [])
    start_obj_id = object_move.get("startid")
    end_obj_id = object_move.get("endid")

    if id := object_move.get("id"):
        ids.append(id)

    if start_obj_id and end_obj_id:
        if start_obj_id > end_obj_id:
            raise Exception(
                f"Cannot perform objmove because startid ({start_obj_id}) is bigger than endid ({end_obj_id})."
            )

        for obj_id in range(start_obj_id, end_obj_id + 1):
            ids.append(obj_id)

    destination_layer = object_move["destlayer"]
    return_nextid_increment = 0

    for id_index in range(len(ids)):
        object_to_move = object_handle_list_props(object_move, ids, id_index)

        obj = get_entry_from_bzs(bzs=bzs, object_def=object_to_move, remove=True)

        if obj is None:
            raise Exception(
                f"Cannot find object to move: {object_to_move}.\nPatch: {object_move}"
            )

        object_type = object_to_move["objtype"].ljust(4)

        # Allow moving objects that *need* a specific id
        if hardcoded_id := object_move.get("hardcoded_id"):
            obj["id"] = hardcoded_id + id_index
        else:
            obj["id"] = (obj["id"] & ~0x3FF) | nextid
            return_nextid_increment += 1
            nextid += 1

        if not object_type in bzs["LAY "][f"l{destination_layer}"]:
            bzs["LAY "][f"l{destination_layer}"][object_type] = []

        bzs["LAY "][f"l{destination_layer}"][object_type].append(obj)

        if not "OBJN" in bzs["LAY "][f"l{destination_layer}"]:
            bzs["LAY "][f"l{destination_layer}"]["OBJN"] = []

        objn = bzs["LAY "][f"l{destination_layer}"]["OBJN"]

        if not obj["name"] in objn:
            objn.append(obj["name"])

    return return_nextid_increment


def pathadd(bzs: dict, path: dict):
    next_pnt = len(bzs["PNT "])

    new_path = DEFAULT_PATH.copy()
    new_path["pnt_start_idx"] = next_pnt
    new_path["pnt_total_count"] = len(path["pnts"])
    bzs["PATH"].append(new_path)

    pnts_to_add = path["pnts"]

    for pnt in pnts_to_add:
        new_pnt = DEFAULT_PNT.copy()

        for key, val in pnt.items():
            if key in new_pnt:
                new_pnt[key] = val

        bzs["PNT "].append(new_pnt)


def layer_override(bzs: dict, patch: dict):
    layer_override = [
        {
            "story_flag": override["story_flag"],
            "night": override["night"],
            "layer": override["layer"],
        }
        for override in patch["override"]
    ]

    bzs["LYSE"] = layer_override


def arcn_add(bzs: dict, patch: dict):
    arcn: list[str] | None = patch.get("arcn", None)

    if arcn == None:
        raise Exception(
            f"Could not find 'arcn' from patch. Did you typo the 'arcn' field?\nPatch: {patch}"
        )

    arcn_set: set[str] = set(bzs.get("ARCN", []))
    arcn_set |= set(arcn)
    bzs["ARCN"] = list(arcn_set)
    # print(patch["layer"], patch["room"], bzs["ARCN"])


class StagePatchHandler:
    def __init__(self, output_path: Path, other_mods: list[str] = []):
        self.base_output_path = output_path
        self.stage_output_path = self.base_output_path / "Stage"
        self.stage_patches: dict[str, list[dict]] = yaml_load(STAGE_PATCHES_PATH)  # type: ignore
        self.check_patches: dict[str, list[tuple]] = defaultdict(list)
        self.other_mods = other_mods

    def handle_stage_patches(self, onlyif_handler: ConditionalPatchHandler):
        for stage in self.stage_patches:
            for patch in self.stage_patches[stage]:
                if not patch.get("type"):
                    raise Exception(f"Patch doesn't have a 'type' field: {patch}")
                if patch["type"] not in VALID_STAGE_PATCH_TYPES:
                    exception_str = (
                        f"Invalid patch with type '{patch['type']}' found.\n"
                    )
                    exception_str += f"Valid patch types: {VALID_STAGE_PATCH_TYPES}\n"
                    exception_str += f"Patch: {patch}"
                    raise Exception(exception_str)

        # Pre-emptively remove unecessary patches since we can't pass
        # the onlyif_handler to other worker processes
        print("Removing unecessary patches")
        self.remove_unnecessary_patches(onlyif_handler)

        start_stage_patching_time = time.process_time()

        bzs_u8 = U8File.get_parsed_U8_from_path(BZS_TEMPLATE_PATH)
        bzs_cache_stage_paths = list(CACHE_BZS_PATH.glob("*"))

        for current_stage_num, bzs_cache_path in enumerate(bzs_cache_stage_paths):
            stage_name = bzs_cache_path.name
            patches = self.stage_patches.get(stage_name, [])
            object_patches = []

            print(f"Patching Stage: {stage_name}")

            # handle layer overrides
            layer_override_patches = list(
                filter(lambda patch: patch["type"] == "layeroverride", patches)
            )

            if len(layer_override_patches) > 1:
                raise Exception(
                    f"Multiple layeroverrides found. {len(layer_override_patches)} layer overrides found for stage {stage_name}, expected 1."
                )

            stage_bzs_bytes = (bzs_cache_path / "stage.bzs").read_bytes()
            stage_bzs = parse_bzs(stage_bzs_bytes)

            if len(layer_override_patches) == 1:
                layer_override(bzs=stage_bzs, patch=layer_override_patches[0])

            bzs_u8.add_file_data(f"dat/{stage_name}_stage.bzs", build_bzs(stage_bzs))

            for obj_patch in filter(
                lambda patch: patch["type"]
                in [
                    "objadd",
                    "objdelete",
                    "objpatch",
                    "objmove",
                    "pathadd",
                    "arcnadd",
                ],
                patches,
            ):
                object_patches.append(obj_patch)

            for room_bzs_path in (CACHE_BZS_PATH / stage_name).glob("room*"):
                roomid = int(room_bzs_path.name.split(".bzs")[0][5:])

                obj_patches_for_current_room = list(
                    filter(
                        lambda patch: patch.get("room") == roomid,
                        object_patches,
                    )
                )
                check_patches_for_current_room = list(
                    filter(
                        lambda patch: patch[0] == roomid,
                        self.check_patches[stage_name],
                    )
                )

                room_bzs_bytes = room_bzs_path.read_bytes()
                room_bzs = parse_bzs(room_bzs_bytes)

                nextid = get_highest_object_id(bzs=room_bzs) + 1

                for patch in obj_patches_for_current_room:
                    patch_type = patch.get("type", None)
                    if patch_type == None:
                        raise Exception(
                            f"Patch is missing a 'type' field and cannot be processed.\nPatch: {patch}"
                        )
                    elif type(patch_type) != str:
                        raise Exception(
                            f"Patch field 'type' is not a string. Found '{type(patch_type)}' instead.\nPatch{patch}"
                        )

                    if patch_type == "objadd":
                        nextid += object_add(
                            bzs=room_bzs,
                            object_add=patch,
                            nextid=nextid,
                        )
                    elif patch_type == "objdelete":
                        object_delete(bzs=room_bzs, object_delete=patch)
                    elif patch_type == "objpatch":
                        object_patch(bzs=room_bzs, object_patch=patch)
                    elif patch_type == "objmove":
                        nextid += object_move(
                            bzs=room_bzs,
                            object_move=patch,
                            nextid=nextid,
                        )
                    elif patch_type == "pathadd":
                        pathadd(bzs=room_bzs, path=patch)
                    elif patch_type == "arcnadd":
                        arcn_add(
                            bzs=room_bzs["LAY "][f"l{patch['layer']}"], patch=patch
                        )
                    else:
                        raise Exception(
                            f"Unsupported patch type '{patch_type}' found.\nPatch: {patch}"
                        )

                for (
                    room,
                    object_name,
                    layer,
                    objectid,
                    itemid,
                    trapid,
                    custom_flag,
                    original_itemid,
                    tbox_subtype,
                ) in check_patches_for_current_room:
                    if object_name == "TBox":
                        patch_tbox(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            objectid,
                            trapid,
                            tbox_subtype,
                        )
                    elif object_name == "Item":
                        patch_freestanding_item(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            objectid,
                            trapid,
                            custom_flag,
                            original_itemid,
                        )
                    elif object_name == "AncJwls":
                        patch_dusk_relic(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            objectid,
                            trapid,
                        )
                    elif object_name == "NpcKyuE":
                        patch_bucha(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            objectid,
                            trapid,
                        )
                    elif object_name == "chest":
                        patch_closet(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            objectid,
                            trapid,
                            room,
                            stage_name,
                        )
                    elif object_name == "EBc":
                        patch_ac_key_boko(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            objectid,
                            trapid,
                        )
                    elif object_name == "HeartCo":
                        patch_heart_container(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            trapid,
                        )
                    elif object_name == "Chandel":
                        patch_chandelier_item(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            trapid,
                        )
                    elif object_name == "Soil":
                        patch_digspot_item(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            objectid,
                            trapid,
                        )
                    elif object_name == "SwSB":
                        patch_goddess_crest(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            objectid,
                            trapid,
                        )
                    elif object_name == "MssbTag":
                        patch_squirrels(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            objectid,
                            trapid,
                        )
                    elif object_name == "WarpObj":
                        patch_trial_gate(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            trapid,
                        )
                    elif object_name == "TgReact":
                        patch_tgreact(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            objectid,
                            trapid,
                            custom_flag,
                        )
                    elif object_name == "Bell":
                        patch_academy_bell(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            trapid,
                        )
                    elif object_name == "Clef":
                        patch_tadtone_group(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            objectid,
                            trapid,
                        )
                    elif object_name == "FrtTree":
                        patch_tree_of_life(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            trapid,
                        )
                    elif object_name == "HrpHint":
                        patch_hrphint(
                            room_bzs["LAY "][f"l{layer}"],
                            itemid,
                            objectid,
                            trapid,
                        )
                    else:
                        print(
                            f"Object name: {object_name} not currently supported for check patching."
                        )

                bzs_u8.add_file_data(
                    f"dat/{stage_name}_room_{roomid}.bzs", build_bzs(room_bzs)
                )

            update_progress_value(
                get_progress_value_from_range(
                    80, 20, current_stage_num, len(bzs_cache_stage_paths)
                )
            )

        write_bytes_create_dirs(
            self.base_output_path / "Stage" / "bzs.arc", bzs_u8.build_U8()
        )

        print(
            f"Patching stages took {(time.process_time() - start_stage_patching_time)} seconds"
        )

    def remove_unnecessary_patches(
        self, onlyif_handler: ConditionalPatchHandler
    ) -> None:
        for patches in self.stage_patches.values():
            for patch in patches.copy():
                if statement := patch.get("onlyif", False):
                    if not onlyif_handler.evaluate_onlyif(statement):
                        patches.remove(patch)

    def __extract_bzs_files(self, stage_file_paths):
        for current_stage_file_num, stage_path in enumerate(stage_file_paths):
            stage_name = stage_path.name
            # Ignore non-stage files
            if stage_name not in BZS_FILE_HASHES:
                continue

            print_progress_text(f"Checking cached files for stage: {stage_name}")
            bzs_stage_dir_path = CACHE_BZS_PATH / stage_name
            bzs_stage_dir_path.mkdir(parents=True, exist_ok=True)

            files_to_extract: list[str] = []

            for bzs_file_name in BZS_FILE_HASHES[stage_name]:
                bzs_stage_file_path = bzs_stage_dir_path / bzs_file_name

                if (
                    not bzs_stage_file_path.exists()
                    or BZS_FILE_HASHES[stage_name][bzs_file_name]
                    != hashlib.sha256(bzs_stage_file_path.read_bytes()).hexdigest()
                ):
                    files_to_extract.append(bzs_file_name)

            if len(files_to_extract) > 0:
                for bzs_file_name in files_to_extract:
                    print_progress_text(f"Extracting {bzs_file_name} for {stage_name}")
                    bzs_stage_file_path = bzs_stage_dir_path / bzs_file_name

                    if bzs_stage_file_path.exists():
                        bzs_stage_file_path.unlink()

                    full_stage_path = stage_path / "NX" / f"{stage_name}_stg_l0.arc.LZ"
                    stage_u8 = U8File.get_parsed_U8_from_path(full_stage_path)

                    if bzs_file_name.endswith("stage.bzs"):
                        bzs = stage_u8.get_file_data("dat/stage.bzs")
                    else:
                        roomid = bzs_file_name.split(".bzs")[0][-2:]

                        if roomid.startswith("_"):
                            roomid = "0" + roomid[-1]

                        room_u8 = stage_u8.get_parsed_U8_from_this_U8(
                            f"rarc/{stage_name}_r{roomid}.arc"
                        )
                        bzs = room_u8.get_file_data("dat/room.bzs")

                    if bzs is None:
                        raise Exception(
                            f"Failed to extract data from stage {stage_name}.\nCould not read bzs data for {bzs_stage_file_path}."
                        )

                    if (
                        BZS_FILE_HASHES[stage_name][bzs_file_name]
                        != hashlib.sha256(bzs).hexdigest()
                    ):
                        raise Exception(
                            f"The bzs data extracted from stage {stage_name} is not correct and cannot be used. Please verify your stage files are correct and try again."
                        )

                    bzs_stage_file_path.write_bytes(bzs)

            update_progress_value(
                get_progress_value_from_range(
                    40, 10, current_stage_file_num, len(stage_file_paths)
                )
            )

    def create_cache(self):
        start_cache_time = time.process_time()

        extracts: dict[dict, dict] = yaml_load(EXTRACTS_PATH)  # type: ignore
        CACHE_PATH.mkdir(parents=True, exist_ok=True)
        CACHE_OARC_PATH.mkdir(parents=True, exist_ok=True)
        CACHE_BZS_PATH.mkdir(parents=True, exist_ok=True)

        self.__extract_bzs_files(stage_file_paths=list(STAGE_FILES_PATH.glob("*")))

        print(
            f"Verifying bzs cache took {(time.process_time() - start_cache_time)} seconds"
        )
        start_arc_patching_time = time.process_time()

        mods = [""]  # Empty string represents default game extract
        mods.extend(self.other_mods)

        default_objectpack_u8 = U8File.get_parsed_U8_from_path(OBJECTPACK_PATH)

        # Remove mod cache each time to prevent old mod files from lingering
        for cache_path in CACHE_OARC_PATH.glob("*"):
            if cache_path.is_dir():
                shutil.rmtree(cache_path)

        for mod in mods:
            cache_oarc_path = CACHE_OARC_PATH / mod
            cache_oarc_path.mkdir(parents=True, exist_ok=True)

            objectpack_path, _ = get_resolved_game_file_path(
                OBJECTPACK_PATH, self.other_mods, mod
            )

            for current_extract_num, extract in enumerate(extracts):
                # objectpack is a special case (not a stage)
                if "objectpack" in extract and objectpack_path.exists():
                    arcs = extract["objectpack"]
                    arcs_not_in_cache = [
                        arc_name
                        for arc_name in arcs
                        if not (cache_oarc_path / f"{arc_name}.arc").exists()
                    ]

                    if len(arcs_not_in_cache) == 0:
                        continue

                    # Allow mod makers to put objectpack arcs in "ModName/oarc"
                    mod_object_path = OTHER_MODS_PATH / mod / "oarc"

                    if mod and mod_object_path.exists():
                        for arc_path in mod_object_path.glob("*.arc"):
                            arc_name = arc_path.name
                            shutil.copyfile(
                                mod_object_path / arc_name,
                                cache_oarc_path / arc_name,
                            )
                            print_progress_text(f"Copying {mod}/{arc_name}")

                    # If a mod doesn't have an objectpack, then skip it
                    if mod and OBJECTPACK_PATH.samefile(objectpack_path):
                        continue

                    objectpack_u8 = U8File.get_parsed_U8_from_path(objectpack_path)
                    oarc_path = objectpack_u8.get_oarc_path()

                    for arc_name in arcs_not_in_cache:
                        arc_data = objectpack_u8.get_file_data(
                            f"{oarc_path}/{arc_name}.arc"
                        )

                        if not arc_data:
                            raise TypeError(
                                f"Expected type bytes but found None for {mod}/{arc_name}."
                            )

                        # If we're extracting arcs from a mod, don't rewrite
                        # the arcs if they're the same as the original game
                        if mod:
                            default_arc_data = default_objectpack_u8.get_file_data(
                                f"oarc/{arc_name}.arc"
                            )
                            if arc_data == default_arc_data:
                                continue

                        print_progress_text(
                            f"Extracting {mod + '/' if mod else ''}{arc_name}"
                        )
                        (cache_oarc_path / f"{arc_name}.arc").write_bytes(arc_data)
                else:
                    stage = extract["stage"]

                    for layer in extract["layers"]:
                        layerid = layer["layerid"]
                        arcs = layer["oarcs"]

                        all_already_in_cache = all(
                            ((cache_oarc_path / f"{arc}.arc").exists() for arc in arcs)
                        )

                        if all_already_in_cache:
                            continue

                        original_stage_path = (
                            STAGE_FILES_PATH
                            / f"{stage}"
                            / "NX"
                            / f"{stage}_stg_l{layerid}.arc.LZ"
                        )
                        stage_path, _ = get_resolved_game_file_path(
                            original_stage_path, self.other_mods, mod
                        )

                        # If this mod doesn't have the specified stage file, then skip it
                        if mod and os.path.samefile(original_stage_path, stage_path):
                            continue

                        stage_u8 = U8File.get_parsed_U8_from_path(stage_path)
                        oarc_path = stage_u8.get_oarc_path()

                        # If we're extracting from a mod, get the original game's stage file to compare arcs against
                        if mod:
                            original_stage_u8 = U8File.get_parsed_U8_from_path(
                                original_stage_path
                            )

                        for arc_name in arcs:
                            arc_data = stage_u8.get_file_data(
                                f"{oarc_path}/{arc_name}.arc"
                            )

                            if not arc_data:
                                raise TypeError(
                                    f"Expected type bytes but found None for {mod}/{arc_name}."
                                )

                            # If we're extracting arcs from a mod, don't cache them if they're the same as the base game
                            if mod:
                                default_arc_data = original_stage_u8.get_file_data(
                                    f"oarc/{arc_name}.arc"
                                )
                                if arc_data == default_arc_data:
                                    continue

                            print_progress_text(
                                f"Extracting {mod + '/' if mod else ''}{arc_name}"
                            )
                            (cache_oarc_path / f"{arc_name}.arc").write_bytes(arc_data)

                if mod == "":
                    update_progress_value(
                        get_progress_value_from_range(
                            45, 5, current_extract_num, len(extracts)
                        )
                    )

        # Once we've extracted all the arcs, look for conflicts between different mods
        mod_arcs = {}
        for mod in self.other_mods:
            for arc in (CACHE_OARC_PATH / mod).glob("*"):
                if arc.name in mod_arcs:
                    raise Exception(
                        f'Mods "{mod_arcs[arc.name]}" and "{mod}" conflict and cannot be used together.'
                    )
                mod_arcs[arc.name] = mod

        end_cache_time = time.process_time()
        print(
            f"Arc extraction took {(end_cache_time - start_arc_patching_time)} seconds"
        )
        print(
            f"Total cache building took {(end_cache_time - start_cache_time)} seconds"
        )

    def add_arcn_for_check(self, stage: str, layer: int, room: int, arcn: str):
        if self.stage_patches.get(stage, None) == None:
            self.stage_patches[stage] = []

        self.stage_patches[stage].append(
            {
                "type": "arcnadd",
                "layer": layer,
                "room": room,
                "arcn": [arcn],
            }
        )

    def add_check_patch(
        self,
        stage: str,
        room: int,
        object_name: str,
        layer: int,
        objectid: str,
        itemid: int,
        trapid: int = 0,
        custom_flag: int = -1,
        original_itemid: int = 0,
        tbox_subtype: int = -1,
    ):
        self.check_patches[stage].append(
            (
                room,
                object_name,
                layer,
                objectid,
                itemid,
                trapid,
                custom_flag,
                original_itemid,
                tbox_subtype,
            )
        )

    def add_entrance_patch(
        self,
        exit_stage: str,
        exit_scen_index: int,
        exit_room: int,
        spawn_stage: str,
        spawn_layer: int,
        spawn_room: int,
        spawn_entrance: int,
    ):
        if exit_stage not in self.stage_patches:
            self.stage_patches[exit_stage] = []

        self.stage_patches[exit_stage].append(
            {
                "name": f"Entrance Patch - {exit_stage} to {spawn_stage}",
                "type": "objpatch",
                "index": exit_scen_index,
                "room": exit_room,
                "objtype": "SCEN",
                "object": {
                    "name": spawn_stage,
                    "layer": spawn_layer,
                    "room": spawn_room,
                    "entrance": spawn_entrance,
                },
            }
        )


def create_shuffled_trial_object_patches(
    world: World, stage_patch_handler: StagePatchHandler
) -> None:
    print_progress_text("Patching trial objects")

    # Go through each stage and collect all the item object positions
    silent_realm_stages = ["S000", "S100", "S200", "S300"]
    shuffle = world.setting("random_trial_object_positions")

    for stage in silent_realm_stages:
        shuffle_objects: list[tuple[int, int]] = []
        shuffle_positions: list[dict[str, float]] = []

        dusk_relic_objects: list[tuple[int, int]] = []
        dusk_relic_positions: list[dict[str, float]] = []

        # Go through all the rooms in the silent realm to collect each item
        for room_bzs_path in (CACHE_BZS_PATH / stage).glob("room*"):
            room_id = int(room_bzs_path.name.split(".bzs")[0][5:])
            room_bzs_bytes = room_bzs_path.read_bytes()
            room_bzs = parse_bzs(room_bzs_bytes)

            for obj in room_bzs["LAY "]["l2"].get("OBJ ", []):

                # Shuffle dusk relics amongst each other even if the shuffle is off. If trial treasuresanity is on
                # this gives the illusion that random dusk relics were chosen for items when in reality we just
                # switched around their positions
                if obj["name"] == "AncJwls" and shuffle.is_any_of("none", "simple"):
                    dusk_relic_objects.append((obj["id"], room_id))
                    dusk_relic_positions.append(
                        {"x": obj["posx"], "y": obj["posy"], "z": obj["posz"]}
                    )

                itemid = obj["params1"] & 0xFF
                if (
                    obj["name"] == "AncJwls" and shuffle.is_any_of("advanced", "full")
                ) or (
                    obj["name"] == "Item"
                    and (
                        (itemid == 0x2A and shuffle == "full")
                        or (
                            itemid == 0x2F
                            and shuffle.is_any_of("simple", "advanced", "full")
                        )
                        or (
                            itemid in (0x2B, 0x2C, 0x2D, 0x2E)
                            and shuffle.is_any_of("simple", "advanced", "full")
                        )
                    )
                ):
                    shuffle_objects.append((obj["id"], room_id))
                    shuffle_positions.append(
                        {"x": obj["posx"], "y": obj["posy"], "z": obj["posz"]}
                    )

        # Once we've collected all the objects and positions we're going to shuffle, shuffle them
        for patch_objects, patch_positions in [
            (dusk_relic_objects, dusk_relic_positions),
            (shuffle_objects, shuffle_positions),
        ]:

            # Shuffle the trial objects for this stage
            random.shuffle(patch_objects)
            assert len(patch_objects) == len(patch_positions)

            # Then pop a position off the list of positions to match with each object
            for object_id, room_id in patch_objects:
                pos = patch_positions.pop()
                position_patch = {
                    "name": f"Position shuffle for {object_id} on {stage}",
                    "type": "objpatch",
                    "id": object_id,
                    "room": room_id,
                    "layer": 2,
                    "objtype": "OBJ",
                    "object": {
                        "posx": pos["x"],
                        "posy": pos["y"],
                        "posz": pos["z"],
                    },
                }

                if stage not in stage_patch_handler.stage_patches:
                    stage_patch_handler.stage_patches[stage] = []

                stage_patch_handler.stage_patches[stage].append(position_patch)
