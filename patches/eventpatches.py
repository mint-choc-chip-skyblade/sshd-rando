from filepathconstants import EVENT_PATCHES_PATH, EVENT_FILES_PATH, OUTPUT_EVENT_PATH
from patches.patchconstants import (
    FLOW_ADD_VARIATIONS,
    SWITCH_ADD_VARIATIONS,
    PARAM1_ALIASES,
    PARAM2_ALIASES,
    DEFAULT_FLOW_TYPE_LOOKUP,
)
from itemconstants import *
from pathlib import Path
from collections import defaultdict

from sslib.msb import parseMSB, buildMSB, add_msbf_branch, process_control_sequences
from sslib.u8file import U8File
from sslib.utils import write_bytes_create_dirs
from sslib.yaml import yaml_load


class EventPatchHandler:
    def __init__(self):
        self.eventPatches = yaml_load(EVENT_PATCHES_PATH)
        self.checkPatches = defaultdict(list)
        self.flowLabelToIndexMapping = {}
        self.textLabelToIndexMapping = {}

    def handle_event_patches(self):
        for eventPath in Path(EVENT_FILES_PATH).glob("*.arc"):
            fileName = eventPath.parts[-1]
            modifiedEventPath = Path(OUTPUT_EVENT_PATH / fileName)

            eventArc = U8File.get_parsed_U8_from_path(eventPath, False)

            # patch text files first
            for eventFilePath in filter(
                lambda name: name[-1] == "t", eventArc.get_all_paths()
            ):
                msbtFileName = eventFilePath.split("/")[-1]
                if msbtFileName[:-5] in self.eventPatches:
                    print(f"Patching {msbtFileName}")
                    parsedMSBT = parseMSB(eventArc.get_file_data(eventFilePath))
                    assert len(parsedMSBT["TXT2"]) == len(parsedMSBT["ATR1"])

                    for patch in self.eventPatches[msbtFileName[:-5]]:
                        # handle text patches here
                        if patch["type"] == "textadd":
                            self.text_add(
                                msbt=parsedMSBT,
                                textAdd=patch,
                                msbtFileName=msbtFileName,
                            )
                        elif patch["type"] == "textpatch":
                            self.text_patch(msbt=parsedMSBT, textPatch=patch)
                    eventArc.set_file_data(eventFilePath, buildMSB(parsedMSBT))
            for eventFilePath in filter(
                lambda name: name[-1] == "f", eventArc.get_all_paths()
            ):
                msbfFileName = eventFilePath.split("/")[-1]
                if (
                    msbfFileName[:-5] in self.eventPatches
                    or msbfFileName[:-5] in self.checkPatches
                    or msbfFileName == "003-ItemGet.msbf"
                ):
                    print(f"Patching {msbfFileName}")
                    parsedMSBF = parseMSB(eventArc.get_file_data(eventFilePath))

                    if msbfFileName[:-5] in self.eventPatches:
                        self.create_flow_label_to_index_mapping(
                            flowPatches=self.eventPatches[msbfFileName[:-5]],
                            msbf=parsedMSBF,
                        )

                        for patch in self.eventPatches[msbfFileName[:-5]]:
                            if (
                                patch["type"]
                                in FLOW_ADD_VARIATIONS + SWITCH_ADD_VARIATIONS
                            ):
                                self.flow_add(msbf=parsedMSBF, flowAdd=patch)
                            elif patch["type"] == "flowpatch":
                                self.flow_patch(msbf=parsedMSBF, flowPatch=patch)
                            elif patch["type"] == "entryadd":
                                self.entry_add(msbf=parsedMSBF, entryAdd=patch)

                    if msbfFileName[:-5] in self.checkPatches:
                        for eventID, itemID in self.checkPatches[msbfFileName[:-5]]:
                            try:
                                eventID = int(eventID)
                            except ValueError:
                                index = self.flowLabelToIndexMapping.get(eventID, None)
                                if index is None:
                                    print(
                                        f"ERROR: Flow label {eventID} not found when patching event check- File: {msbfFileName} EventID: {eventID} ItemID: {itemID}"
                                    )
                                    continue
                                eventID = index
                            parsedMSBF["FLW3"]["flow"][eventID]["param2"] = itemID
                            parsedMSBF["FLW3"]["flow"][eventID][
                                "param3"
                            ] = 9  # give item command

                    if msbfFileName == "003-ItemGet.msbf":
                        handle_progressive_items(parsedMSBF)

                    eventArc.set_file_data(eventFilePath, buildMSB(parsedMSBF))

            write_bytes_create_dirs(modifiedEventPath, eventArc.build_U8())

    def create_flow_label_to_index_mapping(self, flowPatches, msbf):
        self.flowLabelToIndexMapping = {}
        nextIndex = len(msbf["FLW3"]["flow"])

        for flowAdd in filter(
            lambda patch: patch["type"] in FLOW_ADD_VARIATIONS + SWITCH_ADD_VARIATIONS,
            flowPatches,
        ):
            self.flowLabelToIndexMapping[flowAdd["name"]] = nextIndex
            nextIndex += 1

    def flow_add(self, msbf, flowAdd):
        assert (
            len(msbf["FLW3"]["flow"]) == self.flowLabelToIndexMapping[flowAdd["name"]]
        ), f'index has to be the next value in the flow, expected {len(msbf["FLW3"]["flow"])} got {self.flowLabelToIndexMapping[flowAdd["name"]]}'

        if flowAdd["type"] in DEFAULT_FLOW_TYPE_LOOKUP:
            newFlow = DEFAULT_FLOW_TYPE_LOOKUP[flowAdd["type"]].copy()
        else:
            print(
                f"ERROR: Unhandled type {flowAdd['type']} in flowadd {flowAdd['name']}, did you forget to add type to lookup in patchconstants.py?"
            )
            return

        for property, value in flowAdd["flow"].items():
            if property == "next" and not isinstance(value, int):
                index = self.flowLabelToIndexMapping.get(value, None)
                if index is None:
                    print(
                        f"ERROR: flow label {value} not found in file- patch: {flowAdd['name']}"
                    )
                    continue
                value = index
            if property == "param4" and not isinstance(value, int):
                index = self.textLabelToIndexMapping.get(value, None)
                if index is None:
                    print(
                        f"ERROR: text label {value} not found in file- patch: {flowAdd['name']}"
                    )
                    continue
                value = index
            # handle macro properties
            if property in PARAM1_ALIASES:
                newFlow["param1"] = value
                continue
            if property in PARAM2_ALIASES:
                newFlow["param2"] = value
                continue

            newFlow[property] = value

        if flowAdd["type"] in FLOW_ADD_VARIATIONS:
            msbf["FLW3"]["flow"].append(newFlow)
        elif flowAdd["type"] in SWITCH_ADD_VARIATIONS:
            newFlow["type"] = "switch"
            cases = flowAdd["cases"]
            for i, _ in enumerate(cases):
                value = cases[i]
                if not isinstance(value, int):
                    index = self.flowLabelToIndexMapping.get(value, None)
                    if index is None:
                        print(
                            f"ERROR: flow label {value} not found in file- patch: {flowAdd['name']}"
                        )
                        continue
                    cases[i] = index
            add_msbf_branch(msbf=msbf, switch=newFlow, branchpoints=cases)

    def flow_patch(self, msbf, flowPatch):
        flowObject = msbf["FLW3"]["flow"][flowPatch["index"]]
        for property, value in flowPatch.get("flow", {}).items():
            if property == "next" and not isinstance(value, int):
                index = self.flowLabelToIndexMapping.get(value, None)
                if index is None:
                    print(
                        f"ERROR: flow label {value} not found in file- patch: {flowPatch['name']}"
                    )
                    continue
                value = index
            if property == "param4" and not isinstance(value, int):
                index = self.textLabelToIndexMapping.get(value, None)
                if index is None:
                    print(
                        f"ERROR: text label {value} not found in file- patch: {flowPatch['name']}"
                    )
                    continue
                value = index
            flowObject[property] = value
        if flowObject["type"] == "switch":
            cases = flowPatch.get("cases", None)
            if cases:
                assert len(cases) == flowObject["param4"]
                branchStart = flowObject["param5"]
                for i, case in enumerate(cases):
                    if not isinstance(case, int):
                        case = self.flowLabelToIndexMapping.get(case, None)
                        assert (
                            case is not None
                        ), f"ERROR: flow label {case} not found in file- patch: {flowPatch['name']}"
                    msbf["FLW3"]["branch_points"][branchStart + i] = case

    def entry_add(self, msbf, entryAdd):
        value = entryAdd["entry"]["value"]
        if not isinstance(value, int):
            index = self.flowLabelToIndexMapping.get(value, None)
            if index is None:
                print(
                    f"ERROR: flow label {value} not found in file- patch: {entryAdd['entry']}"
                )
                return
            value = index
        newEntry = {
            "name": entryAdd["entry"]["name"],
            "value": value,
        }
        entryPointHash = entrypoint_hash(entryAdd["entry"]["name"], len(msbf["FEN1"]))
        msbf["FEN1"][entryPointHash].append(newEntry)

    def text_add(self, msbt, textAdd, msbtFileName):
        index = len(msbt["TXT2"])
        self.textLabelToIndexMapping[textAdd["name"]] = index
        msbt["TXT2"].append(
            process_control_sequences(textAdd["text"]).encode("utf-16be")
        )
        # had to add a 0 to the end to satisfy BuildMSB's length requirement, if text adds end up breaking, this may be overwriting a param?
        msbt["ATR1"].append([textAdd.get("unk1", 1), textAdd.get("unk2", 0), 0])
        entryName = "%s:%d" % (msbtFileName[-3:], index)
        newEntry = {
            "name": entryName,
            "value": index,
        }
        entryPointHash = entrypoint_hash(entryName, len(msbt["LBL1"]))
        msbt["LBL1"][entryPointHash].append(newEntry)

    def text_patch(self, msbt, textPatch):
        msbt["TXT2"][textPatch["index"]] = process_control_sequences(
            textPatch["text"]
        ).encode("utf-16be")

    def add_check_patch(self, eventFile, eventID, itemID):
        self.checkPatches[eventFile].append((eventID, itemID))


