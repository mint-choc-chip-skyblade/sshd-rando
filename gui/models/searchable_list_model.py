from typing import Union
from PySide6.QtCore import QSortFilterProxyModel, QModelIndex, QPersistentModelIndex, Qt


class SearchableListModel(QSortFilterProxyModel):
    def __init__(self, parent, full_list: list[str]):
        super().__init__(parent)
        self.free_text_filter = ""
        self.full_list = full_list
        self.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.sort(0)

    def lessThan(self, right, left):
        left_check = self.sourceModel().data(left)
        right_check = self.sourceModel().data(right)

        if right_check == "":
            return False

        return self.full_list.index(left_check) > self.full_list.index(right_check)

    def filterAcceptsRow(
        self, source_row: int, source_parent: Union[QModelIndex, QPersistentModelIndex]
    ) -> bool:
        index = self.sourceModel().index(source_row, 0, source_parent)
        return self.free_text_filter.lower() in self.sourceModel().data(index).lower()

    def filterRows(self, free_text_filter):
        self.free_text_filter = free_text_filter
        self.invalidateFilter()
