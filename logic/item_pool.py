
from .settings import *
from .item import *


def generate_item_pool(world) -> None:
    item_pool = (
        [
            "Bomb Bag",
            "Gust Bellows",
            "Whip",
            "Clawshots",
            "Water Dragon Scale",
            "Fireshield Earrings",
            "Stone of Trials",
            "Spiral Charge",
            "Goddess Harp",
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
            "Babys Rattle",
            "Cawlin's Letter",
            "Horned Colossus Beetle",
            "Sea Chart",
            "Triforce of Courage",
            "Triforce of Wisdom",
            "Triforce of Power",
            "Skyview Boss Key",
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
        + ["Group of Tadtones"] * 17
        + ["Key Piece"] * 5
        + ["Skyview Small Key"] * 2
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
            "Skyview Map",
            "Earth Temple Map",
            "Lanayru Mining Facility Map",
            "Ancient Cistern Map",
            "Sandship Map",
            "Fire Sanctuary Map",
            "Sky Keep Map",
        ]
    )

    for item_name in item_pool:
        item = world.get_item(item_name)
        world.item_pool[item] += 1


# Will remove items from the passed in world's item pool
# and add them to the starting pool.
def generate_starting_item_pool(world):
    for item_name, count in world.setting_map.starting_inventory.items():
        item = world.get_item(item_name)
        world.starting_item_pool[item] += count
        world.item_pool[item] -= count
