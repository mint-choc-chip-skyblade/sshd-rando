from util.text import *
from constants.itemconstants import *
from .world import World
from .search import *
import logging
import math


def generate_hints(worlds: list[World]) -> None:
    print_progress_text("Generating Hints")
    sanitize_major_items(worlds)
    calculate_possible_path_locations(worlds)
    calculate_possible_barren_regions(worlds)

    for world in worlds:
        hint_locations: list[Location] = []
        generate_impa_sot_hint(world)
        generate_song_hints(world, hint_locations)
        generate_path_hint_locations(world, hint_locations)
        generate_barren_hint_locations(world, hint_locations)
        generate_item_hint_locations(world, hint_locations)

        # If we weren't able to generate the specified number
        # of hints for path, barren, or item hints then make up
        # for those with extra location hints
        total_num_hints = (
            world.setting("path_hints").value_as_number()
            + world.setting("barren_hints").value_as_number()
            + world.setting("item_hints").value_as_number()
            + world.setting("location_hints").value_as_number()
        )
        total_made_hints = len(hint_locations)
        num_location_hints = total_num_hints - total_made_hints
        generate_location_hint_locations(world, hint_locations, num_location_hints)

        hints_for_category: dict[str, list[Location]] = {
            "fi_hints": [],
            "gossip_stone_hints": [],
        }

        # Distribute each hint to its appropriate placement option
        for i in range(len(hint_locations)):
            location = hint_locations[i]
            type = location.hint.type.lower()

            type_on_fi = world.setting(f"{type}_hints_on_fi") == "on"
            type_on_gossip_stones = (
                world.setting(f"{type}_hints_on_gossip_stones") == "on"
            )

            placement_option = ""
            # If both options for the type are selected, then choose based on the current list index.
            # All hints of a type should be consecutive in the list, so this works for evenly distributing them
            if type_on_fi and type_on_gossip_stones:
                placement_option = "fi_hints" if i % 2 else "gossip_stone_hints"
            elif type_on_fi:
                placement_option = "fi_hints"
            elif type_on_gossip_stones:
                placement_option = "gossip_stone_hints"

            if placement_option:
                hints_for_category[placement_option].append(location)
                logging.getLogger("").debug(
                    f'Hint for "{location}" will be given to {placement_option}'
                )

        if hints_for_category["gossip_stone_hints"]:
            assign_gossip_stone_hints(
                world, worlds, hints_for_category["gossip_stone_hints"]
            )

        if hints_for_category["fi_hints"]:
            world.fi_hints = hints_for_category["fi_hints"]


# Set some items as non-major depending on certain conditions.
# All items are placed at this point, so we'll loop through and check
# all locations individually.
def sanitize_major_items(worlds: list[World]) -> None:

    # If the player starts with any item in this list
    # then the rest of that item are not major items
    one_then_junk_items = [
        PROGRESSIVE_BOW,
        PROGRESSIVE_BUG_NET,
        PROGRESSIVE_SLINGSHOT,
        PROGRESSIVE_POUCH,
        EMPTY_BOTTLE,
    ]

    # Maps items required to enter the corresponding
    # dungeon (assuming no entrance rando). If the dungeon
    # is known to be barren, then the item is non-major
    dungeon_entry_items = {
        KEY_PIECE: "Earth Temple",
        SEA_CHART: "Sandship",
        STONE_OF_TRIALS: "Sky Keep",
    }

    for world in worlds:
        for location in world.get_all_item_locations():
            item = location.current_item
            if (
                (
                    item.name in one_then_junk_items
                    and world.starting_item_pool[item] > 0
                )
                or (
                    item.name in dungeon_entry_items
                    and world.get_dungeon(
                        dungeon_entry_items[item.name]
                    ).should_be_barren()
                    and world.setting("randomize_dungeon_entrances") == "off"
                )
                or (
                    # If all of this item's chain locations are not progression, then
                    # the item is not a major item.
                    all(
                        [
                            True if not world.get_location(loc).progression else False
                            for loc in item.chain_locations
                        ]
                    )
                    and len(item.chain_locations) > 0
                )
            ):
                item.is_major_item = False
                logging.getLogger("").debug(
                    f"{item} is not a major item anymore for {world}"
                )


