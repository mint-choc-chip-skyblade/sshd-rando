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

from constants.tboxsubtypes import tbox_subtypes
from constants.patchconstants import (
    DEFAULT_SOBJ,
    DEFAULT_OBJ,
    DEFAULT_SCEN,
    DEFAULT_PLY,
    DEFAULT_AREA,
    STAGE_OBJECT_NAMES,
    STAGE_FILE_REGEX,
    ROOM_ARC_REGEX,
)

from filepathconstants import (
    RANDO_ROOT_PATH,
    OUTPUT_STAGE_PATH,
    STAGE_FILES_PATH,
    STAGE_PATCHES_PATH,
    OARC_CACHE_PATH,
    EXTRACTS_PATH,
    OBJECTPACK_PATH,
    TITLE2D_SOURCE_PATH,
    TITLE2D_OUTPUT_PATH,
    ENDROLL_SOURCE_PATH,
    ENDROLL_OUTPUT_PATH,
)


def patch_tbox(bzs: dict, itemid: int, object_id_str: str, trapid: int):
    id = int(object_id_str)
    tbox = next(
        filter(lambda x: x["name"] == "TBox" and (x["anglez"] >> 9) == id, bzs["OBJS"]),
        None,
    )

    if tbox is None:
        print(f"ERROR: No tbox id {id} found to patch")
        return

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = trapid

    original_itemid = tbox["anglez"] & 0x1FF

    # Goddess Chests (subtype 0x03) expect the signed negative number of
    # the item id for the item they have (for some reason)
    # 9 bits means 2^9 - 1 = 511
    if tbox_subtypes[original_itemid] == 0x03:
        itemid = 511 - itemid

    # patches item
    tbox["anglez"] = mask_shift_set(tbox["anglez"], 0x1FF, 0, itemid)
    # patches chest type
    tbox["params1"] = mask_shift_set(
        tbox["params1"], 0x3, 4, tbox_subtypes[original_itemid]
    )


def patch_freestanding_item(bzs: dict, itemid: int, object_id_str: str, trapid: int):
    id = int(object_id_str)
    freestanding_item = next(
        filter(
            lambda x: x["name"] == "Item" and ((x["params1"] >> 10) & 0xFF) == id,
            bzs["OBJ "],
        ),
        None,
    )

    if freestanding_item is None:
        print(f"ERROR: No freestanding item id {id} found to patch")
        return

    # Need to check this as itemid is the itemid of the fake item model when trapid > 0
    if trapid:
        trapbits = 254 - trapid
        # Unsets bit 0x00000080 of params2
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


def patch_bucha(bzs: dict, itemid: int, object_id_str: str, trapid: int):
    id = int(object_id_str, 16)
    bucha = next(
        filter(lambda x: x["name"] == "NpcKyuE" and x["id"] == id, bzs["OBJ "]), None
    )

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = trapid

    if bucha is None:
        print(f"ERROR: Bucha's id {id} not found. Cannot patch this check.")
        return

    bucha["params2"] = mask_shift_set(bucha["params2"], 0xFF, 0x8, itemid)


def patch_zeldas_closet(bzs: dict, itemid: int, object_id_str: str, trapid: int):
    id = int(object_id_str)
    closet = next(
        filter(
            lambda x: x["name"] == "chest" and (x["params1"] & 0xFF) == id, bzs["OBJ "]
        ),
        None,
    )

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = trapid

    if closet is None:
        print(f"ERROR: No closet id {id} found to patch")
        return

    closet["params1"] = mask_shift_set(closet["params1"], 0xFF, 8, itemid)


def patch_ac_key_boko(bzs: dict, itemid: int, object_id_str: str, trapid: int):
    id = int(object_id_str, 16)
    boko = next(
        filter(lambda x: x["name"] == "EBc" and x["id"] == id, bzs["OBJ "]), None
    )

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = trapid

    if boko is None:
        print(f"ERROR: No boko id {id} found to patch")
        return

    boko["params2"] = mask_shift_set(boko["params2"], 0xFF, 0x0, itemid)


def patch_heart_container(bzs: dict, itemid: int, trapid: int):
    heart_container = next(filter(lambda x: x["name"] == "HeartCo", bzs["OBJ "]), None)

    if heart_container is None:
        print(f"ERROR: No heart container found to patch")
        return

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = trapid

    heart_container["params1"] = mask_shift_set(
        heart_container["params1"], 0xFF, 16, itemid
    )