def make_progressive_item_events(
    msbf, baseItemStart, itemTextIndexes, itemIDs, storyflags
):
    if len(itemTextIndexes) != len(itemIDs) or len(itemTextIndexes) != len(storyflags):
        raise Exception(
            "itemtextIndexes must be the same length as itemIDs and storyflags to make a progressive item"
        )
    flowIndex = len(msbf["FLW3"]["flow"])
    msbf["FLW3"]["flow"][baseItemStart]["next"] = flowIndex

    for index in range(len(itemTextIndexes) - 1, 0, -1):
        branch = DEFAULT_FLOW_TYPE_LOOKUP["checkstoryflag"].copy()
        branch["param2"] = storyflags[index - 1]
        add_msbf_branch(
            msbf=msbf, switch=branch, branchpoints=[(flowIndex + 1), (flowIndex + 3)]
        )

        event = DEFAULT_FLOW_TYPE_LOOKUP["giveitem"].copy()
        event["param2"] = itemIDs[index]
        event["next"] = flowIndex + 2
        msbf["FLW3"]["flow"].append(event)

        event = DEFAULT_FLOW_TYPE_LOOKUP["setstoryflag"].copy()
        event["param2"] = storyflags[index]
        event["next"] = itemTextIndexes[index]
        msbf["FLW3"]["flow"].append(event)

        flowIndex += 3

    event = DEFAULT_FLOW_TYPE_LOOKUP["setstoryflag"].copy()
    event["param2"] = storyflags[0]
    event["next"] = itemTextIndexes[0]
    msbf["FLW3"]["flow"].append(event)


