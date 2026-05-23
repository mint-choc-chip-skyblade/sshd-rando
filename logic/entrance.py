from .requirements import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .area import Area
    from .world import World


class Entrance:
    sort_counter: int = 1

    NON_ASSUMED_ENTRANCE_TYPES = [
        "Spawn",
        "Faron Region Entrance",
        "Eldin Region Entrance",
        "Lanayru Region Entrance",
    ]

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
        self.original_name: str = self.current_name()
        self.alias: str = self.original_name

        self.requirement: Requirement = requirement_
        self.world: "World" = world_

        self.exit_infos = []
        self.spawn_info = {}
        self.secondary_exit_infos = []
        self.secondary_spawn_info = {}
        self.can_start_at: bool = True

        # Variables used for entrance shuffling
        self.shuffled: bool = False
        self.decoupled: bool = False
        self.disabled: bool = False

        # Primary entrances are those that we think of as
        # "going into" areas. Entering dungeons, entering trials,
        # and entering doors are all primary entrances. The opposite
        # idea, "leaving" areas, are not primary entrances.
        self.primary: bool = False

        # The reverse is the entrance that sends the player in the
        # natural opposite direction of this entrance. The reverse entrance
        # of entering a trial would be the entrance that leaves the trial
        self.reverse: Entrance = None

        # If the entrance is shuffled, self.replaces is the target entrance that replaces
        # this one. If this *is* a target entrance, then self.replaces holds the
        # entrance that this target *corresponds* to.
        self.replaces: Entrance = None

        # If the entrance is shuffled, self.assumed is the target entrance that *corresponds*
        # to this one. So if the entrance is Central Skyloft -> Goddess's Silent Realm,
        # then self.assumed is the target entrance Root -> Goddess's Silent Realm
        self.assumed: Entrance = None

        # Used to sort shuffled entrances in an intuitive order
        # Only potentially shuffled entrances will have a sort priority set
        self.sort_priority: int = 0

        # Additional Entrances that can only be allowed if this entrance is vanilla
        self.conditional_vanilla_connections: list["Entrance"] = []

        # Tracker variables
        self.computed_requirement: Requirement = Requirement(RequirementType.IMPOSSIBLE)

    def current_name(self) -> str:
        return f"{self.parent_area} -> {self.connected_area}"

    def alias_connected_area(self) -> str:
        return self.alias.split(" -> ")[1]

    def alias_parent_area(self) -> str:
        return self.alias.split(" -> ")[0]

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
        if new_connected_area == self.original_connected_area:
            for entrance in self.conditional_vanilla_connections:
                entrance.connect(entrance.original_connected_area)

    def disconnect(self) -> "Area":
        self.connected_area.entrances.remove(self)
        previously_connected = self.connected_area
        self.connected_area = None
        for entrance in self.conditional_vanilla_connections:
            if entrance.connected_area:
                entrance.disconnect()
        return previously_connected

    def bind_two_way(self, return_entrance: "Entrance") -> None:
        self.reverse = return_entrance
        return_entrance.reverse = self

    # Create a new target entrance that corresponds to where this one
    # leads, and attach it to the root of the world graph.
    def get_new_target(self) -> "Entrance":
        target_entrance = Entrance(
            self.world.root, None, Requirement(RequirementType.NOTHING), self.world
        )
        self.world.root.exits.append(target_entrance)
        target_entrance.connect(self.connected_area)
        target_entrance.replaces = self
        target_entrance.alias = self.alias
        return target_entrance

    # Create this entrance's target and disconnect the original entrance
    # This assumes reachable access to the entrance for the entrance shuffling
    # algorithm.
    def assume_reachable(self) -> "Entrance":
        if self.assumed == None:
            self.assumed = self.get_new_target()
            self.disconnect()
        return self.assumed
