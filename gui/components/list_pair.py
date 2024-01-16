from PySide6.QtCore import QObject, QStringListModel, Signal, QAbstractItemModel
from PySide6.QtWidgets import QListView, QPushButton

from gui.models.type_filter_model import TypeFilterModel


class ListPair(QObject):
    listPairChanged = Signal(bool)

    def __init__(
        self,
        current_setting_list: list,
        default_setting_list: list,
        settings_list_view: QListView,
        non_settings_list_view: QListView,
        add_button: QPushButton,
        remove_button: QPushButton,
        reset_button: QPushButton,
        typed_data_dict: dict[str, list[str]] = {},
        excluder_list: list[str] = [],
    ):
        super().__init__()
        self.current_setting_list = current_setting_list
        self.default_setting_list = default_setting_list
        self.settings_list_view = settings_list_view
        self.non_settings_list_view = non_settings_list_view
        self.typed_data = typed_data_dict
        self.setting_options_list: list[str] = [
            data_name for data_name in typed_data_dict
        ]
        self.excluder_list = excluder_list

        self._stored_filter_option_list = ""
        self._stored_filter_non_option_list = ""
        self._stored_type_filter_option_list = ""
        self._stored_type_filter_non_option_list = ""
        self._stored_excluder_list = []

        # Main list
        self.option_list_model = QStringListModel()
        self.option_list_proxy = TypeFilterModel(
            self.settings_list_view,
            self.setting_options_list,
            typed_data_dict,
            excluder_list,
        )

        self.option_list_proxy.setSourceModel(self.option_list_model)
        self.option_list_model.setStringList(current_setting_list)
        self.settings_list_view.setModel(self.option_list_proxy)

        # Secondary List
        self.non_option_list_model = QStringListModel()
        self.non_option_list_proxy = TypeFilterModel(
            self.non_settings_list_view,
            self.setting_options_list,
            typed_data_dict,
            excluder_list,
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
        reset_button.clicked.connect(self.reset)

    def update_option_list_filter(self, new_text: str | None):
        self.option_list_proxy.filterRows(new_text)

    def update_option_list_type_filter(self, type_filter: str):
        self.option_list_proxy.filterType(type_filter)

    def update_non_option_list_filter(self, new_text: str | None):
        self.non_option_list_proxy.filterRows(new_text)

    def update_non_option_list_type_filter(self, type_filter: str):
        self.non_option_list_proxy.filterType(type_filter)

    def add(self):
        self.move_selected_rows(self.non_settings_list_view, self.settings_list_view)
        self.listPairChanged.emit(self.option_list_model.stringList())

    def remove(self):
        self.move_selected_rows(self.settings_list_view, self.non_settings_list_view)
        self.listPairChanged.emit(self.option_list_model.stringList())

    def reset(self):
        self.update(self.default_setting_list)
        self.listPairChanged.emit(self.option_list_model.stringList())

    def update_excluder_list(self, new_excluder_list: list[str]):
        self.excluder_list = new_excluder_list
        self.option_list_proxy.update_excluder_list(new_excluder_list)
        self.non_option_list_proxy.update_excluder_list(new_excluder_list)
        self.option_list_proxy.invalidateFilter()
        self.non_option_list_proxy.invalidateFilter()

    @staticmethod
    def append_row(model: QAbstractItemModel, value):
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
        # A little more complex than *necessary* so that the config file
        # remains ordered correctly
        added_list = [
            added
            for added in self.option_list_proxy.full_list
            if added in self.option_list_model.stringList()
        ]
        return added_list

    def get_not_added(self) -> list:
        not_added_list = [
            added
            for added in self.option_list_proxy.full_list
            if added not in self.option_list_model.stringList()
        ]
        return not_added_list

    def _store_and_remove_filters(self):
        self._stored_filter_option_list = self.option_list_proxy.free_text_filter
        self._stored_filter_non_option_list = (
            self.non_option_list_proxy.free_text_filter
        )
        self.option_list_proxy.filterRows("")
        self.non_option_list_proxy.filterRows("")

        self._stored_type_filter_option_list = self.option_list_proxy.type_filter
        self._stored_type_filter_non_option_list = (
            self.non_option_list_proxy.type_filter
        )
        self.option_list_proxy.filterType("")
        self.non_option_list_proxy.filterType("")

        self._stored_excluder_list = self.excluder_list
        self.update_excluder_list([])

    def _restore_filters(self):
        self.option_list_proxy.filterRows(self._stored_filter_option_list)
        self.non_option_list_proxy.filterRows(self._stored_filter_non_option_list)

        self.option_list_proxy.filterType(self._stored_type_filter_option_list)
        self.non_option_list_proxy.filterType(self._stored_type_filter_non_option_list)

        self.update_excluder_list(self._stored_excluder_list)
