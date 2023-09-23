from .entrance import *
from .item import Item
from .item_pool import get_complete_item_pool
from .world import World
from .search import Search, SearchMode, all_locations_reachable
from collections import Counter, OrderedDict


from typing import TYPE_CHECKING
import yaml
import logging
import random

if TYPE_CHECKING:
    from .world import World

EntrancePool = list[Entrance]
EntrancePools = OrderedDict[str, list[Entrance]]


class EntranceShuffleError(RuntimeError):
    pass


def shuffle_world_entrances(world: World, worlds: list[World]):
    set_all_entrances_data(world)

    entrance_pools = create_entrance_pools(world)
    target_entrance_pools = create_target_pools(entrance_pools)

    # Set plando entrances first
    set_plandomizer_entrances(world, worlds, entrance_pools, target_entrance_pools)

    # Shuffle the entrances
    for entrance_type, entrance_pool in entrance_pools.items():
        shuffle_entrance_pool(
            world, worlds, entrance_pool, target_entrance_pools[entrance_type]
        )


def set_all_entrances_data(world: World) -> None:
    with open("data/entrance_shuffle_data.yaml") as entrance_data_file:
        entrance_shuffle_list = yaml.safe_load(entrance_data_file)

        # Keep track of which double door entrances are together
        coupled_doors: dict[str, list[Entrance]] = {}

        for entrance_data in entrance_shuffle_list:
            # Check that all required fields exist
            for field in ["type", "forward"]:
                if field not in entrance_data:
                    raise EntranceShuffleError(
                        f'"{field}" field is missing in entrance data: {entrance_data}'
                    )

            # Check required fields for forward connection
            for field in ["connection", "spawn_info"]:
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

            # Add double door entrances to their respective tag group
            if "door_couple_tag" in entrance_data:
                tag = entrance_data["door_couple_tag"]
                if tag not in coupled_doors:
                    coupled_doors[tag] = []
                coupled_doors[tag].extend([forward_entrance, return_entrance])

            forward_entrance.type = entrance_type
            forward_entrance.original_type = entrance_type
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
            if "can_start_at" in entrance_data["forward"]:
                forward_entrance.can_start_at = entrance_data["forward"]["can_start_at"]
            forward_entrance.primary = True
            forward_entrance.sort_priority = Entrance.sort_counter
            Entrance.sort_counter += 1
            if return_entrance != None:
                return_entrance.type = entrance_type
                return_entrance.original_type = entrance_type
                return_entrance.exit_infos = (
                    entrance_data["return"]["exit_infos"]
                    if "exit_infos" in entrance_data["return"]
                    else None
                )
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
                if "can_start_at" in entrance_data["return"]:
                    return_entrance.can_start_at = entrance_data["return"][
                        "can_start_at"
                    ]
                return_entrance.sort_priority = Entrance.sort_counter
                Entrance.sort_counter += 1
                forward_entrance.bind_two_way(return_entrance)

        # If double doors are to be coupled, add the coupled door's
        # exit infos to the main door, remove the coupled door entrance,
        # and rename the main door to be more general
        if world.setting("decouple_double_doors") == "off":
            for doors in coupled_doors.values():
                while doors:
                    main_door = doors.pop()
                    coupled_door = next(
                        iter(
                            [
                                door
                                for door in doors
                                if door.primary == main_door.primary
                            ]
                        )
                    )

                    # Add the coupled door's exit_infos to the main door
                    main_door.exit_infos.extend(coupled_door.exit_infos)

                    # Completely remove the coupled door from the world graph
                    doors.remove(coupled_door)
                    coupled_door.connected_area.entrances.remove(coupled_door)
                    coupled_door.parent_area.exits.remove(coupled_door)

                    # Change the main door's name to be more general
                    main_door.original_name = (
                        main_door.original_name.replace(" North", "")
                        .replace(" South", "")
                        .replace(" East", "")
                        .replace(" West", "")
                    )


