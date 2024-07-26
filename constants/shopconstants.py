NEXT_SHOP_INDEXES = {
    24: 28, # extra wallet -> unused1
    28: 29, # unused1 -> unused2
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
    24: 937, # 100R1
    28: 938, # 100R2
    29: 939, # 100R3
    25: 940, # 50R
    27: 941, # 1000R
}

# Buy Decide Scale
DEFAULT_BUY_DECIDE_SCALE = 1.5
BUY_DECIDE_SCALES = {
    1: 1.2,  # Vanilla Small Key (Unused)
    9: 1.0,  # Goddess White Sword (unused)
    10: 1.0,  # Practice Sword (Progressive Sword)
    11: 1.0,  # Goddess Sword (unused)
    12: 1.0,  # Goddess Longsword (unused)
    13: 1.0,  # Master Sword (unused)
    14: 1.0,  # True Master Sword (unused)
    16: 1.2,  # Goddess's Harp
    19: 0.8,  # Bow (Progressive Bow)
    20: 1.2,  # Clawshots
    21: 1.0,  # Bird Statuette (Spiral Charge)
    25: 0.8,  # Ancient Cistern Boss Key
    26: 0.8,  # Fire Sanctuary Boss Key
    27: 0.8,  # Sandship Boss Key
    28: 1.2,  # Key Piece
    29: 0.8,  # Skyview Boss Key
    30: 0.8,  # Earth Temple Boss Key
    31: 0.8,  # Lanayru Mining Facility Boss Key
    49: 1.0,  # Gust Bellows
    52: 1.2,  # Slingshot (Progressive Slingshot)
    53: 1.0,  # Beetle (Progressive Beetle)
    56: 1.2,  # Digging Mitts (Progressive Mitts)
    68: 1.2,  # Water Dragon's Scale
    75: 1.0,  # Hook Beetle (unused)
    76: 1.0,  # Quick Beetle (unused)
    77: 1.0,  # Tough Beetle (unused)
    90: 0.8,  # Iron Bow (unused)
    91: 0.8,  # Sacred Bow (unused)
    92: 1.0,  # Bomb Bag
    93: 1.2,  # Heart Container
    94: 1.2,  # Heart Piece
    99: 1.2,  # Mogma Mitts (unused)
    105: 1.2,  # Scattershot (unused)
    112: 1.2,  # Adventure Pouch (Progressive Pouch)
    113: 1.2,  # Pouch Expansion (unused)
    125: 1.2,  # Hylian Shield
    137: 1.2,  # Whip
    138: 1.2,  # Fireshield Earrings
    158: 1.2,  # Cawlin's Letter
    159: 1.2,  # Horned Colossus Beetle
    160: 1.2,  # Baby Rattle
    177: 1.0,  # Emerald Tablet
    178: 1.0,  # Ruby Tablet
    179: 1.0,  # Amber Tablet
    180: 1.2,  # Stone of Trials
    186: 1.2,  # Ballad of the Goddess
    187: 1.2,  # Farore's Courage
    188: 1.2,  # Nayru's Wisdom
    189: 1.2,  # Din's Power
    190: 1.2,  # Faron Song of the Hero Part
    191: 1.2,  # Eldin Song of the Hero Part
    192: 1.2,  # Lanayru Song of the Hero Part
    193: 1.2,  # Song of the Hero (unused)
    198: 1.2,  # Life Tree Fruit
    200: 1.2,  # Skyview Small Key
    201: 1.2,  # Lanayru Mining Facility Small Key
    202: 1.2,  # Ancient Cistern Small Key
    203: 1.2,  # Fire Sanctuary Small Key
    204: 1.2,  # Sandship Small Key
    205: 1.2,  # Sky Keep Small Key
    206: 1.2,  # Lanayru Caves Small Key
    207: 1.2,  # Skyview Map
    208: 1.2,  # Earth Temple Map
    209: 1.2,  # Lanayru Mining Facility Map
    210: 1.2,  # Ancient Cistern Map
    211: 1.2,  # Fire Sanctuary Map
    212: 1.2,  # Sandship Map
    213: 1.2,  # Sky Keep Map
    214: 0.6,  # Group of Tadtones
}

# Put Scale
DEFAULT_PUT_SCALE = 1.7
PUT_SCALES = {
    1: 1.5,  # Vanilla Small Key (Unused)
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
    49: 1.5,  # Gust Bellows
    52: 1.5,  # Slingshot (Progressive Slingshot)
    53: 1.5,  # Beetle (Progressive Beetle)
    56: 1.5,  # Digging Mitts (Progressive Mitts)
    68: 1.5,  # Water Dragon's Scale
    75: 1.5,  # Hook Beetle (unused)
    76: 1.5,  # Quick Beetle (unused)
    77: 1.5,  # Tough Beetle (unused)
    90: 1.5,  # Iron Bow (unused)
    91: 1.5,  # Sacred Bow (unused)
    92: 1.5,  # Bomb Bag
    93: 1.5,  # Heart Container
    94: 1.5,  # Heart Piece
    99: 1.5,  # Mogma Mitts (unused)
    105: 1.5,  # Scattershot (unused)
    112: 1.4,  # Adventure Pouch (Progressive Pouch)
    113: 1.4,  # Pouch Expansion (unused)
    137: 1.5,  # Whip
    138: 1.5,  # Fireshield Earrings
    158: 1.6,  # Cawlin's Letter
    159: 1.6,  # Horned Colossus Beetle
    160: 1.6,  # Baby Rattle
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
    193: 1.5,  # Song of the Hero (unused)
    200: 1.5,  # Skyview Small Key
    201: 1.5,  # Lanayru Mining Facility Small Key
    202: 1.5,  # Ancient Cistern Small Key
    203: 1.5,  # Fire Sanctuary Small Key
    204: 1.5,  # Sandship Small Key
    205: 1.5,  # Sky Keep Small Key
    206: 1.5,  # Lanayru Caves Small Key
    207: 1.2,  # Skyview Map
    208: 1.2,  # Earth Temple Map
    209: 1.2,  # Lanayru Mining Facility Map
    210: 1.2,  # Ancient Cistern Map
    211: 1.2,  # Fire Sanctuary Map
    212: 1.2,  # Sandship Map
    213: 1.2,  # Sky Keep Map
    214: 1.0,  # Group of Tadtones
}

