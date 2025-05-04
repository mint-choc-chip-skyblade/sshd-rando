# (undiscounted text index, discounted text index)
BEEDLE_TEXT_PATCHES = {
    "Beedle's Airshop - 50 Rupee Item": (
        25,
        26,
    ),
    "Beedle's Airshop - First 100 Rupee Item": (
        23,
        24,
    ),
    "Beedle's Airshop - Second 100 Rupee Item": (
        "Second 100R undiscounted Text",
        "Second 100R discounted Text",
    ),
    "Beedle's Airshop - Third 100 Rupee Item": (
        "Third 100R undiscounted Text",
        "Third 100R discounted Text",
    ),
    "Beedle's Airshop - 300 Rupee Item": (
        19,
        20,
    ),
    "Beedle's Airshop - 600 Rupee Item": (
        29,
        30,
    ),
    "Beedle's Airshop - 800 Rupee Item": (
        27,
        28,
    ),
    "Beedle's Airshop - 1000 Rupee Item": (
        33,
        34,
    ),
    "Beedle's Airshop - 1200 Rupee Item": (
        31,
        32,
    ),
    "Beedle's Airshop - 1600 Rupee Item": (
        21,
        22,
    ),
}

VANILLA_SHOP_PRICES = {
    "Beedle's Airshop - 50 Rupee Item": 50,
    "Beedle's Airshop - First 100 Rupee Item": 100,
    "Beedle's Airshop - Second 100 Rupee Item": 100,
    "Beedle's Airshop - Third 100 Rupee Item": 100,
    "Beedle's Airshop - 300 Rupee Item": 300,
    "Beedle's Airshop - 600 Rupee Item": 600,
    "Beedle's Airshop - 800 Rupee Item": 800,
    "Beedle's Airshop - 1000 Rupee Item": 1000,
    "Beedle's Airshop - 1200 Rupee Item": 1200,
    "Beedle's Airshop - 1600 Rupee Item": 1600,
}

# Each main wallet size +300, +600, +900
WALLET_CAPACITY_BOUNDARIES = [
    300,  # Base Wallet
    600,
    900,
    1200,
    500,  # Medium Wallet
    800,
    1100,
    1400,
    1000,  # Big Wallet
    1300,
    1600,
    1900,
    5000,  # Giant Wallet
    5300,
    5600,
    5900,
    9000,  # Tycoon Wallet
    9300,
    9600,
    9900,
]


NEXT_SHOP_INDEXES = {
    24: 28,  # extra wallet -> unused1
    28: 29,  # unused1 -> unused2
}

TARGET_ARROW_HEIGHT_OFFSETS = {
    28: 100.0,
    29: 100.0,
}

PRICES = {
    28: 100,
    29: 100,
}

EVENT_ENTRYPOINTS = {
    28: 10539,
    29: 10540,
}

SOLD_OUT_STORYFLAGS = {
    26: 814,  # 800R
    23: 813,  # 1600R
    24: 937,  # 100R1
    28: 938,  # 100R2
    29: 939,  # 100R3
    25: 940,  # 50R
    27: 941,  # 1000R
}

