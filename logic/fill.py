from .world import *
from .search import *

import random
import logging


class FillError(RuntimeError):
    pass


class GameNotBeatableError(RuntimeError):
    pass


def fill_worlds(worlds: list[World]):
    # Cache potential area times for each world
    # so we cut down on exit evaluation iterations
    cache_area_and_exit_times(worlds)

    # TODO: Have each world handle special cases before the fill

    # Place Own Worlds Restricted items first
    # and sanitize the item pool afterwards
    for world in worlds:
        place_restricted_items(world, worlds)
        world.sanitize_item_pool()
        world.add_traps()

    item_pool: list[Item] = []
    all_locations: list[Location] = []

    # Combine all worlds' item pools and location pools
    for world in worlds:
        # Filter out hint locations
        all_locations.extend(world.get_all_item_locations())
        for item, count in world.item_pool.items():
            item_pool.extend([item] * count)

    # Place remaining major items in progress locations
    major_items = [item for item in item_pool if item.is_major_item]
    progress_locations = [loc for loc in all_locations if loc.progression]
    assumed_fill(worlds, major_items, [], progress_locations)

    # Remove major items from item pool
    item_pool = [item for item in item_pool if not item.is_major_item]

    # Ensure that at least *some* traps get placed in progress locations if possible
    traps = [item for item in item_pool if item.name in TRAP_SETTING_TO_ITEM.values()]

    if len(traps) > 3:
        traps = traps[:3]
    fast_fill(traps.copy(), progress_locations)

    # Remove placed traps from item pool
    for trap in traps:
        item_pool.remove(trap)

    # Place the rest of the items with fast fill
    fast_fill(item_pool, all_locations)

    if not all_logic_satisfied(worlds):
        # Uncomment if necessary for debugging
        # search = Search(SearchMode.ALL_LOCATIONS_REACHABLE, worlds)
        # search.search_worlds()
        # search.dump_world_graph()
        raise GameNotBeatableError("Logic is not satisfied after placing all items!")


# Assumed fill is an algorithm which statistically places items more
# evenly across the world compared to forward fill. The idea is that
# we first start with all the items, take an item out, search for
# available locations (picking up any placed items along the way),
# and choose a random location of the available ones to place the item.
# Repeat for all items in the items_to_place_list.
def assumed_fill(
    worlds: list[World],
    items_to_place_list: list[Item],
    items_not_yet_placed: list[Item],
    allowed_locations: list[Location],
    world_to_fill: int = -1,
) -> None:
    # Sort locations to keep consistency incase a set
    # was passed in
    allowed_locations.sort()

    # Assumed Fill will sometimes place items in such a way
    # that accidentally locks out being able to place specific
    # items anywhere. Allow the algorithm to retry a reasonable
    # amount of times before throwing an error.
    retries: int = 10
    unsuccessful_placement: bool = True
    while unsuccessful_placement:
        if retries <= 0:
            raise FillError(
                f"Ran out of retries while attempting to place items: {[item.name for item in items_to_place_list]}"
            )
        retries -= 1
        unsuccessful_placement = False

        random.shuffle(items_to_place_list)
        items_to_place = items_to_place_list.copy()
        rollbacks: list[Location] = []

        while len(items_to_place) > 0:
            # Get a random item to place
            item_to_place = items_to_place.pop()

            random.shuffle(allowed_locations)
            spot_to_fill: Location = None

            # Assume we have all the items which haven't been placed yet except the one we're about to place
            assumed_items = items_not_yet_placed.copy()
            assumed_items.extend(items_to_place)
            search = Search(
                SearchMode.ACCESSIBLE_LOCATIONS, worlds, assumed_items, world_to_fill
            )
            search.search_worlds()

            # Loop through the shuffled locations until we find a valid one.
            # If a world is only checking for beatable logic, then we can ignore
            # any access checks and just choose a random location if the world is already beatable
            can_choose_any_location = (
                item_to_place.world.setting("logic_rules") == "beatable_only"
                and item_to_place.world.get_game_winning_item() in search.owned_items
            )
            for location in allowed_locations:
                # Get all reachable Location Access spots for this location
                loc_acc_list = [
                    la
                    for la in location.loc_access_list
                    if can_choose_any_location or la.area in search.visited_areas
                ]
                # If this location is not empty, or has no potentially reachable
                # Location Access spot, then we can't place the item here
                if not location.is_empty() or not loc_acc_list:
                    continue

                if any(
                    [
                        True
                        for la in loc_acc_list
                        if can_choose_any_location
                        or evaluate_location_requirement(search, la)
                        == EvalSuccess.COMPLETE
                    ]
                ):
                    spot_to_fill = location
                    break

            # If we couldn't find a spot to place this item, undo
            # all item placements within this fill attempt and try
            # again from the top.
            if spot_to_fill == None:
                logging.getLogger("").debug(
                    f"No accessible locations to place {item_to_place}. Retrying {retries} more times."
                )
                for location in rollbacks:
                    items_to_place.append(location.current_item)
                    location.remove_current_item()

                # Also add back the randomly selected item
                items_to_place.append(item_to_place)
                rollbacks.clear()
                # Break out of the item placement loop and flag an unsuccessful
                # placement attempt to try again.
                unsuccessful_placement = True
                break

            spot_to_fill.set_current_item(item_to_place)
            rollbacks.append(spot_to_fill)


