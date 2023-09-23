from constants.patchconstants import (
    STAGE_PATCH_PATH_REGEX,
    EVENT_PATCH_PATH_REGEX,
    OARC_ADD_PATH_REGEX,
    SHOP_PATCH_PATH_REGEX,
)

from logic.location import Location
from patches.eventpatchhandler import EventPatchHandler
from patches.stagepatchhandler import StagePatchHandler


def determine_check_patches(
    location_table: dict[str, Location],
    stage_patch_handler: StagePatchHandler,
    event_patch_handler: EventPatchHandler,
):
    for location in location_table.values():
        item = location.current_item

        for path in location.patch_paths:
            if stage_patch_match := STAGE_PATCH_PATH_REGEX.match(path):
                stage = stage_patch_match.group("stage")
                room = int(stage_patch_match.group("room"))
                layer = int(stage_patch_match.group("layer"))
                object_name = stage_patch_match.group("objectName")
                objectid = stage_patch_match.group("objectID")

                if item.oarcs:
                    if isinstance(item.oarcs, list):
                        for oarc in item.oarcs:
                            stage_patch_handler.add_oarc_for_check(stage, layer, oarc)
                    else:
                        stage_patch_handler.add_oarc_for_check(stage, layer, item.oarcs)

                stage_patch_handler.add_check_patch(
                    stage, room, object_name, layer, objectid, item.id
                )

            if event_patch_match := EVENT_PATCH_PATH_REGEX.match(path):
                event_file = event_patch_match.group("eventFile")
                eventid = event_patch_match.group("eventID")
                event_patch_handler.add_check_patch(event_file, eventid, item.id)

            if oarc_add_match := OARC_ADD_PATH_REGEX.match(path):
                stage = oarc_add_match.group("stage")
                layer = int(oarc_add_match.group("layer"))

                if item.oarcs:
                    if isinstance(item.oarcs, list):
                        for oarc in item.oarcs:
                            stage_patch_handler.add_oarc_for_check(stage, layer, oarc)
                    else:
                        stage_patch_handler.add_oarc_for_check(stage, layer, item.oarcs)


def append_dungeon_item_patches(event_patch_handler: EventPatchHandler):
    print("Creating Dungeon Item Patches")

    TEXT_START_SINGLE = "You got the"
    TEXT_START_PLURAL = "You got a"
    DUNGEON_ITEMID_TO_TEXT = {
        200: f"{TEXT_START_PLURAL} <g<Skyview Temple>> Small Key!",
        201: f"{TEXT_START_SINGLE} <y<Lanayru Mining Facility>> Small\nKey!",
        202: f"{TEXT_START_PLURAL} <b<Ancient Cistern>> Small Key!",
        203: f"{TEXT_START_PLURAL} <r<Fire Sanctuary>> Small Key!",
        204: f"{TEXT_START_PLURAL} <y+<Sandship>> Small Key!",
        205: f"{TEXT_START_PLURAL} <s<Sky Keep>> Small Key!",
        206: f"{TEXT_START_SINGLE} <ye<Lanayru Caves>> Small Key!",
        207: f"{TEXT_START_SINGLE} <g<Skyview Temple>> Map!",
        208: f"{TEXT_START_SINGLE} <r+<Earth Temple>> Map!",
        209: f"{TEXT_START_SINGLE} <y<Lanayru Mining Facility>> Map!",
        210: f"{TEXT_START_SINGLE} <b<Ancient Cistern>> Map!",
        211: f"{TEXT_START_SINGLE} <r<Fire Sanctuary>> Map!",
        212: f"{TEXT_START_SINGLE} <y+<Sandship>> Map!",
        213: f"{TEXT_START_SINGLE} <s<Sky Keep>> Map!",
    }

    # Patch the pre-existing entry for the Skyview Small Key (003_200).
    skyview_small_key_text_patch = {
        "name": f"Skyview Key Text",
        "type": "textpatch",
        "index": 251,
        "text": DUNGEON_ITEMID_TO_TEXT[200],
    }

    event_patch_handler.append_to_event_patches(
        "003-ItemGet", skyview_small_key_text_patch
    )

    for itemid in DUNGEON_ITEMID_TO_TEXT:
        textadd_patch = {
            "name": f"Item {itemid} Text",
            "type": "textadd",
            "unk1": 5,
            "unk2": 1,
            "text": DUNGEON_ITEMID_TO_TEXT[itemid],
        }

        flowadd_patch = {
            "name": f"Show Item {itemid} Text",
            "type": "flowadd",
            "flow": {
                "type": "type1",
                "next": -1,
                "param3": 3,
                "param4": f"Item {itemid} Text",
            },
        }

        entryadd_patch = {
            "name": f"Item {itemid} Entry",
            "type": "entryadd",
            "entry": {
                "name": f"003_{itemid}",
                "value": f"Show Item {itemid} Text",
            },
        }

        event_patch_handler.append_to_event_patches("003-ItemGet", textadd_patch)
        event_patch_handler.append_to_event_patches("003-ItemGet", flowadd_patch)
        event_patch_handler.append_to_event_patches("003-ItemGet", entryadd_patch)