def handle_progressive_items(msbf):
    # progressive mitts
    make_progressive_item_events(
        msbf,
        93,
        [35, 231],
        ITEM_FLAGS[PROGRESSIVE_MITTS],
        ITEM_STORY_FLAGS[PROGRESSIVE_MITTS],
    )
    # progressive swords
    make_progressive_item_events(
        msbf,
        136,
        [77, 608, 75, 78, 74, 73],
        ITEM_FLAGS[PROGRESSIVE_SWORD],
        ITEM_STORY_FLAGS[PROGRESSIVE_SWORD],
    )
    # progressive beetle
    make_progressive_item_events(
        msbf,
        96,
        [38, 178, 177, 176],
        ITEM_FLAGS[PROGRESSIVE_BEETLE],
        ITEM_STORY_FLAGS[PROGRESSIVE_BEETLE],
    )
    # progressive bow
    make_progressive_item_events(
        msbf,
        127,
        [68, 163, 162],
        ITEM_FLAGS[PROGRESSIVE_BOW],
        ITEM_STORY_FLAGS[PROGRESSIVE_BOW],
    )
    # progressive slingshot
    make_progressive_item_events(
        msbf,
        97,
        [39, 237],
        ITEM_FLAGS[PROGRESSIVE_SLINGSHOT],
        ITEM_STORY_FLAGS[PROGRESSIVE_SLINGSHOT],
    )
    # progressive bug net
    make_progressive_item_events(
        msbf,
        20,
        [18, 309],
        ITEM_FLAGS[PROGRESSIVE_BUG_NET],
        ITEM_STORY_FLAGS[PROGRESSIVE_BUG_NET],
    )
    # progressive pouch
    make_progressive_item_events(
        msbf,
        258,
        [254, 253],
        ITEM_FLAGS[PROGRESSIVE_POUCH],
        ITEM_STORY_FLAGS[PROGRESSIVE_POUCH],
    )
    # progressive wallets
    make_progressive_item_events(
        msbf,
        250,
        [246, 245, 244, 255],
        ITEM_FLAGS[PROGRESSIVE_WALLET],
        ITEM_STORY_FLAGS[PROGRESSIVE_WALLET],
    )


def entrypoint_hash(name, entries):
    hash = 0
    for char in name:
        hash = (hash * 0x492 + ord(char)) & 0xFFFFFFFF
    return hash % entries
