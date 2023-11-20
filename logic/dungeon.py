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
        self.world: "World" = None
        self.small_key: Item = None
        self.boss_key: Item = None
        self.map: Item = None

    def __str__(self) -> str:
        return self.name

    def should_be_barren(self):
        return (
            not self.required
            and self.world.setting("empty_unrequired_dungeons") == "on"
        )
