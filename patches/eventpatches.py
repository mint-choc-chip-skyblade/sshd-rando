from filepathconstants import EVENT_PATCHES_PATH, EVENT_FILES_PATH, OUTPUT_EVENT_PATH
from patches.patchconstants import (
    FLOW_ADD_VARIATIONS,
    SWITCH_ADD_VARIATIONS,
    PARAM1_ALIASES,
    PARAM2_ALIASES,
    DEFAULT_FLOW_TYPE_LOOKUP,
)
from pathlib import Path

from sslib.msb import parseMSB, buildMSB, add_msbf_branch, process_control_sequences
from sslib.u8file import U8File
from sslib.utils import write_bytes_create_dirs
from sslib.yaml import yaml_load


class EventPatchHandler:
    def __init__(self):
        self.eventPatches = yaml_load(EVENT_PATCHES_PATH)
        self.flowLabelToIndexMapping = {}
        self.textLabels = {}

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
                    parsedMSBT = parseMSB(eventArc.get_file_data(eventFilePath))

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
                if msbfFileName[:-5] in self.eventPatches:
                    parsedMSBF = parseMSB(eventArc.get_file_data(eventFilePath))
                    self.create_flow_label_to_index_mapping(
                        flowPatches=self.eventPatches[msbfFileName[:-5]],
                        msbf=parsedMSBF,
                    )

                    for patch in self.eventPatches[msbfFileName[:-5]]:
                        if patch["type"] in FLOW_ADD_VARIATIONS + SWITCH_ADD_VARIATIONS:
                            self.flow_add(msbf=parsedMSBF, flowAdd=patch)
                        elif patch["type"] == "flowpatch":
                            self.flow_patch(msbf=parsedMSBF, flowPatch=patch)
                        elif patch["type"] == "entryadd":
                            self.entry_add(msbf=parsedMSBF, entryAdd=patch)

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
                index = self.textLabels.get(value, None)
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
                index = self.flowLabelToIndexMapping.get(value, None)
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
                        ), f"ERROR: text label {case} not found in file- patch: {flowPatch['name']}"
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
        self.flowLabelToIndexMapping[textAdd["name"]] = index
        msbt["TXT2"].append(
            process_control_sequences(textAdd["text"]).encode("utf-16be")
        )
        msbt["ATR1"].append([textAdd.get("unk1", 1), textAdd.get("unk2", 0)])
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


def entrypoint_hash(name, entries):
    hash = 0
    for char in name:
        hash = (hash * 0x492 + ord(char)) & 0xFFFFFFFF
    return hash % entries
