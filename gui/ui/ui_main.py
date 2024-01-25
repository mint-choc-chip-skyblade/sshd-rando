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
    QFontComboBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QListView, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(1300, 800)
        main_window.setStyleSheet(u"QToolTip {\n"
"color: #000000;\n"
"background-color: #FFFFFF;\n"
"}")
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.verticalLayout_2 = QVBoxLayout(self.central_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setObjectName(u"tab_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_widget.sizePolicy().hasHeightForWidth())
        self.tab_widget.setSizePolicy(sizePolicy)
        self.tab_widget.setTabShape(QTabWidget.Rounded)
        self.getting_started_tab = QWidget()
        self.getting_started_tab.setObjectName(u"getting_started_tab")
        sizePolicy.setHeightForWidth(self.getting_started_tab.sizePolicy().hasHeightForWidth())
        self.getting_started_tab.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QVBoxLayout(self.getting_started_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.how_to_group_box = QGroupBox(self.getting_started_tab)
        self.how_to_group_box.setObjectName(u"how_to_group_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.how_to_group_box.sizePolicy().hasHeightForWidth())
        self.how_to_group_box.setSizePolicy(sizePolicy1)
        self.horizontalLayout_3 = QHBoxLayout(self.how_to_group_box)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.how_to_extract_group_box = QGroupBox(self.how_to_group_box)
        self.how_to_extract_group_box.setObjectName(u"how_to_extract_group_box")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.how_to_extract_group_box.sizePolicy().hasHeightForWidth())
        self.how_to_extract_group_box.setSizePolicy(sizePolicy2)
        self.verticalLayout_5 = QVBoxLayout(self.how_to_extract_group_box)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.how_to_extract_label = QLabel(self.how_to_extract_group_box)
        self.how_to_extract_label.setObjectName(u"how_to_extract_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.how_to_extract_label.sizePolicy().hasHeightForWidth())
        self.how_to_extract_label.setSizePolicy(sizePolicy3)
        self.how_to_extract_label.setTextFormat(Qt.RichText)
        self.how_to_extract_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.how_to_extract_label.setWordWrap(True)
        self.how_to_extract_label.setOpenExternalLinks(True)
        self.how_to_extract_label.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse)

        self.verticalLayout_5.addWidget(self.how_to_extract_label)


        self.horizontalLayout_3.addWidget(self.how_to_extract_group_box)

        self.how_to_left_arrow_label = QLabel(self.how_to_group_box)
        self.how_to_left_arrow_label.setObjectName(u"how_to_left_arrow_label")
        sizePolicy1.setHeightForWidth(self.how_to_left_arrow_label.sizePolicy().hasHeightForWidth())
        self.how_to_left_arrow_label.setSizePolicy(sizePolicy1)
        self.how_to_left_arrow_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.how_to_left_arrow_label)

        self.how_to_generate_group_box = QGroupBox(self.how_to_group_box)
        self.how_to_generate_group_box.setObjectName(u"how_to_generate_group_box")
        sizePolicy2.setHeightForWidth(self.how_to_generate_group_box.sizePolicy().hasHeightForWidth())
        self.how_to_generate_group_box.setSizePolicy(sizePolicy2)
        self.verticalLayout_6 = QVBoxLayout(self.how_to_generate_group_box)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.how_to_generate_label = QLabel(self.how_to_generate_group_box)
        self.how_to_generate_label.setObjectName(u"how_to_generate_label")
        sizePolicy3.setHeightForWidth(self.how_to_generate_label.sizePolicy().hasHeightForWidth())
        self.how_to_generate_label.setSizePolicy(sizePolicy3)
        self.how_to_generate_label.setTextFormat(Qt.RichText)
        self.how_to_generate_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.how_to_generate_label.setWordWrap(True)
        self.how_to_generate_label.setOpenExternalLinks(True)
        self.how_to_generate_label.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse)

        self.verticalLayout_6.addWidget(self.how_to_generate_label)


        self.horizontalLayout_3.addWidget(self.how_to_generate_group_box)

        self.how_to_right_arrow_label = QLabel(self.how_to_group_box)
        self.how_to_right_arrow_label.setObjectName(u"how_to_right_arrow_label")
        sizePolicy1.setHeightForWidth(self.how_to_right_arrow_label.sizePolicy().hasHeightForWidth())
        self.how_to_right_arrow_label.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.how_to_right_arrow_label)

        self.how_to_running_group_box = QGroupBox(self.how_to_group_box)
        self.how_to_running_group_box.setObjectName(u"how_to_running_group_box")
        sizePolicy2.setHeightForWidth(self.how_to_running_group_box.sizePolicy().hasHeightForWidth())
        self.how_to_running_group_box.setSizePolicy(sizePolicy2)
        self.verticalLayout_7 = QVBoxLayout(self.how_to_running_group_box)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.how_to_running_label = QLabel(self.how_to_running_group_box)
        self.how_to_running_label.setObjectName(u"how_to_running_label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.how_to_running_label.sizePolicy().hasHeightForWidth())
        self.how_to_running_label.setSizePolicy(sizePolicy4)
        self.how_to_running_label.setTextFormat(Qt.RichText)
        self.how_to_running_label.setScaledContents(False)
        self.how_to_running_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.how_to_running_label.setWordWrap(True)
        self.how_to_running_label.setOpenExternalLinks(True)
        self.how_to_running_label.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse)

        self.verticalLayout_7.addWidget(self.how_to_running_label)


        self.horizontalLayout_3.addWidget(self.how_to_running_group_box)


        self.verticalLayout_4.addWidget(self.how_to_group_box)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(-1, -1, -1, 0)
        self.useful_info_group_box = QGroupBox(self.getting_started_tab)
        self.useful_info_group_box.setObjectName(u"useful_info_group_box")
        sizePolicy1.setHeightForWidth(self.useful_info_group_box.sizePolicy().hasHeightForWidth())
        self.useful_info_group_box.setSizePolicy(sizePolicy1)
        self.horizontalLayout_7 = QHBoxLayout(self.useful_info_group_box)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.useful_choose_settings_group_box = QGroupBox(self.useful_info_group_box)
        self.useful_choose_settings_group_box.setObjectName(u"useful_choose_settings_group_box")
        sizePolicy1.setHeightForWidth(self.useful_choose_settings_group_box.sizePolicy().hasHeightForWidth())
        self.useful_choose_settings_group_box.setSizePolicy(sizePolicy1)
        self.verticalLayout_8 = QVBoxLayout(self.useful_choose_settings_group_box)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.choose_settings_label = QLabel(self.useful_choose_settings_group_box)
        self.choose_settings_label.setObjectName(u"choose_settings_label")
        sizePolicy2.setHeightForWidth(self.choose_settings_label.sizePolicy().hasHeightForWidth())
        self.choose_settings_label.setSizePolicy(sizePolicy2)
        self.choose_settings_label.setTextFormat(Qt.RichText)
        self.choose_settings_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.choose_settings_label.setWordWrap(True)
        self.choose_settings_label.setOpenExternalLinks(True)
        self.choose_settings_label.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse)

        self.verticalLayout_8.addWidget(self.choose_settings_label)


        self.horizontalLayout_7.addWidget(self.useful_choose_settings_group_box)

        self.useful_links_group_box = QGroupBox(self.useful_info_group_box)
        self.useful_links_group_box.setObjectName(u"useful_links_group_box")
        sizePolicy1.setHeightForWidth(self.useful_links_group_box.sizePolicy().hasHeightForWidth())
        self.useful_links_group_box.setSizePolicy(sizePolicy1)
        self.horizontalLayout_2 = QHBoxLayout(self.useful_links_group_box)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.links_label = QLabel(self.useful_links_group_box)
        self.links_label.setObjectName(u"links_label")
        sizePolicy1.setHeightForWidth(self.links_label.sizePolicy().hasHeightForWidth())
        self.links_label.setSizePolicy(sizePolicy1)
        self.links_label.setTextFormat(Qt.RichText)
        self.links_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.links_label.setOpenExternalLinks(True)

        self.horizontalLayout_2.addWidget(self.links_label)


        self.horizontalLayout_7.addWidget(self.useful_links_group_box)


        self.gridLayout_7.addWidget(self.useful_info_group_box, 0, 1, 1, 1)

        self.theming_group_box = QGroupBox(self.getting_started_tab)
        self.theming_group_box.setObjectName(u"theming_group_box")
        sizePolicy1.setHeightForWidth(self.theming_group_box.sizePolicy().hasHeightForWidth())
        self.theming_group_box.setSizePolicy(sizePolicy1)
        self.horizontalLayout_6 = QHBoxLayout(self.theming_group_box)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.groupBox = QGroupBox(self.theming_group_box)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.theme_mode_label = QLabel(self.groupBox)
        self.theme_mode_label.setObjectName(u"theme_mode_label")

        self.horizontalLayout.addWidget(self.theme_mode_label)

        self.theme_mode_combo_box = QComboBox(self.groupBox)
        self.theme_mode_combo_box.setObjectName(u"theme_mode_combo_box")
        sizePolicy.setHeightForWidth(self.theme_mode_combo_box.sizePolicy().hasHeightForWidth())
        self.theme_mode_combo_box.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.theme_mode_combo_box)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.theme_presets_label = QLabel(self.groupBox)
        self.theme_presets_label.setObjectName(u"theme_presets_label")

        self.horizontalLayout_8.addWidget(self.theme_presets_label)

        self.theme_presets_combo_box = QComboBox(self.groupBox)
        self.theme_presets_combo_box.setObjectName(u"theme_presets_combo_box")
        sizePolicy.setHeightForWidth(self.theme_presets_combo_box.sizePolicy().hasHeightForWidth())
        self.theme_presets_combo_box.setSizePolicy(sizePolicy)

        self.horizontalLayout_8.addWidget(self.theme_presets_combo_box)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.use_custom_theme_check_box = QCheckBox(self.groupBox)
        self.use_custom_theme_check_box.setObjectName(u"use_custom_theme_check_box")

        self.verticalLayout_3.addWidget(self.use_custom_theme_check_box)

        self.customize_theme_button = QPushButton(self.groupBox)
        self.customize_theme_button.setObjectName(u"customize_theme_button")

        self.verticalLayout_3.addWidget(self.customize_theme_button)

        self.verticalSpacer_2 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)


        self.horizontalLayout_6.addWidget(self.groupBox)

        self.theming_fonts = QGroupBox(self.theming_group_box)
        self.theming_fonts.setObjectName(u"theming_fonts")
        self.verticalLayout_12 = QVBoxLayout(self.theming_fonts)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.font_family_label = QLabel(self.theming_fonts)
        self.font_family_label.setObjectName(u"font_family_label")
        sizePolicy1.setHeightForWidth(self.font_family_label.sizePolicy().hasHeightForWidth())
        self.font_family_label.setSizePolicy(sizePolicy1)

        self.horizontalLayout_9.addWidget(self.font_family_label)

        self.font_family_combo_box = QFontComboBox(self.theming_fonts)
        self.font_family_combo_box.setObjectName(u"font_family_combo_box")
        sizePolicy.setHeightForWidth(self.font_family_combo_box.sizePolicy().hasHeightForWidth())
        self.font_family_combo_box.setSizePolicy(sizePolicy)
        self.font_family_combo_box.setEditable(False)
        self.font_family_combo_box.setFontFilters(QFontComboBox.ScalableFonts)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        self.font_family_combo_box.setCurrentFont(font)

        self.horizontalLayout_9.addWidget(self.font_family_combo_box)


        self.verticalLayout_12.addLayout(self.horizontalLayout_9)

        self.font_size_layout = QHBoxLayout()
        self.font_size_layout.setObjectName(u"font_size_layout")
        self.font_size_label = QLabel(self.theming_fonts)
        self.font_size_label.setObjectName(u"font_size_label")

        self.font_size_layout.addWidget(self.font_size_label)

        self.font_size_spin_box = QSpinBox(self.theming_fonts)
        self.font_size_spin_box.setObjectName(u"font_size_spin_box")
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
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

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer)


        self.horizontalLayout_6.addWidget(self.theming_fonts)

        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)

        self.gridLayout_7.addWidget(self.theming_group_box, 0, 0, 1, 1)

        self.gridLayout_7.setColumnStretch(0, 1)
        self.gridLayout_7.setColumnStretch(1, 1)

        self.verticalLayout_4.addLayout(self.gridLayout_7)

        self.verticalLayout_4.setStretch(0, 2)
        self.verticalLayout_4.setStretch(1, 1)
        self.tab_widget.addTab(self.getting_started_tab, "")
        self.gameplay_tab = QWidget()
        self.gameplay_tab.setObjectName(u"gameplay_tab")
        sizePolicy.setHeightForWidth(self.gameplay_tab.sizePolicy().hasHeightForWidth())
        self.gameplay_tab.setSizePolicy(sizePolicy)
        self.gridLayout_9 = QGridLayout(self.gameplay_tab)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.hint_placements_group_box = QGroupBox(self.gameplay_tab)
        self.hint_placements_group_box.setObjectName(u"hint_placements_group_box")
        self.verticalLayout_24 = QVBoxLayout(self.hint_placements_group_box)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.trap_mode_label = QLabel(self.hint_placements_group_box)
        self.trap_mode_label.setObjectName(u"trap_mode_label")

        self.verticalLayout_24.addWidget(self.trap_mode_label)

        self.setting_trap_mode = QComboBox(self.hint_placements_group_box)
        self.setting_trap_mode.setObjectName(u"setting_trap_mode")

        self.verticalLayout_24.addWidget(self.setting_trap_mode)

        self.trappable_items_label = QLabel(self.hint_placements_group_box)
        self.trappable_items_label.setObjectName(u"trappable_items_label")

        self.verticalLayout_24.addWidget(self.trappable_items_label)

        self.setting_trappable_items = QComboBox(self.hint_placements_group_box)
        self.setting_trappable_items.setObjectName(u"setting_trappable_items")

        self.verticalLayout_24.addWidget(self.setting_trappable_items)

        self.setting_burn_traps = QCheckBox(self.hint_placements_group_box)
        self.setting_burn_traps.setObjectName(u"setting_burn_traps")

        self.verticalLayout_24.addWidget(self.setting_burn_traps)

        self.setting_curse_traps = QCheckBox(self.hint_placements_group_box)
        self.setting_curse_traps.setObjectName(u"setting_curse_traps")

        self.verticalLayout_24.addWidget(self.setting_curse_traps)

        self.setting_noise_traps = QCheckBox(self.hint_placements_group_box)
        self.setting_noise_traps.setObjectName(u"setting_noise_traps")

        self.verticalLayout_24.addWidget(self.setting_noise_traps)

        self.setting_groose_traps = QCheckBox(self.hint_placements_group_box)
        self.setting_groose_traps.setObjectName(u"setting_groose_traps")

        self.verticalLayout_24.addWidget(self.setting_groose_traps)

        self.hint_placements_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_24.addItem(self.hint_placements_vspacer)


        self.gridLayout_9.addWidget(self.hint_placements_group_box, 0, 2, 1, 1)

        self.dungeons_group_box = QGroupBox(self.gameplay_tab)
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


        self.gridLayout_9.addWidget(self.dungeons_group_box, 0, 1, 1, 1)

        self.beat_the_game_group_box = QGroupBox(self.gameplay_tab)
        self.beat_the_game_group_box.setObjectName(u"beat_the_game_group_box")
        self.verticalLayout_13 = QVBoxLayout(self.beat_the_game_group_box)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.required_dungeons_layout = QHBoxLayout()
        self.required_dungeons_layout.setSpacing(0)
        self.required_dungeons_layout.setObjectName(u"required_dungeons_layout")
        self.required_dungeons_label = QLabel(self.beat_the_game_group_box)
        self.required_dungeons_label.setObjectName(u"required_dungeons_label")

        self.required_dungeons_layout.addWidget(self.required_dungeons_label)

        self.setting_required_dungeons = QSpinBox(self.beat_the_game_group_box)
        self.setting_required_dungeons.setObjectName(u"setting_required_dungeons")
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


        self.gridLayout_9.addWidget(self.beat_the_game_group_box, 0, 0, 1, 1)

        self.tweaks_group_box = QGroupBox(self.gameplay_tab)
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
        self.peatrice_conversations_layout.setSpacing(0)
        self.peatrice_conversations_layout.setObjectName(u"peatrice_conversations_layout")
        self.peatrice_conversations_label = QLabel(self.tweaks_group_box)
        self.peatrice_conversations_label.setObjectName(u"peatrice_conversations_label")
        sizePolicy1.setHeightForWidth(self.peatrice_conversations_label.sizePolicy().hasHeightForWidth())
        self.peatrice_conversations_label.setSizePolicy(sizePolicy1)

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

        self.setting_dowsing_after_whitesword = QCheckBox(self.tweaks_group_box)
        self.setting_dowsing_after_whitesword.setObjectName(u"setting_dowsing_after_whitesword")

        self.verticalLayout.addWidget(self.setting_dowsing_after_whitesword)

        self.setting_tunic_swap = QCheckBox(self.tweaks_group_box)
        self.setting_tunic_swap.setObjectName(u"setting_tunic_swap")

        self.verticalLayout.addWidget(self.setting_tunic_swap)

        self.setting_rotating_items = QCheckBox(self.tweaks_group_box)
        self.setting_rotating_items.setObjectName(u"setting_rotating_items")

        self.verticalLayout.addWidget(self.setting_rotating_items)

        self.tweaks_vspacer = QSpacerItem(20, 148, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.tweaks_vspacer)


        self.gridLayout_9.addWidget(self.tweaks_group_box, 0, 3, 1, 1)

        self.tab_widget.addTab(self.gameplay_tab, "")
        self.world_tab = QWidget()
        self.world_tab.setObjectName(u"world_tab")
        sizePolicy.setHeightForWidth(self.world_tab.sizePolicy().hasHeightForWidth())
        self.world_tab.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.world_tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
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


        self.gridLayout_2.addWidget(self.open_world_group_box, 0, 0, 1, 1)

        self.mixed_pools_group_box = QGroupBox(self.world_tab)
        self.mixed_pools_group_box.setObjectName(u"mixed_pools_group_box")
        self.verticalLayout_25 = QVBoxLayout(self.mixed_pools_group_box)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.setting_fs_lava_flow = QCheckBox(self.mixed_pools_group_box)
        self.setting_fs_lava_flow.setObjectName(u"setting_fs_lava_flow")

        self.verticalLayout_25.addWidget(self.setting_fs_lava_flow)

        self.mixed_pools_vspacer = QSpacerItem(20, 148, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_25.addItem(self.mixed_pools_vspacer)


        self.gridLayout_2.addWidget(self.mixed_pools_group_box, 0, 2, 1, 1)

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


        self.gridLayout_2.addWidget(self.entrance_randomization_group_box, 0, 4, 1, 1)

        self.mixed_entrance_pools_group_box = QGroupBox(self.world_tab)
        self.mixed_entrance_pools_group_box.setObjectName(u"mixed_entrance_pools_group_box")
        sizePolicy1.setHeightForWidth(self.mixed_entrance_pools_group_box.sizePolicy().hasHeightForWidth())
        self.mixed_entrance_pools_group_box.setSizePolicy(sizePolicy1)
        self.verticalLayout_28 = QVBoxLayout(self.mixed_entrance_pools_group_box)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.mixed_entrance_pools_list_label = QLabel(self.mixed_entrance_pools_group_box)
        self.mixed_entrance_pools_list_label.setObjectName(u"mixed_entrance_pools_list_label")
        self.mixed_entrance_pools_list_label.setTextFormat(Qt.RichText)
        self.mixed_entrance_pools_list_label.setWordWrap(True)
        self.mixed_entrance_pools_list_label.setOpenExternalLinks(True)
        self.mixed_entrance_pools_list_label.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse)

        self.verticalLayout_28.addWidget(self.mixed_entrance_pools_list_label)

        self.entrance_pool_selection_layout = QGridLayout()
        self.entrance_pool_selection_layout.setObjectName(u"entrance_pool_selection_layout")
        self.highlighted_entrance_pool_label = QLabel(self.mixed_entrance_pools_group_box)
        self.highlighted_entrance_pool_label.setObjectName(u"highlighted_entrance_pool_label")

        self.entrance_pool_selection_layout.addWidget(self.highlighted_entrance_pool_label, 0, 0, 1, 1)

        self.highlighted_entrance_pool_combo_box = QComboBox(self.mixed_entrance_pools_group_box)
        self.highlighted_entrance_pool_combo_box.setObjectName(u"highlighted_entrance_pool_combo_box")

        self.entrance_pool_selection_layout.addWidget(self.highlighted_entrance_pool_combo_box, 0, 1, 1, 1)

        self.selected_entrance_type_label = QLabel(self.mixed_entrance_pools_group_box)
        self.selected_entrance_type_label.setObjectName(u"selected_entrance_type_label")

        self.entrance_pool_selection_layout.addWidget(self.selected_entrance_type_label, 1, 0, 1, 1)

        self.selected_entrance_type_combo_box = QComboBox(self.mixed_entrance_pools_group_box)
        self.selected_entrance_type_combo_box.setObjectName(u"selected_entrance_type_combo_box")

        self.entrance_pool_selection_layout.addWidget(self.selected_entrance_type_combo_box, 1, 1, 1, 1)


        self.verticalLayout_28.addLayout(self.entrance_pool_selection_layout)

        self.entrance_pool_button_layout = QHBoxLayout()
        self.entrance_pool_button_layout.setObjectName(u"entrance_pool_button_layout")
        self.add_entrance_type_button = QPushButton(self.mixed_entrance_pools_group_box)
        self.add_entrance_type_button.setObjectName(u"add_entrance_type_button")

        self.entrance_pool_button_layout.addWidget(self.add_entrance_type_button)

        self.remove_entrance_type_button = QPushButton(self.mixed_entrance_pools_group_box)
        self.remove_entrance_type_button.setObjectName(u"remove_entrance_type_button")

        self.entrance_pool_button_layout.addWidget(self.remove_entrance_type_button)


        self.verticalLayout_28.addLayout(self.entrance_pool_button_layout)

        self.mixed_entrance_pools_reset_button = QPushButton(self.mixed_entrance_pools_group_box)
        self.mixed_entrance_pools_reset_button.setObjectName(u"mixed_entrance_pools_reset_button")

        self.verticalLayout_28.addWidget(self.mixed_entrance_pools_reset_button)

        self.verticalSpacer_4 = QSpacerItem(20, 4, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_28.addItem(self.verticalSpacer_4)

        self.line = QFrame(self.mixed_entrance_pools_group_box)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_28.addWidget(self.line)

        self.verticalSpacer_5 = QSpacerItem(20, 4, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_28.addItem(self.verticalSpacer_5)

        self.mixed_entrance_pools_explainer_label = QLabel(self.mixed_entrance_pools_group_box)
        self.mixed_entrance_pools_explainer_label.setObjectName(u"mixed_entrance_pools_explainer_label")
        sizePolicy3.setHeightForWidth(self.mixed_entrance_pools_explainer_label.sizePolicy().hasHeightForWidth())
        self.mixed_entrance_pools_explainer_label.setSizePolicy(sizePolicy3)
        self.mixed_entrance_pools_explainer_label.setTextFormat(Qt.RichText)
        self.mixed_entrance_pools_explainer_label.setWordWrap(True)
        self.mixed_entrance_pools_explainer_label.setOpenExternalLinks(True)
        self.mixed_entrance_pools_explainer_label.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse)

        self.verticalLayout_28.addWidget(self.mixed_entrance_pools_explainer_label)

        self.mixed_entrance_pools_vspacer = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_28.addItem(self.mixed_entrance_pools_vspacer)


        self.gridLayout_2.addWidget(self.mixed_entrance_pools_group_box, 0, 5, 1, 1)

        self.tab_widget.addTab(self.world_tab, "")
        self.locations_tab = QWidget()
        self.locations_tab.setObjectName(u"locations_tab")
        sizePolicy.setHeightForWidth(self.locations_tab.sizePolicy().hasHeightForWidth())
        self.locations_tab.setSizePolicy(sizePolicy)
        self.gridLayout_3 = QGridLayout(self.locations_tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.locations_button_layout = QVBoxLayout()
        self.locations_button_layout.setObjectName(u"locations_button_layout")
        self.individual_locations_top_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.locations_button_layout.addItem(self.individual_locations_top_vspacer)

        self.include_location_button = QPushButton(self.locations_tab)
        self.include_location_button.setObjectName(u"include_location_button")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.include_location_button.sizePolicy().hasHeightForWidth())
        self.include_location_button.setSizePolicy(sizePolicy6)

        self.locations_button_layout.addWidget(self.include_location_button)

        self.individual_locations_middle_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.locations_button_layout.addItem(self.individual_locations_middle_vspacer)

        self.exclude_location_button = QPushButton(self.locations_tab)
        self.exclude_location_button.setObjectName(u"exclude_location_button")
        sizePolicy6.setHeightForWidth(self.exclude_location_button.sizePolicy().hasHeightForWidth())
        self.exclude_location_button.setSizePolicy(sizePolicy6)

        self.locations_button_layout.addWidget(self.exclude_location_button)

        self.individual_locations_bottom_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.locations_button_layout.addItem(self.individual_locations_bottom_vspacer)

        self.locations_reset_button = QPushButton(self.locations_tab)
        self.locations_reset_button.setObjectName(u"locations_reset_button")

        self.locations_button_layout.addWidget(self.locations_reset_button)


        self.gridLayout_3.addLayout(self.locations_button_layout, 0, 1, 1, 1)

        self.shuffles_group_box = QGroupBox(self.locations_tab)
        self.shuffles_group_box.setObjectName(u"shuffles_group_box")
        sizePolicy1.setHeightForWidth(self.shuffles_group_box.sizePolicy().hasHeightForWidth())
        self.shuffles_group_box.setSizePolicy(sizePolicy1)
        self.verticalLayout_10 = QVBoxLayout(self.shuffles_group_box)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.beedle_shop_shuffle_label = QLabel(self.shuffles_group_box)
        self.beedle_shop_shuffle_label.setObjectName(u"beedle_shop_shuffle_label")

        self.verticalLayout_10.addWidget(self.beedle_shop_shuffle_label)

        self.setting_beedle_shop_shuffle = QComboBox(self.shuffles_group_box)
        self.setting_beedle_shop_shuffle.setObjectName(u"setting_beedle_shop_shuffle")

        self.verticalLayout_10.addWidget(self.setting_beedle_shop_shuffle)

        self.rupee_shuffle_label = QLabel(self.shuffles_group_box)
        self.rupee_shuffle_label.setObjectName(u"rupee_shuffle_label")

        self.verticalLayout_10.addWidget(self.rupee_shuffle_label)

        self.setting_rupee_shuffle = QComboBox(self.shuffles_group_box)
        self.setting_rupee_shuffle.setObjectName(u"setting_rupee_shuffle")

        self.verticalLayout_10.addWidget(self.setting_rupee_shuffle)

        self.setting_underground_rupee_shuffle = QCheckBox(self.shuffles_group_box)
        self.setting_underground_rupee_shuffle.setObjectName(u"setting_underground_rupee_shuffle")

        self.verticalLayout_10.addWidget(self.setting_underground_rupee_shuffle)

        self.setting_goddess_chest_shuffle = QCheckBox(self.shuffles_group_box)
        self.setting_goddess_chest_shuffle.setObjectName(u"setting_goddess_chest_shuffle")

        self.verticalLayout_10.addWidget(self.setting_goddess_chest_shuffle)

        self.setting_gratitude_crystal_shuffle = QCheckBox(self.shuffles_group_box)
        self.setting_gratitude_crystal_shuffle.setObjectName(u"setting_gratitude_crystal_shuffle")

        self.verticalLayout_10.addWidget(self.setting_gratitude_crystal_shuffle)

        self.setting_stamina_fruit_shuffle = QCheckBox(self.shuffles_group_box)
        self.setting_stamina_fruit_shuffle.setObjectName(u"setting_stamina_fruit_shuffle")

        self.verticalLayout_10.addWidget(self.setting_stamina_fruit_shuffle)

        self.npc_closet_shuffle_label = QLabel(self.shuffles_group_box)
        self.npc_closet_shuffle_label.setObjectName(u"npc_closet_shuffle_label")

        self.verticalLayout_10.addWidget(self.npc_closet_shuffle_label)

        self.setting_npc_closet_shuffle = QComboBox(self.shuffles_group_box)
        self.setting_npc_closet_shuffle.setObjectName(u"setting_npc_closet_shuffle")

        self.verticalLayout_10.addWidget(self.setting_npc_closet_shuffle)

        self.shuffles_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.shuffles_vspacer)


        self.gridLayout_3.addWidget(self.shuffles_group_box, 0, 3, 1, 1)

        self.excluded_locations_group_box = QGroupBox(self.locations_tab)
        self.excluded_locations_group_box.setObjectName(u"excluded_locations_group_box")
        self.verticalLayout_18 = QVBoxLayout(self.excluded_locations_group_box)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.excluded_locations_filter_layout = QHBoxLayout()
        self.excluded_locations_filter_layout.setObjectName(u"excluded_locations_filter_layout")
        self.excluded_locations_type_filter = QComboBox(self.excluded_locations_group_box)
        self.excluded_locations_type_filter.setObjectName(u"excluded_locations_type_filter")

        self.excluded_locations_filter_layout.addWidget(self.excluded_locations_type_filter)

        self.excluded_locations_free_search = QLineEdit(self.excluded_locations_group_box)
        self.excluded_locations_free_search.setObjectName(u"excluded_locations_free_search")
        sizePolicy7 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.excluded_locations_free_search.sizePolicy().hasHeightForWidth())
        self.excluded_locations_free_search.setSizePolicy(sizePolicy7)
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


        self.gridLayout_3.addWidget(self.excluded_locations_group_box, 0, 2, 1, 1)

        self.included_locations_group_box = QGroupBox(self.locations_tab)
        self.included_locations_group_box.setObjectName(u"included_locations_group_box")
        self.verticalLayout_9 = QVBoxLayout(self.included_locations_group_box)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.included_locations_filter_layout = QHBoxLayout()
        self.included_locations_filter_layout.setObjectName(u"included_locations_filter_layout")
        self.included_locations_type_filter = QComboBox(self.included_locations_group_box)
        self.included_locations_type_filter.setObjectName(u"included_locations_type_filter")

        self.included_locations_filter_layout.addWidget(self.included_locations_type_filter)

        self.included_locations_free_search = QLineEdit(self.included_locations_group_box)
        self.included_locations_free_search.setObjectName(u"included_locations_free_search")
        sizePolicy7.setHeightForWidth(self.included_locations_free_search.sizePolicy().hasHeightForWidth())
        self.included_locations_free_search.setSizePolicy(sizePolicy7)
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


        self.gridLayout_3.addWidget(self.included_locations_group_box, 0, 0, 1, 1)

        self.gridLayout_3.setColumnStretch(0, 6)
        self.gridLayout_3.setColumnStretch(1, 1)
        self.gridLayout_3.setColumnStretch(2, 6)
        self.gridLayout_3.setColumnStretch(3, 4)
        self.tab_widget.addTab(self.locations_tab, "")
        self.inventory_tab = QWidget()
        self.inventory_tab.setObjectName(u"inventory_tab")
        sizePolicy.setHeightForWidth(self.inventory_tab.sizePolicy().hasHeightForWidth())
        self.inventory_tab.setSizePolicy(sizePolicy)
        self.gridLayout_4 = QGridLayout(self.inventory_tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.randomized_items_group_box = QGroupBox(self.inventory_tab)
        self.randomized_items_group_box.setObjectName(u"randomized_items_group_box")
        sizePolicy1.setHeightForWidth(self.randomized_items_group_box.sizePolicy().hasHeightForWidth())
        self.randomized_items_group_box.setSizePolicy(sizePolicy1)
        self.verticalLayout_15 = QVBoxLayout(self.randomized_items_group_box)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.randomized_items_filter_layout = QHBoxLayout()
        self.randomized_items_filter_layout.setObjectName(u"randomized_items_filter_layout")
        self.randomized_items_type_filter = QComboBox(self.randomized_items_group_box)
        self.randomized_items_type_filter.setObjectName(u"randomized_items_type_filter")

        self.randomized_items_filter_layout.addWidget(self.randomized_items_type_filter)

        self.randomized_items_free_search = QLineEdit(self.randomized_items_group_box)
        self.randomized_items_free_search.setObjectName(u"randomized_items_free_search")
        self.randomized_items_free_search.setClearButtonEnabled(True)

        self.randomized_items_filter_layout.addWidget(self.randomized_items_free_search)


        self.verticalLayout_15.addLayout(self.randomized_items_filter_layout)

        self.randomized_items_list_view = QListView(self.randomized_items_group_box)
        self.randomized_items_list_view.setObjectName(u"randomized_items_list_view")
        sizePolicy8 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.randomized_items_list_view.sizePolicy().hasHeightForWidth())
        self.randomized_items_list_view.setSizePolicy(sizePolicy8)
        self.randomized_items_list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.randomized_items_list_view.setProperty("showDropIndicator", False)
        self.randomized_items_list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.randomized_items_list_view.setSelectionRectVisible(False)

        self.verticalLayout_15.addWidget(self.randomized_items_list_view)


        self.gridLayout_4.addWidget(self.randomized_items_group_box, 0, 0, 1, 1)

        self.starting_items_group_box = QGroupBox(self.inventory_tab)
        self.starting_items_group_box.setObjectName(u"starting_items_group_box")
        self.verticalLayout_11 = QVBoxLayout(self.starting_items_group_box)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.starting_items_filter_layout = QHBoxLayout()
        self.starting_items_filter_layout.setObjectName(u"starting_items_filter_layout")
        self.starting_items_type_filter = QComboBox(self.starting_items_group_box)
        self.starting_items_type_filter.setObjectName(u"starting_items_type_filter")

        self.starting_items_filter_layout.addWidget(self.starting_items_type_filter)

        self.starting_items_free_search = QLineEdit(self.starting_items_group_box)
        self.starting_items_free_search.setObjectName(u"starting_items_free_search")
        self.starting_items_free_search.setClearButtonEnabled(True)

        self.starting_items_filter_layout.addWidget(self.starting_items_free_search)


        self.verticalLayout_11.addLayout(self.starting_items_filter_layout)

        self.starting_items_list_view = QListView(self.starting_items_group_box)
        self.starting_items_list_view.setObjectName(u"starting_items_list_view")
        sizePolicy8.setHeightForWidth(self.starting_items_list_view.sizePolicy().hasHeightForWidth())
        self.starting_items_list_view.setSizePolicy(sizePolicy8)
        self.starting_items_list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.starting_items_list_view.setProperty("showDropIndicator", False)
        self.starting_items_list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.starting_items_list_view.setSelectionRectVisible(False)

        self.verticalLayout_11.addWidget(self.starting_items_list_view)


        self.gridLayout_4.addWidget(self.starting_items_group_box, 0, 2, 1, 1)

        self.inventory_button_layout = QVBoxLayout()
        self.inventory_button_layout.setObjectName(u"inventory_button_layout")
        self.inventory_button_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.starting_items_top_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.inventory_button_layout.addItem(self.starting_items_top_vspacer)

        self.randomize_item_button = QPushButton(self.inventory_tab)
        self.randomize_item_button.setObjectName(u"randomize_item_button")
        sizePolicy6.setHeightForWidth(self.randomize_item_button.sizePolicy().hasHeightForWidth())
        self.randomize_item_button.setSizePolicy(sizePolicy6)

        self.inventory_button_layout.addWidget(self.randomize_item_button)

        self.starting_items_middle_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.inventory_button_layout.addItem(self.starting_items_middle_vspacer)

        self.start_with_item_button = QPushButton(self.inventory_tab)
        self.start_with_item_button.setObjectName(u"start_with_item_button")
        sizePolicy6.setHeightForWidth(self.start_with_item_button.sizePolicy().hasHeightForWidth())
        self.start_with_item_button.setSizePolicy(sizePolicy6)

        self.inventory_button_layout.addWidget(self.start_with_item_button)

        self.starting_items_bottom_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.inventory_button_layout.addItem(self.starting_items_bottom_vspacer)

        self.inventory_reset_button = QPushButton(self.inventory_tab)
        self.inventory_reset_button.setObjectName(u"inventory_reset_button")

        self.inventory_button_layout.addWidget(self.inventory_reset_button)


        self.gridLayout_4.addLayout(self.inventory_button_layout, 0, 1, 1, 1)

        self.item_settings_group_box = QGroupBox(self.inventory_tab)
        self.item_settings_group_box.setObjectName(u"item_settings_group_box")
        sizePolicy1.setHeightForWidth(self.item_settings_group_box.sizePolicy().hasHeightForWidth())
        self.item_settings_group_box.setSizePolicy(sizePolicy1)
        self.verticalLayout_29 = QVBoxLayout(self.item_settings_group_box)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.item_pool_label = QLabel(self.item_settings_group_box)
        self.item_pool_label.setObjectName(u"item_pool_label")

        self.verticalLayout_29.addWidget(self.item_pool_label)

        self.setting_item_pool = QComboBox(self.item_settings_group_box)
        self.setting_item_pool.setObjectName(u"setting_item_pool")

        self.verticalLayout_29.addWidget(self.setting_item_pool)

        self.starting_sword_label = QLabel(self.item_settings_group_box)
        self.starting_sword_label.setObjectName(u"starting_sword_label")

        self.verticalLayout_29.addWidget(self.starting_sword_label)

        self.setting_starting_sword = QComboBox(self.item_settings_group_box)
        self.setting_starting_sword.setObjectName(u"setting_starting_sword")

        self.verticalLayout_29.addWidget(self.setting_starting_sword)

        self.random_starting_tablet_count_layout = QHBoxLayout()
        self.random_starting_tablet_count_layout.setSpacing(0)
        self.random_starting_tablet_count_layout.setObjectName(u"random_starting_tablet_count_layout")
        self.random_starting_tablet_count_label = QLabel(self.item_settings_group_box)
        self.random_starting_tablet_count_label.setObjectName(u"random_starting_tablet_count_label")

        self.random_starting_tablet_count_layout.addWidget(self.random_starting_tablet_count_label)

        self.setting_random_starting_tablet_count = QSpinBox(self.item_settings_group_box)
        self.setting_random_starting_tablet_count.setObjectName(u"setting_random_starting_tablet_count")
        sizePolicy5.setHeightForWidth(self.setting_random_starting_tablet_count.sizePolicy().hasHeightForWidth())
        self.setting_random_starting_tablet_count.setSizePolicy(sizePolicy5)
        self.setting_random_starting_tablet_count.setMaximumSize(QSize(16777215, 16777215))

        self.random_starting_tablet_count_layout.addWidget(self.setting_random_starting_tablet_count)


        self.verticalLayout_29.addLayout(self.random_starting_tablet_count_layout)

        self.random_starting_item_count_layout = QHBoxLayout()
        self.random_starting_item_count_layout.setSpacing(0)
        self.random_starting_item_count_layout.setObjectName(u"random_starting_item_count_layout")
        self.random_starting_item_count_label = QLabel(self.item_settings_group_box)
        self.random_starting_item_count_label.setObjectName(u"random_starting_item_count_label")

        self.random_starting_item_count_layout.addWidget(self.random_starting_item_count_label)

        self.setting_random_starting_item_count = QSpinBox(self.item_settings_group_box)
        self.setting_random_starting_item_count.setObjectName(u"setting_random_starting_item_count")
        sizePolicy5.setHeightForWidth(self.setting_random_starting_item_count.sizePolicy().hasHeightForWidth())
        self.setting_random_starting_item_count.setSizePolicy(sizePolicy5)

        self.random_starting_item_count_layout.addWidget(self.setting_random_starting_item_count)


        self.verticalLayout_29.addLayout(self.random_starting_item_count_layout)

        self.item_settings_vspacer = QSpacerItem(20, 137, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_29.addItem(self.item_settings_vspacer)


        self.gridLayout_4.addWidget(self.item_settings_group_box, 0, 3, 1, 1)

        self.gridLayout_4.setColumnStretch(0, 6)
        self.gridLayout_4.setColumnStretch(1, 1)
        self.gridLayout_4.setColumnStretch(2, 6)
        self.gridLayout_4.setColumnStretch(3, 4)
        self.tab_widget.addTab(self.inventory_tab, "")
        self.hints_tab = QWidget()
        self.hints_tab.setObjectName(u"hints_tab")
        sizePolicy.setHeightForWidth(self.hints_tab.sizePolicy().hasHeightForWidth())
        self.hints_tab.setSizePolicy(sizePolicy)
        self.gridLayout_8 = QGridLayout(self.hints_tab)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.included_hint_locations_group_box = QGroupBox(self.hints_tab)
        self.included_hint_locations_group_box.setObjectName(u"included_hint_locations_group_box")
        sizePolicy1.setHeightForWidth(self.included_hint_locations_group_box.sizePolicy().hasHeightForWidth())
        self.included_hint_locations_group_box.setSizePolicy(sizePolicy1)
        self.verticalLayout_26 = QVBoxLayout(self.included_hint_locations_group_box)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.included_hint_locations_free_search = QLineEdit(self.included_hint_locations_group_box)
        self.included_hint_locations_free_search.setObjectName(u"included_hint_locations_free_search")
        self.included_hint_locations_free_search.setClearButtonEnabled(True)

        self.verticalLayout_26.addWidget(self.included_hint_locations_free_search)

        self.included_hint_locations_list_view = QListView(self.included_hint_locations_group_box)
        self.included_hint_locations_list_view.setObjectName(u"included_hint_locations_list_view")
        sizePolicy8.setHeightForWidth(self.included_hint_locations_list_view.sizePolicy().hasHeightForWidth())
        self.included_hint_locations_list_view.setSizePolicy(sizePolicy8)
        self.included_hint_locations_list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.included_hint_locations_list_view.setProperty("showDropIndicator", False)
        self.included_hint_locations_list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.included_hint_locations_list_view.setSelectionRectVisible(False)

        self.verticalLayout_26.addWidget(self.included_hint_locations_list_view)


        self.gridLayout_8.addWidget(self.included_hint_locations_group_box, 0, 0, 1, 1)

        self.hints_button_layout = QVBoxLayout()
        self.hints_button_layout.setObjectName(u"hints_button_layout")
        self.hints_button_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.hints_top_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.hints_button_layout.addItem(self.hints_top_vspacer)

        self.include_hint_location_button = QPushButton(self.hints_tab)
        self.include_hint_location_button.setObjectName(u"include_hint_location_button")
        sizePolicy6.setHeightForWidth(self.include_hint_location_button.sizePolicy().hasHeightForWidth())
        self.include_hint_location_button.setSizePolicy(sizePolicy6)

        self.hints_button_layout.addWidget(self.include_hint_location_button)

        self.hints_middle_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.hints_button_layout.addItem(self.hints_middle_vspacer)

        self.exclude_hint_location_button = QPushButton(self.hints_tab)
        self.exclude_hint_location_button.setObjectName(u"exclude_hint_location_button")
        sizePolicy6.setHeightForWidth(self.exclude_hint_location_button.sizePolicy().hasHeightForWidth())
        self.exclude_hint_location_button.setSizePolicy(sizePolicy6)

        self.hints_button_layout.addWidget(self.exclude_hint_location_button)

        self.hints_bottom_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.hints_button_layout.addItem(self.hints_bottom_vspacer)

        self.hints_reset_button = QPushButton(self.hints_tab)
        self.hints_reset_button.setObjectName(u"hints_reset_button")

        self.hints_button_layout.addWidget(self.hints_reset_button)


        self.gridLayout_8.addLayout(self.hints_button_layout, 0, 1, 1, 1)

        self.excluded_hint_locations_group_box = QGroupBox(self.hints_tab)
        self.excluded_hint_locations_group_box.setObjectName(u"excluded_hint_locations_group_box")
        self.verticalLayout_27 = QVBoxLayout(self.excluded_hint_locations_group_box)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.excluded_hint_locations_free_search = QLineEdit(self.excluded_hint_locations_group_box)
        self.excluded_hint_locations_free_search.setObjectName(u"excluded_hint_locations_free_search")
        self.excluded_hint_locations_free_search.setClearButtonEnabled(True)

        self.verticalLayout_27.addWidget(self.excluded_hint_locations_free_search)

        self.excluded_hint_locations_list_view = QListView(self.excluded_hint_locations_group_box)
        self.excluded_hint_locations_list_view.setObjectName(u"excluded_hint_locations_list_view")
        sizePolicy8.setHeightForWidth(self.excluded_hint_locations_list_view.sizePolicy().hasHeightForWidth())
        self.excluded_hint_locations_list_view.setSizePolicy(sizePolicy8)
        self.excluded_hint_locations_list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.excluded_hint_locations_list_view.setProperty("showDropIndicator", False)
        self.excluded_hint_locations_list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.excluded_hint_locations_list_view.setSelectionRectVisible(False)

        self.verticalLayout_27.addWidget(self.excluded_hint_locations_list_view)


        self.gridLayout_8.addWidget(self.excluded_hint_locations_group_box, 0, 2, 1, 1)

        self.hints_group_box = QGroupBox(self.hints_tab)
        self.hints_group_box.setObjectName(u"hints_group_box")
        self.verticalLayout_23 = QVBoxLayout(self.hints_group_box)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.setting_gossip_stone_hints = QCheckBox(self.hints_group_box)
        self.setting_gossip_stone_hints.setObjectName(u"setting_gossip_stone_hints")

        self.verticalLayout_23.addWidget(self.setting_gossip_stone_hints)

        self.setting_fi_hints = QCheckBox(self.hints_group_box)
        self.setting_fi_hints.setObjectName(u"setting_fi_hints")

        self.verticalLayout_23.addWidget(self.setting_fi_hints)

        self.setting_impa_sot_hint = QCheckBox(self.hints_group_box)
        self.setting_impa_sot_hint.setObjectName(u"setting_impa_sot_hint")

        self.verticalLayout_23.addWidget(self.setting_impa_sot_hint)

        self.song_hints_label = QLabel(self.hints_group_box)
        self.song_hints_label.setObjectName(u"song_hints_label")

        self.verticalLayout_23.addWidget(self.song_hints_label)

        self.setting_song_hints = QComboBox(self.hints_group_box)
        self.setting_song_hints.setObjectName(u"setting_song_hints")

        self.verticalLayout_23.addWidget(self.setting_song_hints)

        self.path_hints_layout = QHBoxLayout()
        self.path_hints_layout.setSpacing(0)
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
        self.barren_hints_layout.setSpacing(0)
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
        self.location_hints_layout.setSpacing(0)
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
        self.item_hints_layout.setSpacing(0)
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

        self.hints_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_23.addItem(self.hints_vspacer)


        self.gridLayout_8.addWidget(self.hints_group_box, 0, 3, 1, 1)

        self.gridLayout_8.setColumnStretch(0, 6)
        self.gridLayout_8.setColumnStretch(1, 1)
        self.gridLayout_8.setColumnStretch(2, 6)
        self.gridLayout_8.setColumnStretch(3, 4)
        self.tab_widget.addTab(self.hints_tab, "")
        self.logic_tab = QWidget()
        self.logic_tab.setObjectName(u"logic_tab")
        sizePolicy.setHeightForWidth(self.logic_tab.sizePolicy().hasHeightForWidth())
        self.logic_tab.setSizePolicy(sizePolicy)
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
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.tricks_group_box.sizePolicy().hasHeightForWidth())
        self.tricks_group_box.setSizePolicy(sizePolicy9)
        self.gridLayout_6 = QGridLayout(self.tricks_group_box)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.precise_items_group_box = QGroupBox(self.tricks_group_box)
        self.precise_items_group_box.setObjectName(u"precise_items_group_box")
        sizePolicy2.setHeightForWidth(self.precise_items_group_box.sizePolicy().hasHeightForWidth())
        self.precise_items_group_box.setSizePolicy(sizePolicy2)
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


        self.gridLayout_6.addWidget(self.precise_items_group_box, 0, 0, 1, 1)

        self.dives_and_jumps_group_box = QGroupBox(self.tricks_group_box)
        self.dives_and_jumps_group_box.setObjectName(u"dives_and_jumps_group_box")
        sizePolicy2.setHeightForWidth(self.dives_and_jumps_group_box.sizePolicy().hasHeightForWidth())
        self.dives_and_jumps_group_box.setSizePolicy(sizePolicy2)
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

        self.setting_logic_skyview_coiled_rupee_jump = QCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_skyview_coiled_rupee_jump.setObjectName(u"setting_logic_skyview_coiled_rupee_jump")

        self.verticalLayout_19.addWidget(self.setting_logic_skyview_coiled_rupee_jump)

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


        self.gridLayout_6.addWidget(self.dives_and_jumps_group_box, 0, 1, 1, 1)

        self.glitches_group_box = QGroupBox(self.tricks_group_box)
        self.glitches_group_box.setObjectName(u"glitches_group_box")
        sizePolicy2.setHeightForWidth(self.glitches_group_box.sizePolicy().hasHeightForWidth())
        self.glitches_group_box.setSizePolicy(sizePolicy2)
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


        self.gridLayout_6.addWidget(self.glitches_group_box, 0, 2, 1, 1)

        self.miscellaneous_group_box = QGroupBox(self.tricks_group_box)
        self.miscellaneous_group_box.setObjectName(u"miscellaneous_group_box")
        sizePolicy2.setHeightForWidth(self.miscellaneous_group_box.sizePolicy().hasHeightForWidth())
        self.miscellaneous_group_box.setSizePolicy(sizePolicy2)
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


        self.gridLayout_6.addWidget(self.miscellaneous_group_box, 0, 3, 1, 1)

        self.gridLayout_6.setColumnStretch(0, 1)
        self.gridLayout_6.setColumnStretch(1, 1)
        self.gridLayout_6.setColumnStretch(2, 1)
        self.gridLayout_6.setColumnStretch(3, 1)

        self.gridLayout_5.addWidget(self.tricks_group_box, 1, 0, 1, 1)

        self.tab_widget.addTab(self.logic_tab, "")
        self.advanced_tab = QWidget()
        self.advanced_tab.setObjectName(u"advanced_tab")
        sizePolicy.setHeightForWidth(self.advanced_tab.sizePolicy().hasHeightForWidth())
        self.advanced_tab.setSizePolicy(sizePolicy)
        self.horizontalLayout_4 = QHBoxLayout(self.advanced_tab)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.file_setup_group_box = QGroupBox(self.advanced_tab)
        self.file_setup_group_box.setObjectName(u"file_setup_group_box")
        sizePolicy2.setHeightForWidth(self.file_setup_group_box.sizePolicy().hasHeightForWidth())
        self.file_setup_group_box.setSizePolicy(sizePolicy2)
        self.verticalLayout_31 = QVBoxLayout(self.file_setup_group_box)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.output_label = QLabel(self.file_setup_group_box)
        self.output_label.setObjectName(u"output_label")
        sizePolicy1.setHeightForWidth(self.output_label.sizePolicy().hasHeightForWidth())
        self.output_label.setSizePolicy(sizePolicy1)

        self.verticalLayout_31.addWidget(self.output_label)

        self.output_layout = QHBoxLayout()
        self.output_layout.setObjectName(u"output_layout")
        self.output_line_edit = QLineEdit(self.file_setup_group_box)
        self.output_line_edit.setObjectName(u"output_line_edit")

        self.output_layout.addWidget(self.output_line_edit)

        self.output_button = QPushButton(self.file_setup_group_box)
        self.output_button.setObjectName(u"output_button")

        self.output_layout.addWidget(self.output_button)


        self.verticalLayout_31.addLayout(self.output_layout)

        self.verify_extract_label = QLabel(self.file_setup_group_box)
        self.verify_extract_label.setObjectName(u"verify_extract_label")

        self.verticalLayout_31.addWidget(self.verify_extract_label)

        self.verify_extract_layout = QHBoxLayout()
        self.verify_extract_layout.setObjectName(u"verify_extract_layout")
        self.verify_important_extract_button = QPushButton(self.file_setup_group_box)
        self.verify_important_extract_button.setObjectName(u"verify_important_extract_button")

        self.verify_extract_layout.addWidget(self.verify_important_extract_button)

        self.verify_all_extract_button = QPushButton(self.file_setup_group_box)
        self.verify_all_extract_button.setObjectName(u"verify_all_extract_button")

        self.verify_extract_layout.addWidget(self.verify_all_extract_button)


        self.verticalLayout_31.addLayout(self.verify_extract_layout)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_31.addItem(self.verticalSpacer_3)


        self.horizontalLayout_4.addWidget(self.file_setup_group_box)

        self.plandomizer_group_box = QGroupBox(self.advanced_tab)
        self.plandomizer_group_box.setObjectName(u"plandomizer_group_box")
        sizePolicy2.setHeightForWidth(self.plandomizer_group_box.sizePolicy().hasHeightForWidth())
        self.plandomizer_group_box.setSizePolicy(sizePolicy2)
        self.verticalLayout_30 = QVBoxLayout(self.plandomizer_group_box)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.plandomizer_warning_label = QLabel(self.plandomizer_group_box)
        self.plandomizer_warning_label.setObjectName(u"plandomizer_warning_label")
        self.plandomizer_warning_label.setTextFormat(Qt.RichText)
        self.plandomizer_warning_label.setWordWrap(True)
        self.plandomizer_warning_label.setOpenExternalLinks(True)
        self.plandomizer_warning_label.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse)

        self.verticalLayout_30.addWidget(self.plandomizer_warning_label)

        self.config_use_plandomizer = QCheckBox(self.plandomizer_group_box)
        self.config_use_plandomizer.setObjectName(u"config_use_plandomizer")

        self.verticalLayout_30.addWidget(self.config_use_plandomizer)

        self.selected_plandomizer_file_label = QLabel(self.plandomizer_group_box)
        self.selected_plandomizer_file_label.setObjectName(u"selected_plandomizer_file_label")

        self.verticalLayout_30.addWidget(self.selected_plandomizer_file_label)

        self.selected_plandomizer_file_combo_box = QComboBox(self.plandomizer_group_box)
        self.selected_plandomizer_file_combo_box.setObjectName(u"selected_plandomizer_file_combo_box")
        sizePolicy10 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.selected_plandomizer_file_combo_box.sizePolicy().hasHeightForWidth())
        self.selected_plandomizer_file_combo_box.setSizePolicy(sizePolicy10)
        self.selected_plandomizer_file_combo_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.verticalLayout_30.addWidget(self.selected_plandomizer_file_combo_box)

        self.open_plandomizer_folder_button = QPushButton(self.plandomizer_group_box)
        self.open_plandomizer_folder_button.setObjectName(u"open_plandomizer_folder_button")

        self.verticalLayout_30.addWidget(self.open_plandomizer_folder_button)

        self.plandomizer_vspacer = QSpacerItem(20, 369, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_30.addItem(self.plandomizer_vspacer)


        self.horizontalLayout_4.addWidget(self.plandomizer_group_box)

        self.random_settings_group_box = QGroupBox(self.advanced_tab)
        self.random_settings_group_box.setObjectName(u"random_settings_group_box")
        sizePolicy2.setHeightForWidth(self.random_settings_group_box.sizePolicy().hasHeightForWidth())
        self.random_settings_group_box.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.random_settings_group_box)

        self.randomization_settings_group_box = QGroupBox(self.advanced_tab)
        self.randomization_settings_group_box.setObjectName(u"randomization_settings_group_box")
        sizePolicy2.setHeightForWidth(self.randomization_settings_group_box.sizePolicy().hasHeightForWidth())
        self.randomization_settings_group_box.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.randomization_settings_group_box)

        self.tab_widget.addTab(self.advanced_tab, "")

        self.verticalLayout_2.addWidget(self.tab_widget)

        self.settings_descriptions_layout = QHBoxLayout()
        self.settings_descriptions_layout.setObjectName(u"settings_descriptions_layout")
        self.settings_current_option_description_label = QLabel(self.central_widget)
        self.settings_current_option_description_label.setObjectName(u"settings_current_option_description_label")
        sizePolicy11 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.settings_current_option_description_label.sizePolicy().hasHeightForWidth())
        self.settings_current_option_description_label.setSizePolicy(sizePolicy11)
        self.settings_current_option_description_label.setMinimumSize(QSize(0, 64))
        self.settings_current_option_description_label.setTextFormat(Qt.RichText)
        self.settings_current_option_description_label.setWordWrap(True)

        self.settings_descriptions_layout.addWidget(self.settings_current_option_description_label)

        self.settings_default_option_description_label = QLabel(self.central_widget)
        self.settings_default_option_description_label.setObjectName(u"settings_default_option_description_label")
        sizePolicy11.setHeightForWidth(self.settings_default_option_description_label.sizePolicy().hasHeightForWidth())
        self.settings_default_option_description_label.setSizePolicy(sizePolicy11)
        self.settings_default_option_description_label.setMinimumSize(QSize(0, 64))
        self.settings_default_option_description_label.setWordWrap(True)

        self.settings_descriptions_layout.addWidget(self.settings_default_option_description_label)


        self.verticalLayout_2.addLayout(self.settings_descriptions_layout)

        self.footer_grid_layout = QGridLayout()
        self.footer_grid_layout.setObjectName(u"footer_grid_layout")
        self.setting_setting_string = QLineEdit(self.central_widget)
        self.setting_setting_string.setObjectName(u"setting_setting_string")

        self.footer_grid_layout.addWidget(self.setting_setting_string, 0, 1, 1, 1)

        self.setting_string_label = QLabel(self.central_widget)
        self.setting_string_label.setObjectName(u"setting_string_label")

        self.footer_grid_layout.addWidget(self.setting_string_label, 0, 0, 1, 1)

        self.about_button = QPushButton(self.central_widget)
        self.about_button.setObjectName(u"about_button")

        self.footer_grid_layout.addWidget(self.about_button, 2, 0, 1, 1)

        self.randomize_button = QPushButton(self.central_widget)
        self.randomize_button.setObjectName(u"randomize_button")
        sizePolicy12 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.randomize_button.sizePolicy().hasHeightForWidth())
        self.randomize_button.setSizePolicy(sizePolicy12)

        self.footer_grid_layout.addWidget(self.randomize_button, 2, 2, 1, 1)

        self.new_seed_button = QPushButton(self.central_widget)
        self.new_seed_button.setObjectName(u"new_seed_button")

        self.footer_grid_layout.addWidget(self.new_seed_button, 1, 2, 1, 1)

        self.reset_settings_to_default_hlayout = QHBoxLayout()
        self.reset_settings_to_default_hlayout.setObjectName(u"reset_settings_to_default_hlayout")
        self.reset_settings_to_default_left_hspacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.reset_settings_to_default_hlayout.addItem(self.reset_settings_to_default_left_hspacer)

        self.reset_settings_to_default_button = QPushButton(self.central_widget)
        self.reset_settings_to_default_button.setObjectName(u"reset_settings_to_default_button")

        self.reset_settings_to_default_hlayout.addWidget(self.reset_settings_to_default_button)

        self.reset_settings_to_default_right_hspacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.reset_settings_to_default_hlayout.addItem(self.reset_settings_to_default_right_hspacer)


        self.footer_grid_layout.addLayout(self.reset_settings_to_default_hlayout, 2, 1, 1, 1)

        self.seed_label = QLabel(self.central_widget)
        self.seed_label.setObjectName(u"seed_label")

        self.footer_grid_layout.addWidget(self.seed_label, 1, 0, 1, 1)

        self.copy_setting_string_button = QPushButton(self.central_widget)
        self.copy_setting_string_button.setObjectName(u"copy_setting_string_button")

        self.footer_grid_layout.addWidget(self.copy_setting_string_button, 0, 2, 1, 1)

        self.setting_seed = QLineEdit(self.central_widget)
        self.setting_seed.setObjectName(u"setting_seed")

        self.footer_grid_layout.addWidget(self.setting_seed, 1, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.footer_grid_layout)

        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)

        self.tab_widget.setCurrentIndex(7)


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
        self.how_to_left_arrow_label.setText(QCoreApplication.translate("main_window", u"\u279c", None))
        self.how_to_generate_group_box.setTitle(QCoreApplication.translate("main_window", u"Generate a Seed", None))
        self.how_to_generate_label.setText(QCoreApplication.translate("main_window", u"After you have obtained an extract of the vanilla game, you need to tell this randomizer program where the extract is located so that it can be used to generate a seed.<br><br>\n"
"\n"
"Please go to the \"File Setup\" box below and click the \"Browse\" button on the \"Extract\" row. You will then be asked to find the location of your extract.<br><br>\n"
"\n"
"Once the extract has been verified, you can browse the various tabs and customize the settings of your randomizer seed.<br><br>\n"
"\n"
"When you are ready, click the \"Randomize\" button in the bottom right of the screen. By default, the output will be in the <code>output</code> folder where this randomizer program is located.", None))
        self.how_to_right_arrow_label.setText(QCoreApplication.translate("main_window", u"\u279c", None))
        self.how_to_running_group_box.setTitle(QCoreApplication.translate("main_window", u"Running the Seed", None))
        self.how_to_running_label.setText(QCoreApplication.translate("main_window", u"If you want to play this randomizer on a modded Nintendo Switch console, copy the outputted <code>exeFS</code> and <code>romFS</code> folders into the <code>/atmosphere/contents/01002DA013484000</code> folder on your Switch's SD card. You can then run the game like normal and the randomizer will be patched on top of the vanilla game.<br><br>\n"
"\n"
"If you want to play this randomizer on the <a href=\"https://yuzu-emu.org/\">yuzu emulator</a>, open yuzu and right click on your copy of Skyward Sword HD. Click the \"Open Mod Data Location\" option and create a folder called <code>rando</code>. Copy the outputted <code>exeFS</code> and <code>romFS</code> folders into the newly created <code>rando</code> folder.<br><br>\n"
"\n"
"If you want to play the randomizer on the <a href=\"https://ryujinx.org/\">Ryujinx emulator</a>, copy the outputted <code>exeFS</code> and <code>romFS</code> folders into the <code>/Ryujinx/mods/contents/01002DA013484000</code> folder.", None))
        self.useful_info_group_box.setTitle(QCoreApplication.translate("main_window", u"Useful Information", None))
        self.useful_choose_settings_group_box.setTitle(QCoreApplication.translate("main_window", u"Choosing your Settings", None))
        self.choose_settings_label.setText(QCoreApplication.translate("main_window", u"<b>\u279c Gameplay</b>: Customize how the game is played and beaten.<br>\n"
"<b>\u279c World</b>: Pick how open the world is, shortcuts, and entrance randomization.<br>\n"
"<b>\u279c Locations and Shuffles</b>: Pick which locations and shuffles are enabled.<br>\n"
"<b>\u279c Items and Inventory</b>: Pick what items you start with.<br>\n"
"<b>\u279c Hints</b>: Customize the in-game hints that can help you to beat the game.<br>\n"
"<b>\u279c Logic and Tricks</b>: Pick which locations and tricks are enabled.<br>\n"
"<b>\u279c Advanced</b>: Control complex settings such as plandomizer and output folders.", None))
        self.useful_links_group_box.setTitle(QCoreApplication.translate("main_window", u"Links", None))
        self.links_label.setText(QCoreApplication.translate("main_window", u"<b>TODO</b><br>\n"
"\n"
"<b>\u279c</b> <a href=\"https://discord.gg/zkm6yncD\">Discord Server</a><br>\n"
"<b>\u279c</b> <a href=\"https://github.com/mint-choc-chip-skyblade/sshd-rando/issues\">Report a Bug</a><br>\n"
"<b>\u279c</b> <a href=\"\">Location Guide (todo)</a>", None))
        self.theming_group_box.setTitle(QCoreApplication.translate("main_window", u"Accessibility", None))
        self.groupBox.setTitle(QCoreApplication.translate("main_window", u"Theming", None))
        self.theme_mode_label.setText(QCoreApplication.translate("main_window", u"Theme Mode:", None))
        self.theme_presets_label.setText(QCoreApplication.translate("main_window", u"Theme Presets", None))
        self.use_custom_theme_check_box.setText(QCoreApplication.translate("main_window", u"Use Custom Theme", None))
        self.customize_theme_button.setText(QCoreApplication.translate("main_window", u"Customize Theme", None))
        self.theming_fonts.setTitle(QCoreApplication.translate("main_window", u"Fonts", None))
        self.font_family_label.setText(QCoreApplication.translate("main_window", u"Font Family", None))
        self.font_family_combo_box.setPlaceholderText(QCoreApplication.translate("main_window", u"Select Font Family", None))
        self.font_size_label.setText(QCoreApplication.translate("main_window", u"Font Size", None))
        self.font_reset_button.setText(QCoreApplication.translate("main_window", u"Reset", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.getting_started_tab), QCoreApplication.translate("main_window", u"Getting Started", None))
        self.hint_placements_group_box.setTitle(QCoreApplication.translate("main_window", u"Traps", None))
        self.trap_mode_label.setText(QCoreApplication.translate("main_window", u"Trap Mode", None))
        self.trappable_items_label.setText(QCoreApplication.translate("main_window", u"Trappable Items", None))
        self.setting_burn_traps.setText(QCoreApplication.translate("main_window", u"Burn Traps", None))
        self.setting_curse_traps.setText(QCoreApplication.translate("main_window", u"Curse Traps", None))
        self.setting_noise_traps.setText(QCoreApplication.translate("main_window", u"Noise Traps", None))
        self.setting_groose_traps.setText(QCoreApplication.translate("main_window", u"Groose Traps", None))
        self.dungeons_group_box.setTitle(QCoreApplication.translate("main_window", u"Dungeon Items", None))
        self.small_keys_label.setText(QCoreApplication.translate("main_window", u"Small Keys", None))
        self.boss_keys_label.setText(QCoreApplication.translate("main_window", u"Boss Keys", None))
        self.map_mode_label.setText(QCoreApplication.translate("main_window", u"Dungeon Maps", None))
        self.lanayru_caves_key_label.setText(QCoreApplication.translate("main_window", u"Lanayru Caves Small Key", None))
        self.beat_the_game_group_box.setTitle(QCoreApplication.translate("main_window", u"Beat the Game", None))
        self.required_dungeons_label.setText(QCoreApplication.translate("main_window", u"Required Dungeons", None))
        self.setting_empty_unrequired_dungeons.setText(QCoreApplication.translate("main_window", u"Barren Unrequired Dungeons", None))
        self.setting_skip_horde.setText(QCoreApplication.translate("main_window", u"Skip The Horde Fight", None))
        self.setting_skip_g3.setText(QCoreApplication.translate("main_window", u"Skip Ghirahim 3 Fight", None))
        self.setting_skip_demise.setText(QCoreApplication.translate("main_window", u"Skip Demise Fight", None))
        self.tweaks_group_box.setTitle(QCoreApplication.translate("main_window", u"Tweaks and Cosmetics", None))
        self.ammo_availability_label.setText(QCoreApplication.translate("main_window", u"Ammo Availability", None))
        self.peatrice_conversations_label.setText(QCoreApplication.translate("main_window", u"Peatrice Conversations", None))
        self.setting_full_wallet_upgrades.setText(QCoreApplication.translate("main_window", u"Full Wallet Upgrades", None))
        self.setting_dowsing_after_whitesword.setText(QCoreApplication.translate("main_window", u"Fill Dowsing on White Sword", None))
        self.setting_tunic_swap.setText(QCoreApplication.translate("main_window", u"Tunic Swap", None))
        self.setting_rotating_items.setText(QCoreApplication.translate("main_window", u"Rotating Items", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.gameplay_tab), QCoreApplication.translate("main_window", u"Gameplay", None))
        self.open_world_group_box.setTitle(QCoreApplication.translate("main_window", u"Open World", None))
        self.open_thunderhead_label.setText(QCoreApplication.translate("main_window", u"Open Thunderhead", None))
        self.open_lake_floria_label.setText(QCoreApplication.translate("main_window", u"Open Lake Floria", None))
        self.open_earth_temple_label.setText(QCoreApplication.translate("main_window", u"Open Earth Temple", None))
        self.open_lmf_label.setText(QCoreApplication.translate("main_window", u"Open Lanyru Mining Facility", None))
        self.mixed_pools_group_box.setTitle(QCoreApplication.translate("main_window", u"Shortcuts", None))
        self.setting_fs_lava_flow.setText(QCoreApplication.translate("main_window", u"Skip Fire Sanctuary Lava Chase", None))
        self.entrance_randomization_group_box.setTitle(QCoreApplication.translate("main_window", u"Entrance Randomization", None))
        self.setting_randomize_door_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Door Entrances", None))
        self.setting_randomize_interior_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Interior Entrances", None))
        self.setting_randomize_overworld_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Overworld Entrances", None))
        self.setting_randomize_dungeon_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Dungeon Entrances", None))
        self.setting_randomize_trial_gate_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Trial Gate Entrances", None))
        self.random_starting_spawn_label.setText(QCoreApplication.translate("main_window", u"Randomize Starting Spawn", None))
        self.setting_decouple_double_doors.setText(QCoreApplication.translate("main_window", u"Decouple Double Door Entrances", None))
        self.setting_decouple_entrances.setText(QCoreApplication.translate("main_window", u"Decouple Entrances", None))
        self.mixed_entrance_pools_group_box.setTitle(QCoreApplication.translate("main_window", u"Mixed Entrance Pools", None))
        self.mixed_entrance_pools_list_label.setText(QCoreApplication.translate("main_window", u"<html><head/><body><p><span style=\" font-weight:700;\">Defined Entrance Pools:</span><br/><br/>Pool 1: [] <br/>Pool 2: [] <br/>Pool 3: []</p></body></html>", None))
        self.highlighted_entrance_pool_label.setText(QCoreApplication.translate("main_window", u"Highlighted Entrance Pool:", None))
        self.selected_entrance_type_label.setText(QCoreApplication.translate("main_window", u"Selected Entrance Type:", None))
        self.add_entrance_type_button.setText(QCoreApplication.translate("main_window", u"Add Entrance Type", None))
        self.remove_entrance_type_button.setText(QCoreApplication.translate("main_window", u"Remove Entrance Type", None))
        self.mixed_entrance_pools_reset_button.setText(QCoreApplication.translate("main_window", u"Reset", None))
        self.mixed_entrance_pools_explainer_label.setText(QCoreApplication.translate("main_window", u"<b>What are Mixed Entrance Pools?</b>\n"
"<br>\n"
"<br>Mixed entrance pools define how entrance types should be shuffled together.\n"
"<br>By default, turning on an entrance randomizer setting will only shuffle the entrances of that type with each other.\n"
"<br> For example, randomizing dungeon entrances will only shuffle the dungeon entrances with each other. The Sandship entrance could <i>not</i> be shuffled to Wryna's House door or a trial gate entrance.\n"
"<br>\n"
"<br>By defining mixed entrance pools, different entrance types can be shuffled together.\n"
"<br>For example, if a mixed pool was defined as this: [Dungeon, Door, Trial Gate], the Sandship entrance <i>could</i> be shuffled to Wryna's House door or a trial gate entrance.", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.world_tab), QCoreApplication.translate("main_window", u"World", None))
        self.include_location_button.setText(QCoreApplication.translate("main_window", u"Include\n"
"<---", None))
        self.exclude_location_button.setText(QCoreApplication.translate("main_window", u"Exclude\n"
"--->", None))
        self.locations_reset_button.setText(QCoreApplication.translate("main_window", u"Reset", None))
        self.shuffles_group_box.setTitle(QCoreApplication.translate("main_window", u"Shuffles", None))
        self.beedle_shop_shuffle_label.setText(QCoreApplication.translate("main_window", u"Beedle's Shop Shuffle", None))
        self.rupee_shuffle_label.setText(QCoreApplication.translate("main_window", u"Rupee Shuffle", None))
        self.setting_underground_rupee_shuffle.setText(QCoreApplication.translate("main_window", u"Underground Rupee Shuffle", None))
        self.setting_goddess_chest_shuffle.setText(QCoreApplication.translate("main_window", u"Goddess Chest Shuffle", None))
        self.setting_gratitude_crystal_shuffle.setText(QCoreApplication.translate("main_window", u"Gratitude Crystals Shuffle", None))
        self.setting_stamina_fruit_shuffle.setText(QCoreApplication.translate("main_window", u"Stamina Fruits", None))
        self.npc_closet_shuffle_label.setText(QCoreApplication.translate("main_window", u"NPC Closets", None))
        self.excluded_locations_group_box.setTitle(QCoreApplication.translate("main_window", u"Excluded Locations", None))
        self.excluded_locations_free_search.setPlaceholderText(QCoreApplication.translate("main_window", u"Search", None))
        self.included_locations_group_box.setTitle(QCoreApplication.translate("main_window", u"Included Locations", None))
        self.included_locations_type_filter.setPlaceholderText("")
        self.included_locations_free_search.setText("")
        self.included_locations_free_search.setPlaceholderText(QCoreApplication.translate("main_window", u"Search", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.locations_tab), QCoreApplication.translate("main_window", u"Locations and Shuffles", None))
        self.randomized_items_group_box.setTitle(QCoreApplication.translate("main_window", u"Randomized Items", None))
        self.randomized_items_free_search.setText("")
        self.randomized_items_free_search.setPlaceholderText(QCoreApplication.translate("main_window", u"Search", None))
        self.starting_items_group_box.setTitle(QCoreApplication.translate("main_window", u"Starting Items", None))
        self.starting_items_free_search.setText("")
        self.starting_items_free_search.setPlaceholderText(QCoreApplication.translate("main_window", u"Search", None))
        self.randomize_item_button.setText(QCoreApplication.translate("main_window", u"Remove\n"
"<---", None))
        self.start_with_item_button.setText(QCoreApplication.translate("main_window", u"Add\n"
"--->", None))
        self.inventory_reset_button.setText(QCoreApplication.translate("main_window", u"Reset", None))
        self.item_settings_group_box.setTitle(QCoreApplication.translate("main_window", u"Item Settings", None))
        self.item_pool_label.setText(QCoreApplication.translate("main_window", u"Item Pool", None))
        self.starting_sword_label.setText(QCoreApplication.translate("main_window", u"Starting Sword", None))
        self.random_starting_tablet_count_label.setText(QCoreApplication.translate("main_window", u"Random Starting Tablet Count", None))
        self.random_starting_item_count_label.setText(QCoreApplication.translate("main_window", u"Random Starting Item Count", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.inventory_tab), QCoreApplication.translate("main_window", u"Items and Inventory", None))
        self.included_hint_locations_group_box.setTitle(QCoreApplication.translate("main_window", u"Included Hint Locations", None))
        self.included_hint_locations_free_search.setText("")
        self.included_hint_locations_free_search.setPlaceholderText(QCoreApplication.translate("main_window", u"Search", None))
        self.include_hint_location_button.setText(QCoreApplication.translate("main_window", u"Remove\n"
"<---", None))
        self.exclude_hint_location_button.setText(QCoreApplication.translate("main_window", u"Add\n"
"--->", None))
        self.hints_reset_button.setText(QCoreApplication.translate("main_window", u"Reset", None))
        self.excluded_hint_locations_group_box.setTitle(QCoreApplication.translate("main_window", u"Excluded Hint Locations", None))
        self.excluded_hint_locations_free_search.setText("")
        self.excluded_hint_locations_free_search.setPlaceholderText(QCoreApplication.translate("main_window", u"Search", None))
        self.hints_group_box.setTitle(QCoreApplication.translate("main_window", u"Hint Settings", None))
        self.setting_gossip_stone_hints.setText(QCoreApplication.translate("main_window", u"Gossip Stone Hints", None))
        self.setting_fi_hints.setText(QCoreApplication.translate("main_window", u"Fi Hints", None))
        self.setting_impa_sot_hint.setText(QCoreApplication.translate("main_window", u"Past Impa Stone of Trials Hint", None))
        self.song_hints_label.setText(QCoreApplication.translate("main_window", u"Song Hints", None))
        self.path_hints_label.setText(QCoreApplication.translate("main_window", u"Path Hints", None))
        self.barren_hints_label.setText(QCoreApplication.translate("main_window", u"Barren Hints", None))
        self.location_hints_label.setText(QCoreApplication.translate("main_window", u"Location Hints", None))
        self.item_hints_label.setText(QCoreApplication.translate("main_window", u"Item Hints", None))
        self.setting_always_hints.setText(QCoreApplication.translate("main_window", u"Prioritize Remote Location Hints", None))
        self.setting_cryptic_hint_text.setText(QCoreApplication.translate("main_window", u"Cryptic Hint Text", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.hints_tab), QCoreApplication.translate("main_window", u"Hints", None))
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
        self.setting_logic_skyview_coiled_rupee_jump.setText(QCoreApplication.translate("main_window", u"Skyview Coiled Rupee Jump", None))
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
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.logic_tab), QCoreApplication.translate("main_window", u"Logic and Tricks", None))
        self.file_setup_group_box.setTitle(QCoreApplication.translate("main_window", u"Extract and Output Utilities", None))
        self.output_label.setText(QCoreApplication.translate("main_window", u"Output Path:", None))
        self.output_button.setText(QCoreApplication.translate("main_window", u"Browse", None))
        self.verify_extract_label.setText(QCoreApplication.translate("main_window", u"Verify Extracted Game Files:", None))
        self.verify_important_extract_button.setText(QCoreApplication.translate("main_window", u"Verify Important Files", None))
        self.verify_all_extract_button.setText(QCoreApplication.translate("main_window", u"Verify All Files", None))
        self.plandomizer_group_box.setTitle(QCoreApplication.translate("main_window", u"Plandomizer", None))
        self.plandomizer_warning_label.setText(QCoreApplication.translate("main_window", u"<html><head/><body><p><span style=\" font-weight:700;\">WARNING</span>: The plandomizer settings will automatically <span style=\" font-weight:700;\">TURN THEMSELVES OFF</span> when reopening this randomizer program!</p></body></html>", None))
        self.config_use_plandomizer.setText(QCoreApplication.translate("main_window", u"Use Plandomizer File", None))
        self.selected_plandomizer_file_label.setText(QCoreApplication.translate("main_window", u"Selected Plandomizer File:", None))
        self.open_plandomizer_folder_button.setText(QCoreApplication.translate("main_window", u"Open Plandomizer Folder", None))
        self.random_settings_group_box.setTitle(QCoreApplication.translate("main_window", u"Random Settings", None))
        self.randomization_settings_group_box.setTitle(QCoreApplication.translate("main_window", u"Randomization Settings", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.advanced_tab), QCoreApplication.translate("main_window", u"Advanced", None))
        self.settings_current_option_description_label.setText(QCoreApplication.translate("main_window", u"Settings current option description", None))
        self.settings_default_option_description_label.setText(QCoreApplication.translate("main_window", u"Settings default option description", None))
        self.setting_string_label.setText(QCoreApplication.translate("main_window", u"Setting String", None))
        self.about_button.setText(QCoreApplication.translate("main_window", u"About", None))
        self.randomize_button.setText(QCoreApplication.translate("main_window", u"Randomize", None))
        self.new_seed_button.setText(QCoreApplication.translate("main_window", u"New Seed", None))
        self.reset_settings_to_default_button.setText(QCoreApplication.translate("main_window", u"Reset Settings to Default", None))
        self.seed_label.setText(QCoreApplication.translate("main_window", u"Seed:", None))
        self.copy_setting_string_button.setText(QCoreApplication.translate("main_window", u"Copy", None))
    # retranslateUi

