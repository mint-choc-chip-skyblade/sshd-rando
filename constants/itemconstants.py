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
BEEDLES_INSECT_CAGE = "Beedle's Insect Cage"
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
SCRAPPER = "Scrapper"
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
    BEEDLES_INSECT_CAGE: 159,
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
    BEEDLES_INSECT_CAGE: 476,
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
    SCRAPPER: 323,
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

# first value of tuple is the counter flag,
# second is the amount to add
# third is the maximum of the item
ITEM_COUNTS = {
    GRATITUDE_CRYSTAL: (0x1F6, 1, 15),
    GRATITUDE_CRYSTAL_PACK: (0x1F6, 5, 13),
    BOMB_BAG: (0x1F3, 10, 1),
    PROGRESSIVE_BOW: (0x1F2, 20, 1),
    PROGRESSIVE_SLINGSHOT: (0x1ED, 20, 1),
}

TRAP_SETTING_TO_ITEM = {
    "burn_traps": "Burn Trap",
    "curse_traps": "Curse Trap",
    "noise_traps": "Noise Trap",
    "groose_traps": "Groose Trap",
}

TRAP_OARC_NAMES: dict[int, tuple] = {
    # Progressive Sword
    10: ("GetSwordA",),
    # Goddess's Harp
    16: ("GetHarp",),
    # Progressive Bow
    19: (
        "GetBowA",
        "GetBowB",
        "GetBowC",
    ),
    # Clawshots
    20: ("GetHookShot",),
    # Spiral Charge
    21: ("GetBirdStatue",),
    # Ancient Cistern Boss Key
    25: ("GetKeyBoss2A",),
    # Fire Sanctuary Boss Key
    26: ("GetKeyBoss2B",),
    # Sandship Boss Key
    27: ("GetKeyBoss2C",),
    # Key Piece
    28: ("GetKeyKakera",),
    # Skyview Temple Boss Key
    29: ("GetKeyBossA",),
    # Earth Temple Boss Key
    30: ("GetKeyBossB",),
    # Lanayru Mining Facility Boss Key
    31: ("GetKeyBossC",),
    # Gratitude Crystal Pack
    35: ("GetGenki",),
    # Gust Bellows
    49: ("GetVacuum",),
    # Progressive Slingshot
    52: (
        "GetPachinkoA",
        "GetPachinkoB",
    ),
    # Progressive Beetle
    53: (
        "GetBeetleA",
        "GetBeetleB",
        "GetBeetleC",
        "GetBeetleD",
    ),
    # Progressive Mitts
    56: (
        "GetMoleGloveA",
        "GetMoleGloveB",
    ),
    # Water Dragon's Scale
    68: ("GetUroko",),
    # Progressive Bug Net
    71: (
        "GetNetA",
        "GetNetB",
    ),
    # Bomb Bag
    92: ("GetBombBag",),
    # Sea Chart
    98: ("GetMapSea",),
    # Progressive Wallet
    108: ("GetPurseB", "get others"),
    # Progressive Pouch
    112: (
        "GetPouchA",
        "GetPouchB",
    ),
    # Whip
    137: ("GetWhip",),
    # Fireshield Earrings
    138: ("GetEarring",),
    # Empty Bottle
    153: (
        "",
        "get other bottles",
    ),
    # Cawlin's Letter
    158: ("GetKobunALetter",),
    # Beedle's Insect Cage
    159: ("GetTerryCage",),
    # Emerald Tablet
    177: ("GetSekibanMapA",),
    # Ruby Tablet
    178: ("GetSekibanMapB",),
    # Amber Tablet
    179: ("GetSekibanMapC",),
    # Stone of Trials
    180: ("GetSirenKey",),
    # Life Tree Fruit
    198: ("GetFruitB",),
    # Extra Wallet
    199: ("GetSparePurse",),
}
