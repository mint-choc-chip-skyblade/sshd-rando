from .world import *
from .search import *

import random
import logging

class FillError(RuntimeError):
    pass

class GameNotBeatableError(RuntimeError):
    pass

def fill_worlds(worlds: list[World]):
    item_pool: list[Item] = []
    all_locations: list[Location] = []

    # Combine all worlds' item pools and location pools
    for world in worlds:
        # Filter out hint locations
        all_locations.extend(world.location_table.values())
        for item, count in world.item_pool.items():
            item_pool.extend([item] * count)
    
    # Filter out hint locations
    all_locations = [location for location in all_locations if "Hint Location" not in location.types]
    # TODO: Filter out excluded locations
    # TODO: Have each world handle special cases before the fill

    # TODO: Handle Randomizing items that should go into the "any dungeon" or "overworld" pools
    # TODO: Handle junk "any dungeon" and "overworld" pools

    # Place remaining major items
    major_items = [item for item in item_pool if item.is_major_item]
    assumed_fill(worlds, major_items, [], all_locations)

    # Remove major items from item pool
    item_pool = [item for item in item_pool if not item.is_major_item]

    # Place the rest of the items with fast fill
    fast_fill(item_pool, all_locations)

    if (not game_beatable(worlds)):
        raise GameNotBeatableError("Game is not beatable after placing all items!")

    search = Search(SearchMode.ALL_LOCATIONS_REACHABLE, worlds)
    search.search_worlds()
    search.dump_world_graph()


def assumed_fill(worlds: list[World], items_to_place_list: list[Item], items_not_yet_placed: list[Item], allowed_locations: list[Location], world_to_fill: int = -1) -> None:
    # Create a set of valid location_access spots from the list of allowed locations
    location_set: set[Location] = set(allowed_locations)
    valid_locations: list[LocationAccess] = []
    for world in worlds:
        for area in world.areas.values():
            valid_locations.extend([la for la in area.locations if la.location.is_empty() and la.location in location_set])

    
    retries: int = 10
    unsuccessful_placement: bool = True
    while unsuccessful_placement:
        if retries <= 0:
            raise FillError(f"Ran out of retries while attempting to place items: {[item.name for item in items_to_place]}")
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
            search = Search(SearchMode.ACCESSIBLE_LOCATIONS, worlds, assumed_items, world_to_fill)
            search.search_worlds()

            # Loop through the shuffled locations until we find a valid one
            for loc_acesss in valid_locations:
                if not loc_acesss.location.is_empty() or loc_acesss.area not in search.visited_areas:
                    continue
                if evaluate_location_requirement(search, loc_acesss) == EvalSuccess.COMPLETE:
                    spot_to_fill = loc_acesss.location
                    break

            if spot_to_fill == None:
                logging.getLogger('').debug(f"No accessible locations to place {item_to_place}. Retrying {retries} more times.")
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


def fast_fill(items_to_place: list[Item], allowed_locations: list[Location]):
    empty_locations = [location for location in allowed_locations if location.is_empty()]
    if len(items_to_place) > len(empty_locations):
        print('WARNING: more items than locations when placing items with fast fill')
    random.shuffle(empty_locations)
    random.shuffle(items_to_place)
    for location in empty_locations:
        if len(items_to_place) == 0:
            break
        location.set_current_item(items_to_place.pop())