# Display Height Offset
DEFAULT_DISPLAY_HEIGHT_OFFSET = -25.0
DISPLAY_HEIGHT_OFFSETS = {
    # Don't work for some reason
    # 35: -30.0, # Gratitude Crystal Pack
    # 48: -30.0, # Single Gratitude Crystal
    # 165: -20.0, # Eldin Ore
    1: -35.0,  # Vanilla Small Key (unused)
    9: -35.0,  # Goddess White Sword (unused)
    10: -35.0,  # Practice Sword (Progressive Sword)
    11: -35.0,  # Goddess Sword (unused)
    12: -35.0,  # Goddess Longsword (unused)
    13: -35.0,  # Master Sword (unused)
    14: -35.0,  # True Master Sword (unused)
    16: -28.0,  # Goddess's Harp
    19: -35.0,  # Bow (Progressive Bow)
    20: -38.0,  # Clawshots
    21: -32.0,  # Bird Statuette (Spiral Charge)
    25: -37.0,  # Ancient Cistern Boss Key
    26: -36.0,  # Fire Sanctuary Boss Key
    27: -29.0,  # Sandship Boss Key
    28: -35.0,  # Key Piece
    29: -28.0,  # Skyview Boss Key
    30: -28.0,  # Earth Temple Boss Key
    31: -32.0,  # Lanayru Mining Facility Boss Key
    49: -42.0,  # Gust Bellows
    52: -27.0,  # Slingshot (Progressive Slingshot)
    53: -27.0,  # Beetle (Progressive Beetle)
    56: -29.0,  # Digging Mitts (Progressive Mitts)
    68: -29.0,  # Water Dragon's Scale
    75: -27.0,  # Hook Beetle (unused)
    76: -27.0,  # Quick Beetle (unused)
    77: -27.0,  # Tough Beetle (unused)
    90: -35.0,  # Iron Bow (unused)
    91: -35.0,  # Sacred Bow (unused)
    92: -38.0,  # Bomb Bag
    93: -30.0,  # Heart Container
    94: -27.0,  # Heart Piece
    98: -39.0,  # Sea Chart
    99: -29.0,  # Mogma Mitts (unused)
    100: -30.0,  # Heart Medal
    101: -30.0,  # Rupee Medal
    102: -30.0,  # Treasure Medal
    103: -30.0,  # Potion Medal
    104: -30.0,  # Cursed Medal
    105: -27.0,  # Scattershot (unused)
    108: -27.0,  # Medium Wallet (Progressive Wallet)
    109: -27.0,  # Big Wallet (unused)
    110: -27.0,  # Giant Wallet (unused)
    111: -27.0,  # Tycoon Wallet (unused)
    112: -28.0,  # Adventure Pouch (Progressive Pouch)
    113: -28.0,  # Pouch Expansion (unused)
    125: -40.0,  # Hylian Shield
    137: -30.0,  # Whip
    138: -10.0,  # Fireshield Earrings
    159: -32.0,  # Horned Colossus Beetle
    160: -35.0,  # Baby Rattle
    177: -30.0,  # Emerald Tablet
    178: -27.0,  # Ruby Tablet
    179: -40.0,  # Amber Tablet
    180: -29.0,  # Stone of Trials
    186: -28.0,  # Ballad of the Goddess
    187: -28.0,  # Farore's Courage
    188: -28.0,  # Nayru's Wisdom
    189: -28.0,  # Din's Power
    190: -28.0,  # Faron Song of the Hero Part
    191: -28.0,  # Eldin Song of the Hero Part
    192: -28.0,  # Lanayru Song of the Hero Part
    193: -28.0,  # Song of the Hero (unused)
    198: -30.0,  # Life Tree Fruit
    200: -35.0,  # Skyview Small Key
    201: -35.0,  # Lanayru Mining Facility Small Key
    202: -35.0,  # Ancient Cistern Small Key
    203: -35.0,  # Fire Sanctuary Small Key
    204: -35.0,  # Sandship Small Key
    205: -35.0,  # Sky Keep Small Key
    206: -35.0,  # Lanayru Caves Small Key
    207: -20.0,  # Skyview Map
    208: -20.0,  # Earth Temple Map
    209: -20.0,  # Lanayru Mining Facility Map
    210: -20.0,  # Ancient Cistern Map
    211: -20.0,  # Fire Sanctuary Map
    212: -20.0,  # Sandship Map
    213: -20.0,  # Sky Keep Map
    214: 0.0,  # Group of Tadtones
}
