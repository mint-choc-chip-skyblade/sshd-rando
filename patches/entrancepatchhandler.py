from gui.dialogs.dialog_header import print_progress_text
from logic.entrance import Entrance
from patches.stagepatchhandler import StagePatchHandler

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logic.world import World


def determine_entrance_patches(
    shuffled_entrances: list[Entrance], stage_patch_handler: StagePatchHandler
):
    print_progress_text("Creating Entrances Patches")

    for entrance in shuffled_entrances:
        spawn_info = entrance.replaces.spawn_info[0]

        if entrance.exit_infos:
            for exit_info in entrance.exit_infos:
                patch_entrance(exit_info, spawn_info, stage_patch_handler)

        if entrance.replaces.secondary_spawn_info:
            spawn_info = entrance.replaces.secondary_spawn_info[0]

        if entrance.secondary_exit_infos:
            for exit_info in entrance.secondary_exit_infos:
                patch_entrance(exit_info, spawn_info, stage_patch_handler)


def patch_entrance(
    exit_info: dict, spawn_info: dict, stage_patch_handler: StagePatchHandler
):
    exit_stage = exit_info["stage"]
    exit_room = exit_info["room"]
    exit_scen_index = exit_info["index"]

    spawn_stage = spawn_info["stage"]
    spawn_layer = spawn_info["layer"]
    spawn_room = spawn_info["room"]
    spawn_entrance = spawn_info["entrance"]

    stage_patch_handler.add_entrance_patch(
        exit_stage,
        exit_scen_index,
        exit_room,
        spawn_stage,
        spawn_layer,
        spawn_room,
        spawn_entrance,
    )


def patch_required_dungeon_text_trigger(
    world: "World", stage_patch_handler: StagePatchHandler
):
    starting_entrance = world.get_entrance("Link's Spawn -> Knight Academy")

    if starting_entrance.replaces is None:
        entrance_info = starting_entrance.spawn_info[0]
    else:
        entrance_info = starting_entrance.replaces.spawn_info[0]

    stage = entrance_info["stage"]
    if stage not in stage_patch_handler.stage_patches:
        stage_patch_handler.stage_patches[stage] = []

    stage_patch_handler.stage_patches[stage].append(
        {
            "name": "Add NpcTke Required Dungeon Text Trigger",
            "type": "objadd",
            "room": entrance_info["room"],
            "layer": 0,
            "id": 0xFF00,
            "objtype": "OBJ",
            "object": {
                "params1": 0xFFFFFF02,  # 02 = subtype make Fi appear
                "params2": 0xFF1FFFFF,
                "anglex": 0xFFFF,  # no (un)trigger sceneflags
                "angley": 0xFFFF,  # trigger area index = -1
                "anglez": 6899,  # entrypoint 006_899
                "id": 0xFF00,
                "name": "NpcTke",
                "trigstoryfid": 226,  #  Always trigger
                "untrigstoryfid": 954,
            },
        }
    )
