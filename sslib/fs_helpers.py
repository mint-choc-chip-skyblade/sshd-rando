# This file is heavily based on the equivalent file in the Skyward Sword Randomizer codebase (SD).
# That file can be found here: https://github.com/ssrando/ssrando/blob/main/sslib/fs_helpers.py

import struct
from io import BufferedIOBase, BytesIO
from typing import Any

PADDING_BYTES = b"This is padding data to alignme"


class InvalidOffsetError(Exception):
    pass


def read_all_bytes(data: BytesIO | BufferedIOBase) -> bytes:
    data.seek(0)
    return data.read()


def read_bytes(data: BytesIO | BufferedIOBase, offset: int, length: int) -> bytes:
    data.seek(offset)
    return data.read(length)


def write_bytes(data: BytesIO | BufferedIOBase, offset: int, raw_bytes: bytes):
    data.seek(offset)
    data.write(raw_bytes)


def read_and_unpack_bytes(
    data: BytesIO | BufferedIOBase, offset: int, length: int, format_string: str
) -> tuple:
    data.seek(offset)
    requested_data = data.read(length)
    unpacked_data = struct.unpack(format_string, requested_data)
    return unpacked_data


def write_and_pack_bytes(
    data: BytesIO | BufferedIOBase,
    offset: int,
    new_values: list | tuple,
    format_string: str | bytes,
):
    packed_data = struct.pack(format_string, *new_values)
    data.seek(offset)
    data.write(packed_data)


def read_str(data: BytesIO | BufferedIOBase, offset: int, length: int) -> str:
    data_length = data.seek(0, 2)

    if offset + length > data_length:
        raise InvalidOffsetError(
            "Offset 0x%X, length 0x%X is past the end of the data (length 0x%X)."
            % (offset, length, data_length)
        )

    data.seek(offset)
    string = data.read(length).decode("shift_jis")
    string = string.rstrip("\0")  # Remove trailing null bytes
    return string


def try_read_str(
    data: BytesIO | BufferedIOBase, offset: int, length: int
) -> str | None:
    try:
        return read_str(data, offset, length)
    except UnicodeDecodeError:
        return None
    except InvalidOffsetError:
        return None


def read_str_until_null_character(data: BytesIO | BufferedIOBase, offset: int) -> str:
    data_length = data.seek(0, 2)
    if offset > data_length:
        raise InvalidOffsetError(
            "Offset 0x%X is past the end of the data (length 0x%X)."
            % (offset, data_length)
        )

    temp_offset = offset
    str_length = 0

    while temp_offset < data_length:
        data.seek(temp_offset)
        char = data.read(1)

        if char == b"\0":
            break
        else:
            str_length += 1

        temp_offset += 1

    data.seek(offset)
    str = data.read(str_length).decode("shift_jis")

    return str


def write_str(
    data: BytesIO | BufferedIOBase, offset: int, new_string: str, max_length: int
):
    # Writes a fixed-length string.
    # Although it is fixed-length, it still must have a null character terminating it,
    # so the real max length is one less than the passed max_length argument.
    str_len = len(new_string)
    if str_len >= max_length:
        raise Exception(
            'String "%s" is too long (max length including null byte: 0x%X).'
            % (new_string, max_length)
        )

    padding_length = max_length - str_len
    null_padding = b"\x00" * padding_length
    new_value = new_string.encode("shift_jis") + null_padding

    data.seek(offset)
    data.write(new_value)


def write_magic_str(
    data: BytesIO | BufferedIOBase, offset: int, new_string: str, max_length: int
):
    # Writes a fixed-length string that does not have to end with a null byte.
    # This is for magic file format identifiers.

    str_len = len(new_string)
    if str_len > max_length:
        raise Exception(
            "String %s is too long (max length 0x%X)." % (new_string, max_length)
        )

    padding_length = max_length - str_len
    null_padding = b"\x00" * padding_length
    new_value = new_string.encode("shift_jis") + null_padding

    data.seek(offset)
    data.write(new_value)


def write_str_with_null_byte(
    data: BytesIO | BufferedIOBase, offset: int, new_string: str
):
    # Writes a non-fixed length string.
    str_len = len(new_string)
    write_str(data, offset, new_string, str_len + 1)


def read_u8(
    data: BytesIO | BufferedIOBase, offset: int | None, is_little_endian=False
) -> Any:
    if not offset is None:
        data.seek(offset)

    if is_little_endian:
        format = "<B"
    else:
        format = ">B"

    return struct.unpack(format, data.read(1))[0]


def read_u16(
    data: BytesIO | BufferedIOBase, offset: int | None, is_little_endian=False
) -> Any:
    if not offset is None:
        data.seek(offset)

    if is_little_endian:
        format = "<H"
    else:
        format = ">H"

    return struct.unpack(format, data.read(2))[0]