def calculate_possible_path_locations(worlds: list[World]) -> None:
    logging.getLogger("").debug("Generating Path Locations")
    # First generate the goal location keys and also remove items from non-
    # progress locations since they shouldn't be considered when determining
    # path locations
    non_required_locations = {}
    for world in worlds:
        # Defeat Demise is always a goal location
        world.path_locations[world.get_location("Hylia's Realm - Defeat Demise")] = []
        # Required dungeons also have goal locations
        for dungeon in world.dungeons.values():
            if dungeon.required:
                world.path_locations[dungeon.goal_location] = []

        for location in world.location_table.values():
            if not location.progression and not (
                location.has_known_vanilla_item
                and location.current_item.name == GRATITUDE_CRYSTAL
            ):
                non_required_locations[location] = location.current_item
                location.remove_current_item()

    # Determine path locations for each goal location by going through the playthrough
    # and seeing if taking away the item at each location can still access the goal location(s)
    for world in worlds:
        for sphere in worlds[0].playthrough_spheres:
            for location in sphere:
                item_at_location = location.current_item

                # TODO: how can an item_at_location even be null here?
                if item_at_location is None:
                    continue

                # If this location has a small or big key and the key is known to be within the dungeon,
                # then ignore it because the player already knows where those items are. Also ignore race
                # mode locations at the end of dungeons because players know those locations are required.
                if (
                    location.has_known_vanilla_item
                    or location.is_goal_location
                    or (
                        item_at_location.is_dungeon_small_key
                        and world.setting("small_keys").is_any_of(
                            "own_dungeon", "own_region"
                        )
                    )
                    or (
                        item_at_location.is_boss_key
                        and world.setting("boss_keys").is_any_of(
                            "own_dungeon", "own_region"
                        )
                    )
                ):
                    continue

                # Take the item away from the location
                location.remove_current_item()

                # Run a search without the item
                search = Search(SearchMode.ACCESSIBLE_LOCATIONS, worlds)
                search.search_worlds()

                # If we never reach the goal location, then this location is
                # "on the path to" the goal location.
                for goal_location, path_locations in world.path_locations.items():
                    if goal_location not in search.visited_locations:
                        path_locations.append(location)

                # Then give back the location's item
                location.set_current_item(item_at_location)

        # logging.getLogger("").debug(f"Path locations for {world}")
        # for goal_location, path_locations in world.path_locations.items():
        #     goal_name = get_text_data(goal_location.name, "goal_name").get(
        #         "en_US"
        #     )
        #     logging.getLogger("").debug(f"  {goal_name}")
        #     for location in path_locations:
        #         logging.getLogger("").debug(f"  - {location}: {location.current_item}")

    # Give back non-progress items
    for location, item in non_required_locations.items():
        location.set_current_item(item)


def calculate_possible_barren_regions(worlds: list[World]) -> None:
    logging.getLogger("").debug("Calculating Barren Regions")
    for world in worlds:
        potentially_junk_locations = set()
        junk_locations = set()
        for location in world.get_all_item_locations():
            # If this location is progression, then add its hint regions to
            # the set of potentially barren regions
            if location.progression:
                for loc_access in location.loc_access_list:
                    for hint_region in loc_access.area.hint_regions:
                        world.barren_regions[hint_region] = []

            # Prevent small keys and big keys in known places from being barren blockers
            item_at_location = location.current_item
            if (
                location.is_goal_location
                or (
                    item_at_location.is_dungeon_small_key
                    and world.setting("small_keys").is_any_of("vanilla", "own_dungeon")
                )
                or (
                    item_at_location.is_boss_key
                    and world.setting("boss_keys").is_any_of("vanilla", "own_dungeon")
                )
            ):
                junk_locations.add(location)
            # Depending on how items were placed, temporarily set certain
            # items as junk items if all of the item's chain locations also
            # only contain junk
            chain_locations = [
                world.get_location(loc_name)
                for loc_name in location.current_item.chain_locations
            ]
            if location.progression and len(chain_locations) > 0:
                if locations_are_all_junk(chain_locations):
                    junk_locations.add(location)
                    logging.getLogger("").debug(f"{location.current_item} is now junk")
                else:
                    potentially_junk_locations.add(location)

        # Iterate through all the potentially_junk_locations until
        # no new junk locations are set
        new_junk_locations = True
        while new_junk_locations:
            new_junk_locations = False
            for location in potentially_junk_locations:
                chain_locations = [
                    world.get_location(loc_name)
                    for loc_name in location.current_item.chain_locations
                ]
                if location.current_item.is_major_item and locations_are_all_junk(
                    chain_locations
                ):
                    new_junk_locations = True
                    junk_locations.add(location)
                    logging.getLogger("").debug(f"{location.current_item} is now junk")

        # Now loop through all the progression locations again and remove
        # any regions from the barren regions which have non-junk items at
        # any of their locations. Otherwise add the location to the list
        # of locations in the barren region
        for location in world.get_all_item_locations():
            for loc_access in location.loc_access_list:
                for hint_region in loc_access.area.hint_regions:
                    if (
                        location.progression
                        and location.current_item.is_major_item
                        and location not in junk_locations
                        and hint_region in world.barren_regions
                    ):
                        del world.barren_regions[hint_region]
                    elif hint_region in world.barren_regions:
                        world.barren_regions[hint_region].append(location)

        logging.getLogger("").debug(f"Barren regions for {world}")
        for region in world.barren_regions.keys():
            logging.getLogger("").debug(f"- {region}")


