import re

DEFAULT_SOBJ = {
    "params1": 0,
    "params2": 0,
    "posx": 0,
    "posy": 0,
    "posz": 0,
    "sizex": 0,
    "sizey": 0,
    "sizez": 0,
    "anglex": 0,
    "angley": 0,
    "anglez": 0,
    "id": 0,
    "name": "",
}

DEFAULT_OBJ = {
    "params1": 0,
    "params2": 0,
    "posx": 0,
    "posy": 0,
    "posz": 0,
    "anglex": 0,
    "angley": 0,
    "anglez": 0,
    "id": 0,
    "name": "",
}

DEFAULT_SCEN = {
    "name": "",
    "room": 0,
    "layer": 0,
    "entrance": 0,
    "night": 0,
    "byte5": 0,
    "flag6": 0,
    "zero": 0,
    "saveprompt": 0,
}

DEFAULT_PLY = {
    "storyflag": 0,
    "play_cutscene": -1,
    "byte4": -1,
    "posx": 0,
    "posy": 0,
    "posz": 0,
    "anglex": 0,
    "angley": 0,
    "anglez": 0,
    "entrance_id": 6,
}

DEFAULT_AREA = {
    "posx": 0,
    "posy": 0,
    "posz": 0,
    "sizex": 0,
    "sizey": 0,
    "sizez": 0,
    "angle": 0,
    "area_link": -1,
    "unk3": 0,
    "dummy": b"\xFF\xFF\xFF",
}

DEFAULT_PATH = {
    "unk1": -1,
    "unk2": -1,
    "pnt_start_idx": 0,
    "pnt_total_count": 0,
    "unk3": b"\xFF\xFF\xFF\xFF\x00\xFF",
}

DEFAULT_PNT = {
    "posx": 0.0,
    "posy": 0.0,
    "posz": 0.0,
    "unk": b"\xFF\xFF\xFF\xFF",
}

DEFAULT_FLOW = {
    "type": "type1",
    "subType": -1,
    "param1": 0,
    "param2": 0,
    "param3": 0,
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_GIVE_ITEM_FLOW = {
    "type": "type3",
    "subType": 0,
    "param1": 0,
    "param2": -1,  # item id
    "param3": 9,  # give item command
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_SET_ITEM_FLAG_FLOW = {
    "type": "type3",
    "subType": 0,
    "param1": 0,
    "param2": -1,  # item id
    "param3": 53,  # set item flag command
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_SET_STORYFLAG_FLOW = {
    "type": "type3",
    "subType": 0,
    "param1": 0,
    "param2": -1,  # storyflag id
    "param3": 0,
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_SET_SCENEFLAG_FLOW = {
    "type": "type3",
    "subType": 1,
    "param1": -1,  # sceneflag id
    "param2": -1,  # scene index
    "param3": 2,  # give sceneflag command
    "param4": 0,
    "param5": 0,
    "next": -1,
}

DEFAULT_CHECK_STORYFLAG_FLOW = {
    "type": "switch",
    "subType": 6,
    "param1": 0,
    "param2": -1,  # storyflag
    "param3": 3,  # check storyflag command
    "param4": 0,
    "param5": 0,
}

DEFAULT_CHECK_SCENEFLAG_FLOW = {
    "type": "switch",
    "subType": 6,
    "param1": 0,
    "param2": -1,  # sceneflag
    "param3": 6,  # check sceneflag command
    "param4": 0,
    "param5": 0,
}

FLOW_ADD_VARIATIONS = (
    "flowadd",
    "giveitem",
    "setitemflag",
    "setstoryflag",
    "setsceneflag",
)
SWITCH_ADD_VARIATIONS = ("switchadd", "checkstoryflag", "checksceneflag")

PARAM1_ALIASES = ("setsceneflag",)
PARAM2_ALIASES = (
    "itemid",
    "setstoryflag",
    "sceneindex",
    "checkstoryflag",
    "checksceneflag",
)

DEFAULT_FLOW_TYPE_LOOKUP = {
    "flowadd": DEFAULT_FLOW,
    "giveitem": DEFAULT_GIVE_ITEM_FLOW,
    "setitemflag": DEFAULT_SET_ITEM_FLAG_FLOW,
    "setstoryflag": DEFAULT_SET_STORYFLAG_FLOW,
    "setsceneflag": DEFAULT_SET_SCENEFLAG_FLOW,
    "switchadd": DEFAULT_FLOW,
    "checkstoryflag": DEFAULT_CHECK_STORYFLAG_FLOW,
    "checksceneflag": DEFAULT_CHECK_SCENEFLAG_FLOW,
}

STAGE_REGEX = re.compile("(.+)_stg_l([0-9]+).arc.LZ")
EVENT_REGEX = re.compile("([0-9])-[A-Za-z]+.arc")
ROOM_REGEX = re.compile(r"/rarc/(?P<stage>.+)_r(?P<roomid>[0-9]+).arc")
OARC_ARC_REGEX = re.compile(r"/oarc/(?P<name>.+\.arc)")
TEXT_ARC_REGEX = re.compile(
    r"(.+(/|\\))*(?P<lang>(en|es|fr))_US(/|\\)(?P<name>.+\.arc)"
)
