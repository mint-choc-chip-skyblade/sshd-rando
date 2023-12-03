from .settings import *
from .item import *

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import World

all_junk_items: list[str] = [
    "Golden Skull",
    "Goddess Plume",
    "Dusk Relic",
    "Tumbleweed",
    "5 Bombs",
    "Green Rupee",
    "Blue Rupee",
    "Red Rupee",
    "Silver Rupee",
    "Gold Rupee",
    "Semi Rare Treasure",
    "Rare Treasure",
    "Evil Crystal",
    "Eldin Ore",
    "Rupoor",
]


class ItemPoolError(RuntimeError):
    pass


# Generates the item pool for a single world
# Items being placed in vanilla or restricted
# location sets will be filtered out later. Items
# that need to be removed and not placed anywhere
# will be removed now
def generate_item_pool(world: "World") -> None:
    item_pool = (
        [
            "Bomb Bag",
            "Gust Bellows",
            "Whip",
            "Clawshots",
            "Water Dragon's Scale",
            "Fireshield Earrings",
            "Stone of Trials",
            "Spiral Charge",
            "Goddess's Harp",
            "Farore's Courage",
            "Nayru's Wisdom",
            "Din's Power",
            "Ballad of the Goddess",
            "Faron Song of the Hero Part",
            "Eldin Song of the Hero Part",
            "Lanayru Song of the Hero Part",
            "Life Tree Fruit",
            "Scrapper",
            "Emerald Tablet",
            "Ruby Tablet",
            "Amber Tablet",
            "Rattle",
            "Cawlin's Letter",
            "Beedle's Insect Cage",
            "Sea Chart",
            "Triforce of Courage",
            "Triforce of Wisdom",
            "Triforce of Power",
            "Skyview Temple Boss Key",
            "Earth Temple Boss Key",
            "Lanayru Mining Facility Boss Key",
            "Ancient Cistern Boss Key",
            "Sandship Boss Key",
            "Fire Sanctuary Boss Key",
            "Lanayru Mining Facility Small Key",
            "Sky Keep Small Key",
            "Lanayru Caves Small Key",
        ]
        + ["Progressive Slingshot"] * 2
        + ["Progressive Pouch"] * 5
        + ["Progressive Mitts"] * 2
        + ["Progressive Bow"] * 3
        + ["Progressive Beetle"] * 4
        + ["Progressive Bug Net"] * 2
        + ["Progressive Sword"] * 6
        + ["Progressive Wallet"] * 4
        + ["Extra Wallet"] * 3
        + ["Gratitude Crystal Pack"] * 13
        + ["Gratitude Crystal"] * 15
        + ["Empty Bottle"] * 5
        # + ["Group of Tadtones"] * 17
        + ["Key Piece"] * 5
        + ["Skyview Temple Small Key"] * 2
        + ["Ancient Cistern Small Key"] * 2
        + ["Sandship Small Key"] * 2
        + ["Fire Sanctuary Small Key"] * 3
        + [
            "Wooden Shield",  # Non Progress items
            "Hylian Shield",
            "Cursed Medal",
            "Treasure Medal",
            "Potion Medal",
            "Small Seed Satchel",
            "Small Bomb Bag",
            "Small Quiver",
            "Bug Medal",
            "Golden Skull",
            "Goddess Plume",
            "Dusk Relic",
            "Tumbleweed",
            "5 Bombs",
        ]
        + ["Heart Medal"] * 2
        + ["Rupee Medal"] * 2
        + ["Heart Piece"] * 24
        + ["Heart Container"] * 6
        + ["Life Medal"] * 2
        + ["Green Rupee"] * 3
        + ["Blue Rupee"] * 11
        + ["Red Rupee"] * 42
        + ["Silver Rupee"] * 22
        + ["Gold Rupee"] * 11
        + ["Semi Rare Treasure"] * 10
        + ["Golden Skull"] * 1
        + ["Rare Treasure"] * 12
        + ["Evil Crystal"] * 2
        + ["Eldin Ore"] * 2
        + ["Rupoor"] * 5
        + [
            "Skyview Temple Map",
            "Earth Temple Map",
            "Lanayru Mining Facility Map",
            "Ancient Cistern Map",
            "Sandship Map",
            "Fire Sanctuary Map",
            "Sky Keep Map",
        ]
    )

    # if world.setting("traps") == "on":
    #     item_pool += ["Trap"] * 10

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