def patch_chandelier_item(bzs: dict, itemid: int, trapid: int):
    chandelier = next(filter(lambda x: x["name"] == "Chandel", bzs["OBJ "]), None)

    if chandelier is None:
        print(f"ERROR: No chandelier found to patch")
        return

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = trapid

    chandelier["params1"] = mask_shift_set(chandelier["params1"], 0xFF, 8, itemid)


def patch_digspot_item(bzs: dict, itemid: int, object_id_str: str, trapid: int):
    id = int(object_id_str)
    digspot = next(
        filter(
            lambda x: x["name"] == "Soil" and ((x["params1"] >> 4) & 0xFF) == id,
            bzs["OBJ "],
        ),
        None,
    )

    # Don't use fake itemid yet, this needs patching properly first
    if trapid:
        itemid = trapid

    if digspot is None:
        print(f"ERROR: No digspot id {id} found to patch")
        return

    # patch digspot to be the same as key piece digspots in all ways except it keeps it's initial sceneflag
    digspot["params1"] = (digspot["params1"] & 0xFF0) | 0xFF0B1004
    digspot["params2"] = mask_shift_set(digspot["params2"], 0xFF, 0x18, itemid)


# def patch_goddess_crest(bzs: dict, itemid: int, index: str, trapid: int):
#     crest = next(filter(lambda x: x["name"] == "SwSB", bzs["OBJ "]), None)
#     if crest is None:
#         print(f"ERROR: No crest found to patch")
#         return

#     # Don't use fake itemid yet, this needs patching properly first
#     if trapid:
#         itemid = trapid

#     # 3 items patched into same object at different points in the params
#     if index == "0":
#         crest["params1"] = mask_shift_set(crest["params1"], 0xFF, 0x18, itemid)
#     elif index == "1":
#         crest["params1"] = mask_shift_set(crest["params1"], 0xFF, 0x10, itemid)
#     elif index == "2":
#         crest["params2"] = mask_shift_set(crest["params1"], 0xFF, 0x18, itemid)


# def patch_tadtone_group(bzs: dict, itemid: int, groupID: str, trapid: int):
#     groupID = int(groupID, 0)
#     clefs = filter(
#         lambda x: x["name"] == "Clef" and ((x["params1"] >> 3) & 0x1F) == groupID,
#         bzs["OBJ "],
#     )

#     # Don't use fake itemid yet, this needs patching properly first
#     if trapid:
#         itemid = trapid

#     for clef in clefs:
#         clef["anglez"] = mask_shift_set(clef["anglez"], 0xFFFF, 0, itemid)

### still need to do trials


def patch_additional_properties(obj: dict, prop: str, value: int):
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
                print(f'ERROR: unsupported property "{prop}" to patch for object {obj}')

        else:
            print(f'ERROR: unsupported property "{prop}" to patch for object {obj}')

    elif obj["name"] == "TBox":
        if prop == "spawnscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 20, value)
        elif prop == "setscenefid":
            obj["anglex"] = mask_shift_set(obj["anglex"], 0xFF, 0, value)
        elif prop == "itemid":
            obj["anglez"] = mask_shift_set(obj["anglez"], 0x1FF, 0, value)
        else:
            print(f'ERROR: unsupported property "{prop}" to patch for object {obj}')

    elif obj["name"] == "EvntTag":
        if prop == "trigscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 16, value)
        elif prop == "setscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 8, value)
        elif prop == "event":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        else:
            print(f'ERROR: unsupported property "{prop}" to patch for object {obj}')

    elif obj["name"] == "EvfTag":
        if prop == "trigstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 19, value)
        elif prop == "setstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 8, value)
        elif prop == "event":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        else:
            print(f'ERROR: unsupported property "{prop}" to patch for object {obj}')

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
            print(f'ERROR: unsupported property "{prop}" to patch for object {obj}')

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
            print(f'ERROR: unsupported property "{prop}" to patch for object {obj}')

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
            print(f'ERROR: unsupported property "{prop}" to patch for object {obj}')

    else:
        print(f"ERROR: unsupported object to patch {obj}")


