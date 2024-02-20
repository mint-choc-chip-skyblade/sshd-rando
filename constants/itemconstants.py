from constants.itemnames import *


# Item Groups
ALL_TABLETS = (EMERALD_TABLET, RUBY_TABLET, AMBER_TABLET)

COMMON_TREASURES = (
    ELDIN_ORE,
    ANCIENT_FLOWER,
    DUSK_RELIC,
)

UNCOMMON_TREASURES = (
    MONSTER_HORN,
    EVIL_CRYSTAL,
)

RARE_TREASURES = (
    BLUE_BIRD_FEATHER,
    GOLDEN_SKULL,
    GODDESS_PLUME,
)

COMMON_BUGS = (
    DEKU_HORNET,
    SKYLOFT_MANTIS,
    BLESSED_BUTTERFLY,
    SKY_STAG_BEETLE,
)

UNCOMMON_BUGS = (
    WOODLAND_RHINO_BEETLE,
    VOLCANIC_LADYBUG,
    LANAYRU_ANT,
    GERUDO_DRAGONFLY,
)

RARE_BUGS = (
    FARON_GRASSHOPPER,
    SAND_CICADA,
    ELDIN_ROLLER,
    STARRY_FIREFLY,
)

VANILLA_RANDOM_ITEM_TABLE = {
    COMMON_TREASURE: COMMON_TREASURES,
    COMMON_TREASURE2: COMMON_TREASURES,
    UNCOMMON_TREASURE: UNCOMMON_TREASURES,
    RARE_TREASURE: RARE_TREASURES,
    COMMON_BUG: COMMON_BUGS,
    UNCOMMON_BUG: UNCOMMON_BUGS,
    RARE_BUG: RARE_BUGS,
}

CTMC_ITEMS_TO_FILTER_OUT = (
    GRATITUDE_CRYSTAL_PACK,
    GRATITUDE_CRYSTAL,
    EMPTY_BOTTLE,
    PROGRESSIVE_POUCH,
    PROGRESSIVE_WALLET,
    EXTRA_WALLET,
)

ITEMS_NOT_TO_TRAP = (
    HEART,
    SAILCLOTH,
    GODDESS_SWORD,
    GODDESS_LONGSWORD,
    GODDESS_WHITE_SWORD,
    MASTER_SWORD,
    TRUE_MASTER_SWORD,
    STAMINA_FRUIT,
    FARON_SOTH_PART,
    ELDIN_SOTH_PART,
    LANAYRU_SOTH_PART,
    SONG_OF_THE_HERO,
)

# Item Pools
ALL_JUNK_ITEMS: list[str] = [
    GOLDEN_SKULL,
    GODDESS_PLUME,
    DUSK_RELIC,
    TUMBLEWEED,
    FIVE_BOMBS,
    GREEN_RUPEE,
    BLUE_RUPEE,
    RED_RUPEE,
    SILVER_RUPEE,
    GOLD_RUPEE,
    UNCOMMON_TREASURE,
    RARE_TREASURE,
    EVIL_CRYSTAL,
    ELDIN_ORE,
    RUPOOR,
]

