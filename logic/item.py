
class Item:
    def __init__(self, id_: int = -1, name_: str = None, world_ = None, major_item_: bool = False, game_winning_item_: bool = False) -> None:
        self.id: int = id_
        self.name: str = name_
        self.world = world_
        self.is_major_item: bool = major_item_
        self.is_game_winning_item: bool = game_winning_item_

    def __str__(self) -> str:
        return self.name
    
    def __eq__(self, other) -> bool:
        if other == None:
            return False
        return self.id == other.id and self.world.id == other.world.id
    
    def __hash__(self) -> int:
        return (self.id, self.world.id).__hash__()