# Place the items in items_to_place completely randomly within the allowed locations.
# There are no logic checks with this fill.
def fast_fill(items_to_place: list[Item], allowed_locations: list[Location]) -> None:
    empty_locations = [
        location for location in allowed_locations if location.is_empty()
    ]
    if len(items_to_place) > len(empty_locations):
        print(
            f"WARNING: more items than locations when placing items with fast fill. Items: {len(items_to_place)} Locations: {len(empty_locations)}"
        )
    random.shuffle(empty_locations)
    random.shuffle(items_to_place)
    for location in empty_locations:
        if len(items_to_place) == 0:
            break
        location.set_current_item(items_to_place.pop())


def place_restricted_items(world: World, worlds: list[World]) -> None:
    fill_required_dungeon_goal_locations(world, worlds)
    place_own_dungeon_items(world, worlds)
    place_own_region_items(world, worlds)
    place_any_dungeon_items(world, worlds)
    place_overworld_items(world, worlds)


def fill_required_dungeon_goal_locations(world: World, worlds: list[World]):
    # Get all required goal locations
    required_goal_locations = []
    for dungeon in world.dungeons.values():
        if dungeon.required and dungeon.goal_location.is_empty():
            required_goal_locations.append(dungeon.goal_location)

    # Return early if there are no goal locations
    if len(required_goal_locations) == 0:
        return

    # Create the pool of items that will fill the goal locations
    # Keep filling it until its size is equal to the number
    # of required goal locations. Start with Triforce Pieces,
    # then move to swords, and finally major items if there are
    # none of those left
    goal_location_items = []
    triforce_pieces = []
    swords = []
    major_items = []
    # Major items to consider should be "good" major items (can expand this more later)
    major_items_to_consider = [
        "Goddess's Harp",
        "Ballad of the Goddess",
        "Clawshots",
        "Bomb Bag",
        "Whip",
        "Progressive Bow",
        "Progressive Beetle",
        "Fireshield Earrings",
        "Water Dragon's Scale",
    ]
    for item, count in world.item_pool.items():
        if "Triforce" in item.name:
            triforce_pieces.extend([item] * count)
        elif item.name == "Progressive Sword":
            swords.extend([item] * count)
        elif item.name in major_items_to_consider:
            major_items.extend([item] * count)

    random.shuffle(triforce_pieces)
    random.shuffle(major_items)
    while len(goal_location_items) < len(required_goal_locations):
        # Add the appropriate item to the goal location items
        if len(triforce_pieces) > 0:
            goal_location_items.append(triforce_pieces.pop())
        elif len(swords) > 0:
            goal_location_items.append(swords.pop())
        elif len(major_items) > 0:
            goal_location_items.append(major_items.pop())
        else:
            raise FillError(
                "Could not generate a seed because there are no more items left to make enough required dungeons.\nThis could be because the current settings start with too many items."
            )

        # Then take it out of the world's item pool
        world.item_pool[goal_location_items[-1]] -= 1

    # Then place the items in the goal locations
    complete_item_pool = get_complete_item_pool(worlds)
    assumed_fill(
        worlds, goal_location_items, complete_item_pool, required_goal_locations
    )


