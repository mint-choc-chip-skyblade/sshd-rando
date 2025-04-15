from typing import TYPE_CHECKING

from constants.itemconstants import (
    GRATITUDE_CRYSTAL,
    GRATITUDE_CRYSTAL_PACK,
    PROGRESSIVE_WALLET,
    EXTRA_WALLET,
    BOTTLE_ITEMS,
)

if TYPE_CHECKING:
    from .world import World
    from .location import Location


class Item:
    def __init__(
        self,
        id_: int = -1,
        name_: str = None,
        oarcs_: list[str] = [],
        shop_arc_name_: str = None,
        shop_model_name_: str = None,
        world_: "World" = None,
        major_item_: bool = False,
        game_winning_item_: bool = False,
        goddess_chest_: str = None,
    ) -> None:
        self.id: int = id_
        self.name: str = name_
        self.oarcs: list[str] = oarcs_
        self.shop_arc_name: str = shop_arc_name_
        self.shop_model_name: str = shop_model_name_
        self.world: "World" = world_
        self.is_major_item: bool = major_item_
        self.is_game_winning_item: bool = game_winning_item_
        self.goddess_chest: str = goddess_chest_
        self.chain_locations: set["Location"] = set()
        self.was_always_junk: bool = not major_item_

        self.is_dungeon_small_key: bool = (
            " Small Key" in name_ and name_ != "Lanayru Caves Small Key"
        )
        self.is_boss_key: bool = " Boss Key" in name_
        self.is_dungeon_map: bool = " Map" in name_

    def get_goddess_chest(self) -> "Location":
        return self.world.get_location(self.goddess_chest)

    def can_be_in_barren_region(self) -> bool:
        return (
            not self.is_major_item
            or (
                self.is_dungeon_small_key
                and self.world.setting("small_keys").is_any_of("vanilla", "own_dungeon")
            )
            or (
                self.is_boss_key
                and self.world.setting("boss_keys").is_any_of("vanilla", "own_dungeon")
            )
            or (
                self.name == GRATITUDE_CRYSTAL
                and self.world.setting("gratitude_crystal_shuffle") == "off"
            )
        )

    def is_same_or_similar_item(self, other_item: "Item") -> bool:
        if self == other_item:
            return True

        # Gratitude Crystals
        gratitude_crystal_items = {
            self.world.get_item(GRATITUDE_CRYSTAL_PACK),
            self.world.get_item(GRATITUDE_CRYSTAL),
        }
        if self in gratitude_crystal_items and other_item in gratitude_crystal_items:
            return True

        # Wallets
        wallet_items = {
            self.world.get_item(PROGRESSIVE_WALLET),
            self.world.get_item(EXTRA_WALLET),
        }
        if self in wallet_items and other_item in wallet_items:
            return True

        # Bottles
        bottle_items = {self.world.get_item(bottle) for bottle in BOTTLE_ITEMS}
        if self in bottle_items and other_item in bottle_items:
            return True

        return False

    def __str__(self) -> str:
        return (
            self.name
            if self.world.num_worlds == 1
            else f"{self.name} [W{self.world.id + 1}]"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other) -> bool:
        if other == None:
            return False
        return self.id == other.id and self.world.id == other.world.id

    def __lt__(self, other) -> bool:
        if other == None:
            return False
        if self.world.id != other.world.id:
            return self.world.id < other.world.id
        return self.id < other.id

    def __hash__(self) -> int:
        return (self.id, self.world.id).__hash__()
