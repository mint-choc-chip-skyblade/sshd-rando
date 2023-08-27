from .entrance import *
from .item import Item
from .item_pool import get_complete_item_pool
from .world import World
from .search import Search, SearchMode, all_locations_reachable
from collections import Counter


from typing import TYPE_CHECKING
import yaml
import logging
import random

if TYPE_CHECKING:
    from .world import World

EntrancePool = list[Entrance]
EntrancePools = dict[int, list[Entrance]]


class EntranceShuffleError(RuntimeError):
    pass


def shuffle_world_entrances(world: World, worlds: list[World]):
    set_all_entrances_data(world)
    process_plandomizer_entrances(world)

    pools_to_mix: list[int] = []
    entrance_pools = create_entrance_pools(world, pools_to_mix)
    target_entrance_pools = create_target_pools(entrance_pools)

    # TODO: Set Plandomizer Entrances

    # Shuffle the entrances
    for entrance_type, entrance_pool in entrance_pools.items():
        shuffle_entrance_pool(
            world, worlds, entrance_pool, target_entrance_pools[entrance_type]
        )


def set_all_entrances_data(world: World) -> None:
    with open("data/entrance_shuffle_data.yaml") as entrance_data_file:
        entrance_shuffle_list = yaml.safe_load(entrance_data_file)

        for entrance_data in entrance_shuffle_list:
            # Check that all required fields exist
            for field in ["type", "forward"]:
                if field not in entrance_data:
                    raise EntranceShuffleError(
                        f'"{field}" field is missing in entrance data: {entrance_data}'
                    )

            # Check required fields for forward connection
            for field in ["connection", "exit_infos", "spawn_info"]:
                if field not in entrance_data["forward"]:
                    raise EntranceShuffleError(
                        f'"{field}" field is missing in forward entrance data: {entrance_data["forward"]}'
                    )

                if "return" in entrance_data and field not in entrance_data["return"]:
                    raise EntranceShuffleError(
                        f'"{field}" field is missing in return entrance data: {entrance_data["return"]}'
                    )

            entrance_type = entrance_data["type"]
            forward_entrance = world.get_entrance(
                entrance_data["forward"]["connection"]
            )
            return_entrance = (
                world.get_entrance(entrance_data["return"]["connection"])
                if "return" in entrance_data
                else None
            )

            forward_entrance.type = EntranceType.from_str(entrance_type)
            forward_entrance.exit_infos = entrance_data["forward"]["exit_infos"]
            forward_entrance.spawn_info = entrance_data["forward"]["spawn_info"]
            forward_entrance.secondary_exit_infos = (
                entrance_data["forward"]["secondary_exit_infos"]
                if "secondary_exit_infos" in entrance_data["forward"]
                else None
            )
            forward_entrance.secondary_spawn_info = (
                entrance_data["forward"]["secondary_spawn_info"]
                if "secondary_spawn_info" in entrance_data["forward"]
                else None
            )
            forward_entrance.primary = True
            if return_entrance != None:
                return_entrance.type = entrance_type
                return_entrance.exit_infos = entrance_data["return"]["exit_infos"]
                return_entrance.spawn_info = entrance_data["return"]["spawn_info"]
                return_entrance.secondary_exit_infos = (
                    entrance_data["return"]["secondary_exit_infos"]
                    if "secondary_exit_infos" in entrance_data["return"]
                    else None
                )
                return_entrance.secondary_spawn_info = (
                    entrance_data["return"]["secondary_spawn_info"]
                    if "secondary_spawn_info" in entrance_data["return"]
                    else None
                )
                forward_entrance.bind_two_way(return_entrance)


def process_plandomizer_entrances(world: World) -> None:
    pass


def create_entrance_pools(world: World, pools_to_mix: list[int]) -> EntrancePools:
    # TODO: Mixed pools stuff

    entrance_pools: EntrancePools = {}

    if world.setting("randomize_dungeon_entrances") == "on":
        entrance_pools[EntranceType.DUNGEON] = world.get_shuffleable_entrances(
            EntranceType.DUNGEON, only_primary=True
        )

    set_shuffled_entrances(entrance_pools)

    # TODO: Mixed pools stuff

    return entrance_pools


def create_target_pools(entrance_pools: EntrancePools) -> EntrancePools:
    target_entrance_pools: EntrancePools = {}
    for entrance_type, entrance_pool in entrance_pools.items():
        target_entrance_pools[entrance_type] = assume_entrance_pool(entrance_pool)
    return target_entrance_pools


