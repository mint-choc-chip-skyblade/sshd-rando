from PySide6.QtCore import QObject, QStringListModel, Signal
from PySide6.QtWidgets import QListView, QPushButton

from gui.models.searchable_list_model import SearchableListModel
from gui.models.location_type_filter_model import LocationTypeFilterModel


class ListPair(QObject):
    listPairChanged = Signal(bool)

    def __init__(
        self,
        current_setting_list: list,
        settings_list_view: QListView,
        non_settings_list_view: QListView,
        add_button: QPushButton,
        remove_button: QPushButton,
        full_data_dict: list[dict] = [],
        setting_options_list: list = [],
    ):
        super().__init__()
        self.current_setting_list = current_setting_list
        self.settings_list_view = settings_list_view
        self.non_settings_list_view = non_settings_list_view
        self.has_type_filter = len(full_data_dict) > 0
        self.setting_options_list = [
            data_entry["name"] for data_entry in full_data_dict
        ]
        self._stored_filter_option_list = ""
        self._stored_filter_non_option_list = ""
        self._stored_type_filter_option_list = ""
        self._stored_type_filter_non_option_list = ""

        # Main list
        self.option_list_model = QStringListModel()

        if self.has_type_filter:
            self.option_list_proxy = LocationTypeFilterModel(
                self.settings_list_view, setting_options_list, full_data_dict
            )
        else:
            self.option_list_proxy = SearchableListModel(
                self.settings_list_view, self.setting_options_list
            )

        self.option_list_proxy.setSourceModel(self.option_list_model)
        self.option_list_model.setStringList(current_setting_list)
        self.settings_list_view.setModel(self.option_list_proxy)

        # Secondary List
        self.non_option_list_model = QStringListModel()

        if self.has_type_filter:
            self.non_option_list_proxy = LocationTypeFilterModel(
                self.non_settings_list_view, self.setting_options_list, full_data_dict
            )
        else:
            self.non_option_list_proxy = SearchableListModel(
                self.non_settings_list_view, self.setting_options_list
            )

        self.non_option_list_proxy.setSourceModel(self.non_option_list_model)
        self.non_option_list_model.setStringList(
            [
                option
                for option in self.setting_options_list
                if option not in current_setting_list
            ]
        )
        self.non_settings_list_view.setModel(self.non_option_list_proxy)

        add_button.clicked.connect(self.add)
        remove_button.clicked.connect(self.remove)

    def update_option_list_filter(self, new_text: str | None):
        self.option_list_proxy.filterRows(new_text)

    def update_option_list_type_filter(self, type_filter: str | None):
        self.option_list_proxy.filterType(type_filter)

    def update_non_option_list_filter(self, new_text: str | None):
        self.non_option_list_proxy.filterRows(new_text)

    def update_non_option_list_type_filter(self, type_filter: str | None):
        self.non_option_list_proxy.filterType(type_filter)

    def add(self):
        self.move_selected_rows(self.non_settings_list_view, self.settings_list_view)
        self.listPairChanged.emit(self.option_list_model.stringList())

    def remove(self):
        self.move_selected_rows(self.settings_list_view, self.non_settings_list_view)
        self.listPairChanged.emit(self.option_list_model.stringList())

    @staticmethod
    def append_row(model, value):
        model.insertRow(model.rowCount())
        new_row = model.index(model.rowCount() - 1, 0)
        model.setData(new_row, value)
        model.sort(0)

    def move_selected_rows(self, source: QListView, dest: QListView):
        self._store_and_remove_filters()

        selection = source.selectionModel().selectedIndexes()
        # Remove starting from the last so the previous indices remain valid
        selection.sort(reverse=True, key=lambda x: x.row())

        for item in selection:
            value = item.data()
            source.model().removeRow(item.row())
            self.append_row(dest.model(), value)

        self._restore_filters()

    def update(self, current_setting):
        self._store_and_remove_filters()

        not_chosen = self.setting_options_list.copy()

        for choice in current_setting:
            not_chosen.remove(choice)

        self.option_list_model.setStringList(current_setting)
        self.non_option_list_model.setStringList(not_chosen)
        self.settings_list_view.setModel(self.option_list_proxy)
        self.non_settings_list_view.setModel(self.non_option_list_proxy)

        self._restore_filters()

    def get_added(self) -> list:
        return self.option_list_model.stringList()

    def _store_and_remove_filters(self):
        self._stored_filter_option_list = self.option_list_proxy.free_text_filter
        self._stored_filter_non_option_list = (
            self.non_option_list_proxy.free_text_filter
        )
        self.option_list_proxy.filterRows("")
        self.non_option_list_proxy.filterRows("")

        if self.has_type_filter:
            self._stored_type_filter_option_list = self.option_list_proxy.type_filter
            self._stored_type_filter_non_option_list = (
                self.non_option_list_proxy.type_filter
            )
            self.option_list_proxy.filterType("")
            self.non_option_list_proxy.filterType("")

    def _restore_filters(self):
        self.option_list_proxy.filterRows(self._stored_filter_option_list)
        self.non_option_list_proxy.filterRows(self._stored_filter_non_option_list)

        if self.has_type_filter:
            self.option_list_proxy.filterType(self._stored_type_filter_option_list)
            self.non_option_list_proxy.filterType(
                self._stored_type_filter_non_option_list
            )
