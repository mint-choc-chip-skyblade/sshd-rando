
from logic.location import *
from logic.entrance import *
from logic.requirements import TOD

# Helper class to link locations with their requirements
# in a specific area. We don't want to tie requirements
# to the Location class directly since some locations can
# be accessed from multiple areas
class LocationAccess:
    id_counter: int = 0
    def __init__(self, location_: Location, req_: Requirement, area_) -> None:
        self.location: Location = location_
        self.req: Requirement = req_
        self.area = area_
        self.id = self.id_counter
        self.id_counter += 1

# Same for events
class EventAccess:
    def __init__(self, id_: int, req_: Requirement, area_) -> None:
        self.id: int = id_
        self.req: Requirement = req_
        self.area = area_

class Area:
    def __init__(self) -> None:
        self.id: int = None
        self.name: str = None
        self.hint_regions : list[str] = []
        self.events: list[EventAccess] = []
        self.locations: list[LocationAccess] = []
        self.exits: list[Entrance] = []
        self.entrances: list[Entrance] = []
        self.world = None
        self.allowed_tod: int = TOD.ALL # All by default, will set to day only if natural night connections are enforced
        self.can_sleep: bool = False

    def __str__(self) -> str:
        return self.name