def create_entrance_pools(world: World) -> EntrancePools:
    entrance_pools: EntrancePools = {}

    # The order we check the types is the order they'll be shuffled in.
    # This matters because we generally want to shuffle entrances types
    # near the "outside" of the world graph first (dungeons, trial gates),
    # and then types that are farther "inside" aftrewards (interiors, overworld).
    # This reduces the chance of a complete failure of the entrance shuffle
    # algorithm
    if world.setting("random_starting_spawn") != "vanilla":
        entrance_pools["Spawn"] = world.get_shuffleable_entrances(
            "Spawn", only_primary=False
        )

    if world.setting("randomize_dungeon_entrances") == "on":
        entrance_pools["Dungeon"] = world.get_shuffleable_entrances(
            "Dungeon", only_primary=True
        )
        if world.setting("decouple_entrances") == "on":
            entrance_pools["Dungeon Reverse"] = [
                entrance.reverse for entrance in entrance_pools["Dungeon"]
            ]

    if world.setting("randomize_trial_gate_entrances") == "on":
        entrance_pools["Trial Gate"] = world.get_shuffleable_entrances(
            "Trial Gate", only_primary=True
        )
        # Don't enable this until trials stay permanently open
        # if world.setting("decouple_entrances") == "on":
        #     entrance_pools["Trial Gate Reverse"] = [entrance.reverse for entrance in entrance_pools["Trial Gate"]]

    if world.setting("randomize_door_entrances") == "on":
        entrance_pools["Door"] = world.get_shuffleable_entrances(
            "Door", only_primary=True
        )
        if world.setting("decouple_entrances") == "on":
            entrance_pools["Door Reverse"] = [
                entrance.reverse for entrance in entrance_pools["Door"]
            ]

    if world.setting("randomize_interior_entrances") == "on":
        entrance_pools["Interior"] = world.get_shuffleable_entrances(
            "Interior", only_primary=True
        )
        if world.setting("decouple_entrances") == "on":
            entrance_pools["Interior Reverse"] = [
                entrance.reverse for entrance in entrance_pools["Interior"]
            ]

    if world.setting("randomize_overworld_entrances") == "on":
        exclude_overworld_reverse = (
            any("Overworld" in pool for pool in world.setting_map.mixed_entrance_pools)
            and world.setting("decouple_entrances") == "off"
        )
        entrance_pools["Overworld"] = world.get_shuffleable_entrances(
            "Overworld", only_primary=exclude_overworld_reverse
        )

    set_shuffled_entrances(entrance_pools)

    # Set appropriately decoupled types as decoupled
    potentially_decoupled_types = {"Dungeon", "Door", "Interior", "Overworld"}
    if world.setting("decouple_entrances") == "on":
        for type_name in potentially_decoupled_types:
            for entrance_type in [type_name, type_name + " Reverse"]:
                if entrance_type in entrance_pools:
                    for entrance in entrance_pools[entrance_type]:
                        entrance.decoupled = True

    # The mixed pools expect a list of lists, if just a list
    # of types was passed in, then nest it into another list
    mixed_pool_list = []
    if world.setting_map.mixed_entrance_pools:
        if type(world.setting_map.mixed_entrance_pools[0]) is list:
            mixed_pool_list = world.setting_map.mixed_entrance_pools
        else:
            mixed_pool_list = [world.setting_map.mixed_entrance_pools]

    # Set mixed pools
    for i, pool in enumerate(mixed_pool_list):
        # The pool should have at least two types that are being shuffled
        # If the pool has less than two types or some of the specified types
        # aren't being shuffled, then ignore the pool
        if (
            len(
                [
                    entrance_type
                    for entrance_type in pool
                    if entrance_type in entrance_pools
                ]
            )
            < 2
        ):
            continue
        pool_name = "Mixed Pool " + str(i + 1)
        entrance_pools[pool_name] = []
        # For each entrance type, add it to the mixed pool and then
        # delete the original pool
        for type_str in pool:
            for entrance_type in [type_str, type_str + " Reverse"]:
                if entrance_type in entrance_pools:
                    for entrance in entrance_pools[entrance_type]:
                        entrance.type = pool_name
                        entrance_pools[pool_name].append(entrance)
                    del entrance_pools[entrance_type]

    # If Interior or Overworld entrances are still being shuffled
    # make sure we move them to the back of the pools so they still
    # get shuffled last after the mixed pools
    if world.setting("decouple_entrances") == "off":
        for entrance_type in ["Interior", "Overworld"]:
            if entrance_type in entrance_pools:
                # Pop it out of the OrderedDict and then add it
                # back in on the end
                pool = entrance_pools.pop(entrance_type)
                entrance_pools[entrance_type] = pool

    return entrance_pools


