from typing import Union
from PySide6.QtCore import QModelIndex, QPersistentModelIndex
from gui.models.searchable_list_model import SearchableListModel


class LocationTypeFilterModel(SearchableListModel):
    def __init__(self, parent, full_list, full_data_list: list[dict]):
        super().__init__(parent, full_list)
        self.full_data_list = full_data_list
        self.type_filter: str = ""

    def filterAcceptsRow(
        self, source_row: int, source_parent: Union[QModelIndex, QPersistentModelIndex]
    ) -> bool:
        if self.type_filter and not self.type_filter == "All":
            index = self.sourceModel().index(source_row, 0, source_parent)
            name = self.sourceModel().data(index)

            location = [
                location for location in self.full_data_list if location["name"] == name
            ][0]

            if (
                location_type := location.get("type")
            ) is None or self.type_filter not in location_type:
                return False

        return super().filterAcceptsRow(source_row, source_parent)

    def filterType(self, type_filter: str):
        self.type_filter = type_filter
        self.invalidateFilter()