# Buy Decide Scale
DEFAULT_BUY_DECIDE_SCALE = 1.5
BUY_DECIDE_SCALES = {
    8: 1.0,  # 10 Arrows
    10: 1.0,  # Practice Sword (Progressive Sword)
    16: 1.2,  # Goddess's Harp
    19: 1.0,  # Bow (Progressive Bow)
    20: 1.2,  # Clawshots
    21: 1.0,  # Bird Statuette (Spiral Charge)
    25: 0.8,  # Ancient Cistern Boss Key
    26: 0.8,  # Fire Sanctuary Boss Key
    27: 0.8,  # Sandship Boss Key
    28: 1.2,  # Key Piece
    29: 0.8,  # Skyview Boss Key
    30: 0.8,  # Earth Temple Boss Key
    31: 0.8,  # Lanayru Mining Facility Boss Key
    32: 1.7,  # Silver Rupee
    33: 1.7,  # Gold Rupee
    36: 1.2,  # Glittering Spores
    40: 0.8,  # 5 Bombs
    41: 0.8,  # 10 Bombs
    49: 1.0,  # Gust Bellows
    52: 1.2,  # Slingshot (Progressive Slingshot)
    53: 1.0,  # Beetle (Progressive Beetle)
    54: 1.2,  # Bottle of Water
    56: 1.2,  # Digging Mitts (Progressive Mitts)
    55: 1.2,  # Mushroom Spores
    57: 0.8,  # 5 Deku Seeds
    60: 0.8,  # 10 Deku Seeds
    65: 1.2,  # Guardian Potion
    66: 1.2,  # Guardian Potion Plus
    68: 1.2,  # Water Dragon's Scale
    71: 1.2,  # Bug Net (Progressive Bug Net)
    74: 1.2,  # Sacred Water
    78: 1.2,  # Health Potion
    79: 1.2,  # Health Potion Plus
    81: 1.2,  # Health Potion Plus Plus
    84: 1.2,  # Stamina Potion
    85: 1.2,  # Stamina Potion Plus
    86: 1.2,  # Air Potion
    87: 1.2,  # Air Potion Plus
    88: 1.2,  # Fairy in a Bottle
    92: 1.0,  # Bomb Bag
    93: 1.2,  # Heart Container
    94: 1.2,  # Heart Piece
    112: 1.2,  # Adventure Pouch (Progressive Pouch)
    116: 0.8,  # Wooden Shield
    125: 1.0,  # Hylian Shield
    126: 1.2,  # Revitalizing Potion
    127: 1.2,  # Revitalizing Potion Plus
    128: 1.0,  # Small Seed Satchel
    131: 1.0,  # Small Quiver
    134: 1.0,  # Small Bomb Bag
    137: 1.2,  # Whip
    138: 1.2,  # Fireshield Earrings
    153: 1.2,  # Empty Bottle
    158: 1.2,  # Cawlin's Letter
    159: 1.2,  # Horned Colossus Beetle
    160: 1.2,  # Baby Rattle
    163: 1.2,  # Tumbleweed
    165: 1.2,  # Eldin Ore
    166: 1.2,  # Ancient Flower
    168: 1.2,  # Dusk Relic
    171: 1.2,  # Monster Horn
    173: 1.2,  # Evil Crystal
    174: 1.2,  # Blue Bird Feather
    175: 1.2,  # Golden Skull
    176: 1.2,  # Goddess Plume
    177: 1.0,  # Emerald Tablet
    178: 1.0,  # Ruby Tablet
    179: 1.0,  # Amber Tablet
    180: 1.2,  # Stone of Trials
    186: 1.2,  # Ballad of the Goddess
    187: 1.2,  # Farore's Courage
    188: 1.2,  # Nayru's Wisdom
    189: 1.2,  # Din's Power
    190: 1.2,  # Faron Song of the Hero Part (Progressive)
    194: 1.2,  # Revitalizing Potion Plus Plus
    195: 1.2,  # Hot Pumpkin Soup
    196: 1.2,  # Cold Pumpkin Soup
    197: 1.2,  # Life Tree Seedling
    198: 1.2,  # Life Tree Fruit
    200: 1.2,  # Skyview Temple Small Key
    201: 1.2,  # Lanayru Mining Facility Small Key
    202: 1.2,  # Ancient Cistern Small Key
    203: 1.2,  # Fire Sanctuary Small Key
    204: 1.2,  # Sandship Small Key
    205: 1.2,  # Sky Keep Small Key
    206: 1.2,  # Lanayru Caves Small Key
    207: 1.2,  # Skyview Temple Map
    208: 1.2,  # Earth Temple Map
    209: 1.2,  # Lanayru Mining Facility Map
    210: 1.2,  # Ancient Cistern Map
    211: 1.2,  # Fire Sanctuary Map
    212: 1.2,  # Sandship Map
    213: 1.2,  # Sky Keep Map
    214: 0.6,  # Group of Tadtones
    215: 0.4,  # Scrapper
}

