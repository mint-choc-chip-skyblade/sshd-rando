from constants.itemconstants import *
from .settings import *
from .item import *

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import World


class ItemPoolError(RuntimeError):
    pass


# Generates the item pool for a single world
# Items being placed in vanilla or restricted
# location sets will be filtered out later. Items
# that need to be removed and not placed anywhere
# will be removed now
def generate_item_pool(world: "World") -> None:
    item_pool = STANDARD_ITEM_POOL

    match world.setting("item_pool"):
        case "minimal":
            item_pool = MINIMAL_ITEM_POOL
        case "standard":
            item_pool = STANDARD_ITEM_POOL
        case "extra":
            item_pool = EXTRA_ITEM_POOL
        case "plentiful":
            item_pool = PLENTIFUL_ITEM_POOL

    # Remove Key Pieces if the ET Door is open
    if world.setting("open_earth_temple") == "on":
        item_pool = [item for item in item_pool if item != KEY_PIECE]

    if world.setting("small_keys") == "removed":
        item_pool = [
            item
            for item in item_pool
            if not item.endswith(SMALL_KEY) or item == LC_SMALL_KEY
        ]

    if world.setting("lanayru_caves_key") == "removed":
        item_pool.remove(LC_SMALL_KEY)

    if world.setting("boss_keys") == "removed":
        item_pool = [item for item in item_pool if not item.endswith(BOSS_KEY)]

    for item_name in item_pool:
        item = world.get_item(item_name)
        world.item_pool[item] += 1


# Will remove items from the passed in world's item pool
# and add them to the starting pool.
def generate_starting_item_pool(world: "World"):
    starting_items = world.setting_map.starting_inventory

    # Add starting swords
    starting_sword_setting = world.setting_map.settings.get("starting_sword")

    if starting_sword_setting:
        starting_items[PROGRESSIVE_SWORD] = starting_sword_setting.current_option_index

    # Deal with starting tablets
    starting_tablet_count = world.setting("starting_tablet_count").value_as_number()

    if starting_tablet_count > 0:
        inventory_tablets = [
            item for item in world.setting_map.starting_inventory if item in ALL_TABLETS
        ]

        if len(inventory_tablets) + starting_tablet_count >= 3:
            for tablet in ALL_TABLETS:
                starting_items[tablet] = 1
        else:
            tablet_pool = [
                tablet for tablet in ALL_TABLETS if tablet not in inventory_tablets
            ]

            for _ in range(starting_tablet_count):
                random_tablet = random.choice(tablet_pool)
                tablet_pool.remove(random_tablet)
                starting_items[random_tablet] = 1

    for item_name, count in starting_items.items():
        item = world.get_item(item_name)
        world.starting_item_pool[item] += count
        world.item_pool[item] -= count

    # If all three parts of the song of the hero are in the starting inventory
    # replace them with just the singular song of the hero
    all_soth_parts = {
        FARON_SOTH_PART,
        ELDIN_SOTH_PART,
        LANAYRU_SOTH_PART,
    }
    if all(world.get_item(part) in world.starting_item_pool for part in all_soth_parts):
        for part in all_soth_parts:
            part_item = world.get_item(part)
            world.starting_item_pool[part_item] = 0
        world.starting_item_pool[world.get_item(SONG_OF_THE_HERO)] = 1


def get_random_junk_item_name():
    return random.choice([RED_RUPEE, SILVER_RUPEE, UNCOMMON_TREASURE, RARE_TREASURE])


def get_complete_item_pool(worlds: list["World"]) -> list[Item]:
    complete_item_pool: list[Item] = []
    for world in worlds:
        for item, count in world.item_pool.items():
            complete_item_pool.extend([item] * count)
    return complete_item_pool
