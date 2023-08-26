from .location import Location
from .area import Area
from .entrance import Entrance


class Dungeon:
    def __init__(self) -> None:
        self.name = ""
        self.locations: list[Location] = []
        self.goal_locations: list[Location] = []
        self.starting_area: Area = None
        self.starting_entrance: Entrance = None

    def __str__(self) -> str:
        return self.name
