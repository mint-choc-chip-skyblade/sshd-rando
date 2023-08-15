from collections import defaultdict
from filepathconstants import (
    OUTPUT_STAGE_PATH,
    STAGE_FILES_PATH,
    STAGE_PATCHES_PATH,
    OARC_CACHE_PATH,
    EXTRACTS_PATH,
    OBJECTPACK_PATH,
)
from pathlib import Path
import json

from patches.patchconstants import (
    DEFAULT_SOBJ,
    DEFAULT_OBJ,
    DEFAULT_SCEN,
    DEFAULT_PLY,
    DEFAULT_AREA,
    STAGE_REGEX,
    ROOM_REGEX,
)

from sslib.bzs import parseBzs, buildBzs, get_entry_from_bzs, get_highest_object_id
from sslib.u8file import U8File
from sslib.utils import mask_shift_set, write_bytes_create_dirs
from sslib.yaml import yaml_load


def patch_tbox(bzs, itemID, id):
    id = int(id)
    tboxs = list(
        filter(lambda x: x["name"] == "TBox" and (x["anglez"] >> 9) == id, bzs["OBJS"])
    )
    if len(tboxs) == 0:
        print(tboxs)
    obj = tboxs[0]

    obj["anglez"] = mask_shift_set(obj["anglez"], 0x1FF, 0, itemID)
    # obj["params1"] = mask_shift_set(obj["params1"], 0x3, 4, 0x01)


def patch_additional_properties(object, property, value):
    if object["name"].startswith("Npc"):
        if property == "trigstoryfid":
            object["params1"] = mask_shift_set(object["params1"], 0x7FF, 10, value)
        elif property == "untrigstoryfid":
            object["params1"] = mask_shift_set(object["params1"], 0x7FF, 21, value)
        elif property == "talk_behaviour":
            object["anglez"] = value
        elif object["name"] == "NpcTke":
            if property == "trigscenefid":
                object["anglex"] = mask_shift_set(object["anglex"], 0xFF, 0, value)
            elif property == "untrigscenefid":
                object["anglex"] = mask_shift_set(object["anglex"], 0xFF, 8, value)
            elif property == "subtype":
                object["params1"] = mask_shift_set(object["params1"], 0xFF, 0, value)
            else:
                print(
                    f'ERROR: unsupported property "{property}" to patch for object {object}'
                )
        else:
            print(
                f'ERROR: unsupported property "{property}" to patch for object {object}'
            )
    elif object["name"] == "TBox":
        if property == "spawnscenefid":
            object["params1"] = mask_shift_set(object["params1"], 0xFF, 20, value)
        elif property == "setscenefid":
            object["anglex"] = mask_shift_set(object["anglex"], 0xFF, 0, value)
        elif property == "itemid":
            object["anglez"] = mask_shift_set(object["anglez"], 0x1FF, 0, value)
        else:
            print(
                f'ERROR: unsupported property "{property}" to patch for object {object}'
            )
    elif object["name"] == "EvntTag":
        if property == "trigscenefid":
            object["params1"] = mask_shift_set(object["params1"], 0xFF, 16, value)
        elif property == "setscenefid":
            object["params1"] = mask_shift_set(object["params1"], 0xFF, 8, value)
        elif property == "event":
            object["params1"] = mask_shift_set(object["params1"], 0xFF, 0, value)
        else:
            print(
                f'ERROR: unsupported property "{property}" to patch for object {object}'
            )
    elif object["name"] == "EvfTag":
        if property == "trigstoryfid":
            object["params1"] = mask_shift_set(object["params1"], 0x7FF, 19, value)
        elif property == "setstoryfid":
            object["params1"] = mask_shift_set(object["params1"], 0x7FF, 8, value)
        elif property == "event":
            object["params1"] = mask_shift_set(object["params1"], 0xFF, 0, value)
        else:
            print(
                f'ERROR: unsupported property "{property}" to patch for object {object}'
            )
    elif object["name"] == "ScChang":
        if property == "trigstoryfid":
            object["anglex"] = mask_shift_set(object["anglex"], 0x7FF, 0, value)
        elif property == "untrigstoryfid":
            object["anglez"] = mask_shift_set(object["anglez"], 0x7FF, 0, value)
        elif property == "scen_link":
            object["params1"] = mask_shift_set(object["params1"], 0xFF, 0, value)
        elif property == "trigscenefid":
            object["params1"] = mask_shift_set(object["params1"], 0xFF, 24, value)
        else:
            print(
                f'ERROR: unsupported property "{property}" to patch for object {object}'
            )
    elif object["name"] == "SwAreaT":
        if property == "setstoryfid":
            object["anglex"] = mask_shift_set(object["anglex"], 0x7FF, 0, value)
        elif property == "unsetstoryfid":
            object["anglez"] = mask_shift_set(object["anglez"], 0x7FF, 0, value)
        elif property == "setscenefid":
            object["params1"] = mask_shift_set(object["params1"], 0xFF, 0, value)
        elif property == "unsetscenefid":
            object["params1"] = mask_shift_set(object["params1"], 0xFF, 8, value)
        else:
            print(
                f'ERROR: unsupported property "{property}" to patch for object {object}'
            )
    elif object["name"] == "PushBlk":
        if property == "pathIdx":
            object["params1"] = mask_shift_set(object["params1"], 0xFF, 4, value)
        elif property == "goalscenefid":
            object["params1"] = mask_shift_set(object["params1"], 0xFF, 12, value)
        elif property == "useLargerRadius":
            object["params1"] = mask_shift_set(object["params1"], 0x03, 30, value)
        elif property == "isSwitchGoal":
            object["params1"] = mask_shift_set(object["params1"], 0x03, 28, value)
        else:
            print(
                f'ERROR: unsupported property "{property}" to patch for object {object}'
            )
    else:
        print(f"ERROR: unsupported object to patch {object}")


