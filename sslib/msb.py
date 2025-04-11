# This file is heavily based on the equivalent file in the Skyward Sword Randomizer codebase (SD).
# That file can be found here: https://github.com/ssrando/ssrando/blob/main/sslib/msb.py

import struct
from typing import NewType

from .utils import unpack, to_str, to_bytes

FLOWTYPES = {"type1": 1, "switch": 2, "type3": 3, "start": 4}

ParsedMsb = NewType("ParsedMsb", dict)

# both in utf-8
CONTROL_REPLACEMENTS = {
    "<r<": "\x0e\x00\x03\x02\x00",  # red
    "<rd<": "\x0e\x00\x03\x02\x01",  # also red
    "<y+<": "\x0e\x00\x03\x02\x02",  # yellow-white
    "<b<": "\x0e\x00\x03\x02\x03",  # blue
    "<g<": "\x0e\x00\x03\x02\x04",  # green
    "<y<": "\x0e\x00\x03\x02\x05",  # yellow
    "<g+<": "\x0e\x00\x03\x02\x07",  # green rupee green
    "<b+<": "\x0e\x00\x03\x02\x08",  # blue rupee blue
    "<r+<": "\x0e\x00\x03\x02\x09",  # red-white
    "<s<": "\x0e\x00\x03\x02\x0a",  # silver
    "<ye<": "\x0e\x00\x03\x02\x0b",  # gold rupee gold
    "<blk<": "\x0e\x00\x03\x02\x0c",  # rupoor
    ">>": "\x0e\x00\x03\x02\uffff",  # end color
    # start of option token, '-' means cancel (B) option
    "[1]": "\x0e\x01\x00\x02\uffff",
    "[2-]": "\x0e\x01\x01\x02\x00",
    "[2]": "\x0e\x01\x01\x02\uffff",
    "[3-]": "\x0e\x01\x02\x02\x00",
    "[3]": "\x0e\x01\x02\x02\uffff",
    "[4-]": "\x0e\x01\x03\x02\x00",
    "[4]": "\x0e\x01\x03\x02\uffff",
    "<numeric arg0>": "\x0e\x02\x03\x06\x00\x00\xcd",
    "<numeric arg1>": "\x0e\x02\x03\x06\x00\x01\xcd",
    "<numeric arg2>": "\x0e\x02\x03\x06\x00\x02\xcd",
    "<numeric arg3>": "\x0e\x02\x03\x06\x00\x03\xcd",
    "<numeric arg4>": "\x0e\x02\x03\x06\x00\x04\xcd",
    "<numeric arg5>": "\x0e\x02\x03\x06\x00\x05\xcd",
    "<numeric arg6>": "\x0e\x02\x03\x06\x00\x06\xcd",
    "<numeric arg7>": "\x0e\x02\x03\x06\x00\x07\xcd",
    "<numeric arg8>": "\x0e\x02\x03\x06\x00\x08\xcd",
    "<numeric arg9>": "\x0e\x02\x03\x06\x00\x09\xcd",
    "<string arg0>": "\x0e\x02\x02\x04\x00\x00",
    "<string arg1>": "\x0e\x02\x02\x04\x00\x01",
    "<string arg2>": "\x0e\x02\x02\x04\x00\x02",
    "<string arg3>": "\x0e\x02\x02\x04\x00\x03",
    "<heroname>": "\x0e\x02\x00\x00",
    "<slowtext>": "\x0e\x01\x05\x04\x1e\x00",
    "<pause 5>": "\x0e\x01\x04\x02\x05",  # only works with <slowtext> in rando
    "<pause 15>": "\x0e\x01\x04\x02\x0f",  # only works with <slowtext> in rando
    # These are the different actions NPCs can do while talking
    # Must be paired with a sound effect index (?)
    # e.g. <action6 \x03> would perform the NPC action 6 with sound effect 3
    "<action0 ": "\x0e\x01\x09\x04\x00",
    "<action1 ": "\x0e\x01\x09\x04\x01",
    "<action2 ": "\x0e\x01\x09\x04\x02",
    "<action3 ": "\x0e\x01\x09\x04\x03",
    "<action4 ": "\x0e\x01\x09\x04\x04",
    "<action5 ": "\x0e\x01\x09\x04\x05",
    "<action6 ": "\x0e\x01\x09\x04\x06",
    "<action7 ": "\x0e\x01\x09\x04\x07",
    "<action8 ": "\x0e\x01\x09\x04\x08",
    "<action9 ": "\x0e\x01\x09\x04\x09",
    "<actionA ": "\x0e\x01\x09\x04\x0a",
    "<actionB ": "\x0e\x01\x09\x04\x0b",
    "<actionC ": "\x0e\x01\x09\x04\x0c",
    "<actionD ": "\x0e\x01\x09\x04\x0d",
    "<actionE ": "\x0e\x01\x09\x04\x0e",
    "<actionF ": "\x0e\x01\x09\x04\x0f",
    # Different icons within text
    "<icon 30>": "\x0e\x02\x04\x02\u1ecd",  # X button icon
}


