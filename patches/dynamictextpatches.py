from patches.eventpatchhandler import *
from logic.world import *


def add_dynamic_text_patches(
    world: World, event_patch_handler: EventPatchHandler
) -> None:
    print_progress_text("Adding Text Patches")

    add_fi_text_patches(world, event_patch_handler)
    add_gossip_stone_text_patches(world, event_patch_handler)

    if world.impa_sot_hint:
        add_impa_text_patches(world, event_patch_handler)

    add_song_text_patches(world, event_patch_handler)


def add_fi_text_patches(world: World, event_patch_handler: EventPatchHandler) -> None:
    DUNGEON_COLORS = {
        "Skyview Temple": "<g<",
        "Earth Temple": "<r+<",
        "Lanayru Mining Facility": "<y<",
        "Ancient Cistern": "<b<",
        "Sandship": "<y+<",
        "Fire Sanctuary": "<r<",
        "Sky Keep": "<s<",
    }

    colorful_dungeon_text = tuple(
        DUNGEON_COLORS[dungeon] + dungeon + ">>\n"
        for dungeon in DUNGEON_COLORS
        if world.dungeons[dungeon].required
    )

    dungeon_text = ""
    for text in colorful_dungeon_text:
        dungeon_text += text

    match len(colorful_dungeon_text):
        case 0:
            required_dungeons_text = get_text_data("No Required Dungeons Text")
        case 6:
            required_dungeons_text = get_text_data("All Required Dungeons Text")
        case _:
            required_dungeons_text = get_text_data("Some Required Dungeons Text")
            required_dungeons_text = required_dungeons_text.replace(
                "{dungeon_text}",
                dungeon_text,
            )

    event_patch_handler.append_to_event_patches(
        "006-8KenseiNormal",
        {
            "name": "Required Dungeons Text",
            "type": "textadd",
            "textboxtype": 2,
        },
    )
    add_text_data(
        "Required Dungeons Text",
        required_dungeons_text,
    )

    event_patch_handler.append_to_event_patches(
        "006-8KenseiNormal",
        {
            "name": "Display Required Dungeons",
            "type": "flowadd",
            "flow": {
                "type": "type1",
                "next": -1,
                "param3": 68,
                "param4": "Required Dungeons Text",
            },
        },
    )

    fi_hint_chunks: list[list[Text]] = []
    fi_hints = [loc.hint.text for loc in world.fi_hints]
    for i in range(0, len(fi_hints), 8):
        fi_hint_chunks.append(fi_hints[i : i + 8])

    if fi_hint_chunks:
        for ind, hints in enumerate(fi_hint_chunks):
            event_patch_handler.append_to_event_patches(
                "006-8KenseiNormal",
                {
                    "name": f"Display Fi Hints Text {ind}",
                    "type": "flowadd",
                    "flow": {
                        "type": "type1",
                        "next": (
                            f"Display Fi Hints Text {ind + 1}"
                            if ind < (len(fi_hint_chunks) - 1)
                            else -1
                        ),
                        "param3": 68,
                        "param4": f"Fi Hints Text {ind}",
                    },
                },
            )
            event_patch_handler.append_to_event_patches(
                "006-8KenseiNormal",
                {
                    "name": f"Fi Hints Text {ind}",
                    "type": "textadd",
                    "textboxtype": 2,
                },
            )
            add_text_data(
                f"Fi Hints Text {ind}", break_and_make_multiple_textboxes(hints)
            )
    else:
        event_patch_handler.append_to_event_patches(
            "006-8KenseiNormal",
            {
                "name": "Display Fi Hints Text 0",
                "type": "flowadd",
                "flow": {
                    "type": "type1",
                    "next": -1,
                    "param3": 68,
                    "param4": f"No Fi Hints Text",
                },
            },
        )
        event_patch_handler.append_to_event_patches(
            "006-8KenseiNormal",
            {
                "name": f"No Fi Hints Text",
                "type": "textadd",
                "textboxtype": 2,
            },
        )

    event_patch_handler.append_to_event_patches(
        "006-8KenseiNormal",
        {
            "name": "Fi Objective Text",
            "type": "textadd",
            "textboxtype": 2,
        },
    )

    fi_objective_text = get_text_data("Fi Objective Text Template")
    fi_objective_text = fi_objective_text.replace("{required_sword}", "Master Sword")
    add_text_data(
        "Fi Objective Text",
        fi_objective_text,
    )

    # # dungeon status text for Fi
    # for dungeon_index, dungeon in enumerate(ALL_DUNGEONS):
    #     event_patch_handler["006-8KenseiNormal"].append(
    #         {
    #             "name": f"{dungeon} Status Values Command Call",
    #             "type": "flowadd",
    #             "flow": {
    #                 "type": "type3",
    #                 "next": f"Display {dungeon} Status Text",
    #                 "param1": DUNGEONFLAG_INDICES[dungeon],
    #                 "param2": DUNGEON_COMPLETE_STORYFLAGS[dungeon]
    #                 if dungeon in self.placement_file.required_dungeons
    #                 else -1,
    #                 "param3": 71,
    #             },
    #         }
    #     )

    #     event_patch_handler["006-8KenseiNormal"].append(
    #         {
    #             "name": f"Display {dungeon} Status Text",
    #             "type": "flowadd",
    #             "flow": {
    #                 "type": "type1",
    #                 "next": f"{ALL_DUNGEONS[dungeon_index + 1]} Status Values Command Call"
    #                 if dungeon_index < 6
    #                 else -1,
    #                 "param3": 68,
    #                 "param4": f"{dungeon} Status Text",
    #             },
    #         }
    #     )

    #     if dungeon in REGULAR_DUNGEONS:
    #         event_patch_handler["006-8KenseiNormal"].append(
    #             {
    #                 "name": f"{dungeon} Status Text",
    #                 "type": "textadd",
    #                 "textboxtype": 2,
    #                 "text": f"{DUNGEON_COLORS[dungeon] + dungeon}>>: <string arg2> \nSmall Keys: <numeric arg0> \nBoss Key: <string arg0> \nDungeon Map: <string arg1>"
    #                 if dungeon != ET
    #                 else f"{DUNGEON_COLORS[dungeon] + dungeon}>>: <string arg2> \nKey Pieces: <numeric arg0> \nBoss Key: <string arg0> \nDungeon Map: <string arg1>",
    #             }
    #         )
    #     else:
    #         event_patch_handler["006-8KenseiNormal"].append(
    #             {
    #                 "name": "Sky Keep Status Text",
    #                 "type": "textadd",
    #                 "textboxtype": 2,
    #                 "text": f"{DUNGEON_COLORS[SK]}Sky Keep>>\nSmall Keys: <numeric arg0>\n\nDungeon Map: <string arg1>",
    #             }
    #         )


def add_gossip_stone_text_patches(
    world: World, event_patch_handler: EventPatchHandler
) -> None:
    for stone, locations in world.gossip_stone_hints.items():
        hints = [loc.hint.text for loc in locations]
        event_patch_handler.append_to_event_patches(
            stone.hint_textfile,
            {
                "name": f"Hint {stone}",
                "type": "textpatch",
                "index": stone.hint_textindex,
            },
        )
        add_text_data(f"Hint {stone}", break_and_make_multiple_textboxes(hints))


def add_impa_text_patches(world: World, event_patch_handler: EventPatchHandler) -> None:
    event_patch_handler.append_to_event_patches(
        "502-CenterFieldBack",
        {
            "name": "Past Impa SoT Hint",
            "type": "textpatch",
            "index": 6,
        },
    )
    world.impa_sot_hint.text.break_lines()
    add_text_data("Past Impa SoT Hint", world.impa_sot_hint.text)


def add_song_text_patches(world: World, event_patch_handler: EventPatchHandler) -> None:
    # Mapping of song item to label and inventory text index
    song_items = {
        world.get_item("Song of the Hero"): (
            "Full SotH text",
            659,
        ),
        world.get_item("Farore's Courage"): (
            "Farore's Courage Text",
            653,
        ),
        world.get_item("Nayru's Wisdom"): (
            "Nayru's Wisdom Text",
            654,
        ),
        world.get_item("Din's Power"): (
            "Din's Power Text",
            655,
        ),
    }
    for song_item, (
        obtain_text_name,
        inventory_text_idx,
    ) in song_items.items():
        if song_item in world.song_hints:
            useful_text = Text(" ") + world.song_hints[song_item].text
            inventory_text = get_text_data(f"{song_item} Inventory")
            inventory_text += useful_text
            inventory_text.break_lines()
            item_get_text = get_text_data(obtain_text_name)
            item_get_text += useful_text
            item_get_text.break_lines()
        event_patch_handler.append_to_event_patches(
            "003-ItemGet",
            {
                "name": f"{song_item} Inventory",
                "type": "textpatch",
                "index": inventory_text_idx,
            },
        )