def object_add(bzs, objadd, nextID):
    layer = objadd.get("layer", None)
    objectType = objadd["objtype"].ljust(4)
    object = objadd["object"]

    # populate with default object as a base
    if objectType in ["SOBS", "SOBJ", "STAS", "STAG", "SNDT"]:
        newObject = DEFAULT_SOBJ.copy()
    elif objectType in ["OBJS", "OBJ ", "DOOR"]:
        newObject = DEFAULT_OBJ.copy()
    elif objectType == "SCEN":
        newObject = DEFAULT_SCEN.copy()
    elif objectType == "PLY":
        newObject = DEFAULT_PLY.copy()
    elif objectType == "AREA":
        newObject = DEFAULT_AREA.copy()
    else:
        print(f"ERROR: Unknown objtype: {objectType}")
        return

    # check index to verify new index is the next available index
    if "index" in object:
        if layer is None:
            objectList = bzs.get(objectType, [])
        else:
            objectList = bzs["LAY "][f"l{layer}"].get(objectType, [])
        if len(objectList) != object["index"]:
            print(f"ERROR: wrong index on added object: {json.dumps(objadd)}")
            return

    # populate provided properties
    for property, value in object.items():
        if property in newObject:
            newObject[property] = value
        else:
            patch_additional_properties(
                object=newObject, property=property, value=value
            )
    if "id" in newObject:
        newObject["id"] = (newObject["id"] & ~0x3FF) | nextID

    # creates list for object types if don't already exist in bzs
    if layer is None:
        if objectType not in bzs:  # check
            bzs[objectType] = []
        objectList = bzs[objectType]
    else:
        if objectType not in bzs["LAY "][f"l{layer}"]:
            bzs["LAY "][f"l{layer}"][objectType] = []
        objectList = bzs["LAY "][f"l{layer}"][objectType]

    # add object name to objn if it's some type of actor
    if objectType in ["SOBS", "SOBJ", "STAS", "STAG", "SNDT", "OBJS", "OBJ ", "DOOR"]:
        # TODO: this only works if the layer is set
        if not "OBJN" in bzs["LAY "][f"l{layer}"]:
            bzs["LAY "][f"l{layer}"]["OBJN"] = []
        objn = bzs["LAY "][f"l{layer}"]["OBJN"]
        if not object["name"] in objn:
            objn.append(object["name"])

    objectList.append(newObject)


def object_delete(bzs, objdelete):
    object = get_entry_from_bzs(bzs=bzs, objdef=objdelete, remove=True)
    if object is None:
        print(
            f'ERROR: object not found and therefore not deleted- patch {objdelete["name"]}'
        )


