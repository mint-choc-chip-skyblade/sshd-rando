from .world import *
from .search import *

import random
import logging


class FillError(RuntimeError):
    pass


class GameNotBeatableError(RuntimeError):
    pass


def fill_worlds(worlds: list[World]):

    # TODO: Have each world handle special cases before the fill

    # Place Own Worlds Restricted items first
    # and sanitize the item pool afterwards
    for world in worlds:
        place_restricted_items(world, worlds)
        world.sanitize_item_pool()

    item_pool: list[Item] = []
    all_locations: list[Location] = []

    # Combine all worlds' item pools and location pools
    for world in worlds:
        # Filter out hint locations
        all_locations.extend(world.get_all_item_locations())
        for item, count in world.item_pool.items():
            item_pool.extend([item] * count)

    # TODO: Filter out excluded locations

    # Place remaining major items
    major_items = [item for item in item_pool if item.is_major_item]
    assumed_fill(worlds, major_items, [], all_locations)

    # Remove major items from item pool
    item_pool = [item for item in item_pool if not item.is_major_item]

    # Place the rest of the items with fast fill
    fast_fill(item_pool, all_locations)

    if not game_beatable(worlds):
        raise GameNotBeatableError("Game is not beatable after placing all items!")

    # search = Search(SearchMode.ALL_LOCATIONS_REACHABLE, worlds)
    # search.search_worlds()
    # search.dump_world_graph()


def assumed_fill(
    worlds: list[World],
    items_to_place_list: list[Item],
    items_not_yet_placed: list[Item],
    allowed_locations: list[Location] | set[Location],
    world_to_fill: int = -1,
) -> None:
    # Create a set of valid location_access spots from the list of allowed locations
    location_set: set[Location] = set(allowed_locations)
    valid_locations: list[LocationAccess] = []
    for world in worlds:
        for area in world.areas.values():
            valid_locations.extend(
                [
                    la
                    for la in area.locations
                    if la.location.is_empty() and la.location in location_set
                ]
            )

    retries: int = 10
    unsuccessful_placement: bool = True
    while unsuccessful_placement:
        if retries <= 0:
            raise FillError(
                f"Ran out of retries while attempting to place items: {[item.name for item in items_to_place]}"
            )
        retries -= 1
        unsuccessful_placement = False

        random.shuffle(items_to_place_list)
        items_to_place = items_to_place_list.copy()
        rollbacks: list[Location] = []

        while len(items_to_place) > 0:
            # Get a random item to place
            item_to_place = items_to_place.pop()

            random.shuffle(valid_locations)
            spot_to_fill: Location = None

            # Assume we have all the items which haven't been placed yet except the one we're about to place
            assumed_items = items_not_yet_placed.copy()
            assumed_items.extend(items_to_place)
            search = Search(
                SearchMode.ACCESSIBLE_LOCATIONS, worlds, assumed_items, world_to_fill
            )
            search.search_worlds()

            # Loop through the shuffled locations until we find a valid one
            for loc_acesss in valid_locations:
                if (
                    not loc_acesss.location.is_empty()
                    or loc_acesss.area not in search.visited_areas
                ):
                    continue
                if (
                    evaluate_location_requirement(search, loc_acesss)
                    == EvalSuccess.COMPLETE
                ):
                    spot_to_fill = loc_acesss.location
                    break

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


def fast_fill(items_to_place: list[Item], allowed_locations: list[Location]) -> None:
    empty_locations = [
        location for location in allowed_locations if location.is_empty()
    ]
    if len(items_to_place) > len(empty_locations):
        print(f"WARNING: more items than locations when placing items with fast fill. Items: {len(items_to_place)} Locations: {len(empty_locations)}")
    random.shuffle(empty_locations)
    random.shuffle(items_to_place)
    for location in empty_locations:
        if len(items_to_place) == 0:
            break
        location.set_current_item(items_to_place.pop())

def place_restricted_items(world: World, worlds: list[World]) -> None:
    place_own_dungeon_items(world, worlds)
    place_own_region_items(world, worlds)
    place_any_dungeon_items(world, worlds)
    place_overworld_items(world, worlds)

def place_own_dungeon_items(world: World, worlds: list[World]):
    for world in worlds:
        for dungeon in world.dungeons.values():
            own_dungeon_items: list[Item] = []

            if world.setting("small_keys") == "own_dungeon":
                small_key = next(iter([location.original_item for location in dungeon.locations if location.original_item.is_dungeon_small_key]), None)
                own_dungeon_items.extend([small_key] * world.item_pool[small_key])
                world.item_pool[small_key] = 0
            
            if world.setting("boss_keys") == "own_dungeon":
                boss_key = next(iter([location.original_item for location in dungeon.locations if location.original_item.is_boss_key]), None)
                own_dungeon_items.extend([boss_key] * world.item_pool[boss_key])
                world.item_pool[boss_key] = 0

            if world.setting("map_mode").is_any_of("own_dungeon_restricted", "own_dungeon_unrestricted"):
                map_item = next(iter([location.original_item for location in dungeon.locations if location.original_item.is_dungeon_map]), None)
                own_dungeon_items.extend([map_item] * world.item_pool[map_item])
                world.item_pool[map_item] = 0

            # Now place the own dungeon items. If we're restricting maps
            # to not be on Heart Containers or end of dungeon checks, remove
            # the boss key to make these locations not possible to get to, and
            # place the boss keys after

            # Get the complete item pool for all worlds incase of multiworld
            # plandomized items that are required to get to this dungeon
            complete_item_pool = get_complete_item_pool(worlds)
            if world.setting("map_mode") == "own_dungeon_restricted":
                boss_key = [item for item in own_dungeon_items if item.is_boss_key]
                own_dungeon_items = [item for item in own_dungeon_items if not item.is_boss_key]
                assumed_fill(worlds, own_dungeon_items, complete_item_pool, dungeon.locations)
                own_dungeon_items = boss_key
            
            assumed_fill(worlds, own_dungeon_items, complete_item_pool, dungeon.locations)

