from .requirements import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .area import Area
    from .world import World

class Entrance:
    def __init__(
        self,
        parent_area_: 'Area' = None,
        connected_area_: 'Area' = None,
        requirement_: Requirement = None,
        world_: 'World' = None,
    ) -> None:
        self.parent_area: 'Area' = parent_area_
        self.connected_area: 'Area' = connected_area_
        self.original_connected_area: 'Area' = connected_area_
        self.type: str = None
        self.original_name: str = f"{parent_area_} -> {connected_area_}"

        self.requirement: Requirement = requirement_
        self.world: 'World' = world_

        # Variables used for entrance shuffling
        self.shuffled: bool = False
        self.primary: bool = False
        self.decoupled: bool = False
        self.disabled: bool = False
        self.reverse: Entrance = None
        self.replaces: Entrance = None
        self.assumed: Entrance = None

    def __str__(self) -> str:
        return self.original_name
