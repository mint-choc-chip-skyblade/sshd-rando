from typing import Union
from PySide6.QtCore import QSortFilterProxyModel, QModelIndex, QPersistentModelIndex, Qt


class SearchableListModel(QSortFilterProxyModel):
    def __init__(self, parent, full_list):
        super().__init__(parent)
        self.free_text_filter = ""
        self.full_list = full_list
        self.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

    def lessThan(self, right, left):
        leftCheck = self.sourceModel().data(left)
        rightCheck = self.sourceModel().data(right)
        if rightCheck == "":
            return False
        return self.full_list.index(leftCheck) > self.full_list.index(rightCheck)

    def filterAcceptsRow(
        self, source_row: int, source_parent: Union[QModelIndex, QPersistentModelIndex]
    ) -> bool:
        index = self.sourceModel().index(source_row, 0, source_parent)
        return self.free_text_filter.lower() in self.sourceModel().data(index).lower()

    def filterRows(self, free_text_filter):
        self.free_text_filter = free_text_filter
        self.invalidateFilter()