def read_u24(
    data: BytesIO | BufferedIOBase, offset: int | None, is_little_endian=False
) -> Any:
    if not offset is None:
        data.seek(offset)

    # TODO: test if this actually works for little endian.
    if is_little_endian:
        format = "<BH"
    else:
        format = ">BH"

    d = struct.unpack(format, data.read(3))
    return (d[0] << 16) | d[1]


def read_u32(
    data: BytesIO | BufferedIOBase, offset: int | None, is_little_endian=False
) -> Any:
    if not offset is None:
        data.seek(offset)

    if is_little_endian:
        format = "<I"
    else:
        format = ">I"

    return struct.unpack(format, data.read(4))[0]


def read_float(
    data: BytesIO | BufferedIOBase, offset: int | None, is_little_endian=False
) -> Any:
    if not offset is None:
        data.seek(offset)

    if is_little_endian:
        format = "<f"
    else:
        format = ">f"

    return struct.unpack(format, data.read(4))[0]


def read_s8(
    data: BytesIO | BufferedIOBase, offset: int | None, is_little_endian=False
) -> Any:
    if not offset is None:
        data.seek(offset)

    if is_little_endian:
        format = "<b"
    else:
        format = ">b"

    return struct.unpack(format, data.read(1))[0]


def read_s16(
    data: BytesIO | BufferedIOBase, offset: int | None, is_little_endian=False
) -> Any:
    if not offset is None:
        data.seek(offset)

    if is_little_endian:
        format = "<h"
    else:
        format = ">h"

    return struct.unpack(format, data.read(2))[0]


def read_s32(
    data: BytesIO | BufferedIOBase, offset: int | None, is_little_endian=False
) -> Any:
    if not offset is None:
        data.seek(offset)

    if is_little_endian:
        format = "<i"
    else:
        format = ">i"

    return struct.unpack(format, data.read(4))[0]


def write_u8(
    data: BytesIO | BufferedIOBase,
    offset: int | None,
    new_value: bytes | int,
    is_little_endian=False,
):
    if is_little_endian:
        format = "<B"
    else:
        format = ">B"

    new_value = struct.pack(format, new_value)

    if not offset is None:
        data.seek(offset)

    data.write(new_value)


def write_u16(
    data: BytesIO | BufferedIOBase,
    offset: int | None,
    new_value: bytes | int,
    is_little_endian=False,
):
    if is_little_endian:
        format = "<H"
    else:
        format = ">H"

    new_value = struct.pack(format, new_value)

    if not offset is None:
        data.seek(offset)

    data.write(new_value)


def write_u24(
    data: BytesIO | BufferedIOBase,
    offset: int | None,
    value: int,
    is_little_endian=False,
):
    if not offset is None:
        data.seek(offset)

    # TODO: test if this actually works for little endian.
    if is_little_endian:
        format = "<BH"
    else:
        format = ">BH"

    high = value >> 16
    low = value & 0xFFFF
    data.write(struct.pack(format, high, low))


def write_u32(
    data: BytesIO | BufferedIOBase,
    offset: int | None,
    new_value: bytes | int,
    is_little_endian=False,
):
    if is_little_endian:
        format = "<I"
    else:
        format = ">I"

    new_value = struct.pack(format, new_value)

    if not offset is None:
        data.seek(offset)

    data.write(new_value)


def write_float(
    data: BytesIO | BufferedIOBase,
    offset: int | None,
    new_value: bytes | int,
    is_little_endian=False,
):
    if is_little_endian:
        format = "<f"
    else:
        format = ">f"

    new_value = struct.pack(format, new_value)

    if not offset is None:
        data.seek(offset)

    data.write(new_value)


def write_s8(
    data: BytesIO | BufferedIOBase,
    offset: int | None,
    new_value: bytes | int,
    is_little_endian=False,
):
    if is_little_endian:
        format = "<b"
    else:
        format = ">b"

    new_value = struct.pack(format, new_value)

    if not offset is None:
        data.seek(offset)

    data.write(new_value)


def write_s16(
    data: BytesIO | BufferedIOBase,
    offset: int | None,
    new_value: bytes | int,
    is_little_endian=False,
):
    if is_little_endian:
        format = "<h"
    else:
        format = ">h"

    new_value = struct.pack(format, new_value)

    if not offset is None:
        data.seek(offset)

    data.write(new_value)


def write_s32(
    data: BytesIO | BufferedIOBase,
    offset: int | None,
    new_value: bytes | int,
    is_little_endian=False,
):
    if is_little_endian:
        format = "<i"
    else:
        format = ">i"

    new_value = struct.pack(format, new_value)

    if not offset is None:
        data.seek(offset)

    data.write(new_value)


def pad_offset_to_nearest(offset: int, size: int) -> int:
    next_offset = offset + (size - offset % size) % size
    return next_offset
