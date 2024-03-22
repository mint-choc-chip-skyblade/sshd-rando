import shutil
from util.arguments import get_program_args
from gui.dialogs.dialog_header import (
    get_progress_value_from_range,
    print_progress_text,
    update_progress_value,
)
from patches.conditionalpatchhandler import ConditionalPatchHandler
from sslib.bzs import parse_bzs, build_bzs, get_entry_from_bzs, get_highest_object_id
from sslib.utils import mask_shift_set, write_bytes_create_dirs
from sslib.yaml import yaml_load
from sslib.u8file import U8File

from collections import defaultdict
from pathlib import Path
from functools import partial
import json
import multiprocessing as mp

from constants.tboxsubtypes import VANILLA_TBOX_SUBTYPES
from constants.patchconstants import (
    DEFAULT_SOBJ,
    DEFAULT_OBJ,
    DEFAULT_SCEN,
    DEFAULT_PLY,
    DEFAULT_AREA,
    STAGE_FILES_TO_ALWAYS_PATCH,
    STAGE_OBJECT_NAMES,
    STAGE_FILE_REGEX,
    ROOM_ARC_REGEX,
    VALID_STAGE_PATCH_TYPES,
)

from filepathconstants import (
    RANDO_ROOT_PATH,
    STAGE_FILES_PATH,
    STAGE_PATCHES_PATH,
    OARC_CACHE_PATH,
    EXTRACTS_PATH,
    OBJECTPACK_PATH,
    TITLE2D_SOURCE_PATH,
    ENDROLL_SOURCE_PATH,
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


def patch_bucha(bzs: dict, itemid: int, object_id_str: str, trapid: int):
    id = int(object_id_str, 16)
    bucha: dict | None = next(
        filter(lambda x: x["name"] == "NpcKyuE" and x["id"] == id, bzs["OBJ "]), None
    )

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = 34  # rupoor

    if bucha is None:
        raise Exception(f"Bucha's id '{id}' not found. Cannot patch this check.")

    bucha["params2"] = mask_shift_set(bucha["params2"], 0xFF, 0x8, itemid)


def patch_closet(
    bzs: dict, itemid: int, object_id_str: str, trapid: int, room: int, stage: str
):
    id = int(object_id_str, 16)
    closet: dict | None = next(
        filter(lambda x: x["name"] == "chest" and x["id"] == id, bzs["OBJ "]),
        None,
    )

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = 34  # rupoor

    if closet is None:
        raise Exception(f"No closet with id '{id}' found to patch.")

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
        ("F006r", 0, 0xFC16): 82,  # Wryna's Closet           Bx04
        ("F013r", 0, 0xFC0E): 100,  # Sparrot's Closet        Dx10
        ("F014r", 0, 0xFC12): 101,  # Luv and Bertie's Closet Dx20
        ("F015r", 0, 0xFC10): 105,  # Gondo's Closet          Cx02
        ("F016r", 0, 0xFC28): 107,  # Mallara's Closet        Cx04
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

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = 34  # rupoor

    if boko is None:
        raise Exception(f"No Bokoblin (EBc) with id '{id}' found to patch.")

    boko["params2"] = mask_shift_set(boko["params2"], 0xFF, 0x0, itemid)


def patch_heart_container(bzs: dict, itemid: int, trapid: int):
    heart_container: dict | None = next(
        filter(lambda x: x["name"] == "HeartCo", bzs["OBJ "]), None
    )

    if heart_container is None:
        raise Exception(f"No heart container found to patch.")

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = 34  # rupoor

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


def patch_digspot_item(bzs: dict, itemid: int, object_id_str: str, trapid: int):
    id = int(object_id_str)
    digspot: dict | None = next(
        filter(
            lambda x: x["name"] == "Soil" and ((x["params1"] >> 4) & 0xFF) == id,
            bzs["OBJ "],
        ),
        None,
    )

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = 34  # rupoor

    if digspot is None:
        raise Exception(f"No digspot with id '{id}' found to patch.")

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


# def patch_tadtone_group(bzs: dict, itemid: int, groupID: str, trapid: int):
#     groupID = int(groupID, 0)
#     clefs = filter(
#         lambda x: x["name"] == "Clef" and ((x["params1"] >> 3) & 0x1F) == groupID,
#         bzs["OBJ "],
#     )

#     # Don't use fake itemid yet, this needs patching properly first
#     if trapid:
#         itemid = 34 # rupoor

#     for clef in clefs:
#         clef["anglez"] = mask_shift_set(clef["anglez"], 0xFFFF, 0, itemid)


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

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = 34  # rupoor

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


def patch_additional_properties(obj: dict, prop: str, value: int):
    unsupported_prop_execption = f"Cannot patch object with unsupported property.\nUnsupported property: {prop}\nObject: {obj}"

    if obj["name"].startswith("Npc"):
        if prop == "trigstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 10, value)
        elif prop == "untrigstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 21, value)
        elif prop == "talk_behaviour":
            obj["anglez"] = value

        elif obj["name"] == "NpcTke":
            if prop == "trigscenefid":
                obj["anglex"] = mask_shift_set(obj["anglex"], 0xFF, 0, value)
            elif prop == "untrigscenefid":
                obj["anglex"] = mask_shift_set(obj["anglex"], 0xFF, 8, value)
            elif prop == "subtype":
                obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
            else:
                raise Exception(unsupported_prop_execption)

        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "TBox":
        if prop == "spawnscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 20, value)
        elif prop == "setscenefid":
            obj["anglex"] = mask_shift_set(obj["anglex"], 0xFF, 0, value)
        elif prop == "itemid":
            obj["anglez"] = mask_shift_set(obj["anglez"], 0x1FF, 0, value)
        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "EvntTag":
        if prop == "trigscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 16, value)
        elif prop == "setscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 8, value)
        elif prop == "event":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "EvfTag":
        if prop == "trigstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 19, value)
        elif prop == "setstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 8, value)
        elif prop == "event":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "ScChang":
        if prop == "trigstoryfid":
            obj["anglex"] = mask_shift_set(obj["anglex"], 0x7FF, 0, value)
        elif prop == "untrigstoryfid":
            obj["anglez"] = mask_shift_set(obj["anglez"], 0x7FF, 0, value)
        elif prop == "scen_link":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        elif prop == "trigscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 24, value)
        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "SwAreaT":
        if prop == "setstoryfid":
            obj["anglex"] = mask_shift_set(obj["anglex"], 0x7FF, 0, value)
        elif prop == "unsetstoryfid":
            obj["anglez"] = mask_shift_set(obj["anglez"], 0x7FF, 0, value)
        elif prop == "setscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        elif prop == "unsetscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 8, value)
        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "PushBlk":
        if prop == "pathIdx":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 4, value)
        elif prop == "goalscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 12, value)
        elif prop == "useLargerRadius":
            obj["params1"] = mask_shift_set(obj["params1"], 0x03, 30, value)
        elif prop == "isSwitchGoal":
            obj["params1"] = mask_shift_set(obj["params1"], 0x03, 28, value)
        else:
            raise Exception(unsupported_prop_execption)

    else:
        raise Exception(f"Unsupported object to patch: {obj}")