def generate_path_hint_locations(world: World, hint_locations: list) -> None:
    # Shuffle each pool of path locations so that their orders are random
    goal_locations_list = []
    for goal_location, path_locations in world.path_locations.items():
        random.shuffle(path_locations)
        # Initially we want to create hints for required dungeon's goal locations
        # and then add Demise in once we have at least 1 hint for each required dungeon
        if goal_location != world.get_location("Hylia's Realm - Defeat Demise"):
            goal_locations_list.append(goal_location)

    added_demise_path_location = False
    for i in range(world.setting("path_hints").value_as_number()):
        # Try to get at least one hint for each required dungeon first
        goal_location = None
        if i < len(goal_locations_list):
            goal_location = goal_locations_list[i]
        else:
            # Once we've pulled from all required dungeons, then add demise
            # to the list and choose randomly
            if i == len(goal_locations_list) and not added_demise_path_location:
                added_demise_path_location = True
                goal_locations_list.append(
                    world.get_location("Hylia's Realm - Defeat Demise")
                )

            if not goal_locations_list:
                logging.getLogger("").debug("No more possible path hints")
                break

            goal_location = random.choice(goal_locations_list)

        # If we're placing path hints on gossip stones, don't choose any that somehow
        # manage to be before every possible gossip stone
        valid_path_locations = [
            loc
            for loc in world.path_locations[goal_location]
            if world.setting("path_hints_on_gossip_stones") == "off"
            or (
                world.setting("path_hints_on_gossip_stones") == "on"
                and get_possible_gossip_stones(loc)
            )
        ]
        hint_location = get_hintable_location(valid_path_locations)
        if hint_location is None:
            logging.getLogger("").debug(f"No more path locations for {goal_location}")
            goal_locations_list.remove(goal_location)
            i -= 1
            continue

        hint_location.is_hinted = True
        hint_locations.append(hint_location)
        logging.getLogger("").debug(
            f'Chose "{hint_location}" as path hint for "{goal_location}"'
        )
        generate_path_hint_message(hint_location, goal_location)


def generate_barren_hint_locations(world: World, hint_locations: list) -> None:
    # Generate weights for each barren region based on the square root
    # of how many locations are in that region
    barren_pool = []
    barren_weights = []
    for region, locations in world.barren_regions.items():
        barren_locs = [
            loc
            for loc in locations
            if not loc.is_hinted and loc.progression and not loc.has_known_vanilla_item
        ]

        # Skip over any regions that we're already hinting at with
        # the impa or song hints
        if not any(barren_locs):
            continue

        barren_pool.append(region)
        barren_weights.append(math.sqrt(len(barren_locs)))

    for _ in range(world.setting("barren_hints").value_as_number()):
        if not barren_pool:
            logging.getLogger("").debug("No more barren regions to hint at.")
            break
        region = random.choices(barren_pool, weights=barren_weights)[0]
        # Set all locations in the selected barren region as hinted
        # so we don't hint at them again
        for location in world.barren_regions[region]:
            location.is_hinted = True
            generate_barren_hint_message(
                location, get_text_data(region, "pretty").apply_text_color("b")
            )
        hint_locations.append(world.barren_regions[region][0])
        logging.getLogger("").debug(f'Chose "{region}" as a hinted barren region')

        # Reform weights without the hint we just chose
        barren_weights.pop(barren_pool.index(region))
        barren_pool.remove(region)


