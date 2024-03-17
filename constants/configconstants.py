from collections import Counter
import platform
import random

import yaml
from constants.itemnames import *
from filepathconstants import DEFAULT_OUTPUT_PATH, WORDS_PATH


def get_new_seed() -> str:
    with open(WORDS_PATH, "r", encoding="utf-8") as words_file:
        words = yaml.safe_load(words_file)
        new_seed = ""

        for _ in range(0, 4):
            new_seed += random.choice(words)

        return new_seed


CONFIG_FIELDS = (
    "seed",
    "generate_spoiler_log",
    "use_plandomizer",
    "plandomizer_file",
)


PREFERENCE_FIELDS = (
    "output_dir",
    "theme_mode",
    "theme_presets",
    "use_custom_theme",
    "font_family",
    "font_size",
)


SETTINGS_NOT_IN_SETTINGS_LIST = (
    "excluded_locations",
    "excluded_hint_locations",
    "starting_inventory",
    "mixed_entrance_pools",
)


ENTRANCE_TYPES = (
    # "Spawn",
    # "Bird Statue",
    "Dungeon",
    "Door",
    "Interior",
    "Overworld",
    "Trial Gate",
)


DEFAULT_SETTINGS = {
    "output_dir": DEFAULT_OUTPUT_PATH,
    "seed": get_new_seed(),
    "use_plandomizer": False,
    "plandomizer_file": "None",
    "generate_spoiler_log": True,
    "theme_mode": "Auto",
    "theme_presets": "Default",
    "use_custom_theme": False,
    "font_family": "Figtree",
    "font_size": 10,
    "starting_inventory": Counter(
        [
            PROGRESSIVE_POUCH,
            SCRAPPER,
            SV_MAP,
            ET_MAP,
            LMF_MAP,
            AC_MAP,
            SSH_MAP,
            FS_MAP,
            SK_MAP,
        ]
        # + [
        #     "Group of Tadtones",
        # ]
        # * 17
    ),
    "excluded_locations": [
        "Knight Academy - Deliver Kikwi to Owlan",
        "Upper Skyloft - 600 Points in Pumpkin Pull",
        "Central Skyloft - Peatrice's Love",
        "Batreaux - 70 Crystals",
        "Batreaux - 70 Crystals Second Reward",
        "Batreaux - 80 Crystals",
        "Lumpy Pumpkin - Harp Duet with Kina",
        "Lumpy Pumpkin - Deliver Mogma to Kina",
        "Fun Fun Island - 500 Rupees in Dodoh's High Dive",
        "The Sky - Form a Squirrel Ring above Volcanic Island",
        "The Sky - Form a Squirrel Ring above Lumpy Pumpkin",
        "The Sky - Form a Squirrel Ring above Bamboo Island",
        "Inside the Thunderhead - Song from Levias",
        "Bug Heaven - 10 Bugs in 3 Minutes",
        "Shipyard - Heart Stopping Rickety Coaster Track in 1'05",
        "The Goddess's Silent Realm - Collect all Tears Reward",
        "Farore's Silent Realm - Collect all Tears Reward",
        "Nayru's Silent Realm - Collect all Tears Reward",
        "Din's Silent Realm - Collect all Tears Reward",
    ],
    "excluded_hint_locations": [
        "Shipyard - Gossip Stone",
    ],
    "mixed_entrance_pools": [],
}

if platform.system() != "Windows":
    DEFAULT_SETTINGS["font_size"] = 13


def get_default_setting(setting_name: str):
    # Edge case to allow this function to return None without
    # causing the type checking to complain
    if setting_name == "plandomizer_file":
        return DEFAULT_SETTINGS["plandomizer_file"]

    if (setting_value := DEFAULT_SETTINGS.get(setting_name)) is None:
        raise Exception(
            f"Setting with name '{setting_name}' does not have a defined default value.\nTry adding an entry to /constants/configdefaults.py to fix."
        )

    return setting_value


