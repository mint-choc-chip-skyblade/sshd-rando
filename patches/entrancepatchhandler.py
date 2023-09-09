from logic.entrance import Entrance
from patches.stagepatches import StagePatchHandler


def determine_entrance_patches(
    shuffled_entrances: list[Entrance], stage_patch_handler: StagePatchHandler
):
    for entrance in shuffled_entrances:
        spawn_info = entrance.replaces.spawn_info[0]
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
