from sslib.yaml import yaml_load
from filepathconstants import TEMP_PLACEMENT_LIST, ITEMS_PATH, CHECKS_PATH
from patches.patchconstants import (
    STAGE_PATCH_PATH_REGEX,
    EVENT_PATCH_PATH_REGEX,
    OARC_ADD_PATH_REGEX,
    SHOP_PATCH_PATH_REGEX,
)
from collections import defaultdict


def determine_check_patches(stagePatchHandler):
    placements = yaml_load(TEMP_PLACEMENT_LIST)
    checks = yaml_load(CHECKS_PATH)
    items = yaml_load(ITEMS_PATH)
    byItemName = dict((x["name"], x) for x in items)

    stagePatches = defaultdict(list)
    stageOarcs = defaultdict(set)

    for checkName, itemName in placements.items():
        check = checks[checkName]
        item = byItemName[itemName]

        for path in check["Paths"]:
            if stagePatchMatch := STAGE_PATCH_PATH_REGEX.match(path):
                stage = stagePatchMatch.group("stage")
                room = int(stagePatchMatch.group("room"))
                layer = int(stagePatchMatch.group("layer"))
                objectName = stagePatchMatch.group("objectName")
                objectID = stagePatchMatch.group("objectID")
                oarc = item["oarc"]

                if oarc:
                    if isinstance(oarc, list):
                        for o in oarc:
                            # stageOarcs[(stage, layer)].add(o)
                            stagePatchHandler.add_oarc_for_check(stage, layer, o)
                    else:
                        # stageOarcs[(stage, layer)].add(oarc)
                        stagePatchHandler.add_oarc_for_check(stage, layer, oarc)

                # stagePatches[(stage, room)].append(objectName, layer, objectID, item["id"])
                stagePatchHandler.add_check_patch(
                    stage, room, objectName, layer, objectID, item["id"]
                )
