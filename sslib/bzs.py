# Initial parsing from mrcheezes skyward-sword-tools https://github.com/MrCheeze/skywardsword-tools/blob/master/bzs.py
# Used for the parsing of stage and room files.

# This file is heavily based on the equivalent file in the Skyward Sword Randomizer codebase (SD).
# That file can be found here: https://github.com/ssrando/ssrando/blob/main/sslib/bzs.py

from typing import NewType, Tuple
import struct
import json

from constants.patchconstants import STAGE_OBJECT_NAMES

from .utils import unpack, to_str, to_bytes

OBJECT_STRUCTS = {
    "FILE": ("unk dummy", ">hh", 4),
    "SCEN": (
        "name room layer entrance night byte5 flag6 zero saveprompt",
        ">32sbbbbbbbb",
        40,
    ),
    "CAM ": ("unk1 posx posy posz angle unk2 name", ">4s3ff8s16s", 44),
    "PATH": ("unk1 unk2 pnt_start_idx pnt_total_count unk3", ">bbHH6s", 12),
    "PNT ": ("posx posy posz unk", ">3f4s", 16),
    "SPNT": ("posx posy posz unk", ">3f4s", 16),
    "BPNT": (
        "pos1x pos1y pos1z pos2x pos2y pos2z pos3x pos3y pos3z unk",
        ">3f3f3f4s",
        40,
    ),
    "SPTH": ("unk1 unk2 pnt_start_idx pnt_total_count unk3", ">bbHH6s", 12),
    "AREA": (
        "posx posy posz sizex sizey sizez angle area_link unk3 dummy",
        ">3f3fHhb3s",
        32,
    ),
    "EVNT": (
        "unk1 story_flag1 story_flag2 unk2 exit_id unk3 skipevent unk4 sceneflag1 sceneflag2 skipflag dummy1 item dummy2 name",
        ">2shh3sb3sb1sBBBhhh32s",
        56,
    ),
    "PLY ": (
        "storyflag play_cutscene byte4 posx posy posz anglex angley anglez entrance_id",
        ">hbb3f3Hh",
        24,
    ),
    "OBJS": (
        "params1 params2 posx posy posz                   anglex angley anglez id name",
        ">II3fHHHH8s",
        36,
    ),
    "OBJ ": (
        "params1 params2 posx posy posz                   anglex angley anglez id name",
        ">II3fHHHH8s",
        36,
    ),
    "SOBS": (
        "params1 params2 posx posy posz sizex sizey sizez anglex angley anglez id name",
        ">II3f3fHHHH8s",
        48,
    ),
    "SOBJ": (
        "params1 params2 posx posy posz sizex sizey sizez anglex angley anglez id name",
        ">II3f3fHHHH8s",
        48,
    ),
    "STAS": (
        "params1 params2 posx posy posz sizex sizey sizez anglex angley anglez id name",
        ">II3f3fHHHH8s",
        48,
    ),
    "STAG": (
        "params1 params2 posx posy posz sizex sizey sizez anglex angley anglez id name",
        ">II3f3fHHHH8s",
        48,
    ),
    "SNDT": (
        "params1 params2 posx posy posz sizex sizey sizez anglex angley anglez id name",
        ">II3f3fHHHH8s",
        48,
    ),
    "DOOR": (
        "params1 params2 posx posy posz                   anglex angley anglez id name",
        ">II3fHHHH8s",
        36,
    ),
    "LYSE": ("story_flag night layer", ">hbb", 4),
    "STIF": (
        "wtf1 wtf2 wtf3 byte1 flagindex byte3 byte4 unk1 map_name_id unk2",
        ">3fbbbb2sb1s",
        20,
    ),
    "PCAM": ("pos1x pos1y pos1z pos2x pos2y pos2z angle wtf unk", ">3f3fff4s", 36),
    "LYLT": ("layer demo_high demo_low dummy", ">bbbb", 4),
}

NAME_LENGTHS = {
    "SCEN": 32,
    "CAM ": 16,
    "EVNT": 32,
    "OBJS": 8,
    "OBJ ": 8,
    "SOBS": 8,
    "SOBJ": 8,
    "STAS": 8,
    "STAG": 8,
    "SNDT": 8,
    "DOOR": 8,
}

NODE_STRUCT = ">4shhi"
NODE_STRUCT_NAMES = "name count ff offset"

ParsedBzs = NewType("ParsedBzs", dict)


def parse_bzs(data: bytes) -> dict:
    name, count, ff, offset = struct.unpack(">4shhi", data[:12])
    assert ff == -1

    name = name.decode("ascii")
    parsed_object = parse_object(name, count, data[offset:])
    assert type(parsed_object) is dict

    return parsed_object


