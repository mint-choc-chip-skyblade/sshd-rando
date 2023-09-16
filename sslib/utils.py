# This file is heavily based on the equivalent file in the Skyward Sword Randomizer codebase (SD).
# That file can be found here: https://github.com/ssrando/ssrando/blob/main/sslib/utils.py

from collections import namedtuple
from pathlib import Path

import struct


def unpack(fields: str, format_str: str, item: bytes) -> dict:
    return namedtuple("_", fields)._make(struct.unpack(format_str, item))._asdict()


def to_str(byte_str: bytes) -> str:
    """Converts a bytestring, which is shift-jis encoded to a string"""
    return byte_str.split(b"\x00", 1)[0].decode("shift-jis")


def to_bytes(string: str, length: int) -> bytes:
    """Converts a string into shift-jis encoding and padding it with zeroes to the specified length"""
    encoded = string.encode("shift-jis")
    return encoded + (b"\x00" * (length - len(encoded)))


def write_bytes_create_dirs(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def mask_shift_set(value: int, mask: int, shift: int, new_value: int) -> int:
    """
    Replace new_value in value, by applying the mask after the shift
    """
    new_value = new_value & mask
    return (value & ~(mask << shift)) | (new_value << shift)