# Put Scale
DEFAULT_PUT_SCALE = 1.7
PUT_SCALES = {
    16: 1.5,  # Goddess's Harp
    19: 1.5,  # Bow (Progressive Bow)
    20: 1.5,  # Clawshots
    21: 1.2,  # Bird Statuette (Spiral Charge)
    25: 1.2,  # Ancient Cistern Boss Key
    26: 1.2,  # Fire Sanctuary Boss Key
    27: 1.2,  # Sandship Boss Key
    28: 1.5,  # Key Piece
    29: 1.2,  # Skyview Boss Key
    30: 1.2,  # Earth Temple Boss Key
    31: 1.2,  # Lanayru Mining Facility Boss Key
    32: 2.0,  # Silver Rupee
    33: 2.0,  # Gold Rupee
    40: 1.5,  # 5 Bombs
    41: 1.5,  # 10 Bombs
    49: 1.5,  # Gust Bellows
    52: 1.5,  # Slingshot (Progressive Slingshot)
    53: 1.5,  # Beetle (Progressive Beetle)
    56: 1.5,  # Digging Mitts (Progressive Mitts)
    68: 1.5,  # Water Dragon's Scale
    92: 1.5,  # Bomb Bag
    93: 1.5,  # Heart Container
    94: 1.5,  # Heart Piece
    112: 1.4,  # Adventure Pouch (Progressive Pouch)
    137: 1.5,  # Whip
    138: 1.5,  # Fireshield Earrings
    158: 1.6,  # Cawlin's Letter
    159: 1.6,  # Horned Colossus Beetle
    160: 1.6,  # Baby Rattle
    163: 1.2,  # Tumbleweed
    165: 1.2,  # Eldin Ore
    166: 1.2,  # Ancient Flower
    168: 1.2,  # Dusk Relic
    171: 1.2,  # Monster Horn
    173: 1.2,  # Evil Crystal
    174: 1.2,  # Blue Bird Feather
    175: 1.2,  # Golden Skull
    176: 1.2,  # Goddess Plume
    177: 1.5,  # Emerald Tablet
    178: 1.5,  # Ruby Tablet
    179: 1.5,  # Amber Tablet
    180: 1.5,  # Stone of Trials
    186: 1.5,  # Ballad of the Goddess
    187: 1.5,  # Farore's Courage
    188: 1.5,  # Nayru's Wisdom
    189: 1.5,  # Din's Power
    190: 1.5,  # Faron Song of the Hero Part
    191: 1.5,  # Eldin Song of the Hero Part
    192: 1.5,  # Lanayru Song of the Hero Part
    197: 1.5,  # Life Tree Seedling
    198: 1.5,  # Life Tree Fruit
    200: 1.5,  # Skyview Temple Small Key
    201: 1.5,  # Lanayru Mining Facility Small Key
    202: 1.5,  # Ancient Cistern Small Key
    203: 1.5,  # Fire Sanctuary Small Key
    204: 1.5,  # Sandship Small Key
    205: 1.5,  # Sky Keep Small Key
    206: 1.5,  # Lanayru Caves Small Key
    207: 1.2,  # Skyview Temple Map
    208: 1.2,  # Earth Temple Map
    209: 1.2,  # Lanayru Mining Facility Map
    210: 1.2,  # Ancient Cistern Map
    211: 1.2,  # Fire Sanctuary Map
    212: 1.2,  # Sandship Map
    213: 1.2,  # Sky Keep Map
    214: 1.0,  # Group of Tadtones
    215: 0.8,  # Scrapper
}