def generate_item_hint_locations(world: World, hint_locations: list) -> None:
    possible_item_hint_locations: list[Location] = []
    for location in world.get_all_item_locations():
        # if the location is progression...
        # and has a major item...
        # and does not have a known vanilla item...
        # and is not already hinted...
        # and does not have a small key when the keys are in known areas...
        # and does not have a boss key when boss keys are in known areas...
        # and is not a goal location
        # and is not an "always" location when we're using always hints
        # and is not a gratitude crystal pack or single gratitude crystal
        # then it can be hinted as an item hint
        if (
            location.progression
            and location.current_item.is_major_item
            and not location.has_known_vanilla_item
            and not location.is_hinted
            and not (
                location.current_item.is_dungeon_small_key
                and world.setting("small_keys").is_any_of("own_dungeon", "own_region")
            )
            and not (
                location.current_item.is_boss_key
                and world.setting("boss_keys").is_any_of("own_dungeon", "own_region")
            )
            and not location.is_goal_location
            and (
                location.hint_priority != "always" or not world.setting("always_hints")
            )
            and not location.current_item.name.startswith("Gratitude Crystal")
        ):
            possible_item_hint_locations.append(location)

    # Choose randomly until we've selected the appropriate number of hints
    random.shuffle(possible_item_hint_locations)
    for _ in range(world.setting("item_hints").value_as_number()):
        if not possible_item_hint_locations:
            logging.getLogger("").debug("No more possible item hint locations")
            break
        hint_location = possible_item_hint_locations.pop()
        hint_locations.append(hint_location)
        hint_location.is_hinted = True
        generate_item_hint_message(hint_location)
        logging.getLogger("").debug(f'Chose "{hint_location}" as item hint location')


def generate_location_hint_locations(
    world: World, hint_locations: list, num_location_hints
) -> None:
    always_locations = []
    sometimes_locations = []

    # Put locations into always or sometimes based on their hint priority
    for location in world.get_all_item_locations():
        if (
            location.progression
            and not location.is_hinted
            and not location.is_goal_location
        ):
            if location.hint_priority == "always":
                always_locations.append(location)
            elif location.hint_priority == "sometimes":
                sometimes_locations.append(location)

    # If we're not using always hints then add always locations to sometimes locations
    if world.setting("always_hints") == "off":
        sometimes_locations.extend(always_locations)
        always_locations.clear()

    random.shuffle(sometimes_locations)
    random.shuffle(always_locations)

    for i in range(num_location_hints):
        hint_location = None
        if i < len(always_locations):
            hint_location = always_locations[i]
        else:
            if not sometimes_locations:
                logging.getLogger("").debug("No more possible location hints")
                break
            hint_location = sometimes_locations.pop()
        hint_locations.append(hint_location)
        generate_location_hint_message(hint_location)
        logging.getLogger("").debug(
            f'Chose "{hint_location}" as location hint location'
        )


def _process_hint_plurality(hint_text: str, is_plural: bool) -> str:
    plural_start_index = hint_text.index("|")
    plural_end_index = hint_text.index("|", plural_start_index + 1)

    # Removes the pipes as well
    plural_substring = hint_text[plural_start_index + 1 : plural_end_index]
    plural_substring_parts = plural_substring.split("/")
    plural_substring_final = (
        plural_substring_parts[1] if is_plural else plural_substring_parts[0]
    )

    hint_text = (
        hint_text[:plural_start_index]
        + plural_substring_final
        + hint_text[plural_end_index + 1 :]
    )

    return hint_text