def create_target_pools(entrance_pools: EntrancePools) -> EntrancePools:
    target_entrance_pools: EntrancePools = {}
    for entrance_type, entrance_pool in entrance_pools.items():
        if entrance_type == "Spawn":
            target_entrance_pools[entrance_type] = create_spawn_target_pool(
                entrance_pool[0].world
            )
            for entrance in entrance_pool:
                entrance.disconnect()
        else:
            target_entrance_pools[entrance_type] = assume_entrance_pool(entrance_pool)
    return target_entrance_pools


def create_spawn_target_pool(world: World) -> list[Entrance]:
    # Determine all possible starting targets depending on settings
    target_pool: list[Entrance] = []
    starting_spawn_value = world.setting("random_starting_spawn").value()
    match starting_spawn_value:
        case "vanilla":
            assert False  # Should never be hit
        case "bird_statues":
            for entrance_type in ["Bird Statue", "Spawn"]:
                for entrance in world.get_shuffleable_entrances(entrance_type):
                    target_pool.append(entrance.get_new_target())
        case "any_surface_region":
            banned_spawn_regions = {
                "Knight Academy",
                "Upper Skyloft",
                "Central Skyloft",
                "Skyloft Village",
                "Bazaar",
                "Batreaux",
                "The Sky",
                "The Thunderhead",
            }
            for entrance_type in ["Door", "Interior", "Overworld", "Spawn"]:
                for entrance in world.get_shuffleable_entrances(entrance_type):
                    # Ignore any sky/skyloft entrances
                    if (
                        entrance.can_start_at
                        and not entrance.parent_area.get_regions().intersection(
                            banned_spawn_regions
                        )
                    ):
                        target_pool.append(entrance.get_new_target())
        case "anywhere":
            for entrance_type in [
                "Dungeon",
                "Trial Gate",
                "Door",
                "Interior",
                "Overworld",
                "Bird Statue",
                "Spawn",
            ]:
                for entrance in world.get_shuffleable_entrances(entrance_type):
                    if entrance.can_start_at:
                        target_pool.append(entrance.get_new_target())
        case _:
            raise EntranceShuffleError(
                f"Unknown value for random starting spawn: '{starting_spawn_value}'"
            )

    # Don't assume we have access to the random spawn targets
    for entrance in target_pool:
        entrance.requirement.type = RequirementType.IMPOSSIBLE

    return target_pool


