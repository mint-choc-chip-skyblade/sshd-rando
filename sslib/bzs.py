# Initial parsing from mrcheezes skyward-sword-tools https://github.com/MrCheeze/skywardsword-tools/blob/master/bzs.py
# Used for the parsing of stage and room files.

# This file is heavily based on the equivalent file in the Skyward Sword Randomizer codebase (SD).
# That file can be found here: https://github.com/ssrando/ssrando/blob/main/sslib/bzs.py

from typing import NewType, Tuple
from collections import OrderedDict
import struct
import json

from .utils import unpack, toStr, toBytes

nodestruct = ">4shhi"
nodestructnames = "name count ff offset"

ParsedBzs = NewType("ParsedBzs", OrderedDict)


def parseBzs(data: bytes) -> OrderedDict | list:
    name, count, ff, offset = struct.unpack(">4shhi", data[:12])
    assert ff == -1
    name = name.decode("ascii")
    return parseObj(name, count, data[offset:])


def parseObj(objtype, quantity, data):
    if objtype == "V001":
        # root
        parsed = OrderedDict()
        for i in range(quantity):
            addr = i * 12
            name, count, ff, offset = struct.unpack(">4shhi", data[addr : addr + 12])
            assert ff == -1
            name = name.decode("ascii")
            parsed[name] = parseObj(name, count, data[addr + offset :])
            # if name != 'LAY ':
            #    parsed[name]=len(parsed[name])
        return parsed
    elif objtype == "LAY ":
        # different layers of the room (always 29 of them)
        assert quantity == 29
        parsed = OrderedDict()
        for i in range(quantity):
            addr = i * 8
            count, ff, offset = struct.unpack(">hhi", data[addr : addr + 8])
            if count == 0:
                parsed["l%d" % i] = OrderedDict()
            else:
                parsed["l%d" % i] = parseObj("V001", count, data[addr + offset :])
        return parsed

    elif objtype in ("OBJN", "ARCN"):
        parsed = []
        for i in range(quantity):
            addr = data[2 * i] * 0x100 + data[2 * i + 1]
            name = toStr(data[addr:])
            parsed.append(name)
        return parsed
    elif objtype == "RMPL":
        parsed = OrderedDict()
        for i in range(quantity):
            rmpldata = data[4 * i :]
            rmpl_id = rmpldata[0]
            count = rmpldata[1]
            addr = rmpldata[2] * 0x100 + rmpldata[3]
            parsed[rmpl_id] = []
            for j in range(count):
                parsed[rmpl_id].append(rmpldata[addr + 2 * j : addr + 2 * j + 2])
        return parsed

    else:
        # objects with quantities
        parsed = []
        structnames, structdef, size = objectstructs[objtype]
        for i in range(quantity):
            item = data[size * i : size * (i + 1)]
            unpacked = unpack(structnames, structdef, item)
            if "name" in unpacked.keys():
                unpacked["name"] = toStr(unpacked["name"])
            parsed.append(unpacked)

        return parsed


objectstructs = {
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

namelengths = {
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


def buildBzs(root: OrderedDict) -> bytes:
    count, odata = buildObj("V001", root)
    data = struct.pack(nodestruct, b"V001", count, -1, 12) + odata

    # padding
    pad = 32 - (len(data) % 32)
    if pad == 32:
        pad = 0
    data += b"\xFF" * pad
    return data


def buildObj(
    objtype, objdata
) -> Tuple[int, bytes]:  # number of elements, bytes of body
    if objtype == "V001":
        assert type(objdata) == OrderedDict
        offset = len(objdata) * 12
        body = b""
        headerbytes = b""
        for typ, obj in objdata.items():
            count, data = buildObj(typ, obj)
            # pad to 4
            pad = (4 - (len(data) % 4)) * b"\xFF"
            if len(pad) == 4:
                pad = b""
            headerbytes += struct.pack(
                nodestruct,
                typ.encode("ASCII"),
                count,
                -1,
                len(body) - len(headerbytes) + offset,
            )
            body += data + pad
            # body+=(16-(len(body)%16))*b'\xFF'
        return (len(objdata), headerbytes + body)
    elif objtype == "LAY ":
        assert type(objdata) == OrderedDict
        assert len(objdata) == 29
        offset = 29 * 8
        body = b""
        headerbytes = b""
        for layer in objdata.values():
            if not layer:
                headerbytes += struct.pack(">hhi", 0, -1, 0)
            else:
                count, data = buildObj("V001", layer)
                dataoffset = len(body) - len(headerbytes) + offset
                # pad to 4
                pad = (4 - (len(data) % 4)) * b"\xFF"
                if len(pad) == 4:
                    pad = b""
                headerbytes += struct.pack(">hhi", count, -1, dataoffset)
                body += data + pad
        return (29, headerbytes + body)

    elif objtype in ("OBJN", "ARCN"):
        assert type(objdata) == list
        offset = len(objdata) * 2
        sbytes = b""
        headerbytes = b""
        for s in objdata:
            headerbytes += struct.pack(">H", len(sbytes) + offset)
            sbytes += s.encode("ASCII") + b"\x00"
        return (len(objdata), headerbytes + sbytes)
    elif objtype == "RMPL":
        assert type(objdata) == OrderedDict
        offset = len(objdata) * 4
        body = b""
        headerbytes = b""
        for i, s in objdata.items():
            headerbytes += struct.pack(
                ">BBH", i, len(s), len(body) + offset - len(headerbytes)
            )
            body += b"".join(s)
        return (len(objdata), headerbytes + body)

    else:
        assert type(objdata) == list
        for obj in objdata:
            if "name" in obj:
                obj["name"] = toBytes(obj["name"], namelengths[objtype])
        _, structdef, _ = objectstructs[objtype]
        mapped = (struct.pack(structdef, *obj.values()) for obj in objdata)
        return (len(objdata), b"".join(mapped))


def get_entry_from_bzs(
    bzs: OrderedDict, objdef: dict, remove: bool = False
) -> OrderedDict | None:
    id = objdef.get("id", None)
    index = objdef.get("index", None)
    layer = objdef.get("layer", None)
    objtype = objdef["objtype"].ljust(
        4
    )  # OBJ has an whitespace but thats was too error prone for the yaml, so just pad it here
    if layer is None:
        objlist = bzs[objtype]
    else:
        objlist = bzs["LAY "][f"l{layer}"][objtype]
    if not id is None:
        objs = [x for x in objlist if x["id"] == id]
        if len(objs) != 1:
            print(f"Error finding object: {json.dumps(objdef)}")
            return None
        obj = objs[0]
        if remove:
            objlist.remove(obj)
    elif not index is None:
        if index >= len(objlist):
            print(f"Error lisError list index out of range: {json.dumps(objdef)}")
            return None
        if remove:
            obj = objlist.pop(index)
        else:
            obj = objlist[index]
    else:
        print(f"ERROR: neither id nor index given for object {json.dumps(objdef)}")
        return None
    return obj


def get_highest_object_id(bzs) -> int:
    max_id = 0
    for layer in bzs.get("LAY ", {}).values():
        if len(layer) == 0:
            continue
        for objtype in ["OBJS", "OBJ ", "SOBS", "SOBJ", "STAS", "STAG", "SNDT", "DOOR"]:
            if objtype in layer:
                id = layer[objtype][-1]["id"] & 0x3FF
                if id != 0x3FF:  # aparently some objects have the max id?
                    max_id = max(max_id, id)
    return max_id
