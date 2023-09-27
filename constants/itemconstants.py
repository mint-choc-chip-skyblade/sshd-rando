GRATITUDE_CRYSTAL_PACK = "Gratitude Crystal Pack"
GRATITUDE_CRYSTAL = "Gratitude Crystal"

PROGRESSIVE_SWORD = "Progressive Sword"
PROGRESSIVE_MITTS = "Progressive Mitts"
PROGRESSIVE_SLINGSHOT = "Progressive Slingshot"
PROGRESSIVE_BEETLE = "Progressive Beetle"
PROGRESSIVE_BOW = "Progressive Bow"
PROGRESSIVE_BUG_NET = "Progressive Bug Net"
PROGRESSIVE_POUCH = "Progressive Pouch"
PROGRESSIVE_WALLET = "Progressive Wallet"

EMERALD_TABLET = "Emerald Tablet"
RUBY_TABLET = "Ruby Tablet"
AMBER_TABLET = "Amber Tablet"

BOMB_BAG = "Bomb Bag"
CLAWSHOTS = "Clawshots"
WHIP = "Whip"
GUST_BELLOWS = "Gust Bellows"
WATER_DRAGON_SCALE = "Water Dragon's Scale"
FIRESHIELD_EARRINGS = "Fireshield Earrings"
GODDESS_HARP = "Goddess's Harp"
BALLAD_OF_THE_GODDESS = "Ballad of the Goddess"
FARORES_COURAGE = "Farore's Courage"
NAYRUS_WISDOM = "Nayru's Wisdom"
DINS_POWER = "Din's Power"
FARON_SOTH_PART = "Faron Song of the Hero Part"
ELDIN_SOTH_PART = "Eldin Song of the Hero Part"
LANAYRU_SOTH_PART = "Lanayru Song of the Hero Part"
SONG_OF_THE_HERO = "Song of the Hero"
LIFE_TREE_FRUIT = "Life Tree Fruit"
LIFE_TREE_SEEDLING = "Life Tree Seedling"
STONE_OF_TRIALS = "Stone of Trials"
CAWLINS_LETTER = "Cawlin's Letter"
HORNED_COLOSSUS_BEETLE = "Horned Colossus Beetle"
RATTLE = "Rattle"
SEA_CHART = "Sea Chart"
SPIRAL_CHARGE = "Spiral Charge"
HYLIAN_SHIELD = "Hylian Shield"

HEART_CONTANER = "Heart Container"
HEART_PIECE = "Heart Piece"
TRIFORCE_OF_COURAGE = "Triforce of Courage"
TRIFORCE_OF_POWER = "Triforce of Power"
TRIFORCE_OF_WISDOM = "Triforce of Wisdom"
COMPLETE_TRIFORCE = "Completed Triforce"

KEY_PIECE = "Key Piece"
FULL_ET_KEY = "Full ET Key"
EMPTY_BOTTLE = "Empty Bottle"
EXTRA_WALLET = "Extra Wallet"
GROUP_OF_TADTONES = "Group of Tadtones"

# lists are used for progressive items,
# tuples for setting multiple flags for one item
ITEM_ITEMFLAGS = {
    PROGRESSIVE_BOW: [19, 90, 91],
    PROGRESSIVE_BEETLE: [53, 75, 76, 77],
    PROGRESSIVE_BUG_NET: [71, 140],
    PROGRESSIVE_SLINGSHOT: [52, 105],
    PROGRESSIVE_MITTS: [56, 99],
    PROGRESSIVE_POUCH: [112, 113, 113, 113, 113],
    PROGRESSIVE_WALLET: [108, 109, 110, 111],
    PROGRESSIVE_SWORD: [10, 11, 12, 9, 13, 14],
    EXTRA_WALLET: 199,
    EMERALD_TABLET: 177,
    RUBY_TABLET: 178,
    AMBER_TABLET: 179,
    BOMB_BAG: 92,
    CLAWSHOTS: 20,
    WHIP: 137,
    GUST_BELLOWS: 49,
    WATER_DRAGON_SCALE: 68,
    FIRESHIELD_EARRINGS: 138,
    GODDESS_HARP: 16,
    BALLAD_OF_THE_GODDESS: 186,
    FARORES_COURAGE: 187,
    NAYRUS_WISDOM: 188,
    DINS_POWER: 189,
    FARON_SOTH_PART: 190,
    ELDIN_SOTH_PART: 191,
    LANAYRU_SOTH_PART: 192,
    SONG_OF_THE_HERO: 193,
    LIFE_TREE_FRUIT: 198,
    LIFE_TREE_SEEDLING: 197,
    STONE_OF_TRIALS: 180,
    CAWLINS_LETTER: 158,
    HORNED_COLOSSUS_BEETLE: 159,
    RATTLE: 160,
    SEA_CHART: 98,
    TRIFORCE_OF_COURAGE: 95,
    TRIFORCE_OF_POWER: 96,
    TRIFORCE_OF_WISDOM: 97,
    SPIRAL_CHARGE: 21,
    GRATITUDE_CRYSTAL_PACK: 35,
    HYLIAN_SHIELD: 125,
    EMPTY_BOTTLE: 153,
    # SAILCLOTH: 15,
}


