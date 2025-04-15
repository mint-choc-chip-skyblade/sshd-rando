import logging
import random
from constants.itemconstants import CTMC_ITEMS_TO_FILTER_OUT, ITEMS_NOT_TO_TRAP
from constants.patchconstants import (
    STAGE_PATCH_PATH_REGEX,
    EVENT_PATCH_PATH_REGEX,
    OARC_ADD_PATH_REGEX,
    SHOP_PATCH_PATH_REGEX,
)
from constants.shopconstants import *
from gui.dialogs.dialog_header import print_progress_text
from logic.location import Location
from logic.world import World

from patches.asmpatchhandler import ASMPatchHandler
from patches.eventpatchhandler import EventPatchHandler
from patches.stagepatchhandler import StagePatchHandler

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logic.item import Item


def determine_check_patches(
    world: World,
    stage_patch_handler: StagePatchHandler,
    event_patch_handler: EventPatchHandler,
    asm_patch_handler: ASMPatchHandler,
):
    print_progress_text("Creating Location Patches")

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

    # A set is okay here because it doesn't touch any randomization
    playthrough_items = set()

    for sphere in world.playthrough_spheres:
        for location in sphere:
            playthrough_items.add(location.current_item.name)

    for location in location_table.values():
        item = location.current_item

        # Deal with items with custom flags
        custom_flag = 0x3FF  # Value for no custom flag
        original_itemid = 0

        if "Custom Flag" in location.types:
            custom_flag = custom_flags.pop()

        if "Stamina Fruits" in location.types:
            original_itemid = 1

            # Don't patch anything if the stamina fruit is vanilla
            if location.current_item == location.world.get_item("Stamina Fruit"):
                continue

        # Don't patch closets if they're off
        if (
            "Closets" in location.types
            and world.setting("npc_closet_shuffle") == "vanilla"
        ):
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
                    and item.name not in ITEMS_NOT_TO_TRAP
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
                # Fi counts as an NPC for this so also include Crest
                if "NPC" in location.types or "Crests" in location.types:
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
                tbox_subtype = -1

                if object_name == "TBox":
                    if (
                        world.setting("chest_type_matches_contents").value()
                        == "all_contents"
                    ):
                        if item.is_major_item:
                            if len(item.chain_locations) > 0:
                                if (
                                    len(
                                        [
                                            loc
                                            for loc in item.chain_locations
                                            if loc.progression
                                        ]
                                    )
                                    > 0
                                ):
                                    tbox_subtype = 0
                                else:
                                    tbox_subtype = 1
                            else:
                                tbox_subtype = 0
                        else:
                            tbox_subtype = 1

                    if world.setting("chest_type_matches_contents").value() != "off":
                        if (
                            item.name in CTMC_ITEMS_TO_FILTER_OUT
                            and item.name not in playthrough_items
                        ):
                            tbox_subtype = 1
                        elif item.is_boss_key:
                            tbox_subtype = 2
                        elif item.is_dungeon_small_key:
                            if (
                                world.setting("small_keys_in_fancy_chests").value()
                                == "on"
                            ):
                                tbox_subtype = 2
                            else:
                                tbox_subtype = 0
                        elif item.is_dungeon_map:
                            tbox_subtype = 1

                for oarc in item_oarcs:
                    stage_patch_handler.add_arcn_for_check(stage, layer, room, oarc)

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
                    tbox_subtype,
                )

            if event_patch_match := EVENT_PATCH_PATH_REGEX.match(path):
                event_file = event_patch_match.group("eventFile")
                eventid = event_patch_match.group("eventID")
                event_patch_handler.add_check_patch(
                    event_file, eventid, item.id, trapid
                )

            if oarc_add_match := OARC_ADD_PATH_REGEX.match(path):
                stage = oarc_add_match.group("stage")
                room = int(oarc_add_match.group("room"))
                layer = int(oarc_add_match.group("layer"))

                for oarc in item_oarcs:
                    stage_patch_handler.add_arcn_for_check(stage, layer, room, oarc)

            if shop_match := SHOP_PATCH_PATH_REGEX.match(path):
                shop_index = int(shop_match.group("index"))
                stage = "F002r"  # Beedle's Airshop
                layer = 0

                if shop_index < 20 or shop_index >= 30:
                    stage = "F004r"  # Bazaar

                for oarc in item_oarcs:
                    stage_patch_handler.add_arcn_for_check(stage, layer, room, oarc)

                create_shop_data(
                    world, asm_patch_handler, location, shop_index, item, trapid
                )


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


def create_shop_data(
    world: World,
    asm_patch_handler: ASMPatchHandler,
    location: Location,
    shop_index: int,
    item: "Item",
    trapid: int,
):
    itemid = item.id
    item_price = world.shop_prices[location.name]
    trapbits = 0xF

    if trapid > 0:
        trapbits = 254 - trapid

    asm_patch_handler.add_shop_data(
        shop_index,
        BUY_DECIDE_SCALES.get(itemid, DEFAULT_BUY_DECIDE_SCALE),
        PUT_SCALES.get(itemid, DEFAULT_PUT_SCALE),
        TARGET_ARROW_HEIGHT_OFFSETS.get(shop_index, -1),
        itemid,
        item_price,
        EVENT_ENTRYPOINTS.get(shop_index, -1),
        NEXT_SHOP_INDEXES.get(shop_index, -1),
        0xFFFF,
        item.shop_arc_name,
        item.shop_model_name,
        DISPLAY_HEIGHT_OFFSETS.get(itemid, DEFAULT_DISPLAY_HEIGHT_OFFSET),
        trapbits,
        SOLD_OUT_STORYFLAGS.get(shop_index, -1),
    )
