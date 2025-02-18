from constants.itemconstants import *
from constants.patchconstants import (
    FLOW_ADD_VARIATIONS,
    LANGUAGE_NAME_TO_FILE_ID,
    SWITCH_ADD_VARIATIONS,
    PARAM1_ALIASES,
    PARAM2_ALIASES,
    DEFAULT_FLOW_TYPE_LOOKUP,
)

from filepathconstants import (
    EVENT_FILE_PATH_TAILS,
    EVENT_PATCHES_PATH,
    VANILLA_EVENT_FILE_PATHS,
)

from collections import defaultdict
from pathlib import Path
from gui.dialogs.dialog_header import (
    get_progress_value_from_range,
    update_progress_value,
)
from logic.settings import SettingGet
from patches.conditionalpatchhandler import ConditionalPatchHandler
from patches.othermods import get_resolved_game_file_path

from sslib.msb import (
    ParsedMsb,
    parse_msb,
    build_msb,
    add_msbf_branch,
    process_control_sequences,
)
from sslib.u8file import U8File
from sslib.utils import write_bytes_create_dirs
from sslib.yaml import yaml_load
from util.text import get_text_data


class EventPatchError(RuntimeError):
    pass


class EventPatchHandler:
    def __init__(self, output_path: Path, other_mods: list[str]):
        self.event_output_paths: dict[str, Path] = {
            tail.name: output_path / tail for tail in EVENT_FILE_PATH_TAILS
        }
        self.event_patches: dict[str, list[dict]] = yaml_load(EVENT_PATCHES_PATH)  # type: ignore
        self.check_patches: dict[str, list[tuple[str, int, int]]] = defaultdict(list)
        self.flow_label_to_index_mapping = {}
        self.text_label_to_index_mapping = {}
        self.other_mods = other_mods

    def append_to_event_patches(self, file_name: str, event_patch: dict):
        if file_name not in self.event_patches:
            self.event_patches[file_name] = []
        self.event_patches[file_name].append(event_patch)

    def find_event(self, file_name: str, event_name: str) -> dict | None:
        return next(
            (
                patch
                for patch in self.event_patches[file_name]
                if patch["name"] == event_name
            ),
            None,
        )

    def handle_event_patches(
        self, onlyif_handler: ConditionalPatchHandler, language: SettingGet
    ):
        language_event_path = VANILLA_EVENT_FILE_PATHS[
            LANGUAGE_NAME_TO_FILE_ID[language.value()]
        ]
        event_paths = tuple(language_event_path.glob("*.arc"))
        total_event_file_count = len(event_paths)

        for event_path in event_paths:
            patched_event_file_count = event_paths.index(event_path)
            progress_value = get_progress_value_from_range(
                99, 7, patched_event_file_count, total_event_file_count
            )
            update_progress_value(progress_value)

            file_name = event_path.parts[-1]
            modified_event_path = (
                self.event_output_paths[LANGUAGE_NAME_TO_FILE_ID[language.value()]]
                / file_name
            )

            resolved_event_path, mod = get_resolved_game_file_path(
                event_path, self.other_mods
            )

            try:
                event_arc = U8File.get_parsed_U8_from_path(resolved_event_path)

                # patch text files first
                for event_file_path in filter(
                    lambda name: name[-1] == "t", event_arc.get_all_paths()
                ):
                    msbt_file_name = event_file_path.split("/")[-1]
                    if msbt_file_name[:-5] in self.event_patches:
                        print(f"Patching {msbt_file_name}")
                        msbt_data = event_arc.get_file_data(event_file_path)

                        if not msbt_data:
                            raise TypeError("Expected type bytes but found None")

                        parsed_msbt = parse_msb(msbt_data)
                        assert len(parsed_msbt["TXT2"]) == len(parsed_msbt["ATR1"])

                        for patch in self.event_patches[msbt_file_name[:-5]]:
                            if statement := patch.get("onlyif", False):
                                if not onlyif_handler.evaluate_onlyif(statement):
                                    continue

                            # handle text patches here
                            if patch["type"] == "textadd":
                                self.text_add(
                                    msbt=parsed_msbt,
                                    text_add=patch,
                                    msbt_file_name=msbt_file_name,
                                    lang=language_event_path.name,
                                )
                            elif patch["type"] == "textpatch":
                                self.text_patch(
                                    msbt=parsed_msbt,
                                    text_patch=patch,
                                    lang=language_event_path.name,
                                )

                        event_arc.set_file_data(event_file_path, build_msb(parsed_msbt))

                for event_file_path in filter(
                    lambda name: name[-1] == "f", event_arc.get_all_paths()
                ):
                    msbf_file_name = event_file_path.split("/")[-1]

                    if (
                        msbf_file_name[:-5] in self.event_patches
                        or msbf_file_name[:-5] in self.check_patches
                        or msbf_file_name == "003-ItemGet.msbf"
                    ):
                        print(f"Patching {msbf_file_name}")

                        if (
                            event_file_data := event_arc.get_file_data(event_file_path)
                        ) is None:
                            raise TypeError(
                                "Event file data incorrect. Expected bytes but found None."
                            )

                        parsed_msbf = parse_msb(event_file_data)

                        if msbf_file_name[:-5] in self.event_patches:
                            self.create_flow_label_to_index_mapping(
                                flow_patches=self.event_patches[msbf_file_name[:-5]],
                                msbf=parsed_msbf,
                                onlyif_handler=onlyif_handler,
                            )

                            for patch in self.event_patches[msbf_file_name[:-5]]:
                                if statement := patch.get("onlyif", False):
                                    if not onlyif_handler.evaluate_onlyif(statement):
                                        continue

                                if (
                                    patch["type"]
                                    in FLOW_ADD_VARIATIONS + SWITCH_ADD_VARIATIONS
                                ):
                                    self.flow_add(msbf=parsed_msbf, flow_add=patch)
                                elif patch["type"] == "flowpatch":
                                    self.flow_patch(msbf=parsed_msbf, flow_patch=patch)
                                elif patch["type"] == "entryadd":
                                    self.entry_add(msbf=parsed_msbf, entry_add=patch)

                        if msbf_file_name[:-5] in self.check_patches:
                            for eventid, itemid, trapid in self.check_patches[
                                msbf_file_name[:-5]
                            ]:
                                if not eventid.isnumeric():
                                    index = self.flow_label_to_index_mapping.get(
                                        eventid, None
                                    )

                                    if index is None:
                                        raise EventPatchError(
                                            f'Flow label "{eventid}" not found when patching event check.\nFile: {msbf_file_name}.\nEventID: {eventid}.\nItemID: {itemid}.'
                                        )

                                    eventid = index

                                eventid = int(eventid)

                                trapbits = 0

                                # +1 allows 0 == not a trap so spawned NPC items don't break
                                if trapid:
                                    trapbits = (254 - trapid) + 1

                                # Inverted so a value of 0 == not a trap
                                # 11 cos signed numbers are bleh
                                itemid |= (trapbits & 0xF) << 11

                                parsed_msbf["FLW3"]["flow"][eventid]["param2"] = itemid

                                # Give item command == 9
                                parsed_msbf["FLW3"]["flow"][eventid]["param3"] = 9

                        if msbf_file_name == "003-ItemGet.msbf":
                            handle_progressive_items(parsed_msbf)

                        event_arc.set_file_data(event_file_path, build_msb(parsed_msbf))
            except Exception as e:
                if mod:
                    e.add_note(
                        f'This was caused by the "{mod}" mod. This mod is currently incompatible with the randomizer.'
                    )
                raise e

            write_bytes_create_dirs(modified_event_path, event_arc.build_U8())

    def create_flow_label_to_index_mapping(
        self,
        flow_patches: list[dict],
        msbf: ParsedMsb,
        onlyif_handler: ConditionalPatchHandler,
    ):
        self.flow_label_to_index_mapping = {}
        next_index = len(msbf["FLW3"]["flow"])

        for flow_add in filter(
            lambda patch: patch["type"] in FLOW_ADD_VARIATIONS + SWITCH_ADD_VARIATIONS,
            flow_patches,
        ):
            if statement := flow_add.get("onlyif", False):
                if not onlyif_handler.evaluate_onlyif(statement):
                    continue

            self.flow_label_to_index_mapping[flow_add["name"]] = next_index
            next_index += 1

    def flow_add(self, msbf: ParsedMsb, flow_add: dict):
        assert (
            len(msbf["FLW3"]["flow"])
            == self.flow_label_to_index_mapping[flow_add["name"]]
        ), f"Index must be the next value in the flow, expected {len(msbf['FLW3']['flow'])} got {self.flow_label_to_index_mapping[flow_add['name']]}"

        if flow_add["type"] in DEFAULT_FLOW_TYPE_LOOKUP:
            new_flow = DEFAULT_FLOW_TYPE_LOOKUP[flow_add["type"]].copy()
        else:
            print(
                f"ERROR: Unhandled type {flow_add['type']} in flowadd {flow_add['name']}, did you forget to add type to lookup in patchconstants.py?"
            )
            return

        for prop, value in flow_add["flow"].items():
            if prop == "next" and not isinstance(value, int):
                flow_index = self.flow_label_to_index_mapping.get(value, None)

                if flow_index is None:
                    raise EventPatchError(
                        f"Flow label \"{value}\" not found in file.\nPatch: {flow_add['name']}."
                    )

                value = flow_index

            if prop == "param4" and not isinstance(value, int):
                flow_index = self.text_label_to_index_mapping.get(value, None)

                if flow_index is None:
                    raise Exception(
                        f"Text with label '{value}' not found.\nError caused by this patch: {flow_add['name']}.\nDid you forget to add a 'textadd' patch for this text?"
                    )

                value = flow_index
            # handle macro properties
            if prop in PARAM1_ALIASES:
                new_flow["param1"] = value
                continue

            if prop in PARAM2_ALIASES:
                new_flow["param2"] = value
                continue

            new_flow[prop] = value

        if flow_add["type"] in FLOW_ADD_VARIATIONS:
            msbf["FLW3"]["flow"].append(new_flow)
        elif flow_add["type"] in SWITCH_ADD_VARIATIONS:
            new_flow["type"] = "switch"
            cases = flow_add["cases"]

            for i, _ in enumerate(cases):
                value = cases[i]

                if not isinstance(value, int):
                    flow_index = self.flow_label_to_index_mapping.get(value, None)
                    if flow_index is None:
                        raise EventPatchError(
                            f"Flow label \"{value}\" not found in file.\nPatch: {flow_add['name']}."
                        )

                    cases[i] = flow_index

            add_msbf_branch(msbf=msbf, switch=new_flow, branchpoints=cases)

    def flow_patch(self, msbf: ParsedMsb, flow_patch: dict):
        flow_object = msbf["FLW3"]["flow"][flow_patch["index"]]

        for prop, value in flow_patch.get("flow", {}).items():
            if prop == "next" and not isinstance(value, int):
                flow_index = self.flow_label_to_index_mapping.get(value, None)

                if flow_index is None:
                    raise EventPatchError(
                        f"Flow label \"{value}\" not found in file.\nPatch: {flow_patch['name']}."
                    )

                value = flow_index

            if prop == "param4" and not isinstance(value, int):
                flow_index = self.text_label_to_index_mapping.get(value, None)

                if flow_index is None:
                    raise Exception(
                        f"Text with label '{value}' not found.\nError caused by this patch: {flow_patch['name']}.\nDid you forget to add a 'textadd' patch for this text?"
                    )

                value = flow_index

            flow_object[prop] = value

        if flow_object["type"] == "switch":
            cases = flow_patch.get("cases", None)

            if cases:
                assert len(cases) == flow_object["param4"]
                branch_start = flow_object["param5"]

                for i, case in enumerate(cases):
                    if not isinstance(case, int):
                        case = self.flow_label_to_index_mapping.get(case, None)

                        if case is None:
                            raise EventPatchError(
                                f"Flow label \"{case}\" not found in file.\nPatch: {flow_patch['name']}."
                            )

                    msbf["FLW3"]["branch_points"][branch_start + i] = case

    def entry_add(self, msbf: ParsedMsb, entry_add: dict):
        value = entry_add["entry"]["value"]

        if not isinstance(value, int):
            flow_index = self.flow_label_to_index_mapping.get(value, None)

            if flow_index is None:
                raise EventPatchError(
                    f"Flow label \"{value}\" not found in file.\nPatch: {entry_add['entry']}."
                )

            value = flow_index

        new_entry = {
            "name": entry_add["entry"]["name"],
            "value": value,
        }
        entry_point_hash = entrypoint_hash(
            entry_add["entry"]["name"], len(msbf["FEN1"])
        )
        msbf["FEN1"][entry_point_hash].append(new_entry)

    def text_add(self, msbt: ParsedMsb, text_add: dict, msbt_file_name: str, lang: str):
        text_index = len(msbt["TXT2"])
        self.text_label_to_index_mapping[text_add["name"]] = text_index
        msbt["TXT2"].append(
            process_control_sequences(get_text_data(text_add["name"]).get(lang)).encode(
                "utf-16be"
            )
        )

        # Had to add a 0 to the end to satisfy BuildMSB's length requirement, if text adds end up breaking, this may be overwriting a param?
        msbt["ATR1"].append(
            [text_add.get("textboxtype", 1), text_add.get("unk2", 0), 0]
        )
        entry_name = "%s:%d" % (msbt_file_name[-3:], text_index)
        new_entry = {
            "name": entry_name,
            "value": text_index,
        }
        entry_point_hash = entrypoint_hash(entry_name, len(msbt["LBL1"]))
        msbt["LBL1"][entry_point_hash].append(new_entry)

    def text_patch(self, msbt: ParsedMsb, text_patch: dict, lang: str):
        msbt["TXT2"][text_patch["index"]] = process_control_sequences(
            get_text_data(text_patch["name"]).get(lang)
        ).encode("utf-16be")

        # Allow patching other textbox data
        current_text_atr1_data = msbt["ATR1"][text_patch["index"]]

        if (textbox_type := text_patch.get("textboxtype", None)) is not None:
            current_text_atr1_data[0] = textbox_type
        if (unk2 := text_patch.get("unk2", None)) is not None:
            current_text_atr1_data[1] = unk2

        msbt["ATR1"][text_patch["index"]] = current_text_atr1_data

    def add_check_patch(self, event_file: str, eventid: str, itemid: int, trapid: int):
        self.check_patches[event_file].append((eventid, itemid, trapid))