def object_add(bzs: dict, object_add: dict, nextid: int):
    layer = object_add.get("layer", None)
    object_type = object_add["objtype"].ljust(4)
    obj = object_add["object"]

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
        print(f"ERROR: Unknown objtype: {object_type}")
        return

    # check index to verify new index is the next available index
    if "index" in obj:
        if layer is None:
            object_list = bzs.get(object_type, [])
        else:
            object_list = bzs["LAY "][f"l{layer}"].get(object_type, [])

        if len(object_list) != obj["index"]:
            print(f"ERROR: wrong index on added object: {json.dumps(object_add)}")
            return

    # populate provided properties
    for prop, value in obj.items():
        if prop in new_object:
            new_object[prop] = value
        else:
            patch_additional_properties(obj=new_object, prop=prop, value=value)

    if "id" in new_object:
        new_object["id"] = (new_object["id"] & ~0x3FF) | nextid

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
        # TODO: this only works if the layer is set
        if not "OBJN" in bzs["LAY "][f"l{layer}"]:
            bzs["LAY "][f"l{layer}"]["OBJN"] = []

        objn = bzs["LAY "][f"l{layer}"]["OBJN"]

        if not obj["name"] in objn:
            objn.append(obj["name"])

    object_list.append(new_object)


def object_delete(bzs: dict, object_delete: dict):
    obj = get_entry_from_bzs(bzs=bzs, object_def=object_delete, remove=True)

    if obj is None:
        print(
            f'ERROR: object not found and therefore not deleted- patch {object_delete["name"]}'
        )


def object_patch(bzs: dict, object_patch: dict):
    obj = get_entry_from_bzs(bzs=bzs, object_def=object_patch)

    if obj is not None:
        for prop, value in object_patch["object"].items():
            if prop in obj:
                obj[prop] = value
            else:
                patch_additional_properties(obj=obj, prop=prop, value=value)