def place_own_dungeon_items(world: World, worlds: list[World]):
    for dungeon in world.dungeons.values():
        own_dungeon_items: list[Item] = []

        if world.setting("small_keys") == "own_dungeon":
            small_key = dungeon.small_key
            if small_key is not None:
                own_dungeon_items.extend([small_key] * world.item_pool[small_key])
                world.item_pool[small_key] = 0

        if world.setting("boss_keys") == "own_dungeon":
            boss_key = dungeon.boss_key
            if boss_key is not None:
                own_dungeon_items.extend([boss_key] * world.item_pool[boss_key])
                world.item_pool[boss_key] = 0

        if world.setting("map_mode").is_any_of(
            "own_dungeon_restricted", "own_dungeon_unrestricted"
        ):
            map_item = dungeon.map
            own_dungeon_items.extend([map_item] * world.item_pool[map_item])
            world.item_pool[map_item] = 0

        # Get the complete item pool for all worlds incase of multiworld
        # plandomized items that are required to get to this dungeon
        complete_item_pool = get_complete_item_pool(worlds)

        # The possible fill locations depends on if the dungeon is required and if
        # empty unrequired dungeons is enabled or not
        # If the dungeon is not required AND empty unrequired dungeons is on, only choose
        # non-progress locations, else choose progression locations
        fill_locations = []
        if dungeon.should_be_barren():
            fill_locations = [loc for loc in dungeon.locations if not loc.progression]
        else:
            fill_locations = [loc for loc in dungeon.locations if loc.progression]

        # Now place the own dungeon items. If we're restricting maps
        # to not be on Heart Containers or end of dungeon checks, remove
        # the boss key to make these locations not possible to get to, and
        # place the boss keys after
        if world.setting("map_mode") == "own_dungeon_restricted":
            boss_key = [item for item in own_dungeon_items if item.is_boss_key]
            own_dungeon_items = [
                item for item in own_dungeon_items if not item.is_boss_key
            ]
            assumed_fill(worlds, own_dungeon_items, complete_item_pool, fill_locations)
            own_dungeon_items = boss_key

        assumed_fill(worlds, own_dungeon_items, complete_item_pool, fill_locations)


def place_own_region_items(world: World, worlds: list[World]):
    for dungeon in world.dungeons.values():
        own_region_items: list[Item] = []
        own_region_locations: list[Location] = []

        if world.setting("small_keys") == "own_region":
            small_key = dungeon.small_key
            if small_key is not None:
                own_region_items.extend([small_key] * world.item_pool[small_key])
                world.item_pool[small_key] = 0

        if world.setting("boss_keys") == "own_region":
            boss_key = dungeon.boss_key
            if boss_key is not None:
                own_region_items.extend([boss_key] * world.item_pool[boss_key])
                world.item_pool[boss_key] = 0

        if world.setting("map_mode") == "own_region":
            map_item = dungeon.map
            own_region_items.extend([map_item] * world.item_pool[map_item])
            world.item_pool[map_item] = 0

        # Get all locations in the dungeon and the region around the dungeon
        dungeon_regions = dungeon.starting_entrance.parent_area.hint_regions
        own_region_locations.extend(dungeon.locations)
        for location in world.get_all_item_locations():
            if any(
                la
                for la in location.loc_access_list
                if dungeon_regions.intersection(la.area.hint_regions)
            ):
                own_region_locations.append(location)

        # Filter own_region_locations depending on if the dungeon should be barren or not
        if dungeon.should_be_barren():
            own_region_locations = [
                loc for loc in own_region_locations if not loc.progression
            ]
        else:
            own_region_locations = [
                loc for loc in own_region_locations if loc.progression
            ]

        # Get the complete item pool for all worlds incase of multiworld
        # plandomized items that are required to get to this dungeon
        complete_item_pool = get_complete_item_pool(worlds)
        assumed_fill(worlds, own_region_items, complete_item_pool, own_region_locations)

    # Own region place Earth Temple Key Pieces if needed
    if world.setting("open_earth_temple") == "shuffle_eldin":
        key_piece = world.get_item(KEY_PIECE)

        eldin_locations: list[Location] = []
        eldin_items: list[Item] = []
        eldin_items.extend([key_piece] * world.item_pool[key_piece])
        world.item_pool[key_piece] = 0

        for location in world.get_all_item_locations():
            if any(
                la
                for la in location.loc_access_list
                if "Eldin Volcano" in la.area.hint_regions
                or (
                    world.setting("randomize_overworld_entrances") == "off"
                    and "Mogma Turf" in la.area.hint_regions
                )
            ):
                eldin_locations.append(location)

        # Filter down to only progression locations
        eldin_locations = [loc for loc in eldin_locations if loc.progression]

        for l in eldin_locations:
            print(l)

        # Get the complete item pool for all worlds incase of multiworld
        # plandomized items that are required to get to Eldin Volcano
        complete_item_pool = get_complete_item_pool(worlds)
        assumed_fill(worlds, eldin_items, complete_item_pool, eldin_locations)


