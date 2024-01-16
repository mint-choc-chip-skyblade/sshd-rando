from constants.itemconstants import ITEM_POOL
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
    item_pool = ITEM_POOL

    # Remove Key Pieces if the ET Door is open
    if world.setting("open_earth_temple") == "on":
        item_pool = [item for item in item_pool if item != "Key Piece"]

    if world.setting("small_keys") == "removed":
        item_pool = [
            item
            for item in item_pool
            if not item.endswith("Small Key") or item == "Lanayru Caves Small Key"
        ]

    if world.setting("lanayru_caves_key") == "removed":
        item_pool.remove("Lanayru Caves Small Key")

    if world.setting("boss_keys") == "removed":
        item_pool = [item for item in item_pool if not item.endswith("Boss Key")]

    for item_name in item_pool:
        item = world.get_item(item_name)
        world.item_pool[item] += 1


# Will remove items from the passed in world's item pool
# and add them to the starting pool.
def generate_starting_item_pool(world: "World"):
    for item_name, count in world.setting_map.starting_inventory.items():
        item = world.get_item(item_name)
        world.starting_item_pool[item] += count
        world.item_pool[item] -= count

    # If all three parts of the song of the hero are in the starting inventory
    # replace them with just the singular song of the hero
    all_soth_parts = {
        "Faron Song of the Hero Part",
        "Eldin Song of the Hero Part",
        "Lanayru Song of the Hero Part",
    }
    if all(world.get_item(part) in world.starting_item_pool for part in all_soth_parts):
        for part in all_soth_parts:
            part_item = world.get_item(part)
            world.starting_item_pool[part_item] = 0
        world.starting_item_pool[world.get_item("Song of the Hero")] = 1


def get_random_junk_item_name():
    return random.choice(
        ["Red Rupee", "Silver Rupee", "Semi Rare Treasure", "Rare Treasure"]
    )


def get_complete_item_pool(worlds: list["World"]) -> list[Item]:
    complete_item_pool: list[Item] = []
    for world in worlds:
        for item, count in world.item_pool.items():
            complete_item_pool.extend([item] * count)
    return complete_item_pool
