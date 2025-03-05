from constants.shopconstants import BEEDLE_TEXT_PATCHES
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

    add_sky_keep_goal_loc_patches(world)

    add_rando_hash(world, event_patch_handler)

    apply_shop_text_patches(world, event_patch_handler)

    apply_boss_rush_text_patches(world, event_patch_handler)


def add_fi_text_patches(world: World, event_patch_handler: EventPatchHandler) -> None:
    # Required dungeons
    DUNGEON_COLORS = {
        get_text_data("Skyview Temple"): "g",
        get_text_data("Earth Temple"): "r+",
        get_text_data("Lanayru Mining Facility"): "y",
        get_text_data("Ancient Cistern"): "b",
        get_text_data("Sandship"): "y+",
        get_text_data("Fire Sanctuary"): "r",
        get_text_data("Sky Keep"): "s",
    }

    colorful_dungeon_text = tuple(
        dungeon.apply_text_color(DUNGEON_COLORS[dungeon])
        for dungeon in DUNGEON_COLORS
        if world.dungeons[dungeon.text["en_US"]].required
    )

    dungeon_text = Text()
    for text in colorful_dungeon_text:
        dungeon_text += text + Text("\n")

    num_dungeons = len(colorful_dungeon_text)
    if num_dungeons == 0:
        required_dungeons_text = get_text_data("No Required Dungeons Text")
    elif num_dungeons == 7 or (
        num_dungeons == 6 and world.setting("dungeons_include_sky_keep") == "off"
    ):
        required_dungeons_text = get_text_data("All Required Dungeons Text")
    else:
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

    # Fi hints
    # Determines how many hints will be shown back-to-back before a new
    # eventflow is created. The main limiting factor is the number of
    # characters the game can fit into the text buffer ~500 iirc
    FI_HINTS_PER_EVENTFLOW = 6

    fi_hint_chunks: list[list[Text]] = []
    fi_hints = [loc.hint.text for loc in world.fi_hints]
    for i in range(0, len(fi_hints), FI_HINTS_PER_EVENTFLOW):
        fi_hint_chunks.append(fi_hints[i : i + FI_HINTS_PER_EVENTFLOW])

    if fi_hint_chunks:
        for chunk_index, hints in enumerate(fi_hint_chunks):
            event_patch_handler.append_to_event_patches(
                "006-8KenseiNormal",
                {
                    "name": f"Display Fi Hints Text {chunk_index}",
                    "type": "flowadd",
                    "flow": {
                        "type": "type1",
                        "next": (
                            f"Display Fi Hints Text {chunk_index + 1}"
                            if chunk_index < (len(fi_hint_chunks) - 1)
                            else -1
                        ),
                        "param3": 68,
                        "param4": f"Fi Hints Text {chunk_index}",
                    },
                },
            )
            event_patch_handler.append_to_event_patches(
                "006-8KenseiNormal",
                {
                    "name": f"Fi Hints Text {chunk_index}",
                    "type": "textadd",
                    "textboxtype": 2,
                },
            )
            add_text_data(
                f"Fi Hints Text {chunk_index}", break_and_make_multiple_textboxes(hints)
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

    # Fi Notes (Gossip Stone hints that the player has already found)
    all_stone_names = [stone.name for stone in world.get_gossip_stones()]
    current_note_index = 0
    for stone, locations in world.gossip_stone_hints.items():
        hints = [loc.hint.text for loc in locations]

        event_patch_handler.append_to_event_patches(
            "006-8KenseiNormal",
            {
                "name": f"Check Fi Note {current_note_index} Found",
                "type": "checkstoryflag",
                "flow": {"checkstoryflag": 956 + all_stone_names.index(stone.name)},
                "cases": [
                    f"Display Fi Note {current_note_index}",
                    f"Check Fi Note {current_note_index + 1} Found",
                ],
            },
        )
        event_patch_handler.append_to_event_patches(
            "006-8KenseiNormal",
            {
                "name": f"Display Fi Note {current_note_index}",
                "type": "flowadd",
                "flow": {
                    "type": "type1",
                    "next": f"Check Fi Note {current_note_index + 1} Found",
                    "param3": 68,
                    "param4": f"Fi Note {current_note_index} Text",
                },
            },
        )
        event_patch_handler.append_to_event_patches(
            "006-8KenseiNormal",
            {
                "name": f"Fi Note {current_note_index} Text",
                "type": "textadd",
                "textboxtype": 2,
            },
        )
        add_text_data(
            f"Fi Note {current_note_index} Text",
            break_and_make_multiple_textboxes(hints),
        )

        current_note_index += 1

    # Show end of notes text (yes, the name is inaccurate but there's no need to change it)
    event_patch_handler.append_to_event_patches(
        "006-8KenseiNormal",
        {
            "name": f"Check Fi Note {current_note_index} Found",
            "type": "flowadd",
            "flow": {
                "type": "type1",
                "next": -1,
                "param3": 68,
                "param4": "Fi Note No More Information Text",
            },
        },
    )
    event_patch_handler.append_to_event_patches(
        "006-8KenseiNormal",
        {
            "name": "Fi Note No More Information Text",
            "type": "textadd",
            "textboxtype": 2,
        },
    )

    # Objective text
    event_patch_handler.append_to_event_patches(
        "006-8KenseiNormal",
        {
            "name": "Fi Objective Text",
            "type": "textadd",
            "textboxtype": 2,
        },
    )
    fi_objective_text = get_text_data("Fi Objective Text Template")
    sword_name = get_text_data(world.setting("got_sword_requirement").pretty_value())
    fi_objective_text = fi_objective_text.replace("{required_sword}", sword_name)
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
    gossip_stones_in_order = [stone.name for stone in world.get_gossip_stones()]

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

        event_patch_handler.append_to_event_patches(
            stone.hint_textfile,
            {
                "name": f"Go to storyflag for {stone}",
                "type": "flowpatch",
                "index": stone.eventflowindex,
                "flow": {
                    "next": f"Set storyflag for {stone}",
                },
            },
        )
        event_patch_handler.append_to_event_patches(
            stone.hint_textfile,
            {
                "name": f"Set storyflag for {stone}",
                "type": "setstoryflag",
                "flow": {
                    "setstoryflag": 956 + gossip_stones_in_order.index(stone.name),
                    "next": -1,
                },
            },
        )


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
        inventory_text = get_text_data(f"{song_item} Inventory")
        item_get_text = get_text_data(obtain_text_name)
        # If we have extra hint text, add it onto the song text
        if song_item in world.song_hints:
            useful_text = world.song_hints[song_item].text
            inventory_text += useful_text
            item_get_text += useful_text
        inventory_text.break_lines()
        item_get_text.break_lines()
        event_patch_handler.append_to_event_patches(
            "003-ItemGet",
            {
                "name": f"{song_item} Inventory",
                "type": "textpatch",
                "index": inventory_text_idx,
            },
        )


def add_sky_keep_goal_loc_patches(world: World) -> None:
    sky_keep = world.get_dungeon("Sky Keep")
    goal = sky_keep.goal_location
    goal_text = get_text_data("Sky Keep No Goal Location Text")

    if sky_keep.required and goal is not None:
        if goal.name.endswith("Farore"):
            goal_text = get_text_data(
                "Sky Keep Goal Location Sacred Power of Farore Text"
            )
        elif goal.name.endswith("Nayru"):
            goal_text = get_text_data(
                "Sky Keep Goal Location Sacred Power of Nayru Text"
            )
        elif goal.name.endswith("Din"):
            goal_text = get_text_data("Sky Keep Goal Location Sacred Power of Din Text")

    add_text_data("Sky Keep goal location sign text with replaced text", goal_text)


def add_rando_hash(world: World, event_patch_handler: EventPatchHandler) -> None:
    hash = world.config.get_hash()

    event_patch_handler.append_to_event_patches(
        "002-System",
        {"name": "Rando hash on file select", "type": "textpatch", "index": 66},
    )
    add_text_data("Rando hash on file select", Text("") + hash)

    event_patch_handler.append_to_event_patches(
        "002-System",
        {"name": "Rando hash on new file", "type": "textpatch", "index": 69},  # Nice
    )
    add_text_data("Rando hash on new file", Text("") + hash)


def apply_shop_text_patches(
    world: World, event_patch_handler: EventPatchHandler
) -> None:
    for location_name in BEEDLE_TEXT_PATCHES:
        location = world.get_location(location_name)
        sold_item_text = get_text_data(location.current_item.name, "pretty")
        normal_text_index, discounted_text_index = BEEDLE_TEXT_PATCHES[location_name]
        normal_price = world.shop_prices[location_name]
        discounted_price = normal_price // 2

        # Normal shop text
        patch_name = f"{location_name} Normal Text"

        if type(normal_text_index) != int:
            patch_name = normal_text_index
            event_patch_handler.append_to_event_patches(
                "105-Terry",
                {
                    "name": patch_name,
                    "type": "textadd",
                },
            )
        else:
            event_patch_handler.append_to_event_patches(
                "105-Terry",
                {
                    "name": patch_name,
                    "type": "textpatch",
                    "index": normal_text_index,
                },
            )

        shop_normal_text = get_text_data("Beedle Normal Shop Text Template")

        shop_normal_text = shop_normal_text.replace(
            "{sold_item}", Text.apply_text_color(sold_item_text, "y")
        )
        shop_normal_text = shop_normal_text.replace("{normal_price}", str(normal_price))
        shop_normal_text.resolve_plurality(sold_item_text)

        add_text_data(patch_name, shop_normal_text)

        # Discounted shop text
        patch_name = f"{location_name} Discounted Text"

        if type(discounted_text_index) != int:
            patch_name = discounted_text_index
            event_patch_handler.append_to_event_patches(
                "105-Terry",
                {
                    "name": patch_name,
                    "type": "textadd",
                },
            )
        else:
            event_patch_handler.append_to_event_patches(
                "105-Terry",
                {
                    "name": patch_name,
                    "type": "textpatch",
                    "index": discounted_text_index,
                },
            )

        shop_discounted_text = get_text_data("Beedle Discounted Shop Text Template")

        shop_discounted_text = shop_discounted_text.replace(
            "{sold_item}", Text.apply_text_color(sold_item_text, "y")
        )
        shop_discounted_text = shop_discounted_text.replace(
            "{discounted_price}", str(discounted_price)
        )
        shop_discounted_text.resolve_plurality(sold_item_text)

        add_text_data(patch_name, shop_discounted_text)


def apply_boss_rush_text_patches(world: World, event_patch_handler: EventPatchHandler):
    # Patch defeat 4 bosses text.
    boss_rush_item1_patch_name = "Patch Boss Rush 4 Boss Reward Text"

    event_patch_handler.append_to_event_patches(
        "460-RairyuMinigame",
        {
            "name": f"{boss_rush_item1_patch_name}",
            "type": "textpatch",
            "index": 105,
        },
    )

    boss_rush_location1 = world.get_location("Lanayru Gorge - Boss Rush 4 Bosses")
    boss_rush_item1_text = get_text_data(
        boss_rush_location1.current_item.name, "standard"
    )

    add_text_data(boss_rush_item1_patch_name, boss_rush_item1_text)

    # Patch defeat 8 bosses text.
    boss_rush_item2_patch_name = "Patch Boss Rush 8 Boss Reward Text"

    event_patch_handler.append_to_event_patches(
        "460-RairyuMinigame",
        {
            "name": f"{boss_rush_item2_patch_name}",
            "type": "textpatch",
            "index": 109,
        },
    )

    boss_rush_location2 = world.get_location("Lanayru Gorge - Boss Rush 8 Bosses")
    boss_rush_item2_text = get_text_data(
        boss_rush_location2.current_item.name, "standard"
    )

    add_text_data(boss_rush_item2_patch_name, boss_rush_item2_text)

    # Patch Thunder Dragon's intro yapping to include randomized rewards.
    boss_rush_dragon_text_patch_name = "Thunder Dragon Boss Rush Rewards Text"
    boss_rush_dragon_text = get_text_data(
        "Thunder Dragon Boss Rush Rewards Template Text", "standard"
    )

    boss_rush_dragon_text = boss_rush_dragon_text.replace(
        "{boss_rush_item1}",
        Text.apply_text_color(
            get_text_data(boss_rush_location1.current_item.name, "pretty"), "r"
        ),
    )
    boss_rush_dragon_text = boss_rush_dragon_text.replace(
        "{boss_rush_item2}",
        Text.apply_text_color(
            get_text_data(boss_rush_location2.current_item.name, "pretty"), "r"
        ),
    )
    boss_rush_dragon_text.break_lines()

    event_patch_handler.append_to_event_patches(
        "460-RairyuMinigame",
        {
            "name": f"{boss_rush_dragon_text_patch_name}",
            "type": "textpatch",
            "index": 5,
        },
    )

    add_text_data(boss_rush_dragon_text_patch_name, boss_rush_dragon_text)