def place_any_dungeon_items(world: World, worlds: list[World]):
    any_dungeon_items: list[Item] = []
    any_dungeon_locations: list[Location] = []

    # Any dungeon items for should_be_barren dungeons will go in a separate pool
    non_barren_dungeons = [
        dungeon for dungeon in world.dungeons.values() if not dungeon.should_be_barren()
    ]
    barren_dungeons = [
        dungeon for dungeon in world.dungeons.values() if dungeon.should_be_barren()
    ]

    for dungeons in [non_barren_dungeons, barren_dungeons]:
        any_dungeon_items.clear()
        any_dungeon_locations.clear()
        for dungeon in dungeons:
            if world.setting("small_keys") == "any_dungeon":
                small_key = dungeon.small_key
                if small_key is not None:
                    any_dungeon_items.extend([small_key] * world.item_pool[small_key])
                    world.item_pool[small_key] = 0

            if world.setting("boss_keys") == "any_dungeon":
                boss_key = dungeon.boss_key
                if boss_key is not None:
                    any_dungeon_items.extend([boss_key] * world.item_pool[boss_key])
                    world.item_pool[boss_key] = 0

            if world.setting("map_mode") == "any_dungeon":
                map_item = dungeon.map
                any_dungeon_items.extend([map_item] * world.item_pool[map_item])
                world.item_pool[map_item] = 0

            # If this dungeon is not guaranteed barren, only get the progression locations within
            any_dungeon_locations.extend(
                [
                    loc
                    for loc in dungeon.locations
                    if dungeon.should_be_barren() or loc.progression
                ]
            )

        # Get the complete item pool for all worlds incase of multiworld
        # plandomized items that are required to get to this dungeon
        complete_item_pool = get_complete_item_pool(worlds)
        assumed_fill(
            worlds, any_dungeon_items, complete_item_pool, any_dungeon_locations
        )


def place_overworld_items(world: World, worlds: list[World]):
    overworld_items: list[Item] = []
    overworld_locations = [
        loc for loc in world.get_all_item_locations() if loc.progression
    ]

    for dungeon in world.dungeons.values():
        if world.setting("small_keys") == "overworld":
            small_key = dungeon.small_key
            if small_key is not None:
                overworld_items.extend([small_key] * world.item_pool[small_key])
                world.item_pool[small_key] = 0

        if world.setting("boss_keys") == "overworld":
            boss_key = dungeon.boss_key
            if boss_key is not None:
                overworld_items.extend([boss_key] * world.item_pool[boss_key])
                world.item_pool[boss_key] = 0

        if world.setting("map_mode") == "overworld":
            map_item = dungeon.map
            overworld_items.extend([map_item] * world.item_pool[map_item])
            world.item_pool[map_item] = 0

        # Remove locations from this dungeon from the overworld locations
        overworld_locations = [
            loc for loc in overworld_locations if loc not in dungeon.locations
        ]

    if world.setting("lanayru_caves_keys") == "overworld":
        caves_key = world.get_item("Lanayru Caves Small Key")
        overworld_items.extend([caves_key] * world.item_pool[caves_key])
        world.item_pool[caves_key] = 0

    # Get the complete item pool for all worlds incase of multiworld
    # plandomized items that are required to get to this dungeon
    complete_item_pool = get_complete_item_pool(worlds)
    assumed_fill(worlds, overworld_items, complete_item_pool, overworld_locations)


# Cache all the possible times of day for each area and exit.
# This way, the search algorithm doesn't end up testing for
# times of day that we know ahead of time wouldn't be possible
# anyway.
def cache_area_and_exit_times(worlds: list[World]) -> None:
    # Search with the complete item pool to get all possible times
    search_with_items = Search(
        SearchMode.ALL_LOCATIONS_REACHABLE, worlds, get_complete_item_pool(worlds)
    )
    search_with_items.search_worlds()

    for world in worlds:
        logging.getLogger("").debug(f"Caching times for {world}")
        world.exit_time_cache.clear()
        for area_id, area in world.areas.items():
            area_times = (
                search_with_items.area_time[area_id]
                if area_id in search_with_items.area_time
                else TOD.NONE
            )
            for exit_ in area.exits:
                req = exit_.requirement
                world.exit_time_cache[exit_] = TOD.NONE
                for time in ALL_TODS:
                    if time & area_times and evaluate_requirement_at_time(
                        req, search_with_items, time, world
                    ):
                        world.exit_time_cache[exit_] |= time
