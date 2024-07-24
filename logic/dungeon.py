from .location import Location
from .area import Area
from .entrance import Entrance
from .item import Item
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import World


class Dungeon:
    def __init__(self) -> None:
        self.name = ""
        self.locations: list[Location] = []
        self.goal_location: Location = None
        self.starting_area: Area = None
        self.starting_entrance: Entrance = None
        self.required = False
        self.required_reasons = ""
        self.unrequired_reasons = ""
        self.world: "World" = None
        self.small_key: Item = None
        self.boss_key: Item = None
        self.map: Item = None

    def __str__(self) -> str:
        return self.name

    def should_be_barren(self) -> bool:
        # If Sky Keep is explicitly disabled it should always be barren regardless of other settings.
        if (
            self.name == "Sky Keep"
            and self.world.setting("dungeons_include_sky_keep") == "off"
        ):
            return True

        return (
            not self.required
            and self.world.setting("empty_unrequired_dungeons") == "on"
        )

    def goal_location_has_non_major_item(self) -> bool:
        return (
            not self.goal_location.is_empty()
            and not self.goal_location.current_item.is_major_item
        )

    def goal_location_has_major_item(self) -> bool:
        return (
            not self.goal_location.is_empty()
            and self.goal_location.current_item.is_major_item
        )

    def has_any_major_items(self) -> bool:
        for loc in self.locations:
            if (
                not loc.is_empty()
                and loc.current_item.is_major_item
                and not loc.has_known_vanilla_item
            ):
                return True
        return False
