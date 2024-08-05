from logic.requirements import Requirement, RequirementType
from .item import Item
from .hint_class import Hint

import logging
from typing import TYPE_CHECKING

from constants.itemconstants import GRATITUDE_CRYSTAL

if TYPE_CHECKING:
    from .world import World
    from .area import LocationAccess


class Location:
    def __init__(
        self,
        id_: int,
        name_: str,
        types_: list[str],
        is_gui_excluded_location_: bool,
        world_: "World",
        original_item_: Item,
        patch_paths_: list[str],
        goal_location_: bool,
        hint_priority_: str,
        hint_textfile_: str,
        hint_textindex_: int,
        eventflowindex_: int,
    ) -> None:
        self.id: int = id_
        self.name: str = name_
        self.types: list[str] = types_
        self.is_gui_excluded_location: bool = is_gui_excluded_location_
        self.world: "World" = world_
        self.original_item: Item = original_item_
        self.patch_paths: list[str] = patch_paths_
        self.is_goal_location = goal_location_
        self.current_item: Item = None
        self.has_known_vanilla_item: bool = False
        self.loc_access_list: list["LocationAccess"] = []
        self.progression: bool = True  # Set as False later if applicable
        self.is_hinted: bool = False
        self.hint: Hint = Hint()
        self.hint_priority: str = hint_priority_
        self.hint_textfile: str = hint_textfile_
        self.hint_textindex: int = hint_textindex_
        self.hint_importance_text: str = ""
        self.eventflowindex: int = eventflowindex_

        # Tracker variables
        self.marked: bool = False
        self.eud_progression: bool = True
        self.in_semi_logic: bool = False
        self.sphere: int = None
        self.tracked_item: Item = None
        self.tracked_item_image: str = None
        self.computed_requirement: Requirement = Requirement(RequirementType.IMPOSSIBLE)

    def __str__(self) -> str:
        return (
            self.name
            if self.world.num_worlds == 1
            else f"{self.name} [W{self.world.id + 1}]"
        )

    def __lt__(self, other) -> bool:
        return (
            self.id < other.id
            if self.world.id == other.world.id
            else self.world.id < other.world.id
        )

    def is_empty(self) -> bool:
        return self.current_item == None

    def set_current_item(self, item: Item):
        logging.getLogger("").debug(f"Placed {item} at {self}")
        self.current_item = item

    def remove_current_item(self):
        logging.getLogger("").debug(f"Removed {self.current_item} from {self}")
        self.current_item = None

    def get_goal_name(self, language: str) -> str:
        return self.get_text_data(self.name, "goal_name", language)

    def has_vanilla_gratitude_crystal(self) -> bool:
        return (
            self.has_known_vanilla_item and self.original_item.name == GRATITUDE_CRYSTAL
        )

    def has_vanilla_goddess_cube(self) -> bool:
        return self.has_known_vanilla_item and "Goddess Cube" in self.original_item.name

    def is_gossip_stone(self) -> bool:
        return self.hint_textfile != ""

    def has_vanilla_dungeon_key(self) -> bool:
        return (
            self.has_known_vanilla_item
            and self.original_item.name.endswith("Small Key")
            and self.original_item.name != "Lanayru Caves Small Key"
        )