def object_add(bzs: dict, object_add: dict, nextid: int) -> int:
    layer = object_add.get("layer", None)
    object_type = object_add["objtype"].ljust(4)
    obj = object_add["object"]
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
            raise Exception(f"Cannot find object:\n{obj}\nPatch: {object_delete}")


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


# Generic function outside of the StagePatchHandler
# We have to pass all the various patch data to each process
# individually
def patch_and_write_stage(
    stage_path: Path,
    stage_output_path: Path,
    stage_patches,
    check_patches,
    stage_oarc_remove,
    stage_oarc_add,
):
    stage_match = STAGE_FILE_REGEX.match(stage_path.parts[-1])

    if not stage_match:
        raise TypeError("Expected type Match[str] but found None.")

    stage = stage_match[1]
    layer = int(stage_match[2])
    modified_stage_path = (
        stage_output_path / f"{stage}" / "NX" / f"{stage}_stg_l{layer}.arc.LZ"
    )
    # remove arcs
    remove_arcs = set(stage_oarc_remove.get((stage, layer), []))
    # add arcs
    add_arcs = set(stage_oarc_add.get((stage, layer), []))

    patches = stage_patches.get(stage, [])

    object_patches = []
    stage_u8 = None

    # don't remove any arcs that are also set to be added
    remove_arcs = remove_arcs - add_arcs

    # If this isn't layer 0, remove any arcs that layer 0 will have
    if layer != 0:
        stage_l0_path = Path(stage_path.as_posix().replace(f"l{layer}", "l0"))
        stage_l0_u8 = U8File.get_parsed_U8_from_path(stage_l0_path, True)
        # Get the arcs that layer 0 already has
        l0_arcs = set([path.replace("/oarc/", "").replace(".arc", "") for path in stage_l0_u8.get_all_paths() if "oarc/" in path])
        # Subtract the arcs which will be removed
        l0_arcs -= set(stage_oarc_remove.get((stage, 0), []))
        # Add the arcs which will be added
        l0_arcs |= set(stage_oarc_add.get((stage, 0), []))

        # Get the arcs for the current layer
        stage_u8 = U8File.get_parsed_U8_from_path(stage_path, True)
        this_layer_arcs = set([path.replace("/oarc/", "").replace(".arc", "") for path in stage_u8.get_all_paths() if "oarc/" in path])
        # If any arcs are currently on this layer and layer 0, remove them from this layer
        remove_arcs |= l0_arcs.intersection(this_layer_arcs)
        # Don't add arcs which layer 0 already has
        add_arcs -= l0_arcs
        stage_u8 = None

    if len(remove_arcs) > 0:
        stage_u8 = U8File.get_parsed_U8_from_path(stage_path, True)

        for arc in remove_arcs:
            stage_u8.delete_file(f"oarc/{arc}.arc")

    if len(add_arcs) > 0:
        if stage_u8 is None:
            stage_u8 = U8File.get_parsed_U8_from_path(stage_path, True)

        for arc in add_arcs:
            arc_name = f"{arc}.arc"
            oarc_path = OARC_CACHE_PATH / arc_name

            if oarc_path.exists():
                stage_u8.add_file_data(f"oarc/{arc_name}", oarc_path.read_bytes())
            else:
                raise Exception(
                    f"Arc '{arc_name}' cannot be found in oarccache. Try adding the arc to extracts.yaml."
                )

    if layer == 0:
        # handle layer overrides
        layer_override_patches = list(
            filter(lambda patch: patch["type"] == "layeroverride", patches)
        )

        if len(layer_override_patches) > 1:
            raise Exception(
                f"Multiple layeroverrides found. {len(layer_override_patches)} layer overrides found for stage {stage}, expected 1."
            )
        elif len(layer_override_patches) == 1:
            if stage_u8 is None:
                stage_u8 = U8File.get_parsed_U8_from_path(stage_path, True)

            stage_u8_data = stage_u8.get_file_data("dat/stage.bzs")

            if not stage_u8_data:
                raise TypeError("Expected type bytes but found None.")

            stage_bzs = parse_bzs(stage_u8_data)

            layer_override(bzs=stage_bzs, patch=layer_override_patches[0])
            stage_u8.set_file_data("dat/stage.bzs", build_bzs(stage_bzs))

        for obj_patch in filter(
            lambda patch: patch["type"]
            in ["objadd", "objdelete", "objpatch", "objmove"],
            patches,
        ):
            object_patches.append(obj_patch)

        if len(object_patches) + len(check_patches[stage]) > 0:
            if stage_u8 is None:
                stage_u8 = U8File.get_parsed_U8_from_path(stage_path, True)

            room_path_matches = (
                ROOM_ARC_REGEX.match(path) for path in stage_u8.get_all_paths()
            )

            room_path_matches = (path for path in room_path_matches if path is not None)

            for room_path_match in room_path_matches:
                roomid = int(room_path_match.group("roomID"))

                patches_for_current_room = list(
                    filter(
                        lambda patch: patch.get("room") == roomid,
                        object_patches,
                    )
                )

                check_patches_for_current_room = list(
                    filter(
                        lambda patch: patch[0] == roomid,
                        check_patches[stage],
                    )
                )

                if (
                    len(patches_for_current_room) + len(check_patches_for_current_room)
                    > 0
                ):
                    room_u8 = stage_u8.get_parsed_U8_from_this_U8(
                        path=room_path_match.group(0)
                    )
                    room_u8_data = room_u8.get_file_data("dat/room.bzs")

                    if not room_u8_data:
                        raise TypeError("Expected type bytes but found None.")

                    room_bzs = parse_bzs(room_u8_data)

                    nextid = get_highest_object_id(bzs=room_bzs) + 1

                    for patch in patches_for_current_room:
                        if patch["type"] == "objadd":
                            nextid += object_add(
                                bzs=room_bzs,
                                object_add=patch,
                                nextid=nextid,
                            )
                        elif patch["type"] == "objdelete":
                            object_delete(bzs=room_bzs, object_delete=patch)
                        elif patch["type"] == "objpatch":
                            object_patch(bzs=room_bzs, object_patch=patch)
                        elif patch["type"] == "objmove":
                            nextid += object_move(
                                bzs=room_bzs,
                                object_move=patch,
                                nextid=nextid,
                            )
                        else:
                            raise Exception(
                                f"Unsupported patch type ({patch['type']}) found.\nPatch: {patch}"
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
                                stage,
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
                        # elif object_name == "Clef":
                        #     patch_tadtone_group(
                        #         room_bzs["LAY "][f"l{layer}"],
                        #         itemid,
                        #         objectid,
                        #         trapid,
                        #     )
                        else:
                            print(
                                f"Object name: {object_name} not currently supported for check patching."
                            )

                    room_u8.set_file_data("dat/room.bzs", build_bzs(room_bzs))
                    stage_u8.set_file_data(room_path_match.group(0), room_u8.build_U8())

    if stage_u8 is not None:
        print_progress_text(f"Patching Stage: {stage}\tLayer: {layer}")
        write_bytes_create_dirs(modified_stage_path, stage_u8.build_and_compress_U8())
    else:
        print_progress_text(f"Copying Stage: {stage}\tLayer: {layer}")
        write_bytes_create_dirs(modified_stage_path, stage_path.read_bytes())


class StagePatchHandler:
    def __init__(self, output_path: Path):
        self.base_output_path = output_path
        self.stage_output_path = self.base_output_path / "Stage"
        self.stage_patches: dict = yaml_load(STAGE_PATCHES_PATH)  # type: ignore
        self.check_patches: dict[str, list[tuple]] = defaultdict(list)
        self.stage_oarc_remove: dict[tuple[str, int], set[str]] = defaultdict(set)
        self.stage_oarc_add: dict[tuple[str, int], set[str]] = defaultdict(set)

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

        mp_manager = mp.Manager()
        stages_patched_queue = mp_manager.Queue()

        # Create the pool or worker processes
        with mp.Pool() as pool:
            # Create a function which emulates patch_and_write_stage except
            # we only have to pass the stage name to it and all the other args
            # will have their values set here.
            #
            # This is done because we can only pass 1 argument to the function
            # we're kicking off to the pool when using the pool.map method
            patch_stage_func = partial(
                patch_and_write_stage,
                stage_output_path=self.stage_output_path,
                stage_patches=self.stage_patches,
                check_patches=self.check_patches,
                stage_oarc_remove=self.stage_oarc_remove,
                stage_oarc_add=self.stage_oarc_add,
            )

            all_stage_file_paths = tuple(STAGE_FILES_PATH.rglob("*_stg_l*.arc.LZ"))

            # TODO: remove race condition - https://docs.python.org/3/library/multiprocessing.html#exchanging-objects-between-processes
            total_stage_count = len(all_stage_file_paths)

            # imap *can* be slower so only use it with the gui (where we need a progress output)
            if not args.nogui:
                for _ in pool.imap_unordered(
                    patch_stage_func,
                    [stage_path for stage_path in all_stage_file_paths],
                ):
                    stages_patched_queue.put(1)
                    update_progress_value(
                        get_progress_value_from_range(
                            90, 70, stages_patched_queue.qsize(), total_stage_count
                        )
                    )
            else:
                pool.map(
                    patch_stage_func,
                    [stage_path for stage_path in all_stage_file_paths],
                )

    def remove_unnecessary_patches(
        self, onlyif_handler: ConditionalPatchHandler
    ) -> None:
        for patches in self.stage_patches.values():
            for patch in patches.copy():
                if statement := patch.get("onlyif", False):
                    if not onlyif_handler.evaluate_onlyif(statement):
                        patches.remove(patch)

    def create_oarc_cache(self):
        extracts: dict[dict, dict] = yaml_load(EXTRACTS_PATH)  # type: ignore
        OARC_CACHE_PATH.mkdir(parents=True, exist_ok=True)

        for extract in extracts:
            # objectpack is a special case (not a stage)
            if "objectpack" in extract:
                arcs = extract["objectpack"]
                arcs_not_in_cache = [
                    arc_name
                    for arc_name in arcs
                    if not (OARC_CACHE_PATH / f"{arc_name}.arc").exists()
                ]

                if len(arcs_not_in_cache) == 0:
                    continue

                objectpack_u8 = U8File.get_parsed_U8_from_path(OBJECTPACK_PATH, True)

                for arc in arcs_not_in_cache:
                    print_progress_text(f"Extracting {arc}")
                    arc_data = objectpack_u8.get_file_data(f"oarc/{arc}.arc")

                    if not arc_data:
                        raise TypeError("Expected type bytes but found None.")

                    (OARC_CACHE_PATH / f"{arc}.arc").write_bytes(arc_data)
            else:
                stage = extract["stage"]

                for layer in extract["layers"]:
                    layerid = layer["layerid"]
                    arcs = layer["oarcs"]

                    all_already_in_cache = all(
                        ((OARC_CACHE_PATH / f"{arc}.arc").exists() for arc in arcs)
                    )

                    if all_already_in_cache:
                        continue

                    stage_path = Path(
                        STAGE_FILES_PATH
                        / f"{stage}"
                        / "NX"
                        / f"{stage}_stg_l{layerid}.arc.LZ"
                    )
                    stage_u8 = U8File.get_parsed_U8_from_path(stage_path, True)

                    for arc_name in arcs:
                        print_progress_text(f"Extracting {arc_name}")
                        arc_data = stage_u8.get_file_data(f"oarc/{arc_name}.arc")

                        if not arc_data:
                            raise TypeError("Expected type bytes but found None.")

                        (OARC_CACHE_PATH / f"{arc_name}.arc").write_bytes(arc_data)

    def set_oarc_add_remove_from_patches(self):
        for stage, stage_patches in self.stage_patches.items():
            for patch in stage_patches:
                for oarc in patch.get("oarc", []):
                    if patch["type"] == "oarcadd":
                        self.stage_oarc_add[(stage, patch["destlayer"])].add(oarc)
                    elif patch["type"] == "oarcdelete":
                        self.stage_oarc_remove[(stage, patch["layer"])].add(oarc)

    def add_oarc_for_check(self, stage: str, layer: int, oarc: str):
        self.stage_oarc_add[(stage, layer)].add(oarc)

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

    def patch_logo(self):
        print_progress_text("Patching Title Screen Logo")
        logo_data = (RANDO_ROOT_PATH / "assets" / "sshdr-logo.tpl").read_bytes()
        rogo_03_data = (RANDO_ROOT_PATH / "assets" / "th_rogo_03.tpl").read_bytes()
        rogo_04_data = (RANDO_ROOT_PATH / "assets" / "th_rogo_04.tpl").read_bytes()

        # Write title screen logo
        title_2d_arc = U8File.get_parsed_U8_from_path(TITLE2D_SOURCE_PATH, False)
        title_2d_arc.set_file_data("timg/tr_wiiKing2Logo_00.tpl", logo_data)
        title_2d_arc.set_file_data("timg/th_rogo_03.tpl", rogo_03_data)
        title_2d_arc.set_file_data("timg/th_rogo_04.tpl", rogo_04_data)

        # Fix size of rogo stuff (makes the logo text shiny)
        if lyt_file := title_2d_arc.get_file_data("blyt/titleBG_00.brlyt"):
            # Changes the size of the P_loop_00, P_auraR_03, and P_auraR_00 lyt elements
            lyt_file = lyt_file.replace(
                b"\x43\xA4\xC0\x00\x43\x37", b"\x43\xA4\xC0\x00\x43\x69"
            )
            title_2d_arc.set_file_data("blyt/titleBG_00.brlyt", lyt_file)

        write_bytes_create_dirs(
            self.base_output_path / "Layout" / "Title2D.arc", title_2d_arc.build_U8()
        )

        # Write credits logo
        print_progress_text("Patching Credits Logo")
        endroll_arc = U8File.get_parsed_U8_from_path(ENDROLL_SOURCE_PATH, False)
        endroll_arc.set_file_data("timg/th_zeldaRogoEnd_02.tpl", logo_data)
        endroll_arc.set_file_data("timg/th_rogo_03.tpl", rogo_03_data)
        endroll_arc.set_file_data("timg/th_rogo_04.tpl", rogo_04_data)

        # Fix size of rogo stuff (makes the logo text shiny)
        if lyt_file := endroll_arc.get_file_data("blyt/endTitle_00.brlyt"):
            # Changes the size of the P_loop_00, and P_auraR_00 lyt elements
            lyt_file = lyt_file.replace(
                b"\x9A\x40\x49\x99\x9A\x43\x13\x80\x00\x42\xA2",
                b"\x99\x40\x49\x99\x99\x43\x13\x80\x00\x42\xCE",
            )
            endroll_arc.set_file_data("blyt/endTitle_00.brlyt", lyt_file)

        write_bytes_create_dirs(
            self.base_output_path / "Layout" / "EndRoll.arc", endroll_arc.build_U8()
        )