def process_control_sequences(data: str) -> str:
    for orig, replaced in CONTROL_REPLACEMENTS.items():
        data = data.replace(orig, replaced)

    # Catch any closing brackets (only expected from "sound" control codes)
    data = data.replace(">", "")

    return data


def parse_msb(data: bytes) -> ParsedMsb:
    parsed = ParsedMsb({})

    if data[:10] == b"MsgFlwBn\xfe\xff":
        parsed["type"] = "MsgFlwBn"
        assert data[10:16] == b"\x00\x00\x00\x03\x00\x02"
    elif data[:10] == b"MsgStdBn\xfe\xff":
        parsed["type"] = "MsgStdBn"
        assert data[10:16] == b"\x00\x00\x01\x03\x00\x03"
    else:
        raise Exception("Unsupported filetype.")

    assert struct.unpack(">i", data[0x12:0x16])[0] == len(data)
    pos = 0x20

    while pos < len(data):
        seg_header = data[pos : pos + 0x10]
        pos += 0x10
        seg_id, seg_len, zero1, zero2 = struct.unpack(">4siii", seg_header)
        assert zero1 == 0
        assert zero2 == 0
        seg_id = seg_id.decode("ascii")
        seg_data = data[pos : pos + seg_len]
        pos += seg_len
        pos += -pos % 0x10
        assert not seg_id in parsed

        if seg_id == "FLW3":
            parsed["FLW3"] = {}
            parsed["FLW3"]["flow"] = []
            parsed["FLW3"]["branch_points"] = []
            count1, count2 = struct.unpack(">hh12x", seg_data[:0x10])

            for i in range(count1):  # for every node in FLW3
                item = unpack(
                    "type subType param1 param2 next param3 param4 param5",
                    ">bb2xhhhhhh",
                    seg_data[0x10 + 0x10 * i : 0x20 + 0x10 * i],
                )
                assert item["type"] in (1, 2, 3, 4)
                item["type"] = ["type1", "switch", "type3", "start"][item["type"] - 1]
                parsed["FLW3"]["flow"].append(item)

            for i in range(count2):  # for every branch point
                item = struct.unpack(
                    ">h",
                    seg_data[
                        0x10 + 0x10 * count1 + 2 * i : 0x12 + 0x10 * count1 + 2 * i
                    ],
                )[0]
                parsed["FLW3"]["branch_points"].append(item)

        elif seg_id == "FEN1" or seg_id == "LBL1":
            parsed[seg_id] = []
            count = struct.unpack(">i", seg_data[:4])[0]

            for i in range(count):
                count, ptr = struct.unpack(">ii", seg_data[4 + 8 * i : 0xC + 8 * i])
                entrypoint_group = []

                for _ in range(count):
                    strlen = seg_data[ptr]
                    string = seg_data[1 + ptr : 1 + ptr + strlen].decode("ascii")
                    value = struct.unpack(
                        ">i", seg_data[1 + ptr + strlen : 5 + ptr + strlen]
                    )[0]
                    entrypoint = {}
                    entrypoint["name"] = string
                    entrypoint["value"] = value
                    entrypoint_group.append(entrypoint)
                    ptr += 5 + strlen

                parsed[seg_id].append(entrypoint_group)

        elif seg_id == "ATR1":
            parsed["ATR1"] = []
            count, dimension = struct.unpack(">ii", seg_data[:8])

            for i in range(count):
                cur_list = []

                for j in range(dimension):
                    cur_list.append(seg_data[8 + i * dimension + j])

                parsed["ATR1"].append(cur_list)

        elif seg_id == "TXT2":
            parsed["TXT2"] = []
            count = struct.unpack(">i", seg_data[:4])[0]
            indices = [
                struct.unpack(">i", seg_data[4 + 4 * i : 8 + 4 * i])[0]
                for i in range(count)
            ]

            for i in range(count):  # for every item of text
                bytestring = seg_data[
                    indices[i] : (indices[i + 1] if i + 1 < count else seg_len) - 2
                ]
                parsed["TXT2"].append(bytestring)
        else:
            raise Exception(f"Unsupported seg_id: {seg_id}.")

    return parsed