def object_patch(bzs, objpatch):
    object = get_entry_from_bzs(bzs=bzs, objdef=objpatch)
    if object is not None:
        for property, value in objpatch["object"].items():
            if property in object:
                object[property] = value
            else:
                patch_additional_properties(
                    object=object, property=property, value=value
                )


def object_move(bzs, objmove, nextID):
    object = get_entry_from_bzs(bzs=bzs, objdef=objmove, remove=True)
    destLayer = objmove["destlayer"]
    if object is not None:
        objectType = objmove["objtype"].ljust(4)
        object["id"] = (object["id"] & ~0x3FF) | nextID

        if not objectType in bzs["LAY "][f"l{destLayer}"]:
            bzs["LAY "][f"l{destLayer}"][objectType] = []
        bzs["LAY "][f"l{destLayer}"][objectType].append(object)
        objn = bzs["LAY "][f"l{destLayer}"]["OBJN"]
        if not object["name"] in objn:
            objn.append(object["name"])


def layer_override(bzs, patch):
    layerOverride = [
        {
            "story_flag": override["story_flag"],
            "night": override["night"],
            "layer": override["layer"],
        }
        for override in patch["override"]
    ]
    bzs["LYSE"] = layerOverride
    print("Layer overridden")


class StagePatchHandler:
    def __init__(self):
        self.stagePatches = yaml_load(STAGE_PATCHES_PATH)
        self.stageOarcAdd = defaultdict(set)
        self.stageOarcRemove = defaultdict(set)

    def handle_stage_patches(self):
        for stagePath in Path(STAGE_FILES_PATH).rglob("*_stg_l*.arc.LZ"):
            stageMatch = STAGE_REGEX.match(stagePath.parts[-1])
            stage = stageMatch[1]
            layer = int(stageMatch[2])
            modifiedStagePath = Path(
                OUTPUT_STAGE_PATH / f"{stage}" / "NX" / f"{stage}_stg_l{layer}.arc.LZ"
            )
            # remove arcs
            removeArcs = set(self.stageOarcRemove.get((stage, layer), []))
            # add arcs
            addArcs = set(self.stageOarcAdd.get((stage, layer), []))

            if layer == 0 or removeArcs or addArcs:
                patches = self.stagePatches.get(stage, [])

                if len(patches) > 0:
                    print(f"Patching {stage} layer {layer}")
                    objectPatches = []
                    stageU8 = None

                    # don't remove any arcs that are also set to be added
                    removeArcs = removeArcs - addArcs

                    if len(removeArcs) > 0:
                        stageU8 = U8File.get_parsed_U8_from_path(stagePath, True)
                        for arc in removeArcs:
                            stageU8.delete_file(f"oarc/{arc}.arc")

                    if len(addArcs) > 0:
                        if stageU8 is None:
                            stageU8 = U8File.get_parsed_U8_from_path(stagePath, True)
                        for arc in addArcs:
                            arcName = f"{arc}.arc"
                            oarcPath = OARC_CACHE_PATH / arcName
                            if oarcPath.exists():
                                stageU8.add_file_data(
                                    f"oarc/{arcName}", oarcPath.read_bytes()
                                )
                            else:
                                print(f"ERROR: {arcName} not found in oarc cache")

                    # handle layer overrides
                    layerOverridePatches = list(
                        filter(lambda patch: patch["type"] == "layeroverride", patches)
                    )
                    if len(layerOverridePatches) > 1:
                        print(
                            f"ERROR: {len(layerOverridePatches)} layer overrides found for stage {stage}, expected 1"
                        )
                        continue
                    elif len(layerOverridePatches) == 1:
                        if stageU8 is None:
                            stageU8 = U8File.get_parsed_U8_from_path(stagePath, True)
                        stageBZS = parseBzs(stageU8.get_file_data("dat/stage.bzs"))
                        layer_override(bzs=stageBZS, patch=layerOverridePatches[0])
                        stageU8.set_file_data("dat/stage.bzs", buildBzs(stageBZS))

                    for objPatch in filter(
                        lambda patch: patch["type"]
                        in ["objadd", "objdelete", "objpatch", "objmove"],
                        patches,
                    ):
                        objectPatches.append(objPatch)

                    if len(objectPatches) > 0:
                        if stageU8 is None:
                            stageU8 = U8File.get_parsed_U8_from_path(stagePath, True)

                        roomPathMatches = (
                            ROOM_REGEX.match(path) for path in stageU8.get_all_paths()
                        )
                        roomPathMatches = (
                            path for path in roomPathMatches if path is not None
                        )
                        for roomPathMatch in roomPathMatches:
                            roomID = int(roomPathMatch.group("roomid"))

                            patchesForCurrentRoom = list(
                                filter(
                                    lambda patch: patch.get("room") == roomID,
                                    objectPatches,
                                )
                            )
                            if len(patchesForCurrentRoom) > 0:
                                roomU8 = stageU8.get_parsed_U8_from_this_U8(
                                    path=roomPathMatch.group(0)
                                )
                                roomBZS = parseBzs(roomU8.get_file_data("dat/room.bzs"))

                                nextID = get_highest_object_id(bzs=roomBZS) + 1

                                for patch in patchesForCurrentRoom:
                                    if patch["type"] == "objadd":
                                        object_add(
                                            bzs=roomBZS, objadd=patch, nextID=nextID
                                        )
                                        nextID += 1
                                    elif patch["type"] == "objdelete":
                                        object_delete(bzs=roomBZS, objdelete=patch)
                                    elif patch["type"] == "objpatch":
                                        object_patch(bzs=roomBZS, objpatch=patch)
                                    elif patch["type"] == "objmove":
                                        object_move(
                                            bzs=roomBZS, objmove=patch, nextID=nextID
                                        )
                                        nextID += 1
                                    else:
                                        print(
                                            f"ERROR: unsupported patch type {patch['type']} in stage {stage} layer {layer} room {roomID} patches"
                                        )

                                roomU8.set_file_data("dat/room.bzs", buildBzs(roomBZS))
                                stageU8.set_file_data(
                                    roomPathMatch.group(0), roomU8.build_U8()
                                )
                    if (len(layerOverridePatches) + len(objectPatches)) > 0:
                        write_bytes_create_dirs(
                            modifiedStagePath, stageU8.build_and_compress_U8()
                        )
                        continue
            # uncomment if you want to copy over all files for any reason
            # write_bytes_create_dirs(modifiedStagePath, stagePath.read_bytes())

    def create_oarc_cache(self):
        extracts = yaml_load(EXTRACTS_PATH)
        OARC_CACHE_PATH.mkdir(parents=True, exist_ok=True)

        for extract in extracts:
            # objectpack is a special case (not a stage)
            if "objectpack" in extract:
                arcs = extract["objectpack"]
                arcsNotInCache = [
                    arcName
                    for arcName in arcs
                    if not (OARC_CACHE_PATH / f"{arcName}.arc").exists()
                ]
                if len(arcsNotInCache) == 0:
                    continue
                objectpackU8 = U8File.get_parsed_U8_from_path(OBJECTPACK_PATH, True)
                for arc in arcsNotInCache:
                    print(f"Extracting {arc}")
                    arcData = objectpackU8.get_file_data(f"oarc/{arc}.arc")
                    (OARC_CACHE_PATH / f"{arc}.arc").write_bytes(arcData)
            else:
                arcs = extract["oarcs"]
                stage = extract["stage"]
                layer = extract["layer"]
                allAlreadyInCache = all(
                    ((OARC_CACHE_PATH / f"{arc}.arc").exists() for arc in arcs)
                )
                if allAlreadyInCache:
                    continue
                stagePath = Path(
                    STAGE_FILES_PATH
                    / f"{stage}"
                    / "NX"
                    / f"{stage}_stg_l{layer}.arc.LZ"
                )
                stageU8 = U8File.get_parsed_U8_from_path(stagePath, True)

                for arcName in arcs:
                    print(f"Extracting {arcName}")
                    arcData = stageU8.get_file_data(f"oarc/{arcName}.arc")
                    (OARC_CACHE_PATH / f"{arcName}.arc").write_bytes(arcData)

    def set_oarc_add_remove(self):
        for stage, stagePatches in self.stagePatches.items():
            for patch in stagePatches:
                if patch["type"] == "oarcadd":
                    self.stageOarcAdd[(stage, patch["destlayer"])].add(patch["oarc"])
                elif patch["type"] == "oarcdelete":
                    self.stageOarcRemove[(stage, patch["layer"])].add(patch["oarc"])
