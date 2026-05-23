from constants.itemnames import AMBER_TABLET, EMERALD_TABLET, RUBY_TABLET
from filepathconstants import BIRD_STATUE_DATA_PATH, ENTRANCE_SHUFFLE_DATA_PATH
from .entrance import *
from .item import Item
from .item_pool import get_complete_item_pool
from .world import World
from .search import Search, SearchMode, all_logic_satisfied
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

    # Then shuffle entrance pools with non-assumed target pools
    shuffle_non_assumed_entrance_pools(
        world, worlds, entrance_pools, target_entrance_pools
    )

    # Then shuffle the rest of the entrances
    for entrance_type, entrance_pool in entrance_pools.items():
        shuffle_entrance_pool(
            world, worlds, entrance_pool, target_entrance_pools[entrance_type]
        )

    # Unset goal locations that aren't reachable so they can't be chosen
    search = Search(
        SearchMode.ALL_LOCATIONS_REACHABLE, worlds, get_complete_item_pool(worlds)
    )
    search.search_worlds()
    for world in worlds:
        for location in world.get_all_item_locations():
            if location.is_goal_location and location not in search.visited_locations:
                location.is_goal_location = False
                logging.getLogger("").debug(
                    f"Removing {location} as goal location due to it being unreachable"
                )