def make_progressive_item_events(
    msbf: ParsedMsb,
    base_item_start: int,
    item_text_indexes: tuple,
    itemids: list,
    storyflags: list,
):
    if len(item_text_indexes) != len(itemids) or len(item_text_indexes) != len(
        storyflags
    ):
        raise Exception(
            "item_text_indexes must be the same length as itemids and storyflags to make a progressive item"
        )

    flow_index = len(msbf["FLW3"]["flow"])
    msbf["FLW3"]["flow"][base_item_start]["next"] = flow_index

    for index in range(len(item_text_indexes) - 1, 0, -1):
        branch = DEFAULT_FLOW_TYPE_LOOKUP["checkstoryflag"].copy()
        branch["param2"] = storyflags[index - 1]
        add_msbf_branch(
            msbf=msbf, switch=branch, branchpoints=[(flow_index + 1), (flow_index + 3)]
        )

        event = DEFAULT_FLOW_TYPE_LOOKUP["giveitem"].copy()
        event["param2"] = itemids[index]
        event["next"] = flow_index + 2
        msbf["FLW3"]["flow"].append(event)

        event = DEFAULT_FLOW_TYPE_LOOKUP["setstoryflag"].copy()
        event["param2"] = storyflags[index]
        event["next"] = item_text_indexes[index]
        msbf["FLW3"]["flow"].append(event)

        flow_index += 3

    event = DEFAULT_FLOW_TYPE_LOOKUP["setstoryflag"].copy()
    event["param2"] = storyflags[0]
    event["next"] = item_text_indexes[0]
    msbf["FLW3"]["flow"].append(event)