def generate_path_hint_message(location: Location, goal_location: Location) -> None:
    hint_regions = list(
        set(
            [
                region
                for la in location.loc_access_list
                for region in la.area.hint_regions
            ]
        )
    )
    hint_regions.sort()
    hint_region_text = make_text_listing(
        [
            get_text_data(region, "pretty").apply_text_color("b")
            for region in hint_regions
        ]
    )

    goal_name_text = get_text_data(goal_location.name, "goal_name").apply_text_color(
        "r"
    )
    full_text = (
        get_text_data("Path Hint")
        .replace("<regions>", hint_region_text)
        .replace("<goal_name>", goal_name_text)
    )

    # Handle plurality
    for lang in full_text.SUPPORTED_LANGUAGES:
        if full_text.text[lang] != "" and "|" in full_text.text[lang]:
            full_text.text[lang] = _process_hint_plurality(
                full_text.text[lang], len(hint_regions) > 1
            )

    location.hint.text = full_text
    location.hint.type = "Path"


def generate_barren_hint_message(location: Location, barren_region: Text) -> None:
    location.hint.text = get_text_data("Barren Hint").replace("<region>", barren_region)
    location.hint.type = "Barren"


def generate_item_hint_message(location: Location) -> None:
    world = location.world
    # Convert to set and back to list to get rid of duplicates
    hint_regions = list(
        set(
            [
                region
                for la in location.loc_access_list
                for region in la.area.hint_regions
            ]
        )
    )
    hint_regions.sort()
    # Convert to Text objects
    hint_regions = [
        get_text_data(region, "pretty").apply_text_color("b+")
        for region in hint_regions
    ]
    hint_region_text = make_text_listing(hint_regions)

    type_ = "cryptic" if world.setting("cryptic_hint_text") == "on" else "pretty"
    item_text_color = "r" if type_ == "pretty" else ""
    item_text = get_text_data(location.current_item.name, type_).apply_text_color(
        item_text_color
    )

    full_text = (
        get_text_data("Item Hint")
        .replace("<item_pretty_or_cryptic_name>", item_text)
        .replace("<regions>", hint_region_text)
    )

    # Handle plurality
    for lang in full_text.SUPPORTED_LANGUAGES:
        if full_text.text[lang] != "" and "|" in full_text.text[lang]:
            full_text.text[lang] = _process_hint_plurality(
                full_text.text[lang], item_text.is_plural(lang)
            )

    location.hint.text = full_text
    location.hint.type = "Item"


def generate_location_hint_message(location: Location) -> None:
    type_ = (
        "cryptic" if location.world.setting("cryptic_hint_text") == "on" else "pretty"
    )
    color = "r" if type_ == "pretty" else ""
    item = location.current_item

    location_text = get_text_data(location.name, type_).apply_text_color(color)
    item_text = get_text_data(item.name, type_).apply_text_color(color)

    full_text = (
        get_text_data("Location Hint")
        .replace("<location_pretty_or_cryptic_name>", location_text)
        .replace("<item_pretty_or_cryptic_name>", item_text)
    )

    # Handle plurality
    for lang in full_text.SUPPORTED_LANGUAGES:
        if full_text.text[lang] != "" and "|" in full_text.text[lang]:
            full_text.text[lang] = _process_hint_plurality(
                full_text.text[lang], item_text.is_plural(lang)
            )

    location.hint.text = full_text
    location.hint.type = "Location"


