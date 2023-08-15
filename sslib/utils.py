# This file is heavily based on the equivalent file in the Skyward Sword Randomizer codebase (SD).
# That file can be found here: https://github.com/ssrando/ssrando/blob/main/sslib/utils.py

import struct
import collections
import json
from pathlib import Path


def unpack(fields, formatstr, item):
    return (
        collections.namedtuple("_", fields)
        ._make(struct.unpack(formatstr, item))
        ._asdict()
    )


def encodeBytes(bytestr):
    return " ".join(["%02X" % x for x in bytestr])


def objToJson(parsed):
    return json.dumps(
        parsed, indent=4, ensure_ascii=True, allow_nan=False, default=encodeBytes
    )


def toStr(bytestr):
    """Converts a bytestring, which is shift-jis encoded to a string"""
    return bytestr.split(b"\x00", 1)[0].decode("shift-jis")


def toBytes(string, length):
    """Converts a string into shift-jis encoding and padding it with zeroes to the specified length"""
    encoded = string.encode("shift-jis")
    return encoded + (b"\x00" * (length - len(encoded)))


def write_bytes_create_dirs(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def mask_shift_set(value, mask, shift, new_value):
    """
    Replace new_value in value, by applying the mask after the shift
    """
    new_value = new_value & mask
    return (value & ~(mask << shift)) | (new_value << shift)


stagenames = {
    "F000": "Skyloft: Skyloft",
    "F001r": "Skyloft: Knight's Academy",
    "F002r": "Skyloft: Beedle's Airshop",
    "F004r": "Skyloft: Bazaar",
    "F005r": "Skyloft: Orielle & Parrow’s House",
    "F006r": "Skyloft: Repairman Kukiel’s House",
    "F007r": "Skyloft: Piper’s House",
    "F008r": "Skyloft: Inside the Statue of the Goddess",
    "F009r": "Skyloft: Sparring Hall",
    "F010r": "Skyloft: Isle of Songs Tower",
    "F011r": "Skyloft: The Lumpy Pumpkin",
    "F012r": "Skyloft: Demon Guy Batreaux’s House",
    "F013r": "Skyloft: Fortune-teller Sparrot’s House",
    "F014r": "Skyloft: Potion Shop Owner Bertie’s House",
    "F015r": "Skyloft: Scrap Shop Owner Gondo’s House",
    "F016r": "Skyloft: Pipit's House",
    "F017r": "Skyloft: Gear Peddler Rupin’s House",
    "F018r": "Skyloft: Item Check Girl Peatrice’s House",
    "F019r": "Skyloft: Bamboo Island",
    "F020": "The Sky: Sky Field",
    "F021": "The Sky: Cutscene Sky",
    "F023": "The Sky: Thunderhead",
    "D000": "Skyloft: Waterfall Cave",
    "D003_0": "Skyloft: Sky Keep R00 (Enemy)",
    "D003_1": "Skyloft: Sky Keep R01 (Underground)",
    "D003_2": "Skyloft: Sky Keep R02 (Lava)",
    "D003_3": "Skyloft: Sky Keep R03 (Timeshift 2)",
    "D003_4": "Skyloft: Sky Keep R04 (Timeshift 1)",
    "D003_5": "Skyloft: Sky Keep R05 (ツタ系)",
    "D003_6": "Skyloft: Sky Keep R06 (Captain 2)",
    "D003_7": "Skyloft: Sky Keep R07 (Entrance)",
    "D003_8": "Skyloft: Sky Keep R08 Tri Get",
    "S000": "Skyloft: Town Silent Realm",
    "F100": "Faron Woods: Faron Woods",
    "F100_1": "Faron Woods: Inside the Great Tree",
    "F101": "Faron Woods: Deep Woods",
    "F102": "Faron Woods: Lake Floria",
    "F102_1": "Faron Woods: Outside Ancient Cistern",
    "F102_2": "Faron Woods: Faron's Lair",
    "F103": "Faron Woods: Faron Woods (Flooded)",
    "F103_1": "Faron Woods: Forest F3 (Tree Interior)",
    "D100": "Faron Woods: Skyview Temple",
    "D101": "Faron Woods: Ancient Cistern",
    "B100": "Faron Woods: Forest Boss (R00 Ghirahim)",
    "B100_1": "Faron Woods: After Forest Boss (R00 Skyview Spring)",
    "B101": "Faron Woods: Forest Boss (Asura)",
    "B101_1": "Faron Woods: Farore's Candle Room",
    "S100": "Faron Woods: Forest Silent Realm",
    "F200": "Eldin Volcano: Eldin Volcano",
    "F201_1": "Eldin Volcano: Inside Volcano",
    "F201_2": "Eldin Volcano: Volcano F3 (Crater)",
    "F201_3": "Eldin Volcano: Fire Sanctuary Entrance",
    "F201_4": "Eldin Volcano: Volcano Summit - Waterfall",
    "F202": "Eldin Volcano: Volcano F3",
    "F202_1": "Eldin Volcano: Volcano F3 (Fire Dragon Dummy 1)",
    "F202_2": "Eldin Volcano: Volcano F3 (Fire Dragon Dummy 2)",
    "F202_3": "Eldin Volcano: Volcano F3 Completed (Fire Dragon Dummy 1)",
    "F202_4": "Eldin Volcano: Volcano F3 Completed (Fire Dragon Dummy 2)",
    "F210": "Eldin Volcano: Caves",
    "F211": "Eldin Volcano: Thrill Digger",
    "F221": "Eldin Volcano: Volcano F2 (Fire Dragon Room)",
    "D200": "Eldin Volcano: Earth Temple",
    "D201": "Eldin Volcano: Fire Sanctuary (A)",
    "D201_1": "Eldin Volcano: Fire Sanctuary (B)",
    "B200": "Eldin Volcano: Volcano D1 Boss",
    "B201": "Eldin Volcano: Volcano D2 Boss (Ghirahim 2nd Fight)",
    "B201_1": "Eldin Volcano: Volcano D2 Boss (Din's Fire)",
    "B210": "Eldin Volcano: Volcano D1 Boss (Earth Spring)",
    "S200": "Eldin Volcano: Mountain Silent Realm",
    "F300": "Lanayru Desert: Lanayru Desert",
    "F300_1": "Lanayru Desert: Lanayru Mine",
    "F300_2": "Lanayru Desert: Power Generator #1",
    "F300_3": "Lanayru Desert: Power Generator #2",
    "F300_4": "Lanayru Desert: Temple of Time",
    "F300_5": "Lanayru Desert: LMF to ToT",
    "F301": "Lanayru Desert: Lanayru Sand Sea Docks",
    "F301_1": "Lanayru Desert: Lanayru Sand Sea",
    "F301_2": "Lanayru Desert: Pirate Stronghold",
    "F301_3": "Lanayru Desert: Skipper's Retreat",
    "F301_4": "Lanayru Desert: Shipyard",
    "F301_5": "Lanayru Desert: Skipper's Retreat Shack",
    "F301_6": "Lanayru Desert: Desert F2 Timeshift Island",
    "F301_7": "Lanayru Desert: Shipyard Construction Bay",
    "F302": "Lanayru Desert: Lanayru Gorge",
    "F303": "Lanayru Desert: Lanayru Caves",
    "D300": "Lanayru Desert: Lanayru Mining Facility (A)",
    "D300_1": "Lanayru Desert: Lanayru Mining Facility (B)",
    "D301": "Lanayru Desert: Sandship (A)",
    "D301_1": "Lanayru Desert: Sandship (B)",
    "B300": "Lanayru Desert: Desert Boss 00 (Moldarach)",
    "B301": "Lanayru Desert: Desert Boss Kraken",
    "S300": "Lanayru Desert: Sand Silent Realm",
    "F400": "Sealed Grounds: Forest",
    "F401": "Sealed Grounds: Whirlpool",
    "F402": "Sealed Grounds: Temple",
    "F403": "Sealed Grounds: Whirlpool (Past)",
    "F404": "Sealed Grounds: Temple (Past)",
    "F405": "Sealed Grounds: Whirlpool (Cutscene)",
    "F406": "Sealed Grounds: Whirlpool (With Statue)",
    "F407": "Sealed Grounds: Temple (Cutscene)",
    "B400": "Sealed Grounds: Last Boss",
    "Demo": "Staff Roll",
}