def set_plandomizer_entrances(
    world: World,
    worlds: list[World],
    entrance_pools: EntrancePools,
    target_entrance_pools: EntrancePools,
):
    logging.getLogger("").debug("Now Placing plandomized entrances")
    item_pool = get_complete_item_pool(worlds)

    # Attempt to connect each plandomized entrance
    for entrance, target in world.plandomizer_entrances.items():
        entrance_to_connect = entrance
        target_to_connect = target
        entrance_type = entrance.type

        if entrance_type == "None":
            raise EntranceShuffleError(
                f"{entrance} is not an entrance that can be shuffled"
            )
        if target_to_connect.type == "None":
            raise EntranceShuffleError(
                f"{target} is not an entrance that can be shuffled"
            )

        # Check to make sure this type of entrance is being shuffled
        if entrance_type not in entrance_pools:
            # Check if its reverse is being shuffled if decoupled entrances are off
            if (
                not entrance.decoupled
                and entrance.reverse
                and entrance.reverse.type in entrance_pools
            ):
                # If this entrance is already connected, throw an error
                if entrance.connected_area is not None:
                    raise EntranceShuffleError(
                        f"{entrance} has already been connected. If you previously set the reverse of this entrance, you'll need to enabled the Decouple Entrances setting to plandomize this one also"
                    )

                entrance_to_connect = entrance.reverse
                target_to_connect = target.reverse
                entrance_type = entrance_to_connect.type
            else:
                raise EntranceShuffleError(
                    f"Entrance {entrance}'s type is not being shuffled and thus can't be plandomized"
                )

        # Get the appropriate pools
        entrance_pool = entrance_pools[entrance_type]
        target_pool = target_entrance_pools[entrance_type]

        if entrance_to_connect in entrance_pool:
            valid_target_found = False
            for target_entrance in target_pool:
                if target_to_connect == target_entrance.replaces:
                    replace_entrance(
                        worlds, entrance_to_connect, target_entrance, [], item_pool
                    )
                    valid_target_found = True
                    entrance_pool.remove(entrance_to_connect)
                    target_pool.remove(target_entrance)
                    confirm_replacement(entrance_to_connect, target_entrance)
                    break

            if not valid_target_found:
                raise EntranceShuffleError(
                    f"Entrance {target_to_connect} is not a valid target for {entrance}"
                )
        else:
            raise EntranceShuffleError(
                f"Entrance {entrance}'s type is not being shuffled and thus can't be plandomized"
            )

    logging.getLogger("").debug("All plandomizer entrances have been placed")


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
            for target in target_entrance_pools:
                delete_target_entrance(target)
            return

        except EntranceShuffleError as error:
            for entrance, target in rollbacks:
                restore_connections(entrance, target)
            logging.getLogger("").debug(
                f"Failed to place all entrances in a pool for {world}. Will retry {retries} more times"
            )
            logging.getLogger("").debug(f"\t{error}")

    raise EntranceShuffleError("Ran out of retries when shuffling entrances")


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
            f"Failed to connect {entrance} to {target.original_name} (Reason: {error}) {entrance.world}"
        )
        if entrance.connected_area:
            restore_connections(entrance, target)
    return False


def assume_entrance_pool(entrance_pool: EntrancePool) -> EntrancePool:
    assumed_pool: EntrancePool = []
    for entrance in entrance_pool:
        assumed_forward = entrance.assume_reachable()
        if entrance.reverse and not entrance.decoupled:
            assumed_return = entrance.reverse.assume_reachable()
            assumed_forward.bind_two_way(assumed_return)
        assumed_pool.append(assumed_forward)
    return assumed_pool


def set_shuffled_entrances(entrance_pools: EntrancePools) -> None:
    for pool in entrance_pools.values():
        for entrance in pool:
            entrance.shuffled = True
            if entrance.reverse:
                entrance.reverse.shuffled = True


def check_entrances_compatibility(entrance: Entrance, target: Entrance) -> None:
    if entrance.reverse and entrance.reverse == target.replaces:
        raise EntranceShuffleError(f"Attempted self-connection")


def change_connections(entrance: Entrance, target: Entrance) -> None:
    entrance.connect(target.disconnect())
    entrance.replaces = target.replaces
    if entrance.reverse and not entrance.decoupled:
        target.replaces.reverse.connect(entrance.reverse.assumed.disconnect())
        target.replaces.reverse.replaces = entrance.reverse


def restore_connections(entrance: Entrance, target: Entrance) -> None:
    target.connect(entrance.disconnect())
    entrance.replaces = None
    if entrance.reverse and not entrance.decoupled:
        entrance.reverse.assumed.connect(target.replaces.reverse.disconnect())
        target.replaces.reverse.replaces = None


def confirm_replacement(entrance: Entrance, target: Entrance) -> None:
    delete_target_entrance(target)
    logging.getLogger("").debug(
        f"Connected {entrance} to {entrance.connected_area} [{entrance.world}]"
    )
    if entrance.reverse and not entrance.decoupled:
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
