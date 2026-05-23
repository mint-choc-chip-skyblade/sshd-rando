from collections import Counter
import os
import random
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from constants.configconstants import get_default_setting
from constants.itemconstants import STARTABLE_ITEMS
from logic.item import Item
from logic.requirements import (
    Requirement,
    RequirementType,
    evaluate_requirement_at_time,
    visit_requirement,
)
from logic.search import Search, SearchMode
from logic.settings import Setting, SettingMap, get_all_settings_info
from logic.tooltips.tooltips import TooltipsSearch, print_req
from logic.world import World
from util.text import load_text_data

"""
The entire point of the tooltips code is to accurately inform
the user which items are needed to put which checks in logic.
To verify correctness, we can fuzz the code against the base
logic search. Generate a world with some settings, generate
a random inventory, and check that the tooltip expressions are
true if and only if search puts them in logic.
"""


def default_tracker_settings() -> SettingMap:
    load_text_data()
    setting_map = SettingMap()
    setting_map.starting_inventory = get_default_setting("starting_inventory")
    setting_map.excluded_locations = get_default_setting("excluded_locations")
    setting_map.excluded_hint_locations = get_default_setting("excluded_hint_locations")
    setting_map.mixed_entrance_pools = get_default_setting("mixed_entrance_pools")
    all_settings_info = get_all_settings_info()
    for setting, info in all_settings_info.items():
        setting_map.settings[setting] = Setting(
            setting, info.options[info.default_option_index], info
        )

    return setting_map


def test_default_settings():
    settings = default_tracker_settings()

    # TODO maybe avoid having to build two worlds
    logic_world = World(0)
    logic_world.setting_map = settings
    logic_world.num_worlds = 1
    tracker_world = World(0)
    tracker_world.setting_map = settings
    tracker_world.is_tracker = True
    tracker_world.num_worlds = 1

    random.seed("tracker-test")
    logic_world.build()
    random.seed("tracker-test")
    tracker_world.build()

    tooltips = TooltipsSearch(tracker_world)
    tooltips.do_search()

    empty_inventory: Counter[Item] = Counter()

    inventories = [empty_inventory]
    for i in range(len(STARTABLE_ITEMS)):
        inventory = empty_inventory.copy()
        pool = STARTABLE_ITEMS.copy()
        random.shuffle(pool)
        take_items = pool[0:i]
        for i in take_items:
            item = logic_world.get_item(i)
            inventory[item] += 1
        inventories.append(inventory)

    for inventory in inventories:
        search = Search(SearchMode.ACCESSIBLE_LOCATIONS, [logic_world], inventory)
        search.search_worlds()

        tooltip_inventory = inventory.copy()
        for item, count in tracker_world.starting_item_pool.items():
            tooltip_inventory[item] += count

        tooltips_world_search = Search(
            SearchMode.ACCESSIBLE_LOCATIONS, [tracker_world], inventory
        )
        tooltips_world_search.search_worlds()
        # time of days are eliminated here
        mock_tod: int = None  # type: ignore

        i = 0

        for location in logic_world.get_all_item_locations():
            is_in_logic = location in search.visited_locations
            tooltip_requirement = tracker_world.get_location(
                location.name
            ).computed_requirement

            def assert_requirement_type(req: Requirement):
                assert (
                    req.type == RequirementType.TRACKER_NOTE
                    or req.type == RequirementType.AND
                    or req.type == RequirementType.OR
                    or req.type == RequirementType.WALLET_CAPACITY
                    or req.type == RequirementType.GRATITUDE_CRYSTALS
                    or req.type == RequirementType.ITEM
                    or req.type == RequirementType.COUNT
                    or req.type == RequirementType.IMPOSSIBLE
                    or req.type == RequirementType.NOTHING
                )

            visit_requirement(tooltip_requirement, assert_requirement_type)

            is_tooltip_in_logic = evaluate_requirement_at_time(
                tooltip_requirement, tooltips_world_search, mock_tod, tracker_world
            )

            assert (
                is_in_logic == is_tooltip_in_logic
            ), f"{location.name} - {print_req(tooltip_requirement)}"
            if is_in_logic:
                i += 1

        print("matching locations in logic: ", i)
