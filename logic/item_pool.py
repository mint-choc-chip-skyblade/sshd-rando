from constants.itemconstants import *
from .settings import *
from .item import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import World


class ItemPoolError(RuntimeError):
    pass


# Generates the item pool for a single world
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

    # Remove Key Pieces if the ET Door is open
    if world.setting("open_earth_temple") == "on":
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

    for item_name in item_pool:
        if item_name in VANILLA_RANDOM_ITEM_TABLE:
            item_name = random.choice(VANILLA_RANDOM_ITEM_TABLE[item_name])

        item = world.get_item(item_name)

        if (
            world.setting("random_bottle_contents") == "on"
            and item_name in BOTTLE_ITEMS
        ):
            item = world.get_item(random.choice(BOTTLE_ITEMS))
        elif item_name in BOTTLE_ITEMS:
            # Assign vanilla bottle contents
            if (
                world.item_pool[
                    revitalizing_potion := world.get_item(REVITALIZING_POTION)
                ]
                == 0
            ):
                item = revitalizing_potion
            elif (
                world.item_pool[mushroom_spores := world.get_item(MUSHROOM_SPORES)] == 0
            ):
                item = mushroom_spores

        world.item_pool[item] += 1


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

        if item_name == EMPTY_BOTTLE:
            world.starting_item_pool[item] += count

            while count > 0:
                bottle_item_name = random.choice(BOTTLE_ITEMS)

                if world.item_pool[world.get_item(bottle_item_name)] > 0:
                    world.item_pool[world.get_item(bottle_item_name)] -= 1
                    count -= 1
            continue

        world.starting_item_pool[item] += count
        world.item_pool[item] -= count


def get_random_junk_item_name() -> str:
    random_junk_item = random.choice(
        (
            BLUE_RUPEE,
            RED_RUPEE,
            SILVER_RUPEE,
            FIVE_BOMBS,
            FIVE_DEKU_SEEDS,
            TEN_ARROWS,
            COMMON_TREASURE,
            UNCOMMON_TREASURE,
            RARE_TREASURE,
        )
    )

    if random_junk_item in VANILLA_RANDOM_ITEM_TABLE:
        random_junk_item = random.choice(VANILLA_RANDOM_ITEM_TABLE[random_junk_item])

    return random_junk_item


def get_complete_item_pool(worlds: list["World"]) -> list[Item]:
    complete_item_pool: list[Item] = []
    for world in worlds:
        for item, count in world.item_pool.items():
            complete_item_pool.extend([item] * count)
    return complete_item_pool
