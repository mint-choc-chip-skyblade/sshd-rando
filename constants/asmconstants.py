from patches.asmpatchhelper import NsoOffsets


MAIN_NSO_OFFSETS = NsoOffsets(
    text_offset=0x08004000,
    rodata_offset=0x09061000,
    data_offset=0x09563000,
    size=0x09842000 - 0x08004000,
)

SUBSDK1_START = 0x359FF000

SUBSDK8_TEXT_START = 0x360A5000
SUBSDK8_RODATA_START = SUBSDK8_TEXT_START + 0x34A000
SUBSDK8_DATA_START = SUBSDK8_TEXT_START + 0x55A000

SUBSDK_SIZE = SUBSDK8_TEXT_START - SUBSDK1_START
SUBSDK_STARTFLAG_OFFSET = SUBSDK8_RODATA_START + 0x200


# Offsets defined as the equivalent subsdk1 offset plus its size.
SUBSDK_NSO_OFFSETS = NsoOffsets(
    text_offset=SUBSDK8_TEXT_START,
    rodata_offset=SUBSDK8_RODATA_START,
    data_offset=SUBSDK8_DATA_START,
    size=SUBSDK_SIZE,
)

NSO_FLAGS_OFFSET = 0xC
COMPRESSED_SEGMENT_NSO_OFFSET = 0x60

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
    "Faron Silent Realm": 22,
    "Eldin Silent Realm": 23,
    "Lanayru Silent Realm": 24,
    "Skyloft Silent Realm": 25,
}
