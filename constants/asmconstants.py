from patches.asmpatchhelper import NsoOffsets

MAIN_NSO_OFFSETS = NsoOffsets(
    text_offset=0x7100004000,
    rodata_offset=0x7101061000,
    data_offset=0x7101563000,
    size=0x2D033000,  # 0x712D037000 (from gdb) - 0x7100004000
)

SDK_NSO_OFFSETS = NsoOffsets(
    text_offset=0x712E0A5000,
    rodata_offset=0x712E633000,
    data_offset=0x712ECBA000,
    size=0xD34000,  # From gdb: (0x00af47ffff - 0x00ae74c000) + 1
)

SUBSDK1_START = 0x712D9FF000

SUBSDK8_TEXT_START = 0x712E0A5000
SUBSDK8_RODATA_START = SUBSDK8_TEXT_START + 0x34A000
SUBSDK8_DATA_START = SUBSDK8_TEXT_START + 0x55A000

SUBSDK_SIZE = SUBSDK8_TEXT_START - SUBSDK1_START

# Start of .rodata.1 of subsdk1 in Ghidra + size of subsdk1 -> start of .rodata.1 of subsdk8
SUBSDK_STARTFLAG_OFFSET = 0x712E54B200
MAX_STARTFLAGS = 1000
SUBSDK_WARP_TO_START_OFFSET = SUBSDK_STARTFLAG_OFFSET + MAX_STARTFLAGS
SUBSDK_START_COUNTS_OFFSET = SUBSDK_WARP_TO_START_OFFSET + 12  # Size of spawn info
SUBSDK_RNG_SEED_OFFSET = SUBSDK_START_COUNTS_OFFSET + 0xC8  # Size of start counts


# Offsets defined as the equivalent subsdk1 offset plus its size.
SUBSDK_NSO_OFFSETS = NsoOffsets(
    text_offset=SUBSDK8_TEXT_START,
    rodata_offset=SUBSDK8_RODATA_START,
    data_offset=SUBSDK8_DATA_START,
    size=SUBSDK_SIZE,
)

NSO_FLAGS_OFFSET = 0xC
COMPRESSED_SEGMENT_NSO_OFFSET = 0x60

SHOP_ITEM_DATA_OFFSETS = (
    0x0,  # Buy Decide Scale
    0x4,  # Put Scale
    0x8,  # Target Arrow Height Offset
    0xC,  # Item ID
    0xE,  # Price
    0x10,  # Event Entrypoint
    0x12,  # Next Shop Item Index
    0x14,  # Spawn Storyflag
    0x16,  # Arc Name
    0x34,  # Model Name
    0x4C,  # Display Height Offset
    0x50,  # Trapbits
    0x52,  # Sold Out Storyflag
)
SHOP_ITEM_DATA_FORMATS = (
    "<f",  # float  - Buy Decide Scale
    "<f",  # float  - Put Scale
    "<f",  # float  - Target Arrow Height Offset
    "<H",  # short  - Item ID
    "<H",  # short  - Price
    "<H",  # short  - Event Entrypoint
    "<H",  # short  - Next Shop Item Index
    "<H",  # short  - Spawn Storyflag
    None,  # custom - Arc Name
    None,  # custom - Model Name
    "<f",  # Display Height Offset
    "<B",  # byte   - Trapbits
    "<H",  # short - Sold Out Storyflag
)

SCENE_NAME_TO_SCENE_INDEX = {
    "Skyloft": 0,
    "Faron Woods": 1,
    "Lake Floria": 2,
    "Flooded Faron Woods": 3,
    "Eldin Volcano": 4,
    "Eldin Volcano Summit": 5,
    "Unused_6": 6,
    "Lanayru Desert": 7,
    "Lanayru Sand Sea": 8,
    "Lanayru Gorge": 9,
    "Sealed Grounds": 10,
    "Skyview Temple": 11,
    "Ancient Cistern": 12,
    "Unused_13": 13,
    "Earth Temple": 14,
    "Fire Sanctuary": 15,
    "Unused_16": 16,
    "Lanayru Mining Facility": 17,
    "Sandship": 18,
    "-Unused-": 19,
    "Sky Keep": 20,
    "The Sky": 21,
    "Farore's Silent Realm": 22,
    "Din's Silent Realm": 23,
    "Nayru's Silent Realm": 24,
    "The Goddess's Silent Realm": 25,
}
