import random
from constants.itemconstants import TRAP_OARC_NAMES
from constants.patchconstants import (
    STAGE_PATCH_PATH_REGEX,
    EVENT_PATCH_PATH_REGEX,
    OARC_ADD_PATH_REGEX,
    SHOP_PATCH_PATH_REGEX,
)

from logic.config import Config

from logic.location import Location
from patches.eventpatchhandler import EventPatchHandler
from patches.stagepatchhandler import StagePatchHandler


def determine_check_patches(
    location_table: dict[str, Location],
    stage_patch_handler: StagePatchHandler,
    event_patch_handler: EventPatchHandler,
    config: Config,
):
    for location in location_table.values():
        item = location.current_item

        trapid = 0
        itemid = -1
        item_name = ""
        if item is not None:
            itemid = item.id
            item_name = item.name

        # TODO: make sure all models are in extracts.yaml
        if config.settings[0].settings["traps"].value == "on" and item_name.endswith(
            "Trap"
        ):
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(item.name)

            trapid = itemid

            if not item.oarcs:
                item.oarcs = list()

            if isinstance(item.oarcs, list):
                itemid = random.choice(list(TRAP_OARC_NAMES.keys()))
                item.oarcs.append(
                    TRAP_OARC_NAMES[itemid][0]
                )  # TODO: implement variations

                print(itemid, TRAP_OARC_NAMES[itemid], item.oarcs)

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
                    stage, room, object_name, layer, objectid, itemid, trapid
                )

            if event_patch_match := EVENT_PATCH_PATH_REGEX.match(path):
                event_file = event_patch_match.group("eventFile")
                eventid = event_patch_match.group("eventID")
                # TODO: does this need to use the random_item_id from the traps stuff?
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

    DUNGEON_ITEMIDS = [
        200,
        201,
        202,
        203,
        204,
        205,
        206,
        207,
        208,
        209,
        210,
        211,
        212,
        213,
    ]

    # Patch the pre-existing entry for the Skyview Small Key (003_200).
    skyview_small_key_text_patch = {
        "name": f"Skyview Key Text",
        "type": "textpatch",
        "index": 251,
    }

    event_patch_handler.append_to_event_patches(
        "003-ItemGet", skyview_small_key_text_patch
    )

    for itemid in DUNGEON_ITEMIDS:
        textadd_patch = {
            "name": f"Item {itemid} Text",
            "type": "textadd",
            "textboxtype": 5,
            "unk2": 1,
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