def assign_gossip_stone_hints(
    world: World, worlds: list[World], hint_locations: list[Location]
) -> None:
    logging.getLogger("").debug(f"Assigning hints to gossip stones for {world}")
    random.shuffle(hint_locations)

    gossip_stone_locations = world.get_gossip_stones()
    hints_per_stone = math.ceil(len(hint_locations) / len(gossip_stone_locations))

    # Keep trying to place hints until all have been logically placed
    # at least once
    successfully_placed_hints = False
    retry_count = 50
    while not successfully_placed_hints:
        retry_count -= 1
        if retry_count < 0:
            raise RuntimeError(
                "Failed to properly place gossip stone hints. Try using a different seed for generation."
            )

        random.shuffle(hint_locations)
        successfully_placed_hints = True
        for stone in gossip_stone_locations:
            world.gossip_stone_hints[stone] = []

        for location in hint_locations:
            # Remove this item from the world and see which gossip stones
            # are available to place hints
            item_at_location = location.current_item
            location.remove_current_item()

            # Get all available gossip stones for this hint.
            search = Search(SearchMode.ACCESSIBLE_LOCATIONS, worlds)
            search.search_worlds()
            available_gossip_stones = [
                stone
                for stone in gossip_stone_locations
                if stone in search.visited_locations
                and len(world.gossip_stone_hints[stone]) < hints_per_stone
            ]

            if not available_gossip_stones:
                logging.getLogger("").debug(
                    f"No available stones to place hint for {location}"
                )
                location.set_current_item(item_at_location)
                successfully_placed_hints = False
                break

            # Place the hint at the gossip stone
            gossip_stone = random.choice(available_gossip_stones)
            world.gossip_stone_hints[gossip_stone].append(location)
            logging.getLogger("").debug(f'"{gossip_stone}" now hints to {location}')

            location.set_current_item(item_at_location)

    # Once we've placed every hint at least once, duplicate hints
    # and place them randomly until all gossip stones have the
    # necessary number of hints. Don't check for logic here since
    # every hint can already be logically accessed at some stone
    duplicate_hints = hint_locations.copy()
    available_gossip_stones = [
        stone
        for stone, hints in world.gossip_stone_hints.items()
        if len(hints) < hints_per_stone
    ]
    random.shuffle(available_gossip_stones)
    while available_gossip_stones:
        # Reset the pool of duplicate hints if we run out.
        # This way we'll duplicate every hint at least n times
        # before potentially duplicating each hint n + 1 times
        if not duplicate_hints:
            duplicate_hints = hint_locations.copy()

        hint = duplicate_hints.pop()
        stone = next(
            (
                stone
                for stone in available_gossip_stones
                if hint not in world.gossip_stone_hints[stone]
            ),
            None,
        )

        if stone is None:
            logging.getLogger("").debug(
                f"Could not find any gossip stones to hint at {hint}. Trying a different hint."
            )
            continue

        world.gossip_stone_hints[stone].append(hint)
        logging.getLogger("").debug(f"Duplicating hint for {hint} to {stone}")

        # Remove stone from available stones if we've given it the
        # necessary number of hints
        if len(world.gossip_stone_hints[stone]) == hints_per_stone:
            available_gossip_stones.remove(stone)


def generate_impa_sot_hint(world: World) -> None:
    # Return if not generating an impa hint
    if world.setting("impa_sot_hint") == "off":
        return

    sot_location = next(
        (
            loc
            for loc in world.get_all_item_locations()
            if loc.current_item == world.get_item("Stone of Trials")
        ),
        None,
    )

    # If there's no location for the stone of trials, then don't make a hint
    if sot_location is None:
        return

    # All regions that lead to the sot location
    sot_regions = list(
        set(
            [
                region
                for la in sot_location.loc_access_list
                for region in la.area.hint_regions
            ]
        )
    )
    sot_regions.sort()
    sot_regions_text = make_text_listing(
        [
            get_text_data(region, "pretty").apply_text_color("b+")
            for region in sot_regions
        ]
    )

    impa_hint = Hint()
    impa_hint.type = "Impa"
    impa_hint.text = get_text_data("Impa SoT Text").replace(
        "<regions>", sot_regions_text
    )

    world.impa_sot_hint = impa_hint
    logging.getLogger("").debug(f'Created Impa Hint: "{impa_hint}"')


