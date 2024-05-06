from .requirements import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .area import Area
    from .world import World


class Entrance:
    sort_counter: int = 1

    def __init__(
        self,
        parent_area_: "Area" = None,
        connected_area_: "Area" = None,
        requirement_: Requirement = None,
        world_: "World" = None,
    ) -> None:
        self.parent_area: "Area" = parent_area_
        self.connected_area: "Area" = connected_area_
        self.original_connected_area: "Area" = connected_area_
        self.type: str = "None"
        self.original_type: str = "None"
        self.original_name: str = f"{parent_area_} -> {connected_area_}"

        self.requirement: Requirement = requirement_
        self.world: "World" = world_

        self.exit_infos = []
        self.spawn_info = {}
        self.secondary_exit_infos = []
        self.secondary_spawn_info = {}
        self.can_start_at: bool = True

        # Variables used for entrance shuffling
        self.shuffled: bool = False
        self.primary: bool = False
        self.decoupled: bool = False
        self.disabled: bool = False
        self.reverse: Entrance = None
        self.replaces: Entrance = None
        self.assumed: Entrance = None

        # Used to sort shuffled entrances in an intuitive order
        # Only potentially shuffled entrances will have a sort priority set
        self.sort_priority: int = 0

    def __str__(self) -> str:
        return self.original_name

    def __lt__(self, other: "Entrance") -> bool:
        if self.world.id != other.world.id:
            return self.world.id < other.world.id
        if self.sort_priority and other.sort_priority:
            return self.sort_priority < other.sort_priority
        if self.parent_area != other.parent_area:
            return self.parent_area < other.parent_area
        return self.connected_area < other.connected_area

    def disable(self) -> None:
        self.disabled = True

    def enable(self) -> None:
        self.disabled = False

    def connect(self, new_connected_area: "Area") -> None:
        self.connected_area = new_connected_area
        new_connected_area.entrances.append(self)

    def disconnect(self) -> "Area":
        self.connected_area.entrances.remove(self)
        previously_connected = self.connected_area
        self.connected_area = None
        return previously_connected

    def bind_two_way(self, return_entrance: "Entrance") -> None:
        self.reverse = return_entrance
        return_entrance.reverse = self

    def get_new_target(self) -> "Entrance":
        target_entrance = Entrance(
            self.world.root, None, Requirement(RequirementType.NOTHING), self.world
        )
        self.world.root.exits.append(target_entrance)
        target_entrance.connect(self.connected_area)
        target_entrance.replaces = self
        return target_entrance

    def assume_reachable(self) -> "Entrance":
        if self.assumed == None:
            self.assumed = self.get_new_target()
            self.disconnect()
        return self.assumed