def place_own_region_items(world: World, worlds: list[World]):
    for world in worlds:
        for dungeon in world.dungeons.values():
            own_region_items: list[Item] = []
            own_region_locations: list[Location] = []

            if world.setting("small_keys") == "own_region":
                small_key = next(iter([location.original_item for location in dungeon.locations if location.original_item.is_dungeon_small_key]), None)
                own_region_items.extend([small_key] * world.item_pool[small_key])
                world.item_pool[small_key] = 0
            
            if world.setting("boss_keys") == "own_region":
                boss_key = next(iter([location.original_item for location in dungeon.locations if location.original_item.is_boss_key]), None)
                own_region_items.extend([boss_key] * world.item_pool[boss_key])
                world.item_pool[boss_key] = 0

            if world.setting("map_mode") == "own_region":
                map_item = next(iter([location.original_item for location in dungeon.locations if location.original_item.is_dungeon_map]), None)
                own_region_items.extend([map_item] * world.item_pool[map_item])
                world.item_pool[map_item] = 0

            # Get all locations in the dungeon and the region around the dungeon
            dungeon_regions = dungeon.starting_entrance.parent_area.hint_regions
            own_region_locations.extend(dungeon.locations)
            for location in world.get_all_item_locations():
                if any(la for la in location.loc_access_list if dungeon_regions.intersection(la.area.hint_regions)):
                    own_region_locations.append(location)

            # Get the complete item pool for all worlds incase of multiworld
            # plandomized items that are required to get to this dungeon
            complete_item_pool = get_complete_item_pool(worlds)
            assumed_fill(worlds, own_region_items, complete_item_pool, own_region_locations)

def place_any_dungeon_items(world: World, worlds: list[World]):
    for world in worlds:
        any_dungeon_items: list[Item] = []
        any_dungeon_locations: list[Location] = []

        for dungeon in world.dungeons.values():
            if world.setting("small_keys") == "any_dungeon":
                small_key = next(iter([location.original_item for location in dungeon.locations if location.original_item.is_dungeon_small_key]), None)
                any_dungeon_items.extend([small_key] * world.item_pool[small_key])
                world.item_pool[small_key] = 0
            
            if world.setting("boss_keys") == "any_dungeon":
                boss_key = next(iter([location.original_item for location in dungeon.locations if location.original_item.is_boss_key]), None)
                any_dungeon_items.extend([boss_key] * world.item_pool[boss_key])
                world.item_pool[boss_key] = 0

            if world.setting("map_mode") == "any_dungeon":
                map_item = next(iter([location.original_item for location in dungeon.locations if location.original_item.is_dungeon_map]), None)
                any_dungeon_items.extend([map_item] * world.item_pool[map_item])
                world.item_pool[map_item] = 0

            any_dungeon_locations.extend(dungeon.locations)

        # Get the complete item pool for all worlds incase of multiworld
        # plandomized items that are required to get to this dungeon
        complete_item_pool = get_complete_item_pool(worlds)
        assumed_fill(worlds, any_dungeon_items, complete_item_pool, any_dungeon_locations)

def place_overworld_items(world: World, worlds: list[World]):
    for world in worlds:
        overworld_items: list[Item] = []
        overworld_locations: set[Location] = set(world.get_all_item_locations())

        for dungeon in world.dungeons.values():
            if world.setting("small_keys") == "overworld":
                small_key = next(iter([location.original_item for location in dungeon.locations if location.original_item.is_dungeon_small_key]), None)
                overworld_items.extend([small_key] * world.item_pool[small_key])
                world.item_pool[small_key] = 0
            
            if world.setting("boss_keys") == "overworld":
                boss_key = next(iter([location.original_item for location in dungeon.locations if location.original_item.is_boss_key]), None)
                overworld_items.extend([boss_key] * world.item_pool[boss_key])
                world.item_pool[boss_key] = 0

            if world.setting("map_mode") == "overworld":
                map_item = next(iter([location.original_item for location in dungeon.locations if location.original_item.is_dungeon_map]), None)
                overworld_items.extend([map_item] * world.item_pool[map_item])
                world.item_pool[map_item] = 0
            
            # Remove locations from this dungeon from the overworld locations
            overworld_locations = overworld_locations.difference(dungeon.locations)
        
        if world.setting("lanayru_caves_key") == "overworld":
            caves_key = world.get_item("Lanayru Caves Small Key")
            overworld_items.extend([caves_key] * world.item_pool[caves_key])
            world.item_pool[caves_key] = 0

        # Get the complete item pool for all worlds incase of multiworld
        # plandomized items that are required to get to this dungeon
        complete_item_pool = get_complete_item_pool(worlds)
        assumed_fill(worlds, overworld_items, complete_item_pool, overworld_locations)

def get_complete_item_pool(worlds: list[World]) -> list[Item]:
    complete_item_pool: list[Item] = []
    for world in worlds:
        for item, count in world.item_pool.items():
            complete_item_pool.extend([item] * count)
    return complete_item_pool