MINIMAL_ITEM_POOL: list[str] = (
    [
        BOMB_BAG,
        GUST_BELLOWS,
        WHIP,
        CLAWSHOTS,
        PROGRESSIVE_SLINGSHOT,
        PROGRESSIVE_BOW,
        PROGRESSIVE_BUG_NET,
        WATER_DRAGON_SCALE,
        FIRESHIELD_EARRINGS,
        STONE_OF_TRIALS,
        SPIRAL_CHARGE,
        GODDESS_HARP,
        FARORES_COURAGE,
        NAYRUS_WISDOM,
        DINS_POWER,
        BALLAD_OF_THE_GODDESS,
        FARON_SOTH_PART,
        ELDIN_SOTH_PART,
        LANAYRU_SOTH_PART,
        LIFE_TREE_FRUIT,
        SCRAPPER,
        EMERALD_TABLET,
        RUBY_TABLET,
        AMBER_TABLET,
        RATTLE,
        CAWLINS_LETTER,
        BEEDLES_INSECT_CAGE,
        SEA_CHART,
        TRIFORCE_OF_COURAGE,
        TRIFORCE_OF_WISDOM,
        TRIFORCE_OF_POWER,
        SV_BOSS_KEY,
        ET_BOSS_KEY,
        LMF_BOSS_KEY,
        AC_BOSS_KEY,
        SSH_BOSS_KEY,
        FS_BOSS_KEY,
        LMF_SMALL_KEY,
        SK_SMALL_KEY,
        LC_SMALL_KEY,
    ]
    + [PROGRESSIVE_POUCH] * 5
    + [PROGRESSIVE_MITTS] * 2
    + [PROGRESSIVE_BEETLE] * 2
    + [PROGRESSIVE_SWORD] * 6
    + [PROGRESSIVE_WALLET] * 4
    + [EXTRA_WALLET] * 3
    + [GRATITUDE_CRYSTAL_PACK] * 13
    + [GRATITUDE_CRYSTAL] * 15
    + [EMPTY_BOTTLE] * 5
    # + [GROUP_OF_TADTONES] * 17
    + [KEY_PIECE] * 5
    + [SV_SMALL_KEY] * 2
    + [AC_SMALL_KEY] * 2
    + [SSH_SMALL_KEY] * 2
    + [FS_SMALL_KEY] * 3
    + [
        WOODEN_SHIELD,  # Non Progress items
        HYLIAN_SHIELD,
        CURSED_MEDAL,
        TREASURE_MEDAL,
        POTION_MEDAL,
        SMALL_SEED_SATCHEL,
        SMALL_QUIVER,
        SMALL_BOMB_BAG,
        BUG_MEDAL,
        GOLDEN_SKULL,
        GODDESS_PLUME,
        DUSK_RELIC,
        TUMBLEWEED,
        FIVE_BOMBS,
    ]
    + [HEART_MEDAL] * 2
    + [RUPEE_MEDAL] * 2
    + [HEART_PIECE] * 24
    + [HEART_CONTANER] * 6
    + [LIFE_MEDAL] * 2
    + [GREEN_RUPEE] * 3
    + [BLUE_RUPEE] * 11
    + [RED_RUPEE] * 42
    + [SILVER_RUPEE] * 22
    + [GOLD_RUPEE] * 11
    + [UNCOMMON_TREASURE] * 10
    + [GOLDEN_SKULL] * 1
    + [RARE_TREASURE] * 12
    + [EVIL_CRYSTAL] * 2
    + [ELDIN_ORE] * 2
    + [RUPOOR] * 5
    + [
        SV_MAP,
        ET_MAP,
        LMF_MAP,
        AC_MAP,
        SSH_MAP,
        FS_MAP,
        SK_MAP,
    ]
)

STANDARD_ITEM_POOL: list[str] = (
    [
        PROGRESSIVE_SLINGSHOT,
        PROGRESSIVE_BUG_NET,
    ]
    + [PROGRESSIVE_BOW] * 2
    + [PROGRESSIVE_BEETLE] * 2
    + MINIMAL_ITEM_POOL
)

# + 1 extra of main items
EXTRA_ITEM_POOL: list[str] = [
    PROGRESSIVE_BOW,
    BOMB_BAG,
    PROGRESSIVE_BEETLE,
    PROGRESSIVE_BUG_NET,
    PROGRESSIVE_SLINGSHOT,
    CLAWSHOTS,
    WHIP,
    GUST_BELLOWS,
    # SAILCLOTH,
    PROGRESSIVE_MITTS,
    WATER_DRAGON_SCALE,
    FIRESHIELD_EARRINGS,
    EMERALD_TABLET,
    RUBY_TABLET,
    AMBER_TABLET,
] + STANDARD_ITEM_POOL

# + 100% extra of main items
PLENTIFUL_ITEM_POOL: list[str] = (
    [
        BOMB_BAG,
        CLAWSHOTS,
        WHIP,
        GUST_BELLOWS,
        # SAILCLOTH,
        WATER_DRAGON_SCALE,
        FIRESHIELD_EARRINGS,
        EMERALD_TABLET,
        RUBY_TABLET,
        AMBER_TABLET,
    ]
    + [PROGRESSIVE_BOW] * 3
    + [PROGRESSIVE_BEETLE] * 4
    + [PROGRESSIVE_BUG_NET] * 2
    + [PROGRESSIVE_SLINGSHOT] * 2
    + [PROGRESSIVE_MITTS] * 2
    + STANDARD_ITEM_POOL
)

