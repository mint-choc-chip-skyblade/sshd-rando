# from sslib.yaml import yaml_load
# from filepathconstants import TEMP_PLACEMENT_LIST, ITEMS_PATH, CHECKS_PATH
from constants.patchconstants import (
    STAGE_PATCH_PATH_REGEX,
    EVENT_PATCH_PATH_REGEX,
    OARC_ADD_PATH_REGEX,
    SHOP_PATCH_PATH_REGEX,
)


def determine_check_patches(locationTable, stagePatchHandler, eventPatchhandler):
    # placements = yaml_load(TEMP_PLACEMENT_LIST)
    # checks = yaml_load(CHECKS_PATH)
    # items = yaml_load(ITEMS_PATH)
    # byItemName = dict((x["name"], x) for x in items)

    for location in locationTable.values():
        item = location.current_item

        for path in location.patch_paths:
            if stagePatchMatch := STAGE_PATCH_PATH_REGEX.match(path):
                stage = stagePatchMatch.group("stage")
                room = int(stagePatchMatch.group("room"))
                layer = int(stagePatchMatch.group("layer"))
                objectName = stagePatchMatch.group("objectName")
                objectID = stagePatchMatch.group("objectID")

                if item.oarcs:
                    if isinstance(item.oarcs, list):
                        for o in item.oarcs:
                            stagePatchHandler.add_oarc_for_check(stage, layer, o)
                    else:
                        stagePatchHandler.add_oarc_for_check(stage, layer, item.oarcs)

                stagePatchHandler.add_check_patch(
                    stage, room, objectName, layer, objectID, item.id
                )
            if eventPatchMatch := EVENT_PATCH_PATH_REGEX.match(path):
                eventFile = eventPatchMatch.group("eventFile")
                eventID = eventPatchMatch.group("eventID")
                eventPatchhandler.add_check_patch(eventFile, eventID, item.id)
            if oarcAddMatch := OARC_ADD_PATH_REGEX.match(path):
                stage = oarcAddMatch.group("stage")
                layer = int(oarcAddMatch.group("layer"))

                if item.oarcs:
                    if isinstance(item.oarcs, list):
                        for o in item.oarcs:
                            stagePatchHandler.add_oarc_for_check(stage, layer, o)
                    else:
                        stagePatchHandler.add_oarc_for_check(stage, layer, item.oarcs)