def handle_progressive_items(msbf: ParsedMsb):
    # Progressive Mitts
    make_progressive_item_events(
        msbf,
        93,
        (35, 231),
        ITEM_ITEMFLAGS[PROGRESSIVE_MITTS],
        ITEM_STORYFLAGS[PROGRESSIVE_MITTS],
    )

    # Progressive Swords
    make_progressive_item_events(
        msbf,
        136,
        (77, 608, 75, 78, 74, 73),
        ITEM_ITEMFLAGS[PROGRESSIVE_SWORD],
        ITEM_STORYFLAGS[PROGRESSIVE_SWORD],
    )

    # Progressive Beetles
    make_progressive_item_events(
        msbf,
        96,
        (38, 178, 177, 176),
        ITEM_ITEMFLAGS[PROGRESSIVE_BEETLE],
        ITEM_STORYFLAGS[PROGRESSIVE_BEETLE],
    )

    # Progressive Bows
    make_progressive_item_events(
        msbf,
        127,
        (68, 163, 162),
        ITEM_ITEMFLAGS[PROGRESSIVE_BOW],
        ITEM_STORYFLAGS[PROGRESSIVE_BOW],
    )

    # Progressive Slingshots
    make_progressive_item_events(
        msbf,
        97,
        (39, 237),
        ITEM_ITEMFLAGS[PROGRESSIVE_SLINGSHOT],
        ITEM_STORYFLAGS[PROGRESSIVE_SLINGSHOT],
    )

    # Progressive Bug Nets
    make_progressive_item_events(
        msbf,
        20,
        (18, 309),
        ITEM_ITEMFLAGS[PROGRESSIVE_BUG_NET],
        ITEM_STORYFLAGS[PROGRESSIVE_BUG_NET],
    )

    # Progressive Pouches
    make_progressive_item_events(
        msbf,
        258,
        (254, 253, 253, 253, 253),
        ITEM_ITEMFLAGS[PROGRESSIVE_POUCH],
        ITEM_STORYFLAGS[PROGRESSIVE_POUCH],
    )

    # Progressive Wallets
    make_progressive_item_events(
        msbf,
        250,
        (246, 245, 244, 255),
        ITEM_ITEMFLAGS[PROGRESSIVE_WALLET],
        ITEM_STORYFLAGS[PROGRESSIVE_WALLET],
    )

    # Song of the Hero parts
    make_progressive_item_events(
        msbf,
        474,
        (472, 471, 475, 477),
        ITEM_ITEMFLAGS[SOTH_PART],
        ITEM_STORYFLAGS[SOTH_PART],
    )


def entrypoint_hash(name: str, entries: int) -> int:
    hash = 0

    for char in name:
        hash = (hash * 0x492 + ord(char)) & 0xFFFFFFFF

    return hash % entries
