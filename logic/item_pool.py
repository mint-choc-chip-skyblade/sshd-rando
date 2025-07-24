from constants.itemconstants import *
from .settings import *
from .item import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import World


class ItemPoolError(RuntimeError):
    pass


# Generates the item pool for a single world.
# Items being placed in vanilla or restricted
# location sets will be filtered out later. Items
# that need to be removed and not placed anywhere
# will be removed now
def generate_item_pool(world: "World") -> None:
    item_pool = STANDARD_ITEM_POOL

    match world.setting("item_pool"):
        case "minimal":
            item_pool = MINIMAL_ITEM_POOL
        case "standard":
            item_pool = STANDARD_ITEM_POOL
        case "extra":
            item_pool = EXTRA_ITEM_POOL
        case "plentiful":
            item_pool = PLENTIFUL_ITEM_POOL

    # Needed otherwise the "constant" item pools above get editted as well.
    # Doesn't cause problems until multiple seeds are generated.
    item_pool = item_pool.copy()

    # Remove Key Pieces if the ET Door is open
    if world.setting("open_earth_temple") == "open":
        item_pool = [item for item in item_pool if item != KEY_PIECE]

    if world.setting("small_keys") == "removed":
        item_pool = [
            item
            for item in item_pool
            if not item.endswith(SMALL_KEY) or item == LC_SMALL_KEY
        ]

    if world.setting("lanayru_caves_keys") == "removed":
        item_pool = [item for item in item_pool if item != LC_SMALL_KEY]

    if world.setting("boss_keys") == "removed":
        item_pool = [item for item in item_pool if not item.endswith(BOSS_KEY)]

    # Add rupees and treasures to item pool based on the enabled locations.
    # Closets which don't have items in vanilla are set to have Green Rupees.
    # These rupees should be ignored as they would inflate their representation in the item pool.
    types_to_ignore = [
        "Closets",
    ]

    if world.setting("rupee_shuffle") == "intermediate":
        types_to_ignore.append("Advanced Rupees")
    elif world.setting("rupee_shuffle") == "beginner":
        types_to_ignore.append("Advanced Rupees")
        types_to_ignore.append("Intermediate Rupees")
    elif world.setting("rupee_shuffle") == "vanilla":
        types_to_ignore.append("Advanced Rupees")
        types_to_ignore.append("Intermediate Rupees")
        types_to_ignore.append("Beginner Rupees")

    if world.setting("underground_rupee_shuffle") == "off":
        types_to_ignore.append("Underground Rupees")

    if world.setting("hidden_item_shuffle") == "off":
        types_to_ignore.append("Hidden Items")

    if world.setting("goddess_chest_shuffle") == "off":
        types_to_ignore.append("Goddess Chests")

    test_counter = 0
    for loc_name in world.location_table:
        location = world.location_table[loc_name]

        # Filter out non-item locations like gossip stones
        if location.original_item is None:
            continue

        original_item = location.original_item.name

        if original_item in SHUFFLE_DEPENDENT_ITEMS:
            should_add_item_to_pool = True

            for loc_type in location.types:
                if loc_type in types_to_ignore:
                    should_add_item_to_pool = False
                    break

            if should_add_item_to_pool:
                item_pool.append(original_item)
                test_counter += 1

    # Add dusk relics equal to the number of enabled relic checks
    item_pool += (
        [DUSK_RELIC] * world.setting("trial_treasure_shuffle").value_as_number() * 4
    )

    for item_name in item_pool:
        if item_name in VANILLA_RANDOM_ITEM_TABLE:
            item_name = random.choice(VANILLA_RANDOM_ITEM_TABLE[item_name])

        item = world.get_item(item_name)
        world.item_pool[item] += 1

    # Output the item pool for debugging
    # print("Item Pool:")
    # for item in world.item_pool:
    #     print(f"\t{item.name}: {world.item_pool[item]}")


# Will remove items from the passed in world's item pool
# and add them to the starting pool.
def generate_starting_item_pool(world: "World"):
    starting_items = world.setting_map.starting_inventory.copy()

    # Add starting swords
    starting_sword_setting = world.setting_map.settings.get("starting_sword")

    if starting_sword_setting:
        starting_sword_value = starting_sword_setting.value
        starting_items[PROGRESSIVE_SWORD] = starting_sword_setting.info.options.index(
            starting_sword_value
        )

    # Deal with starting tablets
    starting_tablet_count = world.setting(
        "random_starting_tablet_count"
    ).value_as_number()

    if starting_tablet_count > 0:
        inventory_tablets = [
            item for item in world.setting_map.starting_inventory if item in ALL_TABLETS
        ]

        if len(inventory_tablets) + starting_tablet_count >= 3:
            for tablet in ALL_TABLETS:
                starting_items[tablet] = 1
        else:
            tablet_pool = [
                tablet for tablet in ALL_TABLETS if tablet not in inventory_tablets
            ]

            for _ in range(starting_tablet_count):
                random_tablet = random.choice(tablet_pool)
                tablet_pool.remove(random_tablet)
                starting_items[random_tablet] = 1

    # Random starting items
    random_starting_count = world.setting(
        "random_starting_item_count"
    ).value_as_number()

    if random_starting_count > 0:
        random_starting_item_pool = [
            item for item in RANDOM_STARTABLE_ITEMS if item not in starting_items
        ]

        for _ in range(random_starting_count):
            if len(random_starting_item_pool) < 1:
                break

            random_item = random.choice(random_starting_item_pool)
            starting_items[random_item] = starting_items[random_item] + 1
            random_starting_item_pool.remove(random_item)

    # Remove Heart Containers/Pieces for starting health
    extra_hearts = world.setting("starting_hearts").value_as_number() - 6
    for _ in range(extra_hearts):
        # First add heart containers to the starting inventory
        if starting_items[HEART_CONTAINER] < 6:
            starting_items[HEART_CONTAINER] += 1
        # Then add heart pieces in sets of 4
        else:
            starting_items[HEART_PIECE] += 4

    # Populate starting item pool
    for item_name, count in starting_items.items():
        item = world.get_item(item_name)
        world.starting_item_pool[item] += count
        world.item_pool[item] -= count


def get_random_junk_item_name() -> str:
    random_junk_item = random.choice(ALL_JUNK_ITEMS)

    if random_junk_item in VANILLA_RANDOM_ITEM_TABLE:
        random_junk_item = random.choice(VANILLA_RANDOM_ITEM_TABLE[random_junk_item])

    return random_junk_item


# Returns the complete item pool for all worlds in the passed
# in world list
def get_complete_item_pool(worlds: list["World"]) -> list[Item]:
    complete_item_pool: list[Item] = []
    for world in worlds:
        for item, count in world.item_pool.items():
            complete_item_pool.extend([item] * count)
    return complete_item_pool
