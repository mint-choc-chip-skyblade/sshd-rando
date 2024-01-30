from typing import Union
from PySide6.QtCore import QModelIndex, QPersistentModelIndex
from gui.models.searchable_list_model import SearchableListModel


class TypeFilterModel(SearchableListModel):
    def __init__(
        self,
        parent,
        full_list,
        full_data_dict: dict[str, list[str]],
        excluder_list: list[str] = [],
    ):
        super().__init__(parent, full_list)
        self.full_data_dict = full_data_dict
        self.type_filter: str = ""
        self.excluder_list = excluder_list

    def filterAcceptsRow(
        self, source_row: int, source_parent: Union[QModelIndex, QPersistentModelIndex]
    ) -> bool:
        index = self.sourceModel().index(source_row, 0, source_parent)
        name = self.sourceModel().data(index)

        if self.type_filter and not self.type_filter == "All":
            if name in self.full_data_dict:
                data_types = self.full_data_dict[name]

                if data_types is None or self.type_filter not in data_types:
                    return False

        if name in self.excluder_list:
            return False

        return super().filterAcceptsRow(source_row, source_parent)

    def filterType(self, type_filter: str):
        self.type_filter = type_filter
        self.invalidateFilter()

    def update_excluder_list(self, new_excluder_list: list[str]):
        self.excluder_list = new_excluder_list