# The order the items are defined in here determines
# the order they appear on the GUI
STARTABLE_ITEMS: list[str] = (
    [
        EMERALD_TABLET,
        RUBY_TABLET,
        AMBER_TABLET,
        TRIFORCE_OF_COURAGE,
        TRIFORCE_OF_POWER,
        TRIFORCE_OF_WISDOM,
    ]
    + [PROGRESSIVE_BOW] * 3
    + [BOMB_BAG]
    + [PROGRESSIVE_BEETLE] * 4
    + [PROGRESSIVE_BUG_NET] * 2
    + [PROGRESSIVE_SLINGSHOT] * 2
    + [
        CLAWSHOTS,
        WHIP,
        GUST_BELLOWS,
    ]
    + [PROGRESSIVE_POUCH] * 5
    # + [SAILCLOTH]
    + [PROGRESSIVE_MITTS] * 2
    + [
        WATER_DRAGON_SCALE,
        FIRESHIELD_EARRINGS,
        GODDESS_HARP,
        BALLAD_OF_THE_GODDESS,
        FARORES_COURAGE,
        DINS_POWER,
        NAYRUS_WISDOM,
        FARON_SOTH_PART,
        ELDIN_SOTH_PART,
        LANAYRU_SOTH_PART,
        STONE_OF_TRIALS,
        BEEDLES_INSECT_CAGE,
        CAWLINS_LETTER,
        RATTLE,
        LIFE_TREE_FRUIT,
        # LIFE_TREE_SEEDLING,
        SPIRAL_CHARGE,
        SCRAPPER,
        SEA_CHART,
    ]
    + [KEY_PIECE] * 5
    + [PROGRESSIVE_WALLET] * 4
    + [EXTRA_WALLET] * 3
    + [LC_SMALL_KEY]
    + [SV_SMALL_KEY] * 2
    + [LMF_SMALL_KEY]
    + [AC_SMALL_KEY] * 2
    + [SSH_SMALL_KEY] * 2
    + [FS_SMALL_KEY] * 3
    + [SK_SMALL_KEY]
    + [
        SV_MAP,
        ET_MAP,
        LMF_MAP,
        AC_MAP,
        SSH_MAP,
        FS_MAP,
        SK_MAP,
        SV_BOSS_KEY,
        ET_BOSS_KEY,
        LMF_BOSS_KEY,
        AC_BOSS_KEY,
        SSH_BOSS_KEY,
        FS_BOSS_KEY,
    ]
)

RANDOM_STARTABLE_ITEMS = (
    [
        PROGRESSIVE_BOW,
        BOMB_BAG,
        PROGRESSIVE_BUG_NET,
        PROGRESSIVE_SLINGSHOT,
        CLAWSHOTS,
        WHIP,
        GUST_BELLOWS,
        PROGRESSIVE_POUCH,
        # SAILCLOTH,
        WATER_DRAGON_SCALE,
        FIRESHIELD_EARRINGS,
        GODDESS_HARP,
        BALLAD_OF_THE_GODDESS,
        SPIRAL_CHARGE,
    ]
    + [PROGRESSIVE_BEETLE] * 2
    + [PROGRESSIVE_MITTS] * 2
)

# Itemflags
#
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
    SONG_OF_THE_HERO: 369,
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
    PROGRESSIVE_POUCH: [30, 932, 932, 932, 932],  # Adventure Pouch, Pouch Expansion * 4
    # SAILCLOTH: 32
}

# first value is dungeon name
# second value is the flag to set at the scene
ITEM_DUNGEONFLAGS = {
    SV_MAP: ("Skyview Temple", 2),
    ET_MAP: ("Earth Temple", 2),
    LMF_MAP: ("Lanayru Mining Facility", 2),
    AC_MAP: ("Ancient Cistern", 2),
    SSH_MAP: ("Sandship", 2),
    FS_MAP: ("Fire Sanctuary", 2),
    SK_MAP: ("Sky Keep", 2),
    SV_BOSS_KEY: ("Skyview Temple", 12),
    ET_BOSS_KEY: ("Earth Temple", 12),
    LMF_BOSS_KEY: ("Lanayru Mining Facility", 12),
    AC_BOSS_KEY: ("Ancient Cistern", 12),
    SSH_BOSS_KEY: ("Sandship", 12),
    FS_BOSS_KEY: ("Fire Sanctuary", 12),
}

# first value of tuple is the counter flag or dungeon scene index for small keys
# second is the amount to add
# third is the maximum of the item
ITEM_COUNTS = {
    GRATITUDE_CRYSTAL: (0x1F6, 1, 15),
    GRATITUDE_CRYSTAL_PACK: (0x1F6, 5, 13),
    BOMB_BAG: (0x1F3, 10, 1),
    PROGRESSIVE_BOW: (0x1F2, 20, 1),
    PROGRESSIVE_SLINGSHOT: (0x1ED, 20, 1),
    LC_SMALL_KEY: (9, 1, 1),
    SV_SMALL_KEY: (11, 1, 2),
    LMF_SMALL_KEY: (17, 1, 1),
    AC_SMALL_KEY: (12, 1, 2),
    SSH_SMALL_KEY: (18, 1, 2),
    FS_SMALL_KEY: (15, 1, 3),
    SK_SMALL_KEY: (20, 1, 1),
}

TRAP_SETTING_TO_ITEM = {
    "burn_traps": BURN_TRAP,
    "curse_traps": CURSE_TRAP,
    "noise_traps": NOISE_TRAP,
    "groose_traps": GROOSE_TRAP,
}