# Display Height Offset
DEFAULT_DISPLAY_HEIGHT_OFFSET = -25.0
DISPLAY_HEIGHT_OFFSETS = {
    # Don't work for some reason
    # 35: -30.0, # Gratitude Crystal Pack
    # 48: -30.0, # Single Gratitude Crystal
    # 165: -20.0, # Eldin Ore
    2: -23.0,  # Green Rupee
    3: -23.0,  # Blue Rupee
    4: -23.0,  # Red Rupee
    8: -35.0,  # 10 Arrows
    10: -35.0,  # Practice Sword (Progressive Sword)
    16: -30.0,  # Goddess's Harp
    19: -35.0,  # Bow (Progressive Bow)
    20: -38.0,  # Clawshots
    21: -30.0,  # Bird Statuette (Spiral Charge)
    25: -35.0,  # Ancient Cistern Boss Key
    26: -32.0,  # Fire Sanctuary Boss Key
    27: -29.0,  # Sandship Boss Key
    28: -35.0,  # Key Piece
    29: -26.0,  # Skyview Temple Boss Key
    30: -26.0,  # Earth Temple Boss Key
    31: -32.0,  # Lanayru Mining Facility Boss Key
    32: -27.0,  # Silver Rupee
    33: -27.0,  # Gold Rupee
    34: -23.0,  # Rupoor
    36: -28.0,  # Glittering Spores
    49: -39.0,  # Gust Bellows
    52: -26.0,  # Slingshot (Progressive Slingshot)
    53: -28.0,  # Beetle (Progressive Beetle)
    54: -28.0,  # Bottle of Water
    55: -28.0,  # Mushroom Spores
    56: -31.0,  # Digging Mitts (Progressive Mitts)
    57: -20.0,  # 5 Deku Seeds
    60: -24.0,  # 10 Deku Seeds
    65: -28.0,  # Guardian Potion
    66: -28.0,  # Guardian Potion Plus
    68: -26.0,  # Water Dragon's Scale
    70: -28.0,  # Bug Medal
    71: -44.0,  # Bug Net (Progressive Bug Net)
    72: -16.0,  # Fairy
    74: -28.0,  # Sacred Water
    78: -28.0,  # Health Potion
    79: -28.0,  # Health Potion Plus
    81: -28.0,  # Health Potion Plus Plus
    84: -28.0,  # Stamina Potion
    85: -28.0,  # Stamina Potion Plus
    86: -28.0,  # Air Potion
    87: -28.0,  # Air Potion Plus
    88: -28.0,  # Fairy in a Bottle
    92: -38.0,  # Bomb Bag
    93: -29.0,  # Heart Container
    98: -40.0,  # Sea Chart
    100: -28.0,  # Heart Medal
    101: -28.0,  # Rupee Medal
    102: -28.0,  # Treasure Medal
    103: -28.0,  # Potion Medal
    104: -28.0,  # Cursed Medal
    108: -28.0,  # Medium Wallet (Progressive Wallet)
    112: -26.0,  # Adventure Pouch (Progressive Pouch)
    114: -28.0,  # Life Medal
    116: -42.0,  # Wooden Shield
    125: -40.0,  # Hylian Shield
    126: -28.0,  # Revitalizing Potion
    127: -28.0,  # Revitalizing Potion Plus
    128: -24.0,  # Small Seed Satchel
    131: -33.0,  # Small Quiver
    134: -29.0,  # Small Bomb Bag
    137: -29.0,  # Whip
    138: -10.0,  # Fireshield Earrings
    153: -28.0,  # Empty Bottle
    158: -20.0,  # Cawlin's Letter
    159: -30.0,  # Beedle's Insect Cage
    160: -32.0,  # Rattle
    163: -20.0,  # Tumbleweed
    165: -24.0,  # Eldin Ore
    166: -25.0,  # Ancient Flower
    168: -19.0,  # Dusk Relic
    171: -16.0,  # Monster Horn
    173: -19.0,  # Evil Crystal
    174: -19.0,  # Blue Bird Feather
    175: -16.0,  # Golden Skull
    176: -21.0,  # Goddess Plume
    177: -27.0,  # Emerald Tablet
    178: -24.0,  # Ruby Tablet
    179: -38.0,  # Amber Tablet
    180: -29.0,  # Stone of Trials
    186: -30.0,  # Ballad of the Goddess
    187: -30.0,  # Farore's Courage
    188: -30.0,  # Nayru's Wisdom
    189: -30.0,  # Din's Power
    190: -30.0,  # Faron Song of the Hero Part (Progressive)
    194: -28.0,  # Revitalizing Potion Plus Plus
    195: -28.0,  # Hot Pumpkin Soup
    196: -28.0,  # Cold Pumpkin Soup
    197: -38.0,  # Life Tree Seedling
    198: -26.0,  # Life Tree Fruit
    199: -28.0,  # Extra Wallet
    200: -33.0,  # Skyview Temple Small Key
    201: -33.0,  # Lanayru Mining Facility Small Key
    202: -33.0,  # Ancient Cistern Small Key
    203: -33.0,  # Fire Sanctuary Small Key
    204: -33.0,  # Sandship Small Key
    205: -33.0,  # Sky Keep Small Key
    206: -33.0,  # Lanayru Caves Small Key
    207: -25.0,  # Skyview Temple Map
    208: -25.0,  # Earth Temple Map
    209: -25.0,  # Lanayru Mining Facility Map
    210: -25.0,  # Ancient Cistern Map
    211: -25.0,  # Fire Sanctuary Map
    212: -25.0,  # Sandship Map
    213: -25.0,  # Sky Keep Map
    214: 0.0,  # Group of Tadtones
    215: 0.0,  # Scrapper
}