def build_msb(msb: ParsedMsb) -> bytes:
    if msb["type"] == "MsgFlwBn":
        header = b"MsgFlwBn\xfe\xff"
        header += b"\x00\x00\x00\x03\x00\x02"
    elif msb["type"] == "MsgStdBn":
        header = b"MsgStdBn\xfe\xff"
        header += b"\x00\x00\x01\x03\x00\x03"
    else:
        raise Exception(f'Unsupported filetype: {msb["type"]}.')

    header = bytearray(header + b"\x00" * 16)
    total_body = b""

    for seg_id, seg_data in msb.items():
        body = b""

        if seg_id == "type":
            continue
        if seg_id == "FLW3":
            body += struct.pack(
                ">hh", len(seg_data["flow"]), len(seg_data["branch_points"])
            )
            body += b"\x00" * 12

            for flow in seg_data["flow"]:
                body += struct.pack(
                    ">bbhhhhhhh",
                    FLOWTYPES[flow["type"]],
                    flow["subType"],
                    0,
                    flow["param1"],
                    flow["param2"],
                    flow["next"],
                    flow["param3"],
                    flow["param4"],
                    flow["param5"],
                )

            for branch_point in seg_data["branch_points"]:
                body += struct.pack(">h", branch_point)

        elif seg_id == "FEN1" or seg_id == "LBL1":
            data = b""
            offset = len(seg_data) * 8 + 4
            seg_body = b""

            for subseg in seg_data:
                data += struct.pack(">ii", len(subseg), offset + len(seg_body))

                for subsub in subseg:
                    seg_body += struct.pack(">b", len(subsub["name"]))
                    seg_body += subsub["name"].encode("ascii")
                    seg_body += struct.pack(">i", subsub["value"])

            data += seg_body
            body += struct.pack(">i", len(seg_data))
            body += data
        elif seg_id == "ATR1":
            dimension = None

            for atr in seg_data:
                if dimension is None:
                    dimension = len(atr)
                else:
                    assert dimension == len(atr)

            body += struct.pack(">ii", len(seg_data), dimension)

            for atr in seg_data:
                for val in atr:
                    body += struct.pack(">b", val)

        elif seg_id == "TXT2":
            body += struct.pack(">i", len(seg_data))
            offset = 4 * len(seg_data) + 4
            seg_header = b""
            seg_body = b""

            for txt in seg_data:
                seg_header += struct.pack(">i", offset + len(seg_body))
                seg_body += txt + b"\x00\x00"

            body += seg_header
            body += seg_body
        else:
            raise Exception(f"Unsupported seg_id: {seg_id}.")

        total_body += seg_id.encode("ascii")
        total_body += struct.pack(">i", len(body)) + 8 * b"\x00"
        total_body += body
        total_body += (-len(total_body) % 0x10) * b"\xab"

    total_length = len(header) + len(total_body)
    header[0x12] = (total_length >> 24) & 0xFF
    header[0x13] = (total_length >> 16) & 0xFF
    header[0x14] = (total_length >> 8) & 0xFF
    header[0x15] = total_length & 0xFF

    return header + total_body


def add_msbf_branch(msbf: ParsedMsb, switch: dict, branchpoints: list):
    branch_index = len(msbf["FLW3"]["branch_points"])
    msbf["FLW3"]["branch_points"].extend(branchpoints)
    switch["param4"] = len(branchpoints)
    switch["param5"] = branch_index
    msbf["FLW3"]["flow"].append(switch)
