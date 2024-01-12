import logging
import random
from constants.patchconstants import (
    STAGE_PATCH_PATH_REGEX,
    EVENT_PATCH_PATH_REGEX,
    OARC_ADD_PATH_REGEX,
    SHOP_PATCH_PATH_REGEX,
)
from gui.dialogs.dialog_header import print_progress_text
from logic.world import World

from patches.eventpatchhandler import EventPatchHandler
from patches.stagepatchhandler import StagePatchHandler


def determine_check_patches(
    world: World,
    stage_patch_handler: StagePatchHandler,
    event_patch_handler: EventPatchHandler,
):
    # Custom flags currently use 10 total bits as follows
    # in order of most significant to least significant bits:

    # - (1 bit) flag_space_trigger: Used to denote whether this flag is using
    # the unused scene flag space or the unused dungeon flag space

    # - (2 bits) scene index / dungeon index: Used to denote which unused scene/dungeon index the
    # flag is in. There are a total of 4 unused indexes for both scene flags and dungeon flags.
    # Since each index can hold 128 bits, this gives us a total of 1,024 flags to use.

    # - (7 bits) flag: The flag within the unused flag space. Can be any value from 0-127.
    # 128 is used to indicate there being no custom flag (so really we can have up to 1,016 flags)
    custom_flags = [i for i in range(1024) if (i & 0x7F) != 0x7F]
    custom_flags.reverse()

    location_table = world.location_table

    for location in location_table.values():
        item = location.current_item

        # Deal with items with custom flags
        custom_flag = 0x3FF  # Value for no custom flag
        original_itemid = 0

        if "Custom Flag" in location.types:
            custom_flag = custom_flags.pop()

        if "Stamina Fruit" in location.types:
            original_itemid = 1

            # Don't patch anything if the stamina fruit is vanilla
            if location.current_item == location.world.get_item("Stamina Fruit"):
                continue

        # Don't patch closets if they're off
        if "Closet" in location.types and world.setting("npc_closets") == "vanilla":
            continue

        # Deal with traps
        trapid = 0
        trap_oarcs = None
        item_oarcs = []

        if item is not None:
            if item.name.endswith("Trap"):
                trapid = item.id

                trap_oarcs = item.oarcs

                # Don't use items that don't have usable models
                trappable_items = [
                    item
                    for item in world.item_table.values()
                    if item.id < 200  # exclude custom items
                    # Heart, Sailcloth, Non-Practice Swords, Stamina Fruit
                    and item.id not in (6, 15, 9, 11, 12, 13, 14, 42)
                    and not "Song of the Hero" in item.name
                ]

                trappable_items_setting = world.setting("trappable_items")

                if trappable_items_setting == "major_items":
                    trappable_items = [
                        item for item in trappable_items if item.is_major_item
                    ]
                elif trappable_items_setting == "non_major_items":
                    trappable_items = [
                        item for item in trappable_items if not item.is_major_item
                    ]

                # Getting potion models from NPCs is broken rn
                if "NPC" in location.types:
                    trappable_items = [
                        item for item in trappable_items if not "Potion" in item.name
                    ]

                item = random.choice(trappable_items)

            # Combine item.oarcs with trap_oarcs
            item_oarcs = []
            if item.oarcs:
                if isinstance(item.oarcs, list):
                    item_oarcs += item.oarcs
                else:
                    item_oarcs.append(item.oarcs)

            if trap_oarcs:
                if isinstance(trap_oarcs, list):
                    item_oarcs += trap_oarcs
                else:
                    item_oarcs.append(trap_oarcs)

            logging.getLogger("").debug(
                f'Trapped item at "{location}" assigned model of "{item}".'
            )

        for path in location.patch_paths:
            if stage_patch_match := STAGE_PATCH_PATH_REGEX.match(path):
                stage = stage_patch_match.group("stage")
                room = int(stage_patch_match.group("room"))
                layer = int(stage_patch_match.group("layer"))
                object_name = stage_patch_match.group("objectName")
                objectid = stage_patch_match.group("objectID")

                for oarc in item_oarcs:
                    stage_patch_handler.add_oarc_for_check(stage, layer, oarc)

                stage_patch_handler.add_check_patch(
                    stage,
                    room,
                    object_name,
                    layer,
                    objectid,
                    item.id,
                    trapid,
                    custom_flag,
                    original_itemid,
                )

            if event_patch_match := EVENT_PATCH_PATH_REGEX.match(path):
                event_file = event_patch_match.group("eventFile")
                eventid = event_patch_match.group("eventID")
                event_patch_handler.add_check_patch(
                    event_file, eventid, item.id, trapid
                )

            if oarc_add_match := OARC_ADD_PATH_REGEX.match(path):
                stage = oarc_add_match.group("stage")
                layer = int(oarc_add_match.group("layer"))

                for oarc in item_oarcs:
                    stage_patch_handler.add_oarc_for_check(stage, layer, oarc)


def append_dungeon_item_patches(event_patch_handler: EventPatchHandler):
    print_progress_text("Creating Dungeon Item Patches")

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
