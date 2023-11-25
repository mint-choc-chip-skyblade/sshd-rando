# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFontComboBox, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QListView,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QVBoxLayout, QWidget)

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(1200, 800)
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.verticalLayout_2 = QVBoxLayout(self.central_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setTabShape(QTabWidget.Rounded)
        self.getting_started_tab = QWidget()
        self.getting_started_tab.setObjectName(u"getting_started_tab")
        self.verticalLayout_4 = QVBoxLayout(self.getting_started_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.how_to_group_box = QGroupBox(self.getting_started_tab)
        self.how_to_group_box.setObjectName(u"how_to_group_box")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.how_to_group_box.sizePolicy().hasHeightForWidth())
        self.how_to_group_box.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.how_to_group_box)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.how_to_extract_group_box = QGroupBox(self.how_to_group_box)
        self.how_to_extract_group_box.setObjectName(u"how_to_extract_group_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.how_to_extract_group_box.sizePolicy().hasHeightForWidth())
        self.how_to_extract_group_box.setSizePolicy(sizePolicy1)
        self.verticalLayout_5 = QVBoxLayout(self.how_to_extract_group_box)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.how_to_extract_label = QLabel(self.how_to_extract_group_box)
        self.how_to_extract_label.setObjectName(u"how_to_extract_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.how_to_extract_label.sizePolicy().hasHeightForWidth())
        self.how_to_extract_label.setSizePolicy(sizePolicy2)
        self.how_to_extract_label.setTextFormat(Qt.RichText)
        self.how_to_extract_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.how_to_extract_label.setWordWrap(True)
        self.how_to_extract_label.setOpenExternalLinks(True)
        self.how_to_extract_label.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse)

        self.verticalLayout_5.addWidget(self.how_to_extract_label)


        self.horizontalLayout_3.addWidget(self.how_to_extract_group_box)

        self.how_to_left_arrow_label = QLabel(self.how_to_group_box)
        self.how_to_left_arrow_label.setObjectName(u"how_to_left_arrow_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.how_to_left_arrow_label.sizePolicy().hasHeightForWidth())
        self.how_to_left_arrow_label.setSizePolicy(sizePolicy3)
        self.how_to_left_arrow_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.how_to_left_arrow_label)

        self.how_to_generate_group_box = QGroupBox(self.how_to_group_box)
        self.how_to_generate_group_box.setObjectName(u"how_to_generate_group_box")
        sizePolicy1.setHeightForWidth(self.how_to_generate_group_box.sizePolicy().hasHeightForWidth())
        self.how_to_generate_group_box.setSizePolicy(sizePolicy1)
        self.verticalLayout_6 = QVBoxLayout(self.how_to_generate_group_box)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.how_to_generate_label = QLabel(self.how_to_generate_group_box)
        self.how_to_generate_label.setObjectName(u"how_to_generate_label")
        sizePolicy2.setHeightForWidth(self.how_to_generate_label.sizePolicy().hasHeightForWidth())
        self.how_to_generate_label.setSizePolicy(sizePolicy2)
        self.how_to_generate_label.setTextFormat(Qt.RichText)
        self.how_to_generate_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.how_to_generate_label.setWordWrap(True)
        self.how_to_generate_label.setOpenExternalLinks(True)
        self.how_to_generate_label.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse)

        self.verticalLayout_6.addWidget(self.how_to_generate_label)


        self.horizontalLayout_3.addWidget(self.how_to_generate_group_box)

        self.how_to_right_arrow_label = QLabel(self.how_to_group_box)
        self.how_to_right_arrow_label.setObjectName(u"how_to_right_arrow_label")
        sizePolicy3.setHeightForWidth(self.how_to_right_arrow_label.sizePolicy().hasHeightForWidth())
        self.how_to_right_arrow_label.setSizePolicy(sizePolicy3)

        self.horizontalLayout_3.addWidget(self.how_to_right_arrow_label)

        self.how_to_running_group_box = QGroupBox(self.how_to_group_box)
        self.how_to_running_group_box.setObjectName(u"how_to_running_group_box")
        sizePolicy1.setHeightForWidth(self.how_to_running_group_box.sizePolicy().hasHeightForWidth())
        self.how_to_running_group_box.setSizePolicy(sizePolicy1)
        self.verticalLayout_7 = QVBoxLayout(self.how_to_running_group_box)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.how_to_running_label = QLabel(self.how_to_running_group_box)
        self.how_to_running_label.setObjectName(u"how_to_running_label")
        sizePolicy2.setHeightForWidth(self.how_to_running_label.sizePolicy().hasHeightForWidth())
        self.how_to_running_label.setSizePolicy(sizePolicy2)
        self.how_to_running_label.setTextFormat(Qt.RichText)
        self.how_to_running_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.how_to_running_label.setWordWrap(True)
        self.how_to_running_label.setOpenExternalLinks(True)
        self.how_to_running_label.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse)

        self.verticalLayout_7.addWidget(self.how_to_running_label)


        self.horizontalLayout_3.addWidget(self.how_to_running_group_box)


        self.verticalLayout_4.addWidget(self.how_to_group_box)

        self.useful_info_group_box = QGroupBox(self.getting_started_tab)
        self.useful_info_group_box.setObjectName(u"useful_info_group_box")
        self.horizontalLayout = QHBoxLayout(self.useful_info_group_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.useful_choose_settings_group_box = QGroupBox(self.useful_info_group_box)
        self.useful_choose_settings_group_box.setObjectName(u"useful_choose_settings_group_box")
        sizePolicy3.setHeightForWidth(self.useful_choose_settings_group_box.sizePolicy().hasHeightForWidth())
        self.useful_choose_settings_group_box.setSizePolicy(sizePolicy3)
        self.verticalLayout_8 = QVBoxLayout(self.useful_choose_settings_group_box)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.choose_settings_label = QLabel(self.useful_choose_settings_group_box)
        self.choose_settings_label.setObjectName(u"choose_settings_label")
        sizePolicy1.setHeightForWidth(self.choose_settings_label.sizePolicy().hasHeightForWidth())
        self.choose_settings_label.setSizePolicy(sizePolicy1)
        self.choose_settings_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.choose_settings_label.setWordWrap(True)
        self.choose_settings_label.setOpenExternalLinks(True)

        self.verticalLayout_8.addWidget(self.choose_settings_label)


        self.horizontalLayout.addWidget(self.useful_choose_settings_group_box)

        self.useful_links_group_box = QGroupBox(self.useful_info_group_box)
        self.useful_links_group_box.setObjectName(u"useful_links_group_box")
        sizePolicy3.setHeightForWidth(self.useful_links_group_box.sizePolicy().hasHeightForWidth())
        self.useful_links_group_box.setSizePolicy(sizePolicy3)
        self.horizontalLayout_2 = QHBoxLayout(self.useful_links_group_box)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.links_label = QLabel(self.useful_links_group_box)
        self.links_label.setObjectName(u"links_label")
        self.links_label.setOpenExternalLinks(True)

        self.horizontalLayout_2.addWidget(self.links_label)

        self.links_hspacer = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.links_hspacer)


        self.horizontalLayout.addWidget(self.useful_links_group_box)


        self.verticalLayout_4.addWidget(self.useful_info_group_box)

        self.file_setup_group_box = QGroupBox(self.getting_started_tab)
        self.file_setup_group_box.setObjectName(u"file_setup_group_box")
        self.gridLayout = QGridLayout(self.file_setup_group_box)
        self.gridLayout.setObjectName(u"gridLayout")
        self.extract_label = QLabel(self.file_setup_group_box)
        self.extract_label.setObjectName(u"extract_label")
        sizePolicy3.setHeightForWidth(self.extract_label.sizePolicy().hasHeightForWidth())
        self.extract_label.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.extract_label, 1, 0, 1, 1)

        self.extract_line_edit = QLineEdit(self.file_setup_group_box)
        self.extract_line_edit.setObjectName(u"extract_line_edit")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.extract_line_edit.sizePolicy().hasHeightForWidth())
        self.extract_line_edit.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.extract_line_edit, 1, 2, 1, 1)

        self.extract_button = QPushButton(self.file_setup_group_box)
        self.extract_button.setObjectName(u"extract_button")

        self.gridLayout.addWidget(self.extract_button, 1, 3, 1, 1)

        self.output_line_edit = QLineEdit(self.file_setup_group_box)
        self.output_line_edit.setObjectName(u"output_line_edit")

        self.gridLayout.addWidget(self.output_line_edit, 2, 2, 1, 1)

        self.output_label = QLabel(self.file_setup_group_box)
        self.output_label.setObjectName(u"output_label")
        sizePolicy3.setHeightForWidth(self.output_label.sizePolicy().hasHeightForWidth())
        self.output_label.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.output_label, 2, 0, 1, 1)

        self.output_button = QPushButton(self.file_setup_group_box)
        self.output_button.setObjectName(u"output_button")

        self.gridLayout.addWidget(self.output_button, 2, 3, 1, 1)


        self.verticalLayout_4.addWidget(self.file_setup_group_box)

        self.tab_widget.addTab(self.getting_started_tab, "")
        self.world_tab = QWidget()
        self.world_tab.setObjectName(u"world_tab")
        self.gridLayout_2 = QGridLayout(self.world_tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.beat_the_game_group_box = QGroupBox(self.world_tab)
        self.beat_the_game_group_box.setObjectName(u"beat_the_game_group_box")
        self.verticalLayout_13 = QVBoxLayout(self.beat_the_game_group_box)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.required_dungeons_layout = QHBoxLayout()
        self.required_dungeons_layout.setObjectName(u"required_dungeons_layout")
        self.required_dungeons_label = QLabel(self.beat_the_game_group_box)
        self.required_dungeons_label.setObjectName(u"required_dungeons_label")

        self.required_dungeons_layout.addWidget(self.required_dungeons_label)

        self.setting_required_dungeons = QSpinBox(self.beat_the_game_group_box)
        self.setting_required_dungeons.setObjectName(u"setting_required_dungeons")
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.setting_required_dungeons.sizePolicy().hasHeightForWidth())
        self.setting_required_dungeons.setSizePolicy(sizePolicy5)

        self.required_dungeons_layout.addWidget(self.setting_required_dungeons)


        self.verticalLayout_13.addLayout(self.required_dungeons_layout)

        self.setting_empty_unrequired_dungeons = QCheckBox(self.beat_the_game_group_box)
        self.setting_empty_unrequired_dungeons.setObjectName(u"setting_empty_unrequired_dungeons")

        self.verticalLayout_13.addWidget(self.setting_empty_unrequired_dungeons)

        self.setting_skip_horde = QCheckBox(self.beat_the_game_group_box)
        self.setting_skip_horde.setObjectName(u"setting_skip_horde")

        self.verticalLayout_13.addWidget(self.setting_skip_horde)

        self.setting_skip_g3 = QCheckBox(self.beat_the_game_group_box)
        self.setting_skip_g3.setObjectName(u"setting_skip_g3")

        self.verticalLayout_13.addWidget(self.setting_skip_g3)

        self.setting_skip_demise = QCheckBox(self.beat_the_game_group_box)
        self.setting_skip_demise.setObjectName(u"setting_skip_demise")

        self.verticalLayout_13.addWidget(self.setting_skip_demise)

        self.beat_the_game_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_13.addItem(self.beat_the_game_vspacer)


        self.gridLayout_2.addWidget(self.beat_the_game_group_box, 0, 0, 1, 1)

        self.open_world_group_box = QGroupBox(self.world_tab)
        self.open_world_group_box.setObjectName(u"open_world_group_box")
        self.verticalLayout_14 = QVBoxLayout(self.open_world_group_box)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.open_thunderhead_label = QLabel(self.open_world_group_box)
        self.open_thunderhead_label.setObjectName(u"open_thunderhead_label")

        self.verticalLayout_14.addWidget(self.open_thunderhead_label)

        self.setting_open_thunderhead = QComboBox(self.open_world_group_box)
        self.setting_open_thunderhead.setObjectName(u"setting_open_thunderhead")

        self.verticalLayout_14.addWidget(self.setting_open_thunderhead)

        self.open_lake_floria_label = QLabel(self.open_world_group_box)
        self.open_lake_floria_label.setObjectName(u"open_lake_floria_label")

        self.verticalLayout_14.addWidget(self.open_lake_floria_label)

        self.setting_open_lake_floria = QComboBox(self.open_world_group_box)
        self.setting_open_lake_floria.setObjectName(u"setting_open_lake_floria")

        self.verticalLayout_14.addWidget(self.setting_open_lake_floria)

        self.open_earth_temple_label = QLabel(self.open_world_group_box)
        self.open_earth_temple_label.setObjectName(u"open_earth_temple_label")

        self.verticalLayout_14.addWidget(self.open_earth_temple_label)

        self.setting_open_earth_temple = QComboBox(self.open_world_group_box)
        self.setting_open_earth_temple.setObjectName(u"setting_open_earth_temple")

        self.verticalLayout_14.addWidget(self.setting_open_earth_temple)

        self.open_lmf_label = QLabel(self.open_world_group_box)
        self.open_lmf_label.setObjectName(u"open_lmf_label")

        self.verticalLayout_14.addWidget(self.open_lmf_label)

        self.setting_open_lmf = QComboBox(self.open_world_group_box)
        self.setting_open_lmf.setObjectName(u"setting_open_lmf")

        self.verticalLayout_14.addWidget(self.setting_open_lmf)

        self.open_world_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.open_world_vspacer)


        self.gridLayout_2.addWidget(self.open_world_group_box, 0, 1, 1, 1)

        self.dungeons_group_box = QGroupBox(self.world_tab)
        self.dungeons_group_box.setObjectName(u"dungeons_group_box")
        self.verticalLayout_16 = QVBoxLayout(self.dungeons_group_box)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.small_keys_label = QLabel(self.dungeons_group_box)
        self.small_keys_label.setObjectName(u"small_keys_label")

        self.verticalLayout_16.addWidget(self.small_keys_label)

        self.setting_small_keys = QComboBox(self.dungeons_group_box)
        self.setting_small_keys.setObjectName(u"setting_small_keys")

        self.verticalLayout_16.addWidget(self.setting_small_keys)

        self.boss_keys_label = QLabel(self.dungeons_group_box)
        self.boss_keys_label.setObjectName(u"boss_keys_label")

        self.verticalLayout_16.addWidget(self.boss_keys_label)

        self.setting_boss_keys = QComboBox(self.dungeons_group_box)
        self.setting_boss_keys.setObjectName(u"setting_boss_keys")

        self.verticalLayout_16.addWidget(self.setting_boss_keys)

        self.map_mode_label = QLabel(self.dungeons_group_box)
        self.map_mode_label.setObjectName(u"map_mode_label")

        self.verticalLayout_16.addWidget(self.map_mode_label)

        self.setting_map_mode = QComboBox(self.dungeons_group_box)
        self.setting_map_mode.setObjectName(u"setting_map_mode")

        self.verticalLayout_16.addWidget(self.setting_map_mode)

        self.lanayru_caves_key_label = QLabel(self.dungeons_group_box)
        self.lanayru_caves_key_label.setObjectName(u"lanayru_caves_key_label")

        self.verticalLayout_16.addWidget(self.lanayru_caves_key_label)

        self.setting_lanayru_caves_key = QComboBox(self.dungeons_group_box)
        self.setting_lanayru_caves_key.setObjectName(u"setting_lanayru_caves_key")

        self.verticalLayout_16.addWidget(self.setting_lanayru_caves_key)

        self.dungeons_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_16.addItem(self.dungeons_vspacer)


        self.gridLayout_2.addWidget(self.dungeons_group_box, 0, 2, 1, 1)

        self.hint_placements_group_box = QGroupBox(self.world_tab)
        self.hint_placements_group_box.setObjectName(u"hint_placements_group_box")
        self.verticalLayout_24 = QVBoxLayout(self.hint_placements_group_box)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.setting_gossip_stone_hints = QCheckBox(self.hint_placements_group_box)
        self.setting_gossip_stone_hints.setObjectName(u"setting_gossip_stone_hints")

        self.verticalLayout_24.addWidget(self.setting_gossip_stone_hints)

        self.setting_fi_hints = QCheckBox(self.hint_placements_group_box)
        self.setting_fi_hints.setObjectName(u"setting_fi_hints")

        self.verticalLayout_24.addWidget(self.setting_fi_hints)

        self.setting_impa_sot_hint = QCheckBox(self.hint_placements_group_box)
        self.setting_impa_sot_hint.setObjectName(u"setting_impa_sot_hint")

        self.verticalLayout_24.addWidget(self.setting_impa_sot_hint)

        self.song_hints_label = QLabel(self.hint_placements_group_box)
        self.song_hints_label.setObjectName(u"song_hints_label")

        self.verticalLayout_24.addWidget(self.song_hints_label)

        self.setting_song_hints = QComboBox(self.hint_placements_group_box)
        self.setting_song_hints.setObjectName(u"setting_song_hints")

        self.verticalLayout_24.addWidget(self.setting_song_hints)

        self.hint_placements_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_24.addItem(self.hint_placements_vspacer)


        self.gridLayout_2.addWidget(self.hint_placements_group_box, 1, 1, 1, 1)

        self.entrance_randomization_group_box = QGroupBox(self.world_tab)
        self.entrance_randomization_group_box.setObjectName(u"entrance_randomization_group_box")
        self.verticalLayout_17 = QVBoxLayout(self.entrance_randomization_group_box)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.setting_randomize_door_entrances = QCheckBox(self.entrance_randomization_group_box)
        self.setting_randomize_door_entrances.setObjectName(u"setting_randomize_door_entrances")

        self.verticalLayout_17.addWidget(self.setting_randomize_door_entrances)

        self.setting_randomize_interior_entrances = QCheckBox(self.entrance_randomization_group_box)
        self.setting_randomize_interior_entrances.setObjectName(u"setting_randomize_interior_entrances")

        self.verticalLayout_17.addWidget(self.setting_randomize_interior_entrances)

        self.setting_randomize_overworld_entrances = QCheckBox(self.entrance_randomization_group_box)
        self.setting_randomize_overworld_entrances.setObjectName(u"setting_randomize_overworld_entrances")

        self.verticalLayout_17.addWidget(self.setting_randomize_overworld_entrances)

        self.setting_randomize_dungeon_entrances = QCheckBox(self.entrance_randomization_group_box)
        self.setting_randomize_dungeon_entrances.setObjectName(u"setting_randomize_dungeon_entrances")

        self.verticalLayout_17.addWidget(self.setting_randomize_dungeon_entrances)

        self.setting_randomize_trial_gate_entrances = QCheckBox(self.entrance_randomization_group_box)
        self.setting_randomize_trial_gate_entrances.setObjectName(u"setting_randomize_trial_gate_entrances")

        self.verticalLayout_17.addWidget(self.setting_randomize_trial_gate_entrances)

        self.random_starting_spawn_label = QLabel(self.entrance_randomization_group_box)
        self.random_starting_spawn_label.setObjectName(u"random_starting_spawn_label")

        self.verticalLayout_17.addWidget(self.random_starting_spawn_label)

        self.setting_random_starting_spawn = QComboBox(self.entrance_randomization_group_box)
        self.setting_random_starting_spawn.setObjectName(u"setting_random_starting_spawn")

        self.verticalLayout_17.addWidget(self.setting_random_starting_spawn)

        self.setting_decouple_double_doors = QCheckBox(self.entrance_randomization_group_box)
        self.setting_decouple_double_doors.setObjectName(u"setting_decouple_double_doors")

        self.verticalLayout_17.addWidget(self.setting_decouple_double_doors)

        self.setting_decouple_entrances = QCheckBox(self.entrance_randomization_group_box)
        self.setting_decouple_entrances.setObjectName(u"setting_decouple_entrances")

        self.verticalLayout_17.addWidget(self.setting_decouple_entrances)

        self.entrance_randomization_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_17.addItem(self.entrance_randomization_vspacer)


        self.gridLayout_2.addWidget(self.entrance_randomization_group_box, 0, 3, 1, 1)

        self.hints_group_box = QGroupBox(self.world_tab)
        self.hints_group_box.setObjectName(u"hints_group_box")
        self.verticalLayout_23 = QVBoxLayout(self.hints_group_box)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.path_hints_layout = QHBoxLayout()
        self.path_hints_layout.setObjectName(u"path_hints_layout")
        self.path_hints_label = QLabel(self.hints_group_box)
        self.path_hints_label.setObjectName(u"path_hints_label")

        self.path_hints_layout.addWidget(self.path_hints_label)

        self.setting_path_hints = QSpinBox(self.hints_group_box)
        self.setting_path_hints.setObjectName(u"setting_path_hints")
        sizePolicy5.setHeightForWidth(self.setting_path_hints.sizePolicy().hasHeightForWidth())
        self.setting_path_hints.setSizePolicy(sizePolicy5)

        self.path_hints_layout.addWidget(self.setting_path_hints)


        self.verticalLayout_23.addLayout(self.path_hints_layout)

        self.barren_hints_layout = QHBoxLayout()
        self.barren_hints_layout.setObjectName(u"barren_hints_layout")
        self.barren_hints_label = QLabel(self.hints_group_box)
        self.barren_hints_label.setObjectName(u"barren_hints_label")

        self.barren_hints_layout.addWidget(self.barren_hints_label)

        self.setting_barren_hints = QSpinBox(self.hints_group_box)
        self.setting_barren_hints.setObjectName(u"setting_barren_hints")
        sizePolicy5.setHeightForWidth(self.setting_barren_hints.sizePolicy().hasHeightForWidth())
        self.setting_barren_hints.setSizePolicy(sizePolicy5)

        self.barren_hints_layout.addWidget(self.setting_barren_hints)


        self.verticalLayout_23.addLayout(self.barren_hints_layout)

        self.location_hints_layout = QHBoxLayout()
        self.location_hints_layout.setObjectName(u"location_hints_layout")
        self.location_hints_label = QLabel(self.hints_group_box)
        self.location_hints_label.setObjectName(u"location_hints_label")

        self.location_hints_layout.addWidget(self.location_hints_label)

        self.setting_location_hints = QSpinBox(self.hints_group_box)
        self.setting_location_hints.setObjectName(u"setting_location_hints")
        sizePolicy5.setHeightForWidth(self.setting_location_hints.sizePolicy().hasHeightForWidth())
        self.setting_location_hints.setSizePolicy(sizePolicy5)

        self.location_hints_layout.addWidget(self.setting_location_hints)


        self.verticalLayout_23.addLayout(self.location_hints_layout)

        self.item_hints_layout = QHBoxLayout()
        self.item_hints_layout.setObjectName(u"item_hints_layout")
        self.item_hints_label = QLabel(self.hints_group_box)
        self.item_hints_label.setObjectName(u"item_hints_label")

        self.item_hints_layout.addWidget(self.item_hints_label)

        self.setting_item_hints = QSpinBox(self.hints_group_box)
        self.setting_item_hints.setObjectName(u"setting_item_hints")
        sizePolicy5.setHeightForWidth(self.setting_item_hints.sizePolicy().hasHeightForWidth())
        self.setting_item_hints.setSizePolicy(sizePolicy5)

        self.item_hints_layout.addWidget(self.setting_item_hints)


        self.verticalLayout_23.addLayout(self.item_hints_layout)

        self.setting_always_hints = QCheckBox(self.hints_group_box)
        self.setting_always_hints.setObjectName(u"setting_always_hints")

        self.verticalLayout_23.addWidget(self.setting_always_hints)

        self.setting_cryptic_hint_text = QCheckBox(self.hints_group_box)
        self.setting_cryptic_hint_text.setObjectName(u"setting_cryptic_hint_text")

        self.verticalLayout_23.addWidget(self.setting_cryptic_hint_text)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_23.addItem(self.verticalSpacer)


        self.gridLayout_2.addWidget(self.hints_group_box, 1, 0, 1, 1)

        self.tweaks_group_box = QGroupBox(self.world_tab)
        self.tweaks_group_box.setObjectName(u"tweaks_group_box")
        self.verticalLayout = QVBoxLayout(self.tweaks_group_box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ammo_availability_label = QLabel(self.tweaks_group_box)
        self.ammo_availability_label.setObjectName(u"ammo_availability_label")

        self.verticalLayout.addWidget(self.ammo_availability_label)

        self.setting_ammo_availability = QComboBox(self.tweaks_group_box)
        self.setting_ammo_availability.setObjectName(u"setting_ammo_availability")

        self.verticalLayout.addWidget(self.setting_ammo_availability)

        self.peatrice_conversations_layout = QHBoxLayout()
        self.peatrice_conversations_layout.setObjectName(u"peatrice_conversations_layout")
        self.peatrice_conversations_label = QLabel(self.tweaks_group_box)
        self.peatrice_conversations_label.setObjectName(u"peatrice_conversations_label")
        sizePolicy3.setHeightForWidth(self.peatrice_conversations_label.sizePolicy().hasHeightForWidth())
        self.peatrice_conversations_label.setSizePolicy(sizePolicy3)

        self.peatrice_conversations_layout.addWidget(self.peatrice_conversations_label)

        self.setting_peatrice_conversations = QSpinBox(self.tweaks_group_box)
        self.setting_peatrice_conversations.setObjectName(u"setting_peatrice_conversations")
        sizePolicy5.setHeightForWidth(self.setting_peatrice_conversations.sizePolicy().hasHeightForWidth())
        self.setting_peatrice_conversations.setSizePolicy(sizePolicy5)

        self.peatrice_conversations_layout.addWidget(self.setting_peatrice_conversations)


        self.verticalLayout.addLayout(self.peatrice_conversations_layout)

        self.setting_full_wallet_upgrades = QCheckBox(self.tweaks_group_box)
        self.setting_full_wallet_upgrades.setObjectName(u"setting_full_wallet_upgrades")

        self.verticalLayout.addWidget(self.setting_full_wallet_upgrades)

        self.tweaks_vspacer = QSpacerItem(20, 148, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.tweaks_vspacer)


        self.gridLayout_2.addWidget(self.tweaks_group_box, 1, 2, 1, 1)

        self.shortcuts_group_box = QGroupBox(self.world_tab)
        self.shortcuts_group_box.setObjectName(u"shortcuts_group_box")
        self.verticalLayout_25 = QVBoxLayout(self.shortcuts_group_box)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.setting_fs_lava_flow = QCheckBox(self.shortcuts_group_box)
        self.setting_fs_lava_flow.setObjectName(u"setting_fs_lava_flow")

        self.verticalLayout_25.addWidget(self.setting_fs_lava_flow)

        self.verticalSpacer_2 = QSpacerItem(20, 252, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_25.addItem(self.verticalSpacer_2)


        self.gridLayout_2.addWidget(self.shortcuts_group_box, 1, 3, 1, 1)

        self.tab_widget.addTab(self.world_tab, "")
        self.locations_tab = QWidget()
        self.locations_tab.setObjectName(u"locations_tab")
        self.gridLayout_3 = QGridLayout(self.locations_tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.individual_locations_layout = QHBoxLayout()
        self.individual_locations_layout.setObjectName(u"individual_locations_layout")
        self.individual_locations_layout.setContentsMargins(-1, 0, -1, -1)
        self.included_locations_group_box = QGroupBox(self.locations_tab)
        self.included_locations_group_box.setObjectName(u"included_locations_group_box")
        self.verticalLayout_9 = QVBoxLayout(self.included_locations_group_box)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.included_locations_filter_layout = QHBoxLayout()
        self.included_locations_filter_layout.setObjectName(u"included_locations_filter_layout")
        self.included_locations_category_filters = QComboBox(self.included_locations_group_box)
        self.included_locations_category_filters.setObjectName(u"included_locations_category_filters")

        self.included_locations_filter_layout.addWidget(self.included_locations_category_filters)

        self.included_locations_free_search = QLineEdit(self.included_locations_group_box)
        self.included_locations_free_search.setObjectName(u"included_locations_free_search")
        sizePolicy6 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.included_locations_free_search.sizePolicy().hasHeightForWidth())
        self.included_locations_free_search.setSizePolicy(sizePolicy6)
        self.included_locations_free_search.setClearButtonEnabled(True)

        self.included_locations_filter_layout.addWidget(self.included_locations_free_search)


        self.verticalLayout_9.addLayout(self.included_locations_filter_layout)

        self.included_locations_list_view = QListView(self.included_locations_group_box)
        self.included_locations_list_view.setObjectName(u"included_locations_list_view")
        self.included_locations_list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.included_locations_list_view.setProperty("showDropIndicator", False)
        self.included_locations_list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.included_locations_list_view.setSelectionRectVisible(False)

        self.verticalLayout_9.addWidget(self.included_locations_list_view)


        self.individual_locations_layout.addWidget(self.included_locations_group_box)

        self.individual_locations_button_layout = QVBoxLayout()
        self.individual_locations_button_layout.setObjectName(u"individual_locations_button_layout")
        self.individual_locations_top_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.individual_locations_button_layout.addItem(self.individual_locations_top_vspacer)

        self.include_location_button = QPushButton(self.locations_tab)
        self.include_location_button.setObjectName(u"include_location_button")
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.include_location_button.sizePolicy().hasHeightForWidth())
        self.include_location_button.setSizePolicy(sizePolicy7)

        self.individual_locations_button_layout.addWidget(self.include_location_button)

        self.individual_locations_middle_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.individual_locations_button_layout.addItem(self.individual_locations_middle_vspacer)

        self.exclude_location_button = QPushButton(self.locations_tab)
        self.exclude_location_button.setObjectName(u"exclude_location_button")
        sizePolicy7.setHeightForWidth(self.exclude_location_button.sizePolicy().hasHeightForWidth())
        self.exclude_location_button.setSizePolicy(sizePolicy7)

        self.individual_locations_button_layout.addWidget(self.exclude_location_button)

        self.individual_locations_bottom_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.individual_locations_button_layout.addItem(self.individual_locations_bottom_vspacer)


        self.individual_locations_layout.addLayout(self.individual_locations_button_layout)

        self.excluded_locations_group_box = QGroupBox(self.locations_tab)
        self.excluded_locations_group_box.setObjectName(u"excluded_locations_group_box")
        self.verticalLayout_18 = QVBoxLayout(self.excluded_locations_group_box)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.excluded_locations_filter_layout = QHBoxLayout()
        self.excluded_locations_filter_layout.setObjectName(u"excluded_locations_filter_layout")
        self.excluded_locations_category_filters = QComboBox(self.excluded_locations_group_box)
        self.excluded_locations_category_filters.setObjectName(u"excluded_locations_category_filters")

        self.excluded_locations_filter_layout.addWidget(self.excluded_locations_category_filters)

        self.excluded_locations_free_search = QLineEdit(self.excluded_locations_group_box)
        self.excluded_locations_free_search.setObjectName(u"excluded_locations_free_search")
        sizePolicy6.setHeightForWidth(self.excluded_locations_free_search.sizePolicy().hasHeightForWidth())
        self.excluded_locations_free_search.setSizePolicy(sizePolicy6)
        self.excluded_locations_free_search.setClearButtonEnabled(True)

        self.excluded_locations_filter_layout.addWidget(self.excluded_locations_free_search)


        self.verticalLayout_18.addLayout(self.excluded_locations_filter_layout)

        self.excluded_locations_list_view = QListView(self.excluded_locations_group_box)
        self.excluded_locations_list_view.setObjectName(u"excluded_locations_list_view")
        self.excluded_locations_list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.excluded_locations_list_view.setProperty("showDropIndicator", False)
        self.excluded_locations_list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.excluded_locations_list_view.setSelectionRectVisible(False)

        self.verticalLayout_18.addWidget(self.excluded_locations_list_view)


        self.individual_locations_layout.addWidget(self.excluded_locations_group_box)


        self.gridLayout_3.addLayout(self.individual_locations_layout, 3, 1, 1, 1)

        self.location_control_layout = QHBoxLayout()
        self.location_control_layout.setObjectName(u"location_control_layout")
        self.shuffles_group_box = QGroupBox(self.locations_tab)
        self.shuffles_group_box.setObjectName(u"shuffles_group_box")
        self.verticalLayout_10 = QVBoxLayout(self.shuffles_group_box)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.setting_shuffle_single_gratitude_crystals = QCheckBox(self.shuffles_group_box)
        self.setting_shuffle_single_gratitude_crystals.setObjectName(u"setting_shuffle_single_gratitude_crystals")

        self.verticalLayout_10.addWidget(self.setting_shuffle_single_gratitude_crystals)


        self.location_control_layout.addWidget(self.shuffles_group_box)

        self.shops_group_box = QGroupBox(self.locations_tab)
        self.shops_group_box.setObjectName(u"shops_group_box")
        self.verticalLayout_15 = QVBoxLayout(self.shops_group_box)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.randomized_shops_label = QLabel(self.shops_group_box)
        self.randomized_shops_label.setObjectName(u"randomized_shops_label")

        self.verticalLayout_15.addWidget(self.randomized_shops_label)

        self.setting_randomized_shops = QComboBox(self.shops_group_box)
        self.setting_randomized_shops.setObjectName(u"setting_randomized_shops")

        self.verticalLayout_15.addWidget(self.setting_randomized_shops)


        self.location_control_layout.addWidget(self.shops_group_box)


        self.gridLayout_3.addLayout(self.location_control_layout, 0, 1, 1, 1)

        self.tab_widget.addTab(self.locations_tab, "")
        self.inventory_tab = QWidget()
        self.inventory_tab.setObjectName(u"inventory_tab")
        self.tab_widget.addTab(self.inventory_tab, "")
        self.logic_tab = QWidget()
        self.logic_tab.setObjectName(u"logic_tab")
        self.gridLayout_5 = QGridLayout(self.logic_tab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.logic_rules_group_box = QGroupBox(self.logic_tab)
        self.logic_rules_group_box.setObjectName(u"logic_rules_group_box")
        self.horizontalLayout_5 = QHBoxLayout(self.logic_rules_group_box)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.logic_rules_label = QLabel(self.logic_rules_group_box)
        self.logic_rules_label.setObjectName(u"logic_rules_label")

        self.horizontalLayout_5.addWidget(self.logic_rules_label)

        self.setting_logic_rules = QComboBox(self.logic_rules_group_box)
        self.setting_logic_rules.setObjectName(u"setting_logic_rules")

        self.horizontalLayout_5.addWidget(self.setting_logic_rules)

        self.logic_rules_hspacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.logic_rules_hspacer)


        self.gridLayout_5.addWidget(self.logic_rules_group_box, 0, 0, 1, 1)

        self.tricks_group_box = QGroupBox(self.logic_tab)
        self.tricks_group_box.setObjectName(u"tricks_group_box")
        sizePolicy.setHeightForWidth(self.tricks_group_box.sizePolicy().hasHeightForWidth())
        self.tricks_group_box.setSizePolicy(sizePolicy)
        self.horizontalLayout_6 = QHBoxLayout(self.tricks_group_box)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.precise_items_group_box = QGroupBox(self.tricks_group_box)
        self.precise_items_group_box.setObjectName(u"precise_items_group_box")
        self.verticalLayout_20 = QVBoxLayout(self.precise_items_group_box)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.setting_logic_advanced_lizalfos_combat = QCheckBox(self.precise_items_group_box)
        self.setting_logic_advanced_lizalfos_combat.setObjectName(u"setting_logic_advanced_lizalfos_combat")

        self.verticalLayout_20.addWidget(self.setting_logic_advanced_lizalfos_combat)

        self.setting_logic_skyview_precise_slingshot = QCheckBox(self.precise_items_group_box)
        self.setting_logic_skyview_precise_slingshot.setObjectName(u"setting_logic_skyview_precise_slingshot")

        self.verticalLayout_20.addWidget(self.setting_logic_skyview_precise_slingshot)

        self.setting_logic_lmf_ceiling_precise_slingshot = QCheckBox(self.precise_items_group_box)
        self.setting_logic_lmf_ceiling_precise_slingshot.setObjectName(u"setting_logic_lmf_ceiling_precise_slingshot")

        self.verticalLayout_20.addWidget(self.setting_logic_lmf_ceiling_precise_slingshot)

        self.setting_logic_tot_slingshot = QCheckBox(self.precise_items_group_box)
        self.setting_logic_tot_slingshot.setObjectName(u"setting_logic_tot_slingshot")

        self.verticalLayout_20.addWidget(self.setting_logic_tot_slingshot)

        self.setting_logic_bomb_throws = QCheckBox(self.precise_items_group_box)
        self.setting_logic_bomb_throws.setObjectName(u"setting_logic_bomb_throws")

        self.verticalLayout_20.addWidget(self.setting_logic_bomb_throws)

        self.setting_logic_lanayru_mine_quick_bomb = QCheckBox(self.precise_items_group_box)
        self.setting_logic_lanayru_mine_quick_bomb.setObjectName(u"setting_logic_lanayru_mine_quick_bomb")

        self.verticalLayout_20.addWidget(self.setting_logic_lanayru_mine_quick_bomb)

        self.setting_logic_cactus_bomb_whip = QCheckBox(self.precise_items_group_box)
        self.setting_logic_cactus_bomb_whip.setObjectName(u"setting_logic_cactus_bomb_whip")

        self.verticalLayout_20.addWidget(self.setting_logic_cactus_bomb_whip)

        self.setting_logic_beedles_shop_with_bombs = QCheckBox(self.precise_items_group_box)
        self.setting_logic_beedles_shop_with_bombs.setObjectName(u"setting_logic_beedles_shop_with_bombs")

        self.verticalLayout_20.addWidget(self.setting_logic_beedles_shop_with_bombs)

        self.setting_logic_bird_nest_item_from_beedles_shop = QCheckBox(self.precise_items_group_box)
        self.setting_logic_bird_nest_item_from_beedles_shop.setObjectName(u"setting_logic_bird_nest_item_from_beedles_shop")

        self.verticalLayout_20.addWidget(self.setting_logic_bird_nest_item_from_beedles_shop)

        self.setting_logic_precise_beetle = QCheckBox(self.precise_items_group_box)
        self.setting_logic_precise_beetle.setObjectName(u"setting_logic_precise_beetle")

        self.verticalLayout_20.addWidget(self.setting_logic_precise_beetle)

        self.setting_logic_skippers_fast_clawshots = QCheckBox(self.precise_items_group_box)
        self.setting_logic_skippers_fast_clawshots.setObjectName(u"setting_logic_skippers_fast_clawshots")

        self.verticalLayout_20.addWidget(self.setting_logic_skippers_fast_clawshots)

        self.setting_logic_lmf_whip_switch = QCheckBox(self.precise_items_group_box)
        self.setting_logic_lmf_whip_switch.setObjectName(u"setting_logic_lmf_whip_switch")

        self.verticalLayout_20.addWidget(self.setting_logic_lmf_whip_switch)

        self.setting_logic_lmf_whip_armos_room_timeshift_stone = QCheckBox(self.precise_items_group_box)
        self.setting_logic_lmf_whip_armos_room_timeshift_stone.setObjectName(u"setting_logic_lmf_whip_armos_room_timeshift_stone")

        self.verticalLayout_20.addWidget(self.setting_logic_lmf_whip_armos_room_timeshift_stone)

        self.setting_logic_lmf_minecart_jump = QCheckBox(self.precise_items_group_box)
        self.setting_logic_lmf_minecart_jump.setObjectName(u"setting_logic_lmf_minecart_jump")

        self.verticalLayout_20.addWidget(self.setting_logic_lmf_minecart_jump)

        self.setting_logic_present_bow_switches = QCheckBox(self.precise_items_group_box)
        self.setting_logic_present_bow_switches.setObjectName(u"setting_logic_present_bow_switches")

        self.verticalLayout_20.addWidget(self.setting_logic_present_bow_switches)

        self.setting_logic_skykeep_vineclip = QCheckBox(self.precise_items_group_box)
        self.setting_logic_skykeep_vineclip.setObjectName(u"setting_logic_skykeep_vineclip")

        self.verticalLayout_20.addWidget(self.setting_logic_skykeep_vineclip)

        self.precise_items_vspacer = QSpacerItem(20, 87, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_20.addItem(self.precise_items_vspacer)


        self.horizontalLayout_6.addWidget(self.precise_items_group_box)

        self.dives_and_jumps_group_box = QGroupBox(self.tricks_group_box)
        self.dives_and_jumps_group_box.setObjectName(u"dives_and_jumps_group_box")
        self.verticalLayout_19 = QVBoxLayout(self.dives_and_jumps_group_box)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.setting_logic_volcanic_island_dive = QCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_volcanic_island_dive.setObjectName(u"setting_logic_volcanic_island_dive")

        self.verticalLayout_19.addWidget(self.setting_logic_volcanic_island_dive)

        self.setting_logic_east_island_dive = QCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_east_island_dive.setObjectName(u"setting_logic_east_island_dive")

        self.verticalLayout_19.addWidget(self.setting_logic_east_island_dive)

        self.setting_logic_beedles_island_cage_chest_dive = QCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_beedles_island_cage_chest_dive.setObjectName(u"setting_logic_beedles_island_cage_chest_dive")

        self.verticalLayout_19.addWidget(self.setting_logic_beedles_island_cage_chest_dive)

        self.setting_logic_gravestone_jump = QCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_gravestone_jump.setObjectName(u"setting_logic_gravestone_jump")

        self.verticalLayout_19.addWidget(self.setting_logic_gravestone_jump)

        self.setting_logic_waterfall_cave_jump = QCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_waterfall_cave_jump.setObjectName(u"setting_logic_waterfall_cave_jump")

        self.verticalLayout_19.addWidget(self.setting_logic_waterfall_cave_jump)

        self.setting_logic_early_lake_floria = QCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_early_lake_floria.setObjectName(u"setting_logic_early_lake_floria")

        self.verticalLayout_19.addWidget(self.setting_logic_early_lake_floria)

        self.setting_logic_ac_lever_jump_trick = QCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_ac_lever_jump_trick.setObjectName(u"setting_logic_ac_lever_jump_trick")

        self.verticalLayout_19.addWidget(self.setting_logic_ac_lever_jump_trick)

        self.setting_logic_ac_chest_after_whip_hooks_jump = QCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_ac_chest_after_whip_hooks_jump.setObjectName(u"setting_logic_ac_chest_after_whip_hooks_jump")

        self.verticalLayout_19.addWidget(self.setting_logic_ac_chest_after_whip_hooks_jump)

        self.setting_logic_sandship_jump_to_stern = QCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_sandship_jump_to_stern.setObjectName(u"setting_logic_sandship_jump_to_stern")

        self.verticalLayout_19.addWidget(self.setting_logic_sandship_jump_to_stern)

        self.setting_logic_fs_pillar_jump = QCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_fs_pillar_jump.setObjectName(u"setting_logic_fs_pillar_jump")

        self.verticalLayout_19.addWidget(self.setting_logic_fs_pillar_jump)

        self.dives_and_jumps_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_19.addItem(self.dives_and_jumps_vspacer)


        self.horizontalLayout_6.addWidget(self.dives_and_jumps_group_box)

        self.glitches_group_box = QGroupBox(self.tricks_group_box)
        self.glitches_group_box.setObjectName(u"glitches_group_box")
        self.verticalLayout_21 = QVBoxLayout(self.glitches_group_box)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.setting_logic_stuttersprint = QCheckBox(self.glitches_group_box)
        self.setting_logic_stuttersprint.setObjectName(u"setting_logic_stuttersprint")

        self.verticalLayout_21.addWidget(self.setting_logic_stuttersprint)

        self.setting_logic_et_slope_stuttersprint = QCheckBox(self.glitches_group_box)
        self.setting_logic_et_slope_stuttersprint.setObjectName(u"setting_logic_et_slope_stuttersprint")

        self.verticalLayout_21.addWidget(self.setting_logic_et_slope_stuttersprint)

        self.setting_logic_brakeslide = QCheckBox(self.glitches_group_box)
        self.setting_logic_brakeslide.setObjectName(u"setting_logic_brakeslide")

        self.verticalLayout_21.addWidget(self.setting_logic_brakeslide)

        self.setting_logic_tot_skip_brakeslide = QCheckBox(self.glitches_group_box)
        self.setting_logic_tot_skip_brakeslide.setObjectName(u"setting_logic_tot_skip_brakeslide")

        self.verticalLayout_21.addWidget(self.setting_logic_tot_skip_brakeslide)

        self.glitches_vspacer = QSpacerItem(20, 399, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_21.addItem(self.glitches_vspacer)


        self.horizontalLayout_6.addWidget(self.glitches_group_box)

        self.miscellaneous_group_box = QGroupBox(self.tricks_group_box)
        self.miscellaneous_group_box.setObjectName(u"miscellaneous_group_box")
        self.verticalLayout_22 = QVBoxLayout(self.miscellaneous_group_box)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.setting_logic_fire_node_without_hook_beetle = QCheckBox(self.miscellaneous_group_box)
        self.setting_logic_fire_node_without_hook_beetle.setObjectName(u"setting_logic_fire_node_without_hook_beetle")

        self.verticalLayout_22.addWidget(self.setting_logic_fire_node_without_hook_beetle)

        self.setting_logic_skyview_spider_roll = QCheckBox(self.miscellaneous_group_box)
        self.setting_logic_skyview_spider_roll.setObjectName(u"setting_logic_skyview_spider_roll")

        self.verticalLayout_22.addWidget(self.setting_logic_skyview_spider_roll)

        self.setting_logic_et_keese_skyward_strike = QCheckBox(self.miscellaneous_group_box)
        self.setting_logic_et_keese_skyward_strike.setObjectName(u"setting_logic_et_keese_skyward_strike")

        self.verticalLayout_22.addWidget(self.setting_logic_et_keese_skyward_strike)

        self.setting_logic_et_bombless_scaldera = QCheckBox(self.miscellaneous_group_box)
        self.setting_logic_et_bombless_scaldera.setObjectName(u"setting_logic_et_bombless_scaldera")

        self.verticalLayout_22.addWidget(self.setting_logic_et_bombless_scaldera)

        self.setting_logic_lmf_bellowsless_moldarach = QCheckBox(self.miscellaneous_group_box)
        self.setting_logic_lmf_bellowsless_moldarach.setObjectName(u"setting_logic_lmf_bellowsless_moldarach")

        self.verticalLayout_22.addWidget(self.setting_logic_lmf_bellowsless_moldarach)

        self.setting_logic_sandship_itemless_spume = QCheckBox(self.miscellaneous_group_box)
        self.setting_logic_sandship_itemless_spume.setObjectName(u"setting_logic_sandship_itemless_spume")

        self.verticalLayout_22.addWidget(self.setting_logic_sandship_itemless_spume)

        self.setting_logic_sandship_no_combination_hint = QCheckBox(self.miscellaneous_group_box)
        self.setting_logic_sandship_no_combination_hint.setObjectName(u"setting_logic_sandship_no_combination_hint")

        self.verticalLayout_22.addWidget(self.setting_logic_sandship_no_combination_hint)

        self.setting_logic_fs_practice_sword_ghirahim_2 = QCheckBox(self.miscellaneous_group_box)
        self.setting_logic_fs_practice_sword_ghirahim_2.setObjectName(u"setting_logic_fs_practice_sword_ghirahim_2")

        self.verticalLayout_22.addWidget(self.setting_logic_fs_practice_sword_ghirahim_2)

        self.setting_logic_itemless_first_timeshift_stone = QCheckBox(self.miscellaneous_group_box)
        self.setting_logic_itemless_first_timeshift_stone.setObjectName(u"setting_logic_itemless_first_timeshift_stone")

        self.verticalLayout_22.addWidget(self.setting_logic_itemless_first_timeshift_stone)

        self.miscellaneous_vspacer = QSpacerItem(20, 237, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_22.addItem(self.miscellaneous_vspacer)


        self.horizontalLayout_6.addWidget(self.miscellaneous_group_box)


        self.gridLayout_5.addWidget(self.tricks_group_box, 1, 0, 1, 1)

        self.tab_widget.addTab(self.logic_tab, "")
        self.cosmetic_tab = QWidget()
        self.cosmetic_tab.setObjectName(u"cosmetic_tab")
        self.gridLayout_4 = QGridLayout(self.cosmetic_tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.groupBox_3 = QGroupBox(self.cosmetic_tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.setting_tunic_swap = QCheckBox(self.groupBox_3)
        self.setting_tunic_swap.setObjectName(u"setting_tunic_swap")

        self.verticalLayout_11.addWidget(self.setting_tunic_swap)

        self.verticalSpacer_3 = QSpacerItem(20, 576, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_3)


        self.gridLayout_4.addWidget(self.groupBox_3, 0, 0, 1, 1)

        self.tab_widget.addTab(self.cosmetic_tab, "")
        self.advanced_tab = QWidget()
        self.advanced_tab.setObjectName(u"advanced_tab")
        self.tab_widget.addTab(self.advanced_tab, "")
        self.accessibility_tab = QWidget()
        self.accessibility_tab.setObjectName(u"accessibility_tab")
        self.horizontalLayout_4 = QHBoxLayout(self.accessibility_tab)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.theming_group_box = QGroupBox(self.accessibility_tab)
        self.theming_group_box.setObjectName(u"theming_group_box")
        self.verticalLayout_3 = QVBoxLayout(self.theming_group_box)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.theme_mode_label = QLabel(self.theming_group_box)
        self.theme_mode_label.setObjectName(u"theme_mode_label")

        self.verticalLayout_3.addWidget(self.theme_mode_label)

        self.theme_mode_combo_box = QComboBox(self.theming_group_box)
        self.theme_mode_combo_box.setObjectName(u"theme_mode_combo_box")

        self.verticalLayout_3.addWidget(self.theme_mode_combo_box)

        self.theme_presets_label = QLabel(self.theming_group_box)
        self.theme_presets_label.setObjectName(u"theme_presets_label")

        self.verticalLayout_3.addWidget(self.theme_presets_label)

        self.theme_presets_combo_box = QComboBox(self.theming_group_box)
        self.theme_presets_combo_box.setObjectName(u"theme_presets_combo_box")

        self.verticalLayout_3.addWidget(self.theme_presets_combo_box)

        self.use_custom_theme_check_box = QCheckBox(self.theming_group_box)
        self.use_custom_theme_check_box.setObjectName(u"use_custom_theme_check_box")

        self.verticalLayout_3.addWidget(self.use_custom_theme_check_box)

        self.customize_theme_button = QPushButton(self.theming_group_box)
        self.customize_theme_button.setObjectName(u"customize_theme_button")

        self.verticalLayout_3.addWidget(self.customize_theme_button)

        self.theming_vspacer = QSpacerItem(20, 448, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.theming_vspacer)


        self.horizontalLayout_4.addWidget(self.theming_group_box)

        self.theming_fonts = QGroupBox(self.accessibility_tab)
        self.theming_fonts.setObjectName(u"theming_fonts")
        self.verticalLayout_12 = QVBoxLayout(self.theming_fonts)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.font_family_label = QLabel(self.theming_fonts)
        self.font_family_label.setObjectName(u"font_family_label")

        self.verticalLayout_12.addWidget(self.font_family_label)

        self.font_family_combo_box = QFontComboBox(self.theming_fonts)
        self.font_family_combo_box.setObjectName(u"font_family_combo_box")
        sizePolicy3.setHeightForWidth(self.font_family_combo_box.sizePolicy().hasHeightForWidth())
        self.font_family_combo_box.setSizePolicy(sizePolicy3)
        self.font_family_combo_box.setEditable(False)
        self.font_family_combo_box.setFontFilters(QFontComboBox.ScalableFonts)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        self.font_family_combo_box.setCurrentFont(font)

        self.verticalLayout_12.addWidget(self.font_family_combo_box)

        self.font_size_layout = QHBoxLayout()
        self.font_size_layout.setObjectName(u"font_size_layout")
        self.font_size_label = QLabel(self.theming_fonts)
        self.font_size_label.setObjectName(u"font_size_label")

        self.font_size_layout.addWidget(self.font_size_label)

        self.font_size_spin_box = QSpinBox(self.theming_fonts)
        self.font_size_spin_box.setObjectName(u"font_size_spin_box")
        sizePolicy5.setHeightForWidth(self.font_size_spin_box.sizePolicy().hasHeightForWidth())
        self.font_size_spin_box.setSizePolicy(sizePolicy5)
        self.font_size_spin_box.setMinimum(6)
        self.font_size_spin_box.setMaximum(14)
        self.font_size_spin_box.setValue(10)

        self.font_size_layout.addWidget(self.font_size_spin_box)


        self.verticalLayout_12.addLayout(self.font_size_layout)

        self.font_reset_button = QPushButton(self.theming_fonts)
        self.font_reset_button.setObjectName(u"font_reset_button")

        self.verticalLayout_12.addWidget(self.font_reset_button)

        self.fonts_vspacer = QSpacerItem(20, 494, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.fonts_vspacer)


        self.horizontalLayout_4.addWidget(self.theming_fonts)

        self.groupBox_6 = QGroupBox(self.accessibility_tab)
        self.groupBox_6.setObjectName(u"groupBox_6")

        self.horizontalLayout_4.addWidget(self.groupBox_6)

        self.tab_widget.addTab(self.accessibility_tab, "")

        self.verticalLayout_2.addWidget(self.tab_widget)

        self.seed_layout = QGridLayout()
        self.seed_layout.setObjectName(u"seed_layout")
        self.copy_setting_string_button = QPushButton(self.central_widget)
        self.copy_setting_string_button.setObjectName(u"copy_setting_string_button")

        self.seed_layout.addWidget(self.copy_setting_string_button, 1, 3, 1, 1)

        self.setting_seed = QLineEdit(self.central_widget)
        self.setting_seed.setObjectName(u"setting_seed")

        self.seed_layout.addWidget(self.setting_seed, 2, 2, 1, 1)

        self.setting_string = QLineEdit(self.central_widget)
        self.setting_string.setObjectName(u"setting_string")

        self.seed_layout.addWidget(self.setting_string, 1, 2, 1, 1)

        self.new_seed_button = QPushButton(self.central_widget)
        self.new_seed_button.setObjectName(u"new_seed_button")

        self.seed_layout.addWidget(self.new_seed_button, 2, 3, 1, 1)

        self.setting_string_label = QLabel(self.central_widget)
        self.setting_string_label.setObjectName(u"setting_string_label")

        self.seed_layout.addWidget(self.setting_string_label, 1, 0, 1, 1)

        self.seed_label = QLabel(self.central_widget)
        self.seed_label.setObjectName(u"seed_label")

        self.seed_layout.addWidget(self.seed_label, 2, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.seed_layout)

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setObjectName(u"footer_layout")
        self.about_button = QPushButton(self.central_widget)
        self.about_button.setObjectName(u"about_button")

        self.footer_layout.addWidget(self.about_button)

        self.footer_left_hspacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.footer_layout.addItem(self.footer_left_hspacer)

        self.reset_button = QPushButton(self.central_widget)
        self.reset_button.setObjectName(u"reset_button")

        self.footer_layout.addWidget(self.reset_button)

        self.footer_right_hspacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.footer_layout.addItem(self.footer_right_hspacer)

        self.randomize_button = QPushButton(self.central_widget)
        self.randomize_button.setObjectName(u"randomize_button")
        sizePolicy8 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.randomize_button.sizePolicy().hasHeightForWidth())
        self.randomize_button.setSizePolicy(sizePolicy8)

        self.footer_layout.addWidget(self.randomize_button)


        self.verticalLayout_2.addLayout(self.footer_layout)

        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)

        self.tab_widget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"The Legend of Zelda: Skyward Sword HD Randomizer", None))
        self.how_to_group_box.setTitle(QCoreApplication.translate("main_window", u"How to Randomize the Game", None))
        self.how_to_extract_group_box.setTitle(QCoreApplication.translate("main_window", u"Extract the Game", None))
        self.how_to_extract_label.setText(QCoreApplication.translate("main_window", u"Before generating a seed, you need to have a valid extract of the vanilla version of the game.<br><br>\n"
"\n"
"Specifically, you will need to extract the <code>exeFS</code> and <code>romFS</code> files of the 1.0.1 version of the game. You can do this with a modded Nintendo Switch console with a tool such as <a href=\"https://github.com/DarkMatterCore/nxdumptool\">nxdumptool</a> or with the <a href=\"https://ryujinx.org\">Ryujinx emulator</a> (yuzu cannot currently extract the <code>romFS</code> folder)<br><br>\n"
"\n"
"For help with this process, please ask on GitHub or join the Discord server linked below.", None))
        self.how_to_left_arrow_label.setText(QCoreApplication.translate("main_window", u"-->", None))
        self.how_to_generate_group_box.setTitle(QCoreApplication.translate("main_window", u"Generate a Seed", None))
        self.how_to_generate_label.setText(QCoreApplication.translate("main_window", u"After you have obtained an extract of the vanilla game, you need to tell this randomizer program where the extract is located so that it can be used to generate a seed.<br><br>\n"
"\n"
"Please go to the \"File Setup\" box below and click the \"Browse\" button on the \"Extract\" row. You will then be asked to find the location of your extract.<br><br>\n"
"\n"
"Once the extract has been verified, you can browse the various tabs and customize the settings of your randomizer seed.<br><br>\n"
"\n"
"When you are ready, click the \"Randomize\" button in the bottom right of the screen. By default, the output will be in the <code>output</code> folder where this randomizer program is located.", None))
        self.how_to_right_arrow_label.setText(QCoreApplication.translate("main_window", u"-->", None))
        self.how_to_running_group_box.setTitle(QCoreApplication.translate("main_window", u"Running the Seed", None))
        self.how_to_running_label.setText(QCoreApplication.translate("main_window", u"If you want to play this randomizer on a modded Nintendo Switch console, copy the outputted <code>exeFS</code> and <code>romFS</code> folders into the <code>/atmosphere/contents/01002DA013484000</code> folder on your Switch's SD card. You can then run the game like normal and the randomizer will be patched on top of the vanilla game.<br><br>\n"
"\n"
"If you want to play this randomizer on the <a href=\"https://yuzu-emu.org/\">yuzu emulator</a>, open yuzu and right click on your copy of Skyward Sword HD. Click the \"Open Mod Data Location\" option and create a folder called <code>rando</code>. Copy the outputted <code>exeFS</code> and <code>romFS</code> folders into the newly created <code>rando</code> folder.<br><br>\n"
"\n"
"If you want to play the randomizer on the <a href=\"https://ryujinx.org/\">Ryujinx emulator</a>, copy the outputted <code>exeFS</code> and <code>romFS</code> folders into the <code>/Ryujinx/mods/contents/01002DA013484000</code> folder.", None))
        self.useful_info_group_box.setTitle(QCoreApplication.translate("main_window", u"Useful Information", None))
        self.useful_choose_settings_group_box.setTitle(QCoreApplication.translate("main_window", u"Choosing your Settings", None))
        self.choose_settings_label.setText(QCoreApplication.translate("main_window", u"<b>\u2023</b> World: Customize how the world is randomized. Pick dungeon, completion, shuffle, entrance, and other fun settings.<br>\n"
"<b>\u2023</b> Logic: Pick which locations and tricks are enabled.<br>\n"
"<b>\u2023</b> Inventory: Pick what items you start with.<br>\n"
"<b>\u2023</b> Cosmetic: Customize the music and how the player model will look in-game.", None))
        self.useful_links_group_box.setTitle(QCoreApplication.translate("main_window", u"Links", None))
        self.links_label.setText(QCoreApplication.translate("main_window", u"<b>TODO</b><br>\n"
"\n"
"<b>\u2023</b> <a href=\"https://discord.com\">Discord Server (todo)</a><br>\n"
"<b>\u2023</b> <a href=\"https://github.com/mint-choc-chip-skyblade/sshd-rando/issues\">Report a Bug</a><br>\n"
"<b>\u2023</b> <a href=\"\">Location Guide (todo)</a>", None))
        self.file_setup_group_box.setTitle(QCoreApplication.translate("main_window", u"File Setup", None))
        self.extract_label.setText(QCoreApplication.translate("main_window", u"Extract", None))
        self.extract_button.setText(QCoreApplication.translate("main_window", u"Browse", None))
        self.output_label.setText(QCoreApplication.translate("main_window", u"Output", None))
        self.output_button.setText(QCoreApplication.translate("main_window", u"Browse", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.getting_started_tab), QCoreApplication.translate("main_window", u"Getting Started", None))
        self.beat_the_game_group_box.setTitle(QCoreApplication.translate("main_window", u"Beat the Game", None))
        self.required_dungeons_label.setText(QCoreApplication.translate("main_window", u"Required Dungeons", None))
        self.setting_empty_unrequired_dungeons.setText(QCoreApplication.translate("main_window", u"Barren Unrequired Dungeons", None))
        self.setting_skip_horde.setText(QCoreApplication.translate("main_window", u"Skip The Horde Fight", None))
        self.setting_skip_g3.setText(QCoreApplication.translate("main_window", u"Skip Ghirahim 3 Fight", None))
        self.setting_skip_demise.setText(QCoreApplication.translate("main_window", u"Skip Demise Fight", None))
        self.open_world_group_box.setTitle(QCoreApplication.translate("main_window", u"Open World", None))
        self.open_thunderhead_label.setText(QCoreApplication.translate("main_window", u"Open Thunderhead", None))
        self.open_lake_floria_label.setText(QCoreApplication.translate("main_window", u"Open Lake Floria", None))
        self.open_earth_temple_label.setText(QCoreApplication.translate("main_window", u"Open Earth Temple", None))
        self.open_lmf_label.setText(QCoreApplication.translate("main_window", u"Open Lanyru Mining Facility", None))
        self.dungeons_group_box.setTitle(QCoreApplication.translate("main_window", u"Dungeon Items", None))
        self.small_keys_label.setText(QCoreApplication.translate("main_window", u"Small Keys", None))
        self.boss_keys_label.setText(QCoreApplication.translate("main_window", u"Boss Keys", None))
        self.map_mode_label.setText(QCoreApplication.translate("main_window", u"Dungeon Maps", None))
        self.lanayru_caves_key_label.setText(QCoreApplication.translate("main_window", u"Lanayru Caves Small Key", None))
        self.hint_placements_group_box.setTitle(QCoreApplication.translate("main_window", u"Hint Placements", None))
        self.setting_gossip_stone_hints.setText(QCoreApplication.translate("main_window", u"Gossip Stone Hints", None))
        self.setting_fi_hints.setText(QCoreApplication.translate("main_window", u"Fi Hints", None))
        self.setting_impa_sot_hint.setText(QCoreApplication.translate("main_window", u"Past Impa Stone of Trials Hint", None))
        self.song_hints_label.setText(QCoreApplication.translate("main_window", u"Song Hints", None))
        self.entrance_randomization_group_box.setTitle(QCoreApplication.translate("main_window", u"Entrance Randomization", None))
        self.setting_randomize_door_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Door Entrances", None))
        self.setting_randomize_interior_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Interior Entrances", None))
        self.setting_randomize_overworld_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Overworld Entrances", None))
        self.setting_randomize_dungeon_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Dungeon Entrances", None))
        self.setting_randomize_trial_gate_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Trial Gate Entrances", None))
        self.random_starting_spawn_label.setText(QCoreApplication.translate("main_window", u"Randomize Starting Spawn", None))
        self.setting_decouple_double_doors.setText(QCoreApplication.translate("main_window", u"Decouple Double Door Entrances", None))
        self.setting_decouple_entrances.setText(QCoreApplication.translate("main_window", u"Decouple Entrances", None))
        self.hints_group_box.setTitle(QCoreApplication.translate("main_window", u"Hints", None))
        self.path_hints_label.setText(QCoreApplication.translate("main_window", u"Path Hints", None))
        self.barren_hints_label.setText(QCoreApplication.translate("main_window", u"Barren Hints", None))
        self.location_hints_label.setText(QCoreApplication.translate("main_window", u"Location Hints", None))
        self.item_hints_label.setText(QCoreApplication.translate("main_window", u"Item Hints", None))
        self.setting_always_hints.setText(QCoreApplication.translate("main_window", u"Prioritize Remote Location Hints", None))
        self.setting_cryptic_hint_text.setText(QCoreApplication.translate("main_window", u"Cryptic Hint Text", None))
        self.tweaks_group_box.setTitle(QCoreApplication.translate("main_window", u"Tweaks", None))
        self.ammo_availability_label.setText(QCoreApplication.translate("main_window", u"Ammo Availability", None))
        self.peatrice_conversations_label.setText(QCoreApplication.translate("main_window", u"Peatrice Conversations", None))
        self.setting_full_wallet_upgrades.setText(QCoreApplication.translate("main_window", u"Full Wallet Upgrades", None))
        self.shortcuts_group_box.setTitle(QCoreApplication.translate("main_window", u"Shortcuts", None))
        self.setting_fs_lava_flow.setText(QCoreApplication.translate("main_window", u"Skip Fire Sanctuary Lava Chase", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.world_tab), QCoreApplication.translate("main_window", u"World", None))
        self.included_locations_group_box.setTitle(QCoreApplication.translate("main_window", u"Included Locations", None))
        self.included_locations_category_filters.setPlaceholderText("")
        self.included_locations_free_search.setText("")
        self.included_locations_free_search.setPlaceholderText(QCoreApplication.translate("main_window", u"Search", None))
        self.include_location_button.setText(QCoreApplication.translate("main_window", u"Include\n"
"<---", None))
        self.exclude_location_button.setText(QCoreApplication.translate("main_window", u"Exclude\n"
"--->", None))
        self.excluded_locations_group_box.setTitle(QCoreApplication.translate("main_window", u"Excluded Locations", None))
        self.excluded_locations_free_search.setPlaceholderText(QCoreApplication.translate("main_window", u"Search", None))
        self.shuffles_group_box.setTitle(QCoreApplication.translate("main_window", u"Shuffles", None))
        self.setting_shuffle_single_gratitude_crystals.setText(QCoreApplication.translate("main_window", u"Single Gratitude Crystals", None))
        self.shops_group_box.setTitle(QCoreApplication.translate("main_window", u"Shops", None))
        self.randomized_shops_label.setText(QCoreApplication.translate("main_window", u"Randomize Shops", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.locations_tab), QCoreApplication.translate("main_window", u"Locations", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.inventory_tab), QCoreApplication.translate("main_window", u"Inventory", None))
        self.logic_rules_group_box.setTitle(QCoreApplication.translate("main_window", u"Logic", None))
        self.logic_rules_label.setText(QCoreApplication.translate("main_window", u"Logic Mode", None))
        self.tricks_group_box.setTitle(QCoreApplication.translate("main_window", u"Tricks", None))
        self.precise_items_group_box.setTitle(QCoreApplication.translate("main_window", u"Precise Items", None))
        self.setting_logic_advanced_lizalfos_combat.setText(QCoreApplication.translate("main_window", u"Advanced Lizalfos Combat", None))
        self.setting_logic_skyview_precise_slingshot.setText(QCoreApplication.translate("main_window", u"Skyview Temple Precise Slingshot", None))
        self.setting_logic_lmf_ceiling_precise_slingshot.setText(QCoreApplication.translate("main_window", u"Lanayru Mining Facility Precise Slingshot", None))
        self.setting_logic_tot_slingshot.setText(QCoreApplication.translate("main_window", u"Temple of Time Precise Slingshot", None))
        self.setting_logic_bomb_throws.setText(QCoreApplication.translate("main_window", u"Precise Bomb Throws", None))
        self.setting_logic_lanayru_mine_quick_bomb.setText(QCoreApplication.translate("main_window", u"Lanayru Mine Quick Bomb", None))
        self.setting_logic_cactus_bomb_whip.setText(QCoreApplication.translate("main_window", u"Whip Bomb Flowers off Cacti", None))
        self.setting_logic_beedles_shop_with_bombs.setText(QCoreApplication.translate("main_window", u"Beedle's Shop with Bombs", None))
        self.setting_logic_bird_nest_item_from_beedles_shop.setText(QCoreApplication.translate("main_window", u"Bird's Nest from Beedle's Shop", None))
        self.setting_logic_precise_beetle.setText(QCoreApplication.translate("main_window", u"Precise Beetle Flying", None))
        self.setting_logic_skippers_fast_clawshots.setText(QCoreApplication.translate("main_window", u"Skipper's Retreat Fast Clawshots", None))
        self.setting_logic_lmf_whip_switch.setText(QCoreApplication.translate("main_window", u"Lanayru Mining Facility Whip Switch", None))
        self.setting_logic_lmf_whip_armos_room_timeshift_stone.setText(QCoreApplication.translate("main_window", u"Lanayru Mining Facility Whip Timeshift Stone", None))
        self.setting_logic_lmf_minecart_jump.setText(QCoreApplication.translate("main_window", u"Lanayru Mining Facility Ride on Minecart", None))
        self.setting_logic_present_bow_switches.setText(QCoreApplication.translate("main_window", u"Present Bow Switch Shots", None))
        self.setting_logic_skykeep_vineclip.setText(QCoreApplication.translate("main_window", u"Sky Keep Vine Clip", None))
        self.dives_and_jumps_group_box.setTitle(QCoreApplication.translate("main_window", u"Dives and Jumps", None))
        self.setting_logic_volcanic_island_dive.setText(QCoreApplication.translate("main_window", u"Volcanic Island Dive", None))
        self.setting_logic_east_island_dive.setText(QCoreApplication.translate("main_window", u"Thunderhead East Island Dive", None))
        self.setting_logic_beedles_island_cage_chest_dive.setText(QCoreApplication.translate("main_window", u"Beedle's Island Cage Chest Dive", None))
        self.setting_logic_gravestone_jump.setText(QCoreApplication.translate("main_window", u"Gravestone Jump", None))
        self.setting_logic_waterfall_cave_jump.setText(QCoreApplication.translate("main_window", u"Waterfall Cave Jump", None))
        self.setting_logic_early_lake_floria.setText(QCoreApplication.translate("main_window", u"Early Lake Floria Jumpslash", None))
        self.setting_logic_ac_lever_jump_trick.setText(QCoreApplication.translate("main_window", u"Ancient Cistern Lever Jump", None))
        self.setting_logic_ac_chest_after_whip_hooks_jump.setText(QCoreApplication.translate("main_window", u"Ancient Cistern Chest after Whip Hooks Jump", None))
        self.setting_logic_sandship_jump_to_stern.setText(QCoreApplication.translate("main_window", u"Sandship Jump to Stern", None))
        self.setting_logic_fs_pillar_jump.setText(QCoreApplication.translate("main_window", u"Fire Sanctuary Pillar Jump", None))
        self.glitches_group_box.setTitle(QCoreApplication.translate("main_window", u"Glitches", None))
        self.setting_logic_stuttersprint.setText(QCoreApplication.translate("main_window", u"Stutter Sprinting", None))
        self.setting_logic_et_slope_stuttersprint.setText(QCoreApplication.translate("main_window", u"Earth Temple Slope Stuttersprint", None))
        self.setting_logic_brakeslide.setText(QCoreApplication.translate("main_window", u"Brakesliding", None))
        self.setting_logic_tot_skip_brakeslide.setText(QCoreApplication.translate("main_window", u"Temple of Time Skip Brakeslide", None))
        self.miscellaneous_group_box.setTitle(QCoreApplication.translate("main_window", u"Miscellaneous", None))
        self.setting_logic_fire_node_without_hook_beetle.setText(QCoreApplication.translate("main_window", u"Fire Node without Hook Beetle", None))
        self.setting_logic_skyview_spider_roll.setText(QCoreApplication.translate("main_window", u"Skyview Temple Spider Roll", None))
        self.setting_logic_et_keese_skyward_strike.setText(QCoreApplication.translate("main_window", u"Earth Temple Keese Skyward Strike", None))
        self.setting_logic_et_bombless_scaldera.setText(QCoreApplication.translate("main_window", u"Earth Temple Bomb Flower Scaldera", None))
        self.setting_logic_lmf_bellowsless_moldarach.setText(QCoreApplication.translate("main_window", u"Lanayru Mining Facility Moldarach\n"
"without Gust Bellows", None))
        self.setting_logic_sandship_itemless_spume.setText(QCoreApplication.translate("main_window", u"Sandship Itemless Spume", None))
        self.setting_logic_sandship_no_combination_hint.setText(QCoreApplication.translate("main_window", u"Sandship No Combination Hint", None))
        self.setting_logic_fs_practice_sword_ghirahim_2.setText(QCoreApplication.translate("main_window", u"Fire Sanctuary Ghirahim 2 with\n"
"Practice Sword", None))
        self.setting_logic_itemless_first_timeshift_stone.setText(QCoreApplication.translate("main_window", u"Itemless First Timeshift Stone", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.logic_tab), QCoreApplication.translate("main_window", u"Logic", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("main_window", u"GroupBox", None))
        self.setting_tunic_swap.setText(QCoreApplication.translate("main_window", u"Tunic Swap", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.cosmetic_tab), QCoreApplication.translate("main_window", u"Cosmetic", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.advanced_tab), QCoreApplication.translate("main_window", u"Advanced", None))
        self.theming_group_box.setTitle(QCoreApplication.translate("main_window", u"Theming", None))
        self.theme_mode_label.setText(QCoreApplication.translate("main_window", u"Theme Mode", None))
        self.theme_presets_label.setText(QCoreApplication.translate("main_window", u"Theme Presets", None))
        self.use_custom_theme_check_box.setText(QCoreApplication.translate("main_window", u"Use Custom Theme", None))
        self.customize_theme_button.setText(QCoreApplication.translate("main_window", u"Customize Theme", None))
        self.theming_fonts.setTitle(QCoreApplication.translate("main_window", u"Fonts", None))
        self.font_family_label.setText(QCoreApplication.translate("main_window", u"Font Family", None))
        self.font_family_combo_box.setPlaceholderText(QCoreApplication.translate("main_window", u"Select Font Family", None))
        self.font_size_label.setText(QCoreApplication.translate("main_window", u"Font Size", None))
        self.font_reset_button.setText(QCoreApplication.translate("main_window", u"Reset", None))
        self.groupBox_6.setTitle("")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.accessibility_tab), QCoreApplication.translate("main_window", u"Accessibility", None))
        self.copy_setting_string_button.setText(QCoreApplication.translate("main_window", u"Copy", None))
        self.new_seed_button.setText(QCoreApplication.translate("main_window", u"New Seed", None))
        self.setting_string_label.setText(QCoreApplication.translate("main_window", u"Setting String", None))
        self.seed_label.setText(QCoreApplication.translate("main_window", u"Seed:", None))
        self.about_button.setText(QCoreApplication.translate("main_window", u"About", None))
        self.reset_button.setText(QCoreApplication.translate("main_window", u"Reset Settings to Default", None))
        self.randomize_button.setText(QCoreApplication.translate("main_window", u"Randomize", None))
    # retranslateUi