def parse_object(object_type: str, quantity: int, object_data: bytes) -> dict | list:
    if object_type == "V001":
        # root
        parsed = {}

        for i in range(quantity):
            address = i * 12
            name, count, ff, offset = struct.unpack(
                ">4shhi", object_data[address : address + 12]
            )
            assert ff == -1
            name = name.decode("ascii")
            parsed[name] = parse_object(name, count, object_data[address + offset :])

        return parsed

    elif object_type == "LAY ":
        # different layers of the room (always 29 of them)
        assert quantity == 29
        parsed = {}

        for i in range(quantity):
            address = i * 8
            count, ff, offset = struct.unpack(
                ">hhi", object_data[address : address + 8]
            )

            if count == 0:
                parsed["l%d" % i] = {}
            else:
                parsed["l%d" % i] = parse_object(
                    "V001", count, object_data[address + offset :]
                )

        return parsed

    elif object_type in ("OBJN", "ARCN"):
        parsed = []

        for i in range(quantity):
            address = object_data[2 * i] * 0x100 + object_data[2 * i + 1]
            name = to_str(object_data[address:])
            parsed.append(name)

        return parsed

    elif object_type == "RMPL":
        parsed = {}

        for i in range(quantity):
            rmpl_data = object_data[4 * i :]
            rmpl_id = rmpl_data[0]
            count = rmpl_data[1]
            address = rmpl_data[2] * 0x100 + rmpl_data[3]
            parsed[rmpl_id] = []

            for j in range(count):
                parsed[rmpl_id].append(rmpl_data[address + 2 * j : address + 2 * j + 2])

        return parsed

    else:
        # objects with quantities
        parsed = []
        struct_names, struct_def, size = OBJECT_STRUCTS[object_type]

        for i in range(quantity):
            item = object_data[size * i : size * (i + 1)]
            unpacked = unpack(struct_names, struct_def, item)

            if "name" in unpacked.keys():
                unpacked["name"] = to_str(unpacked["name"])

            parsed.append(unpacked)

        return parsed


def build_bzs(root: dict) -> bytes:
    count, object_data = build_object("V001", root)
    data = struct.pack(NODE_STRUCT, b"V001", count, -1, 12) + object_data

    # padding
    pad = 32 - (len(data) % 32)
    if pad == 32:
        pad = 0
    data += b"\xff" * pad
    return data


def build_object(
    object_type, object_data
) -> Tuple[int, bytes]:  # number of elements, bytes of body
    if object_type == "V001":
        assert type(object_data) == dict
        offset = len(object_data) * 12
        body = b""
        header_bytes = b""

        for data_type, obj in object_data.items():
            count, data = build_object(data_type, obj)
            # pad to 4
            pad = (4 - (len(data) % 4)) * b"\xff"
            if len(pad) == 4:
                pad = b""
            header_bytes += struct.pack(
                NODE_STRUCT,
                data_type.encode("ASCII"),
                count,
                -1,
                len(body) - len(header_bytes) + offset,
            )
            body += data + pad

        return (len(object_data), header_bytes + body)
    elif object_type == "LAY ":
        assert type(object_data) == dict
        assert len(object_data) == 29
        offset = 29 * 8
        body = b""
        header_bytes = b""

        for layer in object_data.values():
            if not layer:
                header_bytes += struct.pack(">hhi", 0, -1, 0)
            else:
                count, data = build_object("V001", layer)
                dataoffset = len(body) - len(header_bytes) + offset
                # pad to 4
                pad = (4 - (len(data) % 4)) * b"\xff"
                if len(pad) == 4:
                    pad = b""
                header_bytes += struct.pack(">hhi", count, -1, dataoffset)
                body += data + pad

        return (29, header_bytes + body)

    elif object_type in ("OBJN", "ARCN"):
        assert type(object_data) == list
        offset = len(object_data) * 2
        sbytes = b""
        header_bytes = b""

        for string in object_data:
            header_bytes += struct.pack(">H", len(sbytes) + offset)
            sbytes += string.encode("ASCII") + b"\x00"

        return (len(object_data), header_bytes + sbytes)

    elif object_type == "RMPL":
        assert type(object_data) == dict
        offset = len(object_data) * 4
        body = b""
        header_bytes = b""

        for i, string in object_data.items():
            header_bytes += struct.pack(
                ">BBH", i, len(string), len(body) + offset - len(header_bytes)
            )
            body += b"".join(string)

        return (len(object_data), header_bytes + body)

    else:
        assert type(object_data) == list

        for obj in object_data:
            if "name" in obj:
                obj["name"] = to_bytes(obj["name"], NAME_LENGTHS[object_type])

        _, struct_def, _ = OBJECT_STRUCTS[object_type]
        mapped = (struct.pack(struct_def, *obj.values()) for obj in object_data)

        return (len(object_data), b"".join(mapped))


def get_entry_from_bzs(
    bzs: dict, object_def: dict, remove: bool = False
) -> dict | None:
    id = object_def.get("id", None)
    index = object_def.get("index", None)
    layer = object_def.get("layer", None)
    object_type = object_def["objtype"].ljust(
        4
    )  # OBJ has an whitespace but thats was too error prone for the yaml, so just pad it here

    if layer is None:
        object_list = bzs[object_type]
    else:
        object_list = bzs["LAY "][f"l{layer}"][object_type]

    if not id is None:
        objs = [x for x in object_list if x["id"] == id]

        if len(objs) != 1:
            print(f"Error finding object: {json.dumps(object_def)}")
            return None

        obj = objs[0]

        if remove:
            object_list.remove(obj)

    elif not index is None:
        if index >= len(object_list):
            print(f"Error lisError list index out of range: {json.dumps(object_def)}")
            return None

        if remove:
            obj = object_list.pop(index)
        else:
            obj = object_list[index]

    else:
        print(f"ERROR: neither id nor index given for object {json.dumps(object_def)}")
        return None

    return obj


def get_highest_object_id(bzs: dict) -> int:
    max_id = 0

    for layer in bzs.get("LAY ", {}).values():
        if len(layer) == 0:
            continue

        for object_type in STAGE_OBJECT_NAMES:
            if object_type in layer:
                id = layer[object_type][-1]["id"] & 0x3FF

                if id != 0x3FF:  # aparently some objects have the max id?
                    max_id = max(max_id, id)

    return max_id