# lists are used for progressive items,
# tuples for setting multiple flags for one item
ITEM_STORYFLAGS = {
    EMERALD_TABLET: 46,
    RUBY_TABLET: 47,
    AMBER_TABLET: 48,
    HORNED_COLOSSUS_BEETLE: 476,
    CAWLINS_LETTER: 547,
    SPIRAL_CHARGE: 364,
    SEA_CHART: 271,
    WATER_DRAGON_SCALE: 206,  # Completed Faron Trial
    FIRESHIELD_EARRINGS: 207,  # Completed Eldin Trial
    CLAWSHOTS: 208,  # Completed Lanayru Trial
    STONE_OF_TRIALS: (210, 209),  # Obtained SoT, Completed Hylia's Trial
    GODDESS_HARP: (9, 140),  # Harp, Watched Groose CS
    BALLAD_OF_THE_GODDESS: 194,
    TRIFORCE_OF_COURAGE: 729,
    TRIFORCE_OF_POWER: 728,
    TRIFORCE_OF_WISDOM: 730,
    COMPLETE_TRIFORCE: 645,
    FULL_ET_KEY: 120,
    PROGRESSIVE_SWORD: [
        906,
        907,
        908,
        909,
        910,
        911,
    ],  # Practice, Goddess, Long, White, MS, TMS
    PROGRESSIVE_MITTS: [904, 905],  # Digging Mitts, Mogma Mitts
    PROGRESSIVE_BEETLE: [912, 913, 942, 943],  # Beetle, Heetle, Queetle, Teetle
    PROGRESSIVE_WALLET: [915, 916, 917, 918],  # Medium, Big, Giant, Tycoon
    PROGRESSIVE_BOW: [944, 945, 946],  # Bow, Iron, Sacred
    PROGRESSIVE_SLINGSHOT: [947, 948],  # Slingshot, Scatershot
    PROGRESSIVE_BUG_NET: [949, 950],  # Bug Net, Big Bug Net
    PROGRESSIVE_POUCH: [30, 932, 932, 932, 932]  # Adventure Pouch, Pouch Expansion * 4
    # SAILCLOTH: 32
}

FREESTANDING_ITEMS_TO_USE_DEFAULT_SCALING = [
    93,  # Heart Container
    95,  # Triforce of Courage
    96,  # Triforce of Power
    97,  # Triforce of Wisdom
    160,  # Rattle
]