def set_all_entrances_data(world: World) -> None:
    with open(ENTRANCE_SHUFFLE_DATA_PATH, encoding="utf-8") as entrance_data_file:
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
            forward_entrance.exit_infos = entrance_data["forward"].get(
                "exit_infos", None
            )
            forward_entrance.spawn_info = entrance_data["forward"]["spawn_info"]
            forward_entrance.secondary_exit_infos = entrance_data["forward"].get(
                "secondary_exit_infos", None
            )
            forward_entrance.secondary_spawn_info = entrance_data["forward"].get(
                "secondary_spawn_infos", None
            )
            forward_entrance.can_start_at = entrance_data["forward"].get(
                "can_start_at", True
            )
            if alias := entrance_data["forward"].get("alias", None):
                forward_entrance.alias = alias
            forward_entrance.primary = True
            forward_entrance.sort_priority = Entrance.sort_counter
            if conditional_vanilla_connections := entrance_data["forward"].get(
                "conditional_vanilla_connections", None
            ):
                forward_entrance.conditional_vanilla_connections.extend(
                    [world.get_entrance(e) for e in conditional_vanilla_connections]
                )
            Entrance.sort_counter += 1
            if return_entrance != None:
                return_entrance.type = entrance_type
                return_entrance.original_type = entrance_type
                return_entrance.exit_infos = entrance_data["return"].get(
                    "exit_infos", None
                )
                return_entrance.spawn_info = entrance_data["return"].get(
                    "spawn_info", None
                )
                return_entrance.secondary_exit_infos = entrance_data["return"].get(
                    "secondary_exit_infos", None
                )
                return_entrance.secondary_spawn_info = entrance_data["return"].get(
                    "secondary_spawn_info", None
                )
                return_entrance.can_start_at = entrance_data["return"].get(
                    "can_start_at", True
                )
                if alias := entrance_data["return"].get("alias", None):
                    return_entrance.alias = alias
                return_entrance.sort_priority = Entrance.sort_counter
                Entrance.sort_counter += 1
                if conditional_vanilla_connections := entrance_data["return"].get(
                    "conditional_vanilla_connections", None
                ):
                    return_entrance.conditional_vanilla_connections.extend(
                        [world.get_entrance(e) for e in conditional_vanilla_connections]
                    )
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

                    # Change the main door's name and alias to be more general
                    main_door.original_name = (
                        main_door.original_name.replace(" North", "")
                        .replace(" South", "")
                        .replace(" East", "")
                        .replace(" West", "")
                    )
                    main_door.alias = (
                        main_door.alias.replace(" North", "")
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

    if world.setting("random_starting_statues") == "on":
        # These need to be separate pools since they have different
        # target entrances
        entrance_pools["Faron Region Entrance"] = world.get_shuffleable_entrances(
            "Faron Region Entrance", only_primary=False
        )
        entrance_pools["Eldin Region Entrance"] = world.get_shuffleable_entrances(
            "Eldin Region Entrance", only_primary=False
        )
        entrance_pools["Lanayru Region Entrance"] = world.get_shuffleable_entrances(
            "Lanayru Region Entrance", only_primary=False
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
        if world.setting("decouple_entrances") == "on":
            entrance_pools["Trial Gate Reverse"] = [
                entrance.reverse for entrance in entrance_pools["Trial Gate"]
            ]

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

            # Push the forward interior pool back behind the interior reverse pool in the shuffle order.
            # We do this because the target entrance of Waterfall Cave -> Skyloft Past Waterfall Cave
            # is finicky and requires Night access to ensure all it's locations are reachable.
            # By placing it after the forward interior entrances, we significantly reduce the
            # chances of a placement failure.
            interior_pool = entrance_pools.pop("Interior")
            entrance_pools["Interior"] = interior_pool

    if world.setting("randomize_overworld_entrances") == "on":
        # Normally we allow any overworld entrances to link together.
        # However, if overworld entrances are mixed with other entrance types
        # that expect to only match with exclusively primary or non-primary
        # entrances, we have to separate overworld entrances by their primary/
        # non-primary distinction to fit with the other entrances
        exclude_overworld_reverse = (
            any("Overworld" in pool for pool in world.setting_map.mixed_entrance_pools)
            and world.setting("decouple_entrances") == "off"
        )
        entrance_pools["Overworld"] = world.get_shuffleable_entrances(
            "Overworld", only_primary=exclude_overworld_reverse
        )

    # Match pool types
    for type, pool in entrance_pools.items():
        for entrance in pool:
            entrance.type = type

    set_shuffled_entrances(entrance_pools)

    # Set appropriately decoupled types as decoupled
    potentially_decoupled_types = {
        "Dungeon",
        "Door",
        "Interior",
        "Overworld",
        "Trial Gate",
    }
    if world.setting("decouple_entrances") == "on":
        for type_name in potentially_decoupled_types:
            for entrance_type in [type_name, type_name + " Reverse"]:
                if entrance_type in entrance_pools:
                    for entrance in entrance_pools[entrance_type]:
                        entrance.decoupled = True

    mixed_pool_list = world.setting_map.mixed_entrance_pools

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
        elif entrance_type.endswith(" Region Entrance"):
            target_entrance_pools[entrance_type] = create_starting_statue_target_pool(
                region=entrance_type.replace(" Region Entrance", ""),
                world=entrance_pool[0].world,
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
    banned_spawn_regions: set[str] = set()
    banned_spawn_pillars: set[str] = set()
    shuffled_entrance_types: set[str] = set()

    def can_start_at_entrance(entrance: Entrance):
        if (
            entrance.can_start_at
            and not entrance.parent_area.get_regions().intersection(
                banned_spawn_regions
            )
            and (
                entrance.type != "Bird Statue"
                or entrance.original_name.split(" -> ")[0] not in banned_spawn_pillars
            )
        ):
            return True
        return False

    if world.setting("limit_starting_spawn") == "on":
        if world.starting_item_pool[world.get_item(EMERALD_TABLET)] == 0:
            banned_spawn_pillars.add("Faron Pillar")
            banned_spawn_regions |= {
                "Sealed Grounds",
                "Faron Woods",
                "Lake Floria",
                "Great Tree",
            }
        if world.starting_item_pool[world.get_item(RUBY_TABLET)] == 0:
            banned_spawn_pillars.add("Eldin Pillar")
            banned_spawn_regions |= {
                "Eldin Volcano",
                "Mogma Turf",
                "Volcano Summit",
                "Bokoblin Base",
            }
        if world.starting_item_pool[world.get_item(AMBER_TABLET)] == 0:
            banned_spawn_pillars.add("Lanayru Pillar")
            banned_spawn_regions |= {
                "Lanayru Mine",
                "Lanayru Desert",
                "Temple of Time",
                "Lanayru Caves",
                "Ancient Harbour",
                "Lanayru Sand Sea",
                "Lanayru Gorge",
            }

    match starting_spawn_value:
        case "vanilla":
            assert False  # Should never be hit
        case "bird_statues":
            shuffled_entrance_types |= {"Bird Statue", "Spawn"}
        case "any_surface_region":
            banned_spawn_regions |= {
                "Knight Academy",
                "Upper Skyloft",
                "Central Skyloft",
                "Skyloft Village",
                "Bazaar",
                "Batreaux's House",
                "Sky",
                "Inside the Thunderhead",
            }
            shuffled_entrance_types |= {"Door", "Interior", "Overworld", "Spawn"}
        case "anywhere":
            shuffled_entrance_types |= {
                "Trial Gate",
                "Door",
                "Interior",
                "Overworld",
                "Bird Statue",
                "Spawn",
            }
        case _:
            raise EntranceShuffleError(
                f"Unknown value for random starting spawn: '{starting_spawn_value}'"
            )

    for entrance_type in sorted(shuffled_entrance_types):
        for entrance in world.get_shuffleable_entrances(entrance_type):
            if can_start_at_entrance(entrance):
                new_target_entrance = entrance.get_new_target()
                target_pool.append(new_target_entrance)

                # Don't assume we have access to the random spawn targets
                new_target_entrance.requirement.set_as_impossible()

    return target_pool


def create_starting_statue_target_pool(region: str, world: World) -> list[Entrance]:
    target_pool: list[Entrance] = []
    for entrance in world.get_shuffleable_entrances("Bird Statue"):
        if (
            entrance.can_start_at
            and entrance.original_name != "Eldin Pillar -> Inside the Volcano Statue"
            and entrance.original_name.startswith(region)
        ):
            new_target_entrance = entrance.get_new_target()
            target_pool.append(new_target_entrance)

            # Don't assume we have access to any of the pillar targets
            new_target_entrance.requirement.set_as_impossible()

    return target_pool


def set_plandomizer_entrances(
    world: World,
    worlds: list[World],
    entrance_pools: EntrancePools,
    target_entrance_pools: EntrancePools,
):
    logging.getLogger("").debug("Now Placing plandomized entrances")
    item_pool = get_complete_item_pool(worlds)

    # Check to see if we'll have any disconnected, non-assumed entrances while
    # setting plandomizer entrances. If we do, then we can't validate the world
    # while setting plandomzier entrances since the non-assumed entrances aren't set
    unset_non_assumed_entrances: bool = any(
        [
            True
            for type, pool in entrance_pools.items()
            if type in Entrance.NON_ASSUMED_ENTRANCE_TYPES
            for entrance in pool
            if entrance not in world.plandomizer.entrances
        ]
    )

    # Attempt to connect each plandomized entrance
    for entrance, target in world.plandomizer.entrances.items():
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
                    f"Entrance {entrance}'s type ({entrance.type}) is not being shuffled and thus can't be plandomized"
                )

        # Get the appropriate pools
        entrance_pool = entrance_pools[entrance_type]
        target_pool = target_entrance_pools[entrance_type]

        if entrance_to_connect.reverse in entrance_pool:
            entrance_to_connect = entrance_to_connect.reverse
            target_to_connect = target_to_connect.reverse

        if entrance_to_connect in entrance_pool:
            valid_target_found = False
            for target_entrance in target_pool:
                if target_to_connect == target_entrance.replaces:
                    check_entrances_compatibility(entrance_to_connect, target_entrance)
                    change_connections(entrance_to_connect, target_entrance)
                    if not unset_non_assumed_entrances:
                        validate_world(world, worlds, entrance_to_connect, item_pool)
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
                f"Entrance {entrance}'s type ({entrance.type}) is not being shuffled and thus can't be plandomized"
            )

    logging.getLogger("").debug("All plandomizer entrances have been placed")


def shuffle_non_assumed_entrance_pools(
    world: World,
    worlds: list[World],
    entrance_pools: EntrancePools,
    target_entrance_pools: EntrancePools,
):
    non_assumed_entrances = {
        pool[0]: target_entrance_pools[type]
        for type, pool in entrance_pools.items()
        if len(pool) > 0 and type in Entrance.NON_ASSUMED_ENTRANCE_TYPES
    }

    item_pool = get_complete_item_pool(worlds)

    # The idea here is we want to try shuffling all the non-assumed entrances
    # at the same time since we can't validate the world after each one individually
    # (That would require assuming access to entrances which we can't guarantee access to)
    # Realistically, this should never take more than 1 or 2 tries unless there's some wacky
    # plandomizer stuff going on

    retries = 20
    while retries > 0:
        rollbacks = []
        # Connect each entrance to a random target in its pool
        for entrance, targets in non_assumed_entrances.items():
            random_target = random.choice(targets)
            rollbacks.append((entrance, random_target))
            change_connections(entrance, random_target)

        try:
            # Then try to validate the world
            validate_world(world, worlds, None, item_pool)
            # If we're successful, we can confirm our replacements
            # and break out of the loop
            for entrance, target in rollbacks:
                confirm_replacement(entrance, target)
            break
        except EntranceShuffleError as e:
            # If we're unsuccessful, restore the invalid connections
            # and try again
            logging.getLogger("").debug(
                f"Failed to connect non-assumed entrances. Reason {e}"
            )
            retries -= 1
            for entrance, target in rollbacks:
                restore_connections(entrance, target)

    if retries <= 0:
        raise EntranceShuffleError(
            "Ran out of retries when attempting to place non-assumed entrances"
        )

    # Remove the non-assumed types from the original entrance pools
    for type in Entrance.NON_ASSUMED_ENTRANCE_TYPES:
        entrance_pools.pop(type, None)


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

    raise EntranceShuffleError(
        "Ran out of retries when shuffling entrances. If you see this error, try using a few different seeds to see if any generate successfully"
    )


def shuffle_entrances(
    worlds: list[World],
    entrance_pool: list[Entrance],
    target_entrance_pool: list[Entrance],
    rollbacks: list[tuple[Entrance, Entrance]],
) -> None:
    complete_item_pool = get_complete_item_pool(worlds)
    random.shuffle(entrance_pool)

    for entrance in entrance_pool:
        # If this entrance is already connected, then continue on to the next one
        if entrance.connected_area is not None:
            continue
        random.shuffle(target_entrance_pool)

        for target in target_entrance_pool:
            # If this target has already been used, try the next one
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
            f"Failed to connect {entrance} to {target.replaces.original_name} (Reason: {error}) {entrance.world}"
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
    if not all_logic_satisfied(worlds, item_pool):
        raise EntranceShuffleError(f"Not all logic is satisfied!")

    # Check to make sure that there's at least 1 sphere 0 location reachable
    # with no items except the starting inventory
    sphere_zero_search = Search(SearchMode.SPHERE_ZERO, worlds)
    sphere_zero_search.search_worlds()
    sphere_zero_locs = [
        l
        for l in sphere_zero_search.visited_locations
        if l.progression and "Goddess Cube" not in l.types
    ]
    if len(sphere_zero_locs) == 0 and not sphere_zero_search.found_disconnected_exit:
        raise EntranceShuffleError(f"No Sphere 0 locations reachable at the start!")