def object_move(bzs: dict, object_move: dict, nextid: int):
    obj = get_entry_from_bzs(bzs=bzs, object_def=object_move, remove=True)
    destination_layer = object_move["destlayer"]

    if obj is not None:
        object_type = object_move["objtype"].ljust(4)
        obj["id"] = (obj["id"] & ~0x3FF) | nextid

        if not object_type in bzs["LAY "][f"l{destination_layer}"]:
            bzs["LAY "][f"l{destination_layer}"][object_type] = []

        bzs["LAY "][f"l{destination_layer}"][object_type].append(obj)

        if not "OBJN" in bzs["LAY "][f"l{destination_layer}"]:
            bzs["LAY "][f"l{destination_layer}"]["OBJN"] = []

        objn = bzs["LAY "][f"l{destination_layer}"]["OBJN"]

        if not obj["name"] in objn:
            objn.append(obj["name"])


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
    stage_path: Path, stage_patches, check_patches, stage_oarc_remove, stage_oarc_add
):
    stage_match = STAGE_FILE_REGEX.match(stage_path.parts[-1])

    if not stage_match:
        raise TypeError("Expected type Match[str] but found None.")

    stage = stage_match[1]
    layer = int(stage_match[2])
    modified_stage_path = Path(
        OUTPUT_STAGE_PATH / f"{stage}" / "NX" / f"{stage}_stg_l{layer}.arc.LZ"
    )
    # remove arcs
    remove_arcs = set(stage_oarc_remove.get((stage, layer), []))
    # add arcs
    add_arcs = set(stage_oarc_add.get((stage, layer), []))

    if layer == 0 or remove_arcs or add_arcs:
        patches = stage_patches.get(stage, [])

        print(f"Patching Stage: {stage}\tLayer: {layer}")
        object_patches = []
        stage_u8 = None

        # don't remove any arcs that are also set to be added
        remove_arcs = remove_arcs - add_arcs

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
                    print(f"ERROR: {arc_name} not found in oarc cache")

        if layer == 0:
            # handle layer overrides
            layer_override_patches = list(
                filter(lambda patch: patch["type"] == "layeroverride", patches)
            )

            if len(layer_override_patches) > 1:
                print(
                    f"ERROR: {len(layer_override_patches)} layer overrides found for stage {stage}, expected 1"
                )
                return
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

                room_path_matches = (
                    path for path in room_path_matches if path is not None
                )

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
                        len(patches_for_current_room)
                        + len(check_patches_for_current_room)
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
                                object_add(
                                    bzs=room_bzs,
                                    object_add=patch,
                                    nextid=nextid,
                                )
                                nextid += 1
                            elif patch["type"] == "objdelete":
                                object_delete(bzs=room_bzs, object_delete=patch)
                            elif patch["type"] == "objpatch":
                                object_patch(bzs=room_bzs, object_patch=patch)
                            elif patch["type"] == "objmove":
                                object_move(
                                    bzs=room_bzs,
                                    object_move=patch,
                                    nextid=nextid,
                                )
                                nextid += 1
                            else:
                                print(
                                    f"ERROR: unsupported patch type {patch['type']} in stage {stage} layer {layer} room {roomid} patches"
                                )

                        for (
                            room,
                            object_name,
                            layer,
                            objectid,
                            itemid,
                            trapid,
                        ) in check_patches_for_current_room:
                            if object_name == "TBox":
                                patch_tbox(
                                    room_bzs["LAY "][f"l{layer}"],
                                    itemid,
                                    objectid,
                                    trapid,
                                )
                            elif object_name == "Item":
                                patch_freestanding_item(
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
                                patch_zeldas_closet(
                                    room_bzs["LAY "][f"l{layer}"],
                                    itemid,
                                    objectid,
                                    trapid,
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
                            # elif object_name == "SwSB":
                            #     patch_goddess_crest(
                            #         room_bzs["LAY "][f"l{layer}"],
                            #         itemid,
                            #         objectid,
                            #         trapid,
                            #     )
                            # elif object_name == "Clef":
                            #     patch_tadtone_group(
                            #         room_bzs["LAY "][f"l{layer}"],
                            #         itemid,
                            #         objectid,
                            #         trapid,
                            #     )
                            else:
                                print(
                                    f"Object name: {object_name} not current supported for check patching"
                                )

                        room_u8.set_file_data("dat/room.bzs", build_bzs(room_bzs))
                        stage_u8.set_file_data(
                            room_path_match.group(0), room_u8.build_U8()
                        )

        if stage_u8 is not None:
            write_bytes_create_dirs(
                modified_stage_path, stage_u8.build_and_compress_U8()
            )

        # uncomment if you want to copy over all files for any reason
        # write_bytes_create_dirs(modifiedStagePath, stagePath.read_bytes())


class StagePatchHandler:
    def __init__(self):
        self.stage_patches: dict = yaml_load(STAGE_PATCHES_PATH)
        self.check_patches: dict[str, list[tuple]] = defaultdict(list)
        self.stage_oarc_remove: dict[tuple[str, int], set[str]] = defaultdict(set)
        self.stage_oarc_add: dict[tuple[str, int], set[str]] = defaultdict(set)

    def handle_stage_patches(self, onlyif_handler: ConditionalPatchHandler):
        # Pre-emptively remove unecessary patches since we can't pass
        # the onlyif_handler to other worker processes
        print("Removing unecessary patches")
        self.remove_unnecessary_patches(onlyif_handler)

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
                stage_patches=self.stage_patches,
                check_patches=self.check_patches,
                stage_oarc_remove=self.stage_oarc_remove,
                stage_oarc_add=self.stage_oarc_add,
            )
            pool.map(
                patch_stage_func,
                [
                    stage_path
                    for stage_path in Path(STAGE_FILES_PATH).rglob("*_stg_l*.arc.LZ")
                ],
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
        extracts: dict[dict, dict] = yaml_load(EXTRACTS_PATH)
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
                    print(f"Extracting {arc}")
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
                        print(f"Extracting {arc_name}")
                        arc_data = stage_u8.get_file_data(f"oarc/{arc_name}.arc")

                        if not arc_data:
                            raise TypeError("Expected type bytes but found None.")

                        (OARC_CACHE_PATH / f"{arc_name}.arc").write_bytes(arc_data)

    def set_oarc_add_remove_from_patches(self):
        for stage, stage_patches in self.stage_patches.items():
            for patch in stage_patches:
                if patch["type"] == "oarcadd":
                    self.stage_oarc_add[(stage, patch["destlayer"])].add(patch["oarc"])
                elif patch["type"] == "oarcdelete":
                    self.stage_oarc_remove[(stage, patch["layer"])].add(patch["oarc"])

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
    ):
        self.check_patches[stage].append(
            (room, object_name, layer, objectid, itemid, trapid)
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
        print("Patching Title Screen Logo")
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

        write_bytes_create_dirs(TITLE2D_OUTPUT_PATH, title_2d_arc.build_U8())

        # Write credits logo
        print("Patching Credits Logo")
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

        write_bytes_create_dirs(ENDROLL_OUTPUT_PATH, endroll_arc.build_U8())