def shuffle_entrance_pool(
    world: World,
    worlds: list[World],
    entrance_pool: EntrancePool,
    target_entrance_pools: EntrancePool,
    retries: int = 20,
) -> None:
    while retries > 0:
        retries -= 1
        rollbacks = []
        try:
            shuffle_entrances(worlds, entrance_pool, target_entrance_pools, rollbacks)
            for entrance, target in rollbacks:
                confirm_replacement(entrance, target)

        except EntranceShuffleError as error:
            for entrance, target in rollbacks:
                restore_connections(entrance, target)
            logging.getLogger("").debug(
                f"Failed to place all entrances in a pool for {world}. Will retry {retries} more times"
            )
            logging.getLogger("").debug(f"\t{error}")


def shuffle_entrances(
    worlds: list[World],
    entrance_pool: list[Entrance],
    target_entrance_pool: list[Entrance],
    rollbacks: list[tuple[Entrance, Entrance]],
) -> None:
    complete_item_pool = get_complete_item_pool(worlds)
    random.shuffle(entrance_pool)

    for entrance in entrance_pool:
        if entrance.connected_area is not None:
            continue
        random.shuffle(target_entrance_pool)

        for target in target_entrance_pool:
            if target.connected_area is None:
                continue

            if replace_entrance(
                worlds, entrance, target, rollbacks, complete_item_pool
            ):
                break

        if entrance.connected_area is None:
            raise EntranceShuffleError(
                f"No more valid entrances to replace {entrance} in {entrance.world}"
            )


def replace_entrance(
    worlds: list[World],
    entrance: Entrance,
    target: Entrance,
    rollbacks: list[tuple[Entrance, Entrance]],
    complete_item_pool: Counter[Item],
) -> None:
    try:
        check_entrances_compatibility(entrance, target)
        change_connections(entrance, target)
        validate_world(entrance.world, worlds, entrance, complete_item_pool)
        rollbacks.append((entrance, target))
        return True
    except EntranceShuffleError as error:
        logging.getLogger("").debug(
            f"Failed to connect {entrance} to {target} (Reason: {error}) {entrance.world}"
        )
        if entrance.connected_area:
            restore_connections(entrance, target)
    return False


def assume_entrance_pool(entrance_pool: EntrancePool) -> EntrancePool:
    assumed_pool: EntrancePool = []
    for entrance in entrance_pool:
        assumed_forward = entrance.assume_reachable()
        if entrance.reverse != None and not entrance.decoupled:
            assumed_return = entrance.reverse.assume_reachable()
            assumed_forward.bind_two_way(assumed_return)
        assumed_pool.append(assumed_forward)
    return assumed_pool


def set_shuffled_entrances(entrance_pools: EntrancePools) -> None:
    for pool in entrance_pools.values():
        for entrance in pool:
            entrance.shuffled = True


def check_entrances_compatibility(entrance: Entrance, target: Entrance) -> None:
    pass


def change_connections(entrance: Entrance, target: Entrance) -> None:
    entrance.connect(target.disconnect())
    entrance.replaces = target.replaces
    if entrance.reverse:
        target.replaces.reverse.connect(entrance.reverse.assumed.disconnect())
        target.replaces.reverse.replaces = entrance.reverse


def restore_connections(entrance: Entrance, target: Entrance) -> None:
    target.connect(entrance.disconnect())
    entrance.replaces = None
    if entrance.reverse:
        entrance.reverse.assumed.connect(target.replaces.reverse.disconnect())
        target.replaces.reverse.replaces = None


def confirm_replacement(entrance: Entrance, target: Entrance) -> None:
    delete_target_entrance(target)
    logging.getLogger("").debug(
        f"Connected {entrance} to {entrance.connected_area} [{entrance.world}]"
    )
    if entrance.reverse:
        replaced_reverse = target.replaces.reverse
        delete_target_entrance(entrance.reverse.assumed)
        logging.getLogger("").debug(
            f"Connected {replaced_reverse} to {replaced_reverse.connected_area}"
        )


def delete_target_entrance(target: Entrance) -> None:
    if target.connected_area is not None:
        target.disconnect()
    if target.parent_area is not None:
        target.parent_area.exits.remove(target)
        target.parent_area = None


def validate_world(
    world: World, worlds: list[World], entrance: Entrance, item_pool: Counter[Item]
) -> None:
    # Validate that the world is still beatable
    if not all_locations_reachable(worlds, item_pool):
        raise EntranceShuffleError(f"Not all locations are reachable!")
