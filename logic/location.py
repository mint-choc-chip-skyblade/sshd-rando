from .item import Item
from .hint_class import Hint

import logging
from typing import TYPE_CHECKING

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
        self.eventflowindex: int = eventflowindex_

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
