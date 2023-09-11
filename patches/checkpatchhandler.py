# from sslib.yaml import yaml_load
# from filepathconstants import TEMP_PLACEMENT_LIST, ITEMS_PATH, CHECKS_PATH
from constants.patchconstants import (
    STAGE_PATCH_PATH_REGEX,
    EVENT_PATCH_PATH_REGEX,
    OARC_ADD_PATH_REGEX,
    SHOP_PATCH_PATH_REGEX,
)


def determine_check_patches(locationTable, stagePatchHandler, eventPatchhandler):
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


def append_dungeon_item_patches(eventPatchHandler):
    print("Creating Dungeon Item Patches")

    TEXT_START_SINGLE = "You got the"
    TEXT_START_PLURAL = "You got a"
    DUNGEON_ITEMID_TO_TEXT = {
        201: f"{TEXT_START_SINGLE} <y<Lanayru Mining Facility>> Small\nKey!",
        202: f"{TEXT_START_PLURAL} <b<Ancient Cistern>> Small Key!",
        203: f"{TEXT_START_PLURAL} <r<Fire Sanctuary>> Small Key!",
        204: f"{TEXT_START_PLURAL} <y+<Sandship>> Small Key!",
        205: f"{TEXT_START_PLURAL} <s<Sky Keep>> Small Key!",
        206: f"{TEXT_START_SINGLE} <ye<Lanayru Caves>> Small Key!",
        207: f"{TEXT_START_SINGLE} <g<Skyview>> Map!",
        208: f"{TEXT_START_SINGLE} <r+<Earth Temple>> Map!",
        209: f"{TEXT_START_SINGLE} <y<Lanayru Mining Facility>> Map!",
        210: f"{TEXT_START_SINGLE} <b<Ancient Cistern>> Map!",
        211: f"{TEXT_START_SINGLE} <r<Fire Sanctuary>> Map!",
        212: f"{TEXT_START_SINGLE} <y+<Sandship>> Map!",
        213: f"{TEXT_START_SINGLE} <s<Sky Keep>> Map!",
    }

    # Patch the pre-existing entry for the Skyview Small Key (003_200).
    skyviewSmallKeyTextPatch = {
        "name": f"Skyview Key Text",
        "type": "textpatch",
        "index": 251,
        "text": f"You got a\nSkyview Small Key!",
    }

    eventPatchHandler.append_to_event_patches("003-ItemGet", skyviewSmallKeyTextPatch)

    for itemid in DUNGEON_ITEMID_TO_TEXT:
        textaddPatch = {
            "name": f"Item {itemid} Text",
            "type": "textadd",
            "unk1": 5,
            "unk2": 1,
            "text": DUNGEON_ITEMID_TO_TEXT[itemid],
        }

        flowaddPatch = {
            "name": f"Show Item {itemid} Text",
            "type": "flowadd",
            "flow": {
                "type": "type1",
                "next": -1,
                "param3": 3,
                "param4": f"Item {itemid} Text",
            },
        }

        entryaddPatch = {
            "name": f"Item {itemid} Entry",
            "type": "entryadd",
            "entry": {
                "name": f"003_{itemid}",
                "value": f"Show Item {itemid} Text",
            },
        }

        eventPatchHandler.append_to_event_patches("003-ItemGet", textaddPatch)
        eventPatchHandler.append_to_event_patches("003-ItemGet", flowaddPatch)
        eventPatchHandler.append_to_event_patches("003-ItemGet", entryaddPatch)
