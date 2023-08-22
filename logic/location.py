from .item import Item
from .requirements import Requirement

import logging

class Location:
    def __init__(self, id_: int, name_: str, types_: list[str], world_, original_item_ : Item) -> None:
        self.id: int = id_
        self.name: str = name_
        self.types: list[str] = types_
        self.world = world_
        self.original_item = original_item_
        self.current_item: Item = None
        self.loc_access_list: list = []


    def __str__(self) -> str:
        return self.name if self.world.num_worlds == 1 else f"{self.name} [W{self.world.id + 1}]"
    
    def __lt__(self, other) -> bool:
        return self.id < other.id if self.world.id == other.world.id else self.world.id < other.world.id 

    def is_empty(self) -> bool:
        return self.current_item == None
    
    
    def set_current_item(self, item: Item):
        logging.getLogger('').debug(f"Placed {item} at {self}")
        self.current_item = item


    def remove_current_item(self):
        logging.getLogger('').debug(f"Removed {self.current_item} at {self}")
        self.current_item = None