FREESTANDING_ITEM_OFFSETS = {
    1: 0.0,  # Vanilla Small Key (unused)
    2: 0.0,  # Green Rupee
    3: 0.0,  # Blue Rupee
    4: 0.0,  # Red Rupee
    5: 0.0,  # Completed Triforce (unused)
    6: 0.0,  # Heart (unused)
    7: 0.0,  # Single Arrow (unused)
    8: 0.0,  # Arrow Bundle (unused)
    9: 0.0,  # Goddess White Sword (unused)
    10: 20.0,  # Practice Sword (Progressive Sword)
    11: 0.0,  # Goddess Sword (unused)
    12: 0.0,  # Goddess Longsword (unused)
    13: 0.0,  # Master Sword (unused)
    14: 0.0,  # True Master Sword (unused)
    15: 0.0,  # Sailcloth (unused)
    16: 20.0,  # Goddess's Harp
    17: 0.0,  # Spirit Vessel (unused)
    19: 23.0,  # Bow (Progressive Bow)
    20: 25.0,  # Clawshots
    21: 25.0,  # Bird Statuette (Spiral Charge)
    25: 30.0,  # Ancient Cistern Boss Key
    26: 30.0,  # Fire Sanctuary Boss Key
    27: 24.0,  # Sandship Boss Key
    28: 24.0,  # Key Piece
    29: 24.0,  # Skyview Boss Key
    30: 24.0,  # Earth Temple Boss Key
    31: 27.0,  # Lanayru Mining Facility Boss Key
    32: 0.0,  # Silver Rupee
    33: 0.0,  # Gold Rupee
    34: 0.0,  # Rupoor
    35: 18.0,  # Gratitude Crystal Pack
    36: 0.0,  # Glittering Spores + Bottle (unused)
    40: 0.0,  # 5 Bombs (unused)
    41: 0.0,  # 10 Bombs (unused)
    42: 0.0,  # Stamina Fruit (unused)
    43: 0.0,  # Tear of Farore (unused)
    44: 0.0,  # Tear of Din (unused)
    45: 0.0,  # Tear of Nayru (unused)
    46: 0.0,  # Sacred Tear (unused)
    47: 0.0,  # Light Fruit (unused)
    48: 18.0,  # Gratitude Crystal
    49: 26.0,  # Gust Bellows
    50: 0.0,  # Vanilla Dungeon Map (unused)
    51: 0.0,  # Vanilla Dungeon Map (unused)
    52: 16.0,  # Slingshot (Progressive Slingshot)
    53: 18.0,  # Beetle (Progressive Beetle)
    54: 0.0,  # Water (unused)
    55: 0.0,  # Mushroom Spores (unused)
    56: 20.0,  # Digging Mitts (Progressive Mitts)
    57: 0.0,  # 5 Deku Seeds (unused)
    60: 0.0,  # 10 Deku Seeds (unused)
    63: 15.0,  # Semi-Rare Treasure
    64: 15.0,  # Rare Treasure
    65: 0.0,  # Guardian Potion (unused)
    66: 0.0,  # Guardian Potion+ (unused)
    68: 16.0,  # Water Dragon's Scale
    71: 26.0,  # Bug Net
    74: 0.0,  # Sacred Water (unused)
    75: 0.0,  # Hook Beetle (unused)
    76: 0.0,  # Quick Beetle (unused)
    77: 0.0,  # Tough Beetle (unused)
    78: 0.0,  # Heart Potion (unused)
    79: 0.0,  # Heart Potion+ (unused)
    81: 0.0,  # Heart Potion++ (unused)
    84: 0.0,  # Stamina Potion (unused)
    85: 0.0,  # Stamina Potion+ (unused)
    86: 0.0,  # Air Potion (unused)
    87: 0.0,  # Air Potion+ (unused)
    90: 0.0,  # Iron Bow (unused)
    91: 0.0,  # Sacred Bow (unused)
    92: 26.0,  # Bomb Bag
    93: 0.0,  # Heart Container
    94: 0.0,  # Heart Piece
    95: 24.0,  # Triforce of Courage
    96: 24.0,  # Triforce of Power
    97: 24.0,  # Triforce of Wisdom
    98: 23.0,  # Sea Chart
    99: 0.0,  # Mogma Mitts (unused)
    100: 16.0,  # Heart Medal
    101: 16.0,  # Rupee Medal
    102: 16.0,  # Treasure Medal
    103: 16.0,  # Potion Medal
    104: 16.0,  # Cursed Medal
    105: 0.0,  # Scattershot (unused)
    108: 16.0,  # Medium Wallet (Progressive Wallet)
    109: 0.0,  # Big Wallet (unused)
    110: 0.0,  # Giant Wallet (unused)
    111: 0.0,  # Tycoon Wallet (unused)
    112: 0.0,  # Adventure Pouch (Progressive Pouch)
    113: 0.0,  # Pouch Expansion (unused)
    114: 16.0,  # Life Medal
    116: 23.0,  # Wooden Shield
    117: 0.0,  # Banded Shield (unused)
    118: 0.0,  # Braced Shield (unused)
    119: 0.0,  # Iron Shield (unused)
    120: 0.0,  # Reinforced Shield (unused)
    121: 0.0,  # Fortified Shield (unused)
    122: 0.0,  # Sacred Shield (unused)
    123: 0.0,  # Divine Shield (unused)
    124: 0.0,  # Goddess Shield (unused)
    125: 23.0,  # Hylian Shield
    126: 0.0,  # Revitalizing Potion (unused)
    127: 0.0,  # Revitalizing Potion+ (unused)
    128: 14.0,  # Small Seed Satchel
    129: 0.0,  # Medium Seed Satchel (unused)
    130: 0.0,  # Large Seed Satchel (unused)
    131: 19.0,  # Small Quiver
    132: 0.0,  # Medium Quiver (unused)
    133: 0.0,  # Large Quiver (unused)
    134: 18.0,  # Small Bomb Bag
    135: 0.0,  # Medium Bomb Bag (unused)
    136: 00.0,  # Large Bomb Bag (unused)
    137: 19.0,  # Whip
    138: 6.0,  # Fireshield Earrings
    140: 0.0,  # Big Bug Net (unused)
    153: 16.0,  # Empty Bottle
    158: 12.0,  # Cawlin's Letter
    159: 20.0,  # Horned Colossus Beetle
    160: 5.0,  # Rattle
    161: 16.0,  # Hornet Larvae (unused)
    162: 16.0,  # Bird Feather (unused)
    163: 16.0,  # Tumbleweed
    164: 16.0,  # Lizard Tail (unused)
    165: 18.0,  # Eldin Ore
    166: 16.0,  # Ancient Flower (unused)
    167: 16.0,  # Amber Relic (unused)
    168: 16.0,  # Dusk Relic
    169: 16.0,  # Jelly Blob (unused)
    170: 16.0,  # Monster Claw (unused)
    171: 12.0,  # Monster Horn
    172: 16.0,  # Ornamental Skull (unused)
    173: 16.0,  # Evil Crystal
    174: 16.0,  # Blue Bird Feather
    175: 14.0,  # Golden Skull
    176: 17.0,  # Goddess Plume
    177: 19.0,  # Emerald Tablet
    178: 16.0,  # Ruby Tablet
    179: 24.0,  # Amber Tablet
    180: 20.0,  # Stone of Trials
    186: 20.0,  # Ballad of the Goddess
    187: 20.0,  # Farore's Courage
    188: 20.0,  # Nayru's Wisdom
    189: 20.0,  # Din's Power
    190: 20.0,  # Faron Song of the Hero Part
    191: 20.0,  # Eldin Song of the Hero Part
    192: 20.0,  # Lanayru Song of the Hero Part
    193: 0.0,  # Song of the Hero (unused)
    194: 0.0,  # Revitalizing Potion++ (unused)
    195: 0.0,  # Hot Pumpkin Soup (unused)
    196: 0.0,  # Cold Pumpkin Soup (unused)
    197: 0.0,  # Life Tree Seedling (unused)
    198: 16.0,  # Life Tree Fruit
    199: 16.0,  # Extra Wallet
    200: 0.0,  # Skyview Temple Small Key
    201: 0.0,  # Lanayru Mining Facility Small Key
    202: 0.0,  # Ancient Cistern Small Key
    203: 0.0,  # Fire Sanctuary Small Key
    204: 0.0,  # Sandship Small Key
    205: 0.0,  # Sky Keep Small Key
    206: 0.0,  # Lanayru Caves Small Key
    207: 20.0,  # Skyview Temple Map
    208: 19.0,  # Earth Temple Map
    209: 19.0,  # Lanayru Mining Facility Map
    210: 19.0,  # Ancient Cistern Map
    211: 19.0,  # Fire Sanctuary Map
    212: 19.0,  # Sandship Map
    213: 19.0,  # Sky Keep Map
    214: 0.0,  # Group of Tadtones
    215: 0.0,  # Scrapper
}