LOCATION_ALIASES = {
    "Sealed Temple - Slingshot above Doors to Sealed Grounds Whirlpool": "Sealed Temple - Slingshot above Doors to Sealed Grounds Spiral",
    "Skyloft Village - Stamina Fruit": "Skyloft Village - Stamina Fruit above Mallara's House",
    "Deep Woods - Stamina Fruit": "Deep Woods - Stamina Fruit on Hanging Ledge",
    "Great Tree - Blow Small Yellow Mushroom after Vines": "Inside the Great Tree - Blow Small Yellow Mushroom after Vines",
    "Great Tree - Blow Large Yellow Mushroom after Vines": "Inside the Great Tree - Blow Large Yellow Mushroom after Vines",
    "Great Tree - Blow Red Mushroom after Swinging Platforms West": "Inside the Great Tree - Blow Red Mushroom after Swinging Platforms West",
    "Great Tree - Blow Tall Blue Mushroom after Swinging Platforms South": "Inside the Great Tree - Blow Tall Blue Mushroom after Swinging Platforms South",
    "Great Tree - Chest": "Inside the Great Tree - Chest guarded by Deku Baba",
    "Great Tree - Blow Tree Spiral on Highest Pathway": "Inside the Great Tree - Blow Tree Spiral on Highest Pathway",
    "Batreaux - 5 Crystals": "Batreaux's House - 5 Gratitude Crystals Reward",
    "Batreaux - 10 Crystals": "Batreaux's House - 10 Gratitude Crystals Reward",
    "Batreaux - 30 Crystals": "Batreaux's House - 30 Gratitude Crystals Reward",
    "Batreaux - 30 Crystals Chest": "Batreaux's House - 30 Gratitude Crystals Reward Chest",
    "Batreaux - 40 Crystals": "Batreaux's House - 40 Gratitude Crystals Reward",
    "Batreaux - 50 Crystals": "Batreaux's House - 50 Gratitude Crystals Reward",
    "Batreaux - 70 Crystals": "Batreaux's House - 70 Gratitude Crystals First Reward",
    "Batreaux - 70 Crystals Second Reward": "Batreaux's House - 70 Gratitude Crystals Second Reward",
    "Batreaux - 80 Crystals": "Batreaux's House - 80 Gratitude Crystals Reward",
    "The Thunderhead - Song from Levias": "Inside the Thunderhead - Song from Levias",
    "Bug Heaven - Nearby Gossip Stone": "Inside the Thunderhead - Gossip Stone near Bug Heaven",
    "Thunderhead East Island - Chest": "Inside the Thunderhead - Chest on East Island",
    "Thunderhead East Island - Goddess Chest": "Inside the Thunderhead - Goddess Chest on East Island",
    "Mogma Mitts Island - First Goddess Chest": "Inside the Thunderhead - Mogma Mitts Island First Goddess Chest",
    "Mogma Mitts Island - Second Goddess Chest": "Inside the Thunderhead - Mogma Mitts Island Second Goddess Chest",
    "Upper Skyloft - Pumpkin Archery -- 600 Points": "Upper Skyloft - 600 Points in Pumpkin Pull",
    "Lumpy Pumpkin - Harp Minigame": "Lumpy Pumpkin - Harp Duet with Kina",
    "Fun Fun Island - Minigame -- 500 Rupees": "Fun Fun Island - 500 Rupees in Dodoh's High Dive",
    "Bug Heaven - Minigame -- 10 Bugs in 3 Minutes": "Bug Heaven - 10 Bugs in 3 Minutes",
    "Shipyard - Rickety Coaster -- Heart Stopping Track in 1'05": "Shipyard - Heart Stopping Rickety Coaster Track in 1'05",
    "Knight Academy - Owlan's Crystals": "Knight Academy - Deliver Kikwi to Owlan",
    "Knight Academy - Fledge's Crystals": "Knight Academy - Help Fledge Workout",
    "Knight Academy - Ghost/Pipit's Crystals": "Knight Academy - Deliver Cawlin's Letter",
    "Central Skyloft - Wryna's Crystals": "Central Skyloft - Wryna's Gratitude",
    "Central Skyloft - Parrow's Crystals": "Central Skyloft - Parrow's Gratitude",
    "Central Skyloft - Peater/Peatrice's Crystals": "Central Skyloft - Peatrice's Love",
    "Skyloft Village - Mallara's Crystals": "Skyloft Village - Clean Mallara's House",
    "Skyloft Village - Bertie's Crystals": "Skyloft Village - Deliver Rattle to Bertie",
    "Skyloft Village - Sparrot's Crystals": "Skyloft Village - Deliver Crystal Ball to Sparrot",
    "Lumpy Pumpkin - Kina's Crystals": "Lumpy Pumpkin - Deliver Mogma to Kina",
    "Orielle's Island - Orielle's Crystals": "Orielle's Island - Heal Orielle's Loftwing",
    "Beedle's Island - Beedle's Crystals": "Beedle's Island - Deliver Beedle's Insect Cage",
    "Fun Fun Island - Dodoh's Crystals": "Fun Fun Island - Deliver Party Wheel to Dodoh",
    "Beedle's Shop - 300 Rupee Item": "Beedle's Airshop - 300 Rupee Item",
    "Beedle's Shop - 600 Rupee Item": "Beedle's Airshop - 600 Rupee Item",
    "Beedle's Shop - 1200 Rupee Item": "Beedle's Airshop - 1200 Rupee Item",
    "Beedle's Shop - 800 Rupee Item": "Beedle's Airshop - 800 Rupee Item",
    "Beedle's Shop - 1600 Rupee Item": "Beedle's Airshop - 1600 Rupee Item",
    "Beedle's Shop - First 100 Rupee Item": "Beedle's Airshop - First 100 Rupee Item",
    "Beedle's Shop - Second 100 Rupee Item": "Beedle's Airshop - Second 100 Rupee Item",
    "Beedle's Shop - Third 100 Rupee Item": "Beedle's Airshop - Third 100 Rupee Item",
    "Beedle's Shop - 50 Rupee Item": "Beedle's Airshop - 50 Rupee Item",
    "Beedle's Shop - 1000 Rupee Item": "Beedle's Airshop - 1000 Rupee Item",
    "Upper Skyloft - Chest near Goddess Statue": "Upper Skyloft - Chest below Goddess Statue",
    "Sparring Hall - Chest": "Sparring Hall - Chest in Back Room",
    "Sparring Hall - Crystal": "Sparring Hall - Crystal on Roof Beam",
    "Knight Academy - In Link's Closet": "Knight Academy - Link's Closet",
    "Knight Academy - In Fledge's Closet": "Knight Academy - Fledge's Closet",
    "Knight Academy - In Groose's Closet": "Knight Academy - Groose's Closet",
    "Knight Academy - In Owlan's Closet": "Knight Academy - Owlan's Closet",
    "Knight Academy - In Karane's Closet": "Knight Academy - Karane's Closet",
    "Knight Academy - In Zelda's Closet": "Knight Academy - Zelda's Closet",
    "Central Skyloft - Shed Chest": "Central Skyloft - Chest in Shed",
    "Central Skyloft - Shed Goddess Chest": "Central Skyloft - Goddess Chest in Shed",
    "Central Skyloft - West Cliff Goddess Chest": "Central Skyloft - Goddess Chest on West Cliff Island",
    "Central Skyloft - Floating Island Goddess Chest": "Central Skyloft - Goddess Chest on Island near Waterfall",
    "Central Skyloft - Waterfall Goddess Chest": "Central Skyloft - Goddess Chest on Waterfall Island",
    "Lumpy Pumpkin - Chandelier": "Lumpy Pumpkin - Item on Chandelier",
    "Beedle's Island - Crystal": "Beedle's Island - Crystal on Airshop Propeller",
    "Beedle's Island - Cage Goddess Chest": "Beedle's Island - Goddess Chest in Cage",
    "Fun Fun Island - Goddess Chest": "Fun Fun Island - Goddess Chest below Island",
    "Bamboo Island - Goddess Chest": "Bamboo Island - Goddess Chest behind Entrance",
    "Island near Bamboo Island - Goddess Chest": "Island near Bamboo Island - Top Goddess Chest",
    "Northeast Island - Cage Goddess Chest": "Northeast Island - Goddess Chest in Cage",
    "Lumpy Pumpkin - Outside Goddess Chest": "Lumpy Pumpkin - Goddess Chest near Gossip Stone",
    "Triple Island - Cage Goddess Chest": "Triple Island - Goddess Chest in Cage",
    "Sealed Temple - Chest": "Sealed Temple - Chest near The Old One",
    "Faron Woods - Item on Tree": "Faron Woods - Item on Great Tree",
    "Deep Woods - Chest": "Deep Woods - Chest near Bird Statue",
    "Lake Floria - Chest": "Lake Floria - Chest near Bird Statue",
    "Eldin Volcano - Chest after Crawlspace": "Eldin Volcano - Chest after Blocked Crawlspace",
    "Eldin Volcano - Digging Spot below Tower": "Eldin Volcano - Digging Spot below Tower West of Earth Temple",
    "Eldin Volcano - Digging Spot after Vents": "Eldin Volcano - Digging Spot after Sand Slide Vents",
    "Mogma Turf - Sand Slide Chest": "Mogma Turf - Chest after Sand Slide",
    "Volcano Summit - Item behind Digging": "Volcano Summit - Item after Underground Tunnel near Gossip Stone",
    "Lanayru Desert - Chest near Sand Oasis": "Lanayru Desert - Chest on Sand Oasis Wall",
    "Lanayru Desert - Secret Passageway Chest": "Lanayru Desert - Chest in Northeast Secret Passageway",
    "Fire Node - Shortcut Chest": "Fire Node - Raised Chest",
    "Lightning Node - First Chest": "Lightning Node - Front Chest",
    "Lightning Node - Second Chest": "Lightning Node - Middle Chest",
    "Lanayru Caves - Chest": "Lanayru Caves - Chest near Golo",
    "Lanayru Gorge - Item on Pillar": "Lanayru Gorge - Item on Pillar below Dragon",
    "Lanayru Gorge - Digging Spot": "Lanayru Gorge - Life Tree Digging Spot",
    "Lanayru Gorge - Slingshot Left Sandfall Source": "Lanayru Gorge - Slingshot Left Sandfall Source near Life Tree",
    "Lanayru Gorge - Slingshot Right Sandfall Source": "Lanayru Gorge - Slingshot Right Sandfall Source near Life Tree",
    "Lanayru Gorge - Rupee in High Tunnel after Bridge 1": "Lanayru Gorge - Rupee in Sandfall Tunnel near Life Tree 1",
    "Lanayru Gorge - Rupee in High Tunnel after Bridge 2": "Lanayru Gorge - Rupee in Sandfall Tunnel near Life Tree 2",
    "Lanayru Gorge - Rupee in High Tunnel after Bridge 3": "Lanayru Gorge - Rupee in Sandfall Tunnel near Life Tree 3",
    "Lanayru Gorge - Rupee in High Tunnel after Bridge 4": "Lanayru Gorge - Rupee in Sandfall Tunnel near Life Tree 4",
    "Lanayru Gorge - Rupee in High Tunnel after Bridge 5": "Lanayru Gorge - Rupee in Sandfall Tunnel near Life Tree 5",
    "Ancient Harbour - Rupee on First Pillar": "Ancient Harbour - Rupee on Highest Clawshot Pillar",
    "Ancient Harbour - Left Rupee on Entrance Crown": "Ancient Harbour - North Rupee on Entrance Crown",
    "Ancient Harbour - Right Rupee on Entrance Crown": "Ancient Harbour - South Rupee on Entrance Crown",
    "Skipper's Retreat - Chest after Moblin": "Skipper's Retreat - Chest near Low Zipline",
    "Skipper's Retreat - Chest on top of Cacti Pillar": "Skipper's Retreat - Chest on Cacti Pillar",
    "Pirate Stronghold Interior - First Chest": "Pirate Stronghold Interior - Chest behind Electric Fence",
    "Pirate Stronghold Interior - Second Chest": "Pirate Stronghold Interior - Chest before Deku Babas",
    "Pirate Stronghold Interior - Third Chest": "Pirate Stronghold Interior - Chest before Double Armos Fight",
    "Skyview Temple - Rupee on Lower Tree Branch before Hub Room": "Skyview Temple - Rupee on Lower Tree Root before Hub Room",
    "Earth Temple - Vent Chest": "Earth Temple - Chest after Air Vent in First Room",
    "Earth Temple - Rupee above Drawbridge": "Earth Temple - Rupee above First Drawbridge",
    "Earth Temple - Chest behind Bombable Rock": "Earth Temple - Chest behind Southwest Bombable Rock",
    "Earth Temple - Chest Left of Main Room Bridge": "Earth Temple - Northwest Chest Main Room",
    "Earth Temple - Rupee in Lava Tunnel": "Earth Temple - Rupee in Dragon's Neck in Lava Tunnel",
    "Earth Temple - Chest Guarded by Lizalfos": "Earth Temple - Northeast Chest Guarded by Lizalfos",
    "Lanayru Mining Facility - First Chest in Hub Room": "Lanayru Mining Facility - Chest after Breakable Boxes in Hub Room",
    "Lanayru Mining Facility - Shortcut Chest in Main Hub": "Lanayru Mining Facility - Raised Chest in Hub Room after Minecart",
    "Ancient Cistern - First Rupee in East Part in Short Tunnel": "Ancient Cistern - First Rupee in East Room in Short Tunnel",
    "Ancient Cistern - Second Rupee in East Part in Short Tunnel": "Ancient Cistern - Second Rupee in East Room in Short Tunnel",
    "Ancient Cistern - Third Rupee in East Part in Short Tunnel": "Ancient Cistern - Third Rupee in East Room in Short Tunnel",
    "Ancient Cistern - Rupee in East Part in Cubby": "Ancient Cistern - Rupee in East Room in Cubby",
    "Ancient Cistern - Rupee in East Part in Main Tunnel": "Ancient Cistern - Rupee in East Room in Main Tunnel",
    "Ancient Cistern - Chest in East Part": "Ancient Cistern - Chest in East Room",
    "Ancient Cistern - Chest behind the Waterfall": "Ancient Cistern - Chest behind Waterfall",
    "Ancient Cistern - Bokoblin": "Ancient Cistern - Whip Item from Bokoblin between Pipes",
    "Sandship - Chest at the Stern": "Sandship - Chest at Ship's Stern",
    "Fire Sanctuary - Chest on Balcony": "Fire Sanctuary - Chest on Balcony after Single Magmanos Fight",
    "Fire Sanctuary - First Chest in Water Fruit Room": "Fire Sanctuary - Lower Chest in Water Fruit Room",
    "Fire Sanctuary - Second Chest in Water Fruit Room": "Fire Sanctuary - Raised Chest in Water Fruit Room",
    "Fire Sanctuary - Rescue First Trapped Mogma Chest": "Fire Sanctuary - Chest from First Trapped Mogma",
    "Fire Sanctuary - Rescue Second Trapped Mogma Chest": "Fire Sanctuary - Chest from Second Trapped Mogma",
    "Sky Keep - First Chest": "Sky Keep - Chest in First Room",
    "Sky Keep - Chest after Dreadfuse": "Sky Keep - Chest after Dreadfuse Fight",
}

SETTING_ALIASES = {
    "fs_lava_flow": "shortcut_fs_lava_flow",
}