def generate_song_hints(world: World, hint_locations: list[Location]) -> None:
    # If we're not generating song hints, don't do anything
    if world.setting("song_hints") == "off":
        return

    # If trial gates are shuffled and mixed, then don't generate any song hints
    if world.setting("randomize_trial_gate_entrances") == "on":
        for pool in world.setting_map.mixed_entrance_pools:
            if "Trial Gate" in pool and len(pool) > 1:
                return

    logging.getLogger("").debug("Generating Song Hints")

    # Mapping of song item to trial gate entrance
    trial_gate_entrances = {
        "Song of the Hero": "Central Skyloft -> The Goddess's Silent Realm",
        "Farore's Courage": "Faron Woods -> Farore's Silent Realm",
        "Din's Power": "Volcano Ascent -> Din's Silent Realm",
        "Nayru's Wisdom": "Lanayru Desert North -> Nayru's Silent Realm",
    }

    # Mapping of song item to locations in associated silent realm
    trial_gate_locations: dict[Item, list[Location]] = {}

    # Gather all the locations for each song
    for song_name, entrance_name in trial_gate_entrances.items():
        song = world.get_item(song_name)
        trial_gate_locations[song] = []
        entrance = world.get_entrance(entrance_name)
        silent_realm = (
            entrance.connected_area
            if entrance.connected_area
            else world.get_area(entrance_name.split(" -> ")[1])
        )
        for loc_access in silent_realm.locations:
            trial_gate_locations[song].append(loc_access.location)
            loc_access.location.is_hinted = True

    # Generate hint text depending on setting and what items are in the silent realm
    for song, locations in trial_gate_locations.items():
        world.song_hints[song] = Hint()
        hint = world.song_hints[song]
        hint.type = "Song"
        match world.setting("song_hints"):
            case "basic":
                # If there are any major items in the silent realm
                if any([loc for loc in locations if loc.current_item.is_major_item]):
                    hint.text = get_text_data("Trial Useful")
                else:
                    hint.text = get_text_data("Trial Useless")

            case "advanced":
                # If there are any items on the path to Demise
                if any(
                    [
                        loc
                        for loc in locations
                        if loc
                        in world.path_locations[
                            world.get_location("Hylia's Realm - Defeat Demise")
                        ]
                    ]
                ):
                    hint.text = get_text_data("Trial Required")
                # If there are any major items in the silent realm
                elif any([loc for loc in locations if loc.current_item.is_major_item]):
                    hint.text = get_text_data("Trial Useful")
                else:
                    hint.text = get_text_data("Trial Useless")

            case "direct":
                useful_locations = [
                    loc for loc in locations if loc.current_item.is_major_item
                ]
                if not useful_locations:
                    hint.text = get_text_data("Trial Direct Nothing")
                else:
                    # There's only enough text space to hint at one full item name, so calculate which item
                    # is the most logically useful among the set and display that item name. The most logically
                    # useful item is whichever item blocks the most checks.
                    most_useful_location = None
                    # Keep track of the least amount of locations unlocked so far
                    unlocked_locations = len(world.location_table) + 1
                    for location in useful_locations:
                        item_at_location = location.current_item
                        location.remove_current_item()

                        search = Search(SearchMode.ACCESSIBLE_LOCATIONS, world.worlds)
                        search.search_worlds()
                        # If removing the item at this location leads to fewer unlocked
                        # locations, then it's the most logically useful
                        visisted_progression_locations = [
                            loc for loc in search.visited_locations if loc.progression
                        ]
                        if (
                            len(visisted_progression_locations) < unlocked_locations
                            or most_useful_location is None
                        ):
                            most_useful_location = location
                            unlocked_locations = len(visisted_progression_locations)

                        location.set_current_item(item_at_location)

                    first_item_text = get_text_data(
                        f"{most_useful_location.current_item.name}", "pretty"
                    ).apply_text_color("r")
                    # If there are still more useful locations in the silent realm, then list how many there are
                    if len(useful_locations) == 1:
                        hint_text_to_append = get_text_data("Trial Direct One").replace(
                            "<item>", first_item_text
                        )
                    elif len(useful_locations) == 2:
                        hint_text_to_append = get_text_data("Trial Direct Two").replace(
                            "<item>", first_item_text
                        )
                    else:
                        useful_locations.remove(most_useful_location)
                        hint_text_to_append = (
                            get_text_data("Trial Direct Three Plus")
                            .replace("<item>", first_item_text)
                            .replace("%d", str(len(useful_locations)))
                        )

                    # Handle plurality
                    for lang in hint_text_to_append.SUPPORTED_LANGUAGES:
                        if (
                            hint_text_to_append.text[lang] != ""
                            and "|" in hint_text_to_append.text[lang]
                        ):
                            hint_text_to_append.text[lang] = _process_hint_plurality(
                                hint_text_to_append.text[lang],
                                first_item_text.is_plural(lang),
                            )

                    hint.text += hint_text_to_append

        logging.getLogger("").debug(f'Generated hint "{hint.text}" for song {song}')


def locations_are_all_junk(locations: list[Location]) -> bool:
    return all([not loc.current_item.is_major_item for loc in locations])


def get_hintable_location(locations: list[Location]) -> Location | None:
    for location in locations:
        if not location.is_hinted:
            return location
    return None
