# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
    QListView, QMainWindow, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QTextEdit, QVBoxLayout, QWidget)

from gui.components.tracker_toggle_st_button import TrackerToggleSTButton
from gui.components.tristate_check_box import RandoTriStateCheckBox

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(1387, 873)
        main_window.setStyleSheet(u"QToolTip {color: #000000; background-color: #FFFFFF;}")
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setStyleSheet(u"QToolTip {color: #000000; background-color: #FFFFFF;}")
        self.verticalLayout_2 = QVBoxLayout(self.central_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setObjectName(u"tab_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_widget.sizePolicy().hasHeightForWidth())
        self.tab_widget.setSizePolicy(sizePolicy)
        self.tab_widget.setStyleSheet(u"QToolTip {color: #000000; background-color: #FFFFFF;}")
        self.tab_widget.setTabShape(QTabWidget.TabShape.Rounded)
        self.getting_started_tab = QWidget()
        self.getting_started_tab.setObjectName(u"getting_started_tab")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.getting_started_tab.sizePolicy().hasHeightForWidth())
        self.getting_started_tab.setSizePolicy(sizePolicy1)
        self.verticalLayout_4 = QVBoxLayout(self.getting_started_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.how_to_group_box = QGroupBox(self.getting_started_tab)
        self.how_to_group_box.setObjectName(u"how_to_group_box")
        sizePolicy.setHeightForWidth(self.how_to_group_box.sizePolicy().hasHeightForWidth())
        self.how_to_group_box.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.how_to_group_box)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.how_to_extract_group_box = QGroupBox(self.how_to_group_box)
        self.how_to_extract_group_box.setObjectName(u"how_to_extract_group_box")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.how_to_extract_group_box.sizePolicy().hasHeightForWidth())
        self.how_to_extract_group_box.setSizePolicy(sizePolicy2)
        self.verticalLayout_5 = QVBoxLayout(self.how_to_extract_group_box)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.how_to_extract_label = QLabel(self.how_to_extract_group_box)
        self.how_to_extract_label.setObjectName(u"how_to_extract_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.how_to_extract_label.sizePolicy().hasHeightForWidth())
        self.how_to_extract_label.setSizePolicy(sizePolicy3)
        self.how_to_extract_label.setTextFormat(Qt.TextFormat.RichText)
        self.how_to_extract_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.how_to_extract_label.setWordWrap(True)
        self.how_to_extract_label.setOpenExternalLinks(True)
        self.how_to_extract_label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.verticalLayout_5.addWidget(self.how_to_extract_label)


        self.horizontalLayout_3.addWidget(self.how_to_extract_group_box)

        self.how_to_left_arrow_label = QLabel(self.how_to_group_box)
        self.how_to_left_arrow_label.setObjectName(u"how_to_left_arrow_label")
        sizePolicy.setHeightForWidth(self.how_to_left_arrow_label.sizePolicy().hasHeightForWidth())
        self.how_to_left_arrow_label.setSizePolicy(sizePolicy)
        self.how_to_left_arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.how_to_left_arrow_label)

        self.useful_choose_settings_group_box = QGroupBox(self.how_to_group_box)
        self.useful_choose_settings_group_box.setObjectName(u"useful_choose_settings_group_box")
        sizePolicy2.setHeightForWidth(self.useful_choose_settings_group_box.sizePolicy().hasHeightForWidth())
        self.useful_choose_settings_group_box.setSizePolicy(sizePolicy2)
        self.verticalLayout_8 = QVBoxLayout(self.useful_choose_settings_group_box)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.choose_settings_label = QLabel(self.useful_choose_settings_group_box)
        self.choose_settings_label.setObjectName(u"choose_settings_label")
        sizePolicy3.setHeightForWidth(self.choose_settings_label.sizePolicy().hasHeightForWidth())
        self.choose_settings_label.setSizePolicy(sizePolicy3)
        self.choose_settings_label.setTextFormat(Qt.TextFormat.RichText)
        self.choose_settings_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.choose_settings_label.setWordWrap(True)
        self.choose_settings_label.setOpenExternalLinks(True)
        self.choose_settings_label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.verticalLayout_8.addWidget(self.choose_settings_label)


        self.horizontalLayout_3.addWidget(self.useful_choose_settings_group_box)

        self.how_to_middle_arrow_label = QLabel(self.how_to_group_box)
        self.how_to_middle_arrow_label.setObjectName(u"how_to_middle_arrow_label")
        self.how_to_middle_arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.how_to_middle_arrow_label)

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
        self.how_to_generate_label.setTextFormat(Qt.TextFormat.RichText)
        self.how_to_generate_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.how_to_generate_label.setWordWrap(True)
        self.how_to_generate_label.setOpenExternalLinks(True)
        self.how_to_generate_label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.verticalLayout_6.addWidget(self.how_to_generate_label)


        self.horizontalLayout_3.addWidget(self.how_to_generate_group_box)

        self.how_to_right_arrow_label = QLabel(self.how_to_group_box)
        self.how_to_right_arrow_label.setObjectName(u"how_to_right_arrow_label")
        sizePolicy.setHeightForWidth(self.how_to_right_arrow_label.sizePolicy().hasHeightForWidth())
        self.how_to_right_arrow_label.setSizePolicy(sizePolicy)
        self.how_to_right_arrow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.how_to_right_arrow_label)

        self.how_to_running_group_box = QGroupBox(self.how_to_group_box)
        self.how_to_running_group_box.setObjectName(u"how_to_running_group_box")
        sizePolicy2.setHeightForWidth(self.how_to_running_group_box.sizePolicy().hasHeightForWidth())
        self.how_to_running_group_box.setSizePolicy(sizePolicy2)
        self.verticalLayout_7 = QVBoxLayout(self.how_to_running_group_box)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.how_to_running_label = QLabel(self.how_to_running_group_box)
        self.how_to_running_label.setObjectName(u"how_to_running_label")
        sizePolicy3.setHeightForWidth(self.how_to_running_label.sizePolicy().hasHeightForWidth())
        self.how_to_running_label.setSizePolicy(sizePolicy3)
        self.how_to_running_label.setTextFormat(Qt.TextFormat.RichText)
        self.how_to_running_label.setScaledContents(False)
        self.how_to_running_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.how_to_running_label.setWordWrap(True)
        self.how_to_running_label.setOpenExternalLinks(True)
        self.how_to_running_label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.verticalLayout_7.addWidget(self.how_to_running_label)


        self.horizontalLayout_3.addWidget(self.how_to_running_group_box)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(2, 1)
        self.horizontalLayout_3.setStretch(4, 1)
        self.horizontalLayout_3.setStretch(6, 1)

        self.verticalLayout_4.addWidget(self.how_to_group_box)

        self.middle_grid_layout = QGridLayout()
        self.middle_grid_layout.setObjectName(u"middle_grid_layout")
        self.middle_grid_layout.setContentsMargins(-1, -1, -1, 0)
        self.useful_info_group_box = QGroupBox(self.getting_started_tab)
        self.useful_info_group_box.setObjectName(u"useful_info_group_box")
        sizePolicy.setHeightForWidth(self.useful_info_group_box.sizePolicy().hasHeightForWidth())
        self.useful_info_group_box.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.useful_info_group_box)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.guides_label = QLabel(self.useful_info_group_box)
        self.guides_label.setObjectName(u"guides_label")
        sizePolicy.setHeightForWidth(self.guides_label.sizePolicy().hasHeightForWidth())
        self.guides_label.setSizePolicy(sizePolicy)
        self.guides_label.setTextFormat(Qt.TextFormat.RichText)
        self.guides_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.guides_label.setWordWrap(True)
        self.guides_label.setOpenExternalLinks(True)
        self.guides_label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.horizontalLayout.addWidget(self.guides_label)

        self.community_label = QLabel(self.useful_info_group_box)
        self.community_label.setObjectName(u"community_label")
        sizePolicy.setHeightForWidth(self.community_label.sizePolicy().hasHeightForWidth())
        self.community_label.setSizePolicy(sizePolicy)
        self.community_label.setTextFormat(Qt.TextFormat.RichText)
        self.community_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.community_label.setWordWrap(True)
        self.community_label.setOpenExternalLinks(True)
        self.community_label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.horizontalLayout.addWidget(self.community_label)


        self.middle_grid_layout.addWidget(self.useful_info_group_box, 0, 1, 1, 1)

        self.accessibility_group_box = QGroupBox(self.getting_started_tab)
        self.accessibility_group_box.setObjectName(u"accessibility_group_box")
        sizePolicy.setHeightForWidth(self.accessibility_group_box.sizePolicy().hasHeightForWidth())
        self.accessibility_group_box.setSizePolicy(sizePolicy)
        self.horizontalLayout_6 = QHBoxLayout(self.accessibility_group_box)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.theming_group_box = QGroupBox(self.accessibility_group_box)
        self.theming_group_box.setObjectName(u"theming_group_box")
        self.theming_group_box.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.verticalLayout_3 = QVBoxLayout(self.theming_group_box)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.theme_mode_layout = QHBoxLayout()
        self.theme_mode_layout.setObjectName(u"theme_mode_layout")
        self.theme_mode_label = QLabel(self.theming_group_box)
        self.theme_mode_label.setObjectName(u"theme_mode_label")

        self.theme_mode_layout.addWidget(self.theme_mode_label)

        self.theme_mode_combo_box = QComboBox(self.theming_group_box)
        self.theme_mode_combo_box.setObjectName(u"theme_mode_combo_box")
        sizePolicy1.setHeightForWidth(self.theme_mode_combo_box.sizePolicy().hasHeightForWidth())
        self.theme_mode_combo_box.setSizePolicy(sizePolicy1)

        self.theme_mode_layout.addWidget(self.theme_mode_combo_box)


        self.verticalLayout_3.addLayout(self.theme_mode_layout)

        self.theme_presets_layout = QHBoxLayout()
        self.theme_presets_layout.setObjectName(u"theme_presets_layout")
        self.theme_presets_label = QLabel(self.theming_group_box)
        self.theme_presets_label.setObjectName(u"theme_presets_label")

        self.theme_presets_layout.addWidget(self.theme_presets_label)

        self.theme_presets_combo_box = QComboBox(self.theming_group_box)
        self.theme_presets_combo_box.setObjectName(u"theme_presets_combo_box")
        sizePolicy1.setHeightForWidth(self.theme_presets_combo_box.sizePolicy().hasHeightForWidth())
        self.theme_presets_combo_box.setSizePolicy(sizePolicy1)

        self.theme_presets_layout.addWidget(self.theme_presets_combo_box)


        self.verticalLayout_3.addLayout(self.theme_presets_layout)

        self.customize_theme_layout = QHBoxLayout()
        self.customize_theme_layout.setObjectName(u"customize_theme_layout")
        self.use_custom_theme_check_box = QCheckBox(self.theming_group_box)
        self.use_custom_theme_check_box.setObjectName(u"use_custom_theme_check_box")

        self.customize_theme_layout.addWidget(self.use_custom_theme_check_box)

        self.customize_theme_button = QPushButton(self.theming_group_box)
        self.customize_theme_button.setObjectName(u"customize_theme_button")

        self.customize_theme_layout.addWidget(self.customize_theme_button)


        self.verticalLayout_3.addLayout(self.customize_theme_layout)

        self.theming_vspacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.theming_vspacer)


        self.horizontalLayout_6.addWidget(self.theming_group_box)

        self.theming_fonts = QGroupBox(self.accessibility_group_box)
        self.theming_fonts.setObjectName(u"theming_fonts")
        self.verticalLayout_12 = QVBoxLayout(self.theming_fonts)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.font_family_layout = QHBoxLayout()
        self.font_family_layout.setObjectName(u"font_family_layout")
        self.font_family_label = QLabel(self.theming_fonts)
        self.font_family_label.setObjectName(u"font_family_label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.font_family_label.sizePolicy().hasHeightForWidth())
        self.font_family_label.setSizePolicy(sizePolicy4)

        self.font_family_layout.addWidget(self.font_family_label)

        self.font_family_combo_box = QFontComboBox(self.theming_fonts)
        self.font_family_combo_box.setObjectName(u"font_family_combo_box")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.font_family_combo_box.sizePolicy().hasHeightForWidth())
        self.font_family_combo_box.setSizePolicy(sizePolicy5)
        self.font_family_combo_box.setEditable(False)
        self.font_family_combo_box.setMinimumContentsLength(1)
        self.font_family_combo_box.setFontFilters(QFontComboBox.FontFilter.ScalableFonts)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(10)
        self.font_family_combo_box.setCurrentFont(font)

        self.font_family_layout.addWidget(self.font_family_combo_box)


        self.verticalLayout_12.addLayout(self.font_family_layout)

        self.font_size_layout = QHBoxLayout()
        self.font_size_layout.setObjectName(u"font_size_layout")
        self.font_size_label = QLabel(self.theming_fonts)
        self.font_size_label.setObjectName(u"font_size_label")

        self.font_size_layout.addWidget(self.font_size_label)

        self.font_size_spin_box = QSpinBox(self.theming_fonts)
        self.font_size_spin_box.setObjectName(u"font_size_spin_box")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.font_size_spin_box.sizePolicy().hasHeightForWidth())
        self.font_size_spin_box.setSizePolicy(sizePolicy6)
        self.font_size_spin_box.setMinimum(6)
        self.font_size_spin_box.setMaximum(14)
        self.font_size_spin_box.setValue(10)

        self.font_size_layout.addWidget(self.font_size_spin_box)


        self.verticalLayout_12.addLayout(self.font_size_layout)

        self.font_reset_button = QPushButton(self.theming_fonts)
        self.font_reset_button.setObjectName(u"font_reset_button")

        self.verticalLayout_12.addWidget(self.font_reset_button)

        self.fonts_vspacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_12.addItem(self.fonts_vspacer)


        self.horizontalLayout_6.addWidget(self.theming_fonts)

        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)

        self.middle_grid_layout.addWidget(self.accessibility_group_box, 0, 2, 1, 1)

        self.presets_group_box = QGroupBox(self.getting_started_tab)
        self.presets_group_box.setObjectName(u"presets_group_box")
        sizePolicy.setHeightForWidth(self.presets_group_box.sizePolicy().hasHeightForWidth())
        self.presets_group_box.setSizePolicy(sizePolicy)
        self.verticalLayout_34 = QVBoxLayout(self.presets_group_box)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.selected_preset_layout = QHBoxLayout()
        self.selected_preset_layout.setObjectName(u"selected_preset_layout")
        self.selected_preset_label = QLabel(self.presets_group_box)
        self.selected_preset_label.setObjectName(u"selected_preset_label")

        self.selected_preset_layout.addWidget(self.selected_preset_label)

        self.selected_preset_combo_box = QComboBox(self.presets_group_box)
        self.selected_preset_combo_box.setObjectName(u"selected_preset_combo_box")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.selected_preset_combo_box.sizePolicy().hasHeightForWidth())
        self.selected_preset_combo_box.setSizePolicy(sizePolicy7)
        self.selected_preset_combo_box.setMinimumContentsLength(1)

        self.selected_preset_layout.addWidget(self.selected_preset_combo_box)


        self.verticalLayout_34.addLayout(self.selected_preset_layout)

        self.presets_button_layout = QHBoxLayout()
        self.presets_button_layout.setObjectName(u"presets_button_layout")
        self.presets_delete_button = QPushButton(self.presets_group_box)
        self.presets_delete_button.setObjectName(u"presets_delete_button")

        self.presets_button_layout.addWidget(self.presets_delete_button)

        self.presets_save_new_button = QPushButton(self.presets_group_box)
        self.presets_save_new_button.setObjectName(u"presets_save_new_button")

        self.presets_button_layout.addWidget(self.presets_save_new_button)

        self.presets_apply_button = QPushButton(self.presets_group_box)
        self.presets_apply_button.setObjectName(u"presets_apply_button")

        self.presets_button_layout.addWidget(self.presets_apply_button)


        self.verticalLayout_34.addLayout(self.presets_button_layout)

        self.presets_vspacer = QSpacerItem(20, 86, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_34.addItem(self.presets_vspacer)


        self.middle_grid_layout.addWidget(self.presets_group_box, 0, 0, 1, 1)

        self.middle_grid_layout.setColumnStretch(0, 1)
        self.middle_grid_layout.setColumnStretch(1, 1)
        self.middle_grid_layout.setColumnStretch(2, 2)

        self.verticalLayout_4.addLayout(self.middle_grid_layout)

        self.verticalLayout_4.setStretch(0, 2)
        self.verticalLayout_4.setStretch(1, 1)
        self.tab_widget.addTab(self.getting_started_tab, "")
        self.gameplay_tab = QWidget()
        self.gameplay_tab.setObjectName(u"gameplay_tab")
        sizePolicy1.setHeightForWidth(self.gameplay_tab.sizePolicy().hasHeightForWidth())
        self.gameplay_tab.setSizePolicy(sizePolicy1)
        self.gridLayout_9 = QGridLayout(self.gameplay_tab)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
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

        self.lanayru_caves_keys_label = QLabel(self.dungeons_group_box)
        self.lanayru_caves_keys_label.setObjectName(u"lanayru_caves_keys_label")

        self.verticalLayout_16.addWidget(self.lanayru_caves_keys_label)

        self.setting_lanayru_caves_keys = QComboBox(self.dungeons_group_box)
        self.setting_lanayru_caves_keys.setObjectName(u"setting_lanayru_caves_keys")

        self.verticalLayout_16.addWidget(self.setting_lanayru_caves_keys)

        self.boss_key_puzzles_label = QLabel(self.dungeons_group_box)
        self.boss_key_puzzles_label.setObjectName(u"boss_key_puzzles_label")

        self.verticalLayout_16.addWidget(self.boss_key_puzzles_label)

        self.setting_boss_key_puzzles = QComboBox(self.dungeons_group_box)
        self.setting_boss_key_puzzles.setObjectName(u"setting_boss_key_puzzles")

        self.verticalLayout_16.addWidget(self.setting_boss_key_puzzles)

        self.dungeons_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.dungeons_vspacer)


        self.gridLayout_9.addWidget(self.dungeons_group_box, 0, 1, 1, 1)

        self.tweaks_group_box = QGroupBox(self.gameplay_tab)
        self.tweaks_group_box.setObjectName(u"tweaks_group_box")
        self.verticalLayout = QVBoxLayout(self.tweaks_group_box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.setting_spawn_hearts = RandoTriStateCheckBox(self.tweaks_group_box)
        self.setting_spawn_hearts.setObjectName(u"setting_spawn_hearts")

        self.verticalLayout.addWidget(self.setting_spawn_hearts)

        self.setting_upgraded_skyward_strike = RandoTriStateCheckBox(self.tweaks_group_box)
        self.setting_upgraded_skyward_strike.setObjectName(u"setting_upgraded_skyward_strike")

        self.verticalLayout.addWidget(self.setting_upgraded_skyward_strike)

        self.setting_faster_air_meter_depletion = RandoTriStateCheckBox(self.tweaks_group_box)
        self.setting_faster_air_meter_depletion.setObjectName(u"setting_faster_air_meter_depletion")

        self.verticalLayout.addWidget(self.setting_faster_air_meter_depletion)

        self.damage_multiplier_layout = QHBoxLayout()
        self.damage_multiplier_layout.setObjectName(u"damage_multiplier_layout")
        self.damage_multiplier_label = QLabel(self.tweaks_group_box)
        self.damage_multiplier_label.setObjectName(u"damage_multiplier_label")

        self.damage_multiplier_layout.addWidget(self.damage_multiplier_label)

        self.setting_damage_multiplier = QSpinBox(self.tweaks_group_box)
        self.setting_damage_multiplier.setObjectName(u"setting_damage_multiplier")
        sizePolicy6.setHeightForWidth(self.setting_damage_multiplier.sizePolicy().hasHeightForWidth())
        self.setting_damage_multiplier.setSizePolicy(sizePolicy6)

        self.damage_multiplier_layout.addWidget(self.setting_damage_multiplier)


        self.verticalLayout.addLayout(self.damage_multiplier_layout)

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
        sizePolicy.setHeightForWidth(self.peatrice_conversations_label.sizePolicy().hasHeightForWidth())
        self.peatrice_conversations_label.setSizePolicy(sizePolicy)

        self.peatrice_conversations_layout.addWidget(self.peatrice_conversations_label)

        self.setting_peatrice_conversations = QSpinBox(self.tweaks_group_box)
        self.setting_peatrice_conversations.setObjectName(u"setting_peatrice_conversations")
        sizePolicy6.setHeightForWidth(self.setting_peatrice_conversations.sizePolicy().hasHeightForWidth())
        self.setting_peatrice_conversations.setSizePolicy(sizePolicy6)

        self.peatrice_conversations_layout.addWidget(self.setting_peatrice_conversations)


        self.verticalLayout.addLayout(self.peatrice_conversations_layout)

        self.setting_random_bottle_contents = RandoTriStateCheckBox(self.tweaks_group_box)
        self.setting_random_bottle_contents.setObjectName(u"setting_random_bottle_contents")

        self.verticalLayout.addWidget(self.setting_random_bottle_contents)

        self.setting_full_wallet_upgrades = RandoTriStateCheckBox(self.tweaks_group_box)
        self.setting_full_wallet_upgrades.setObjectName(u"setting_full_wallet_upgrades")

        self.verticalLayout.addWidget(self.setting_full_wallet_upgrades)

        self.setting_skip_harp_playing = RandoTriStateCheckBox(self.tweaks_group_box)
        self.setting_skip_harp_playing.setObjectName(u"setting_skip_harp_playing")

        self.verticalLayout.addWidget(self.setting_skip_harp_playing)

        self.random_trial_object_positions_label = QLabel(self.tweaks_group_box)
        self.random_trial_object_positions_label.setObjectName(u"random_trial_object_positions_label")

        self.verticalLayout.addWidget(self.random_trial_object_positions_label)

        self.setting_random_trial_object_positions = QComboBox(self.tweaks_group_box)
        self.setting_random_trial_object_positions.setObjectName(u"setting_random_trial_object_positions")

        self.verticalLayout.addWidget(self.setting_random_trial_object_positions)

        self.tweaks_vspacer = QSpacerItem(20, 148, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.tweaks_vspacer)


        self.gridLayout_9.addWidget(self.tweaks_group_box, 0, 3, 1, 1)

        self.beat_the_game_group_box = QGroupBox(self.gameplay_tab)
        self.beat_the_game_group_box.setObjectName(u"beat_the_game_group_box")
        self.verticalLayout_13 = QVBoxLayout(self.beat_the_game_group_box)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.got_sword_requirement_label = QLabel(self.beat_the_game_group_box)
        self.got_sword_requirement_label.setObjectName(u"got_sword_requirement_label")

        self.verticalLayout_13.addWidget(self.got_sword_requirement_label)

        self.setting_got_sword_requirement = QComboBox(self.beat_the_game_group_box)
        self.setting_got_sword_requirement.setObjectName(u"setting_got_sword_requirement")

        self.verticalLayout_13.addWidget(self.setting_got_sword_requirement)

        self.required_dungeons_layout = QHBoxLayout()
        self.required_dungeons_layout.setSpacing(0)
        self.required_dungeons_layout.setObjectName(u"required_dungeons_layout")
        self.required_dungeons_label = QLabel(self.beat_the_game_group_box)
        self.required_dungeons_label.setObjectName(u"required_dungeons_label")

        self.required_dungeons_layout.addWidget(self.required_dungeons_label)

        self.setting_required_dungeons = QSpinBox(self.beat_the_game_group_box)
        self.setting_required_dungeons.setObjectName(u"setting_required_dungeons")
        sizePolicy6.setHeightForWidth(self.setting_required_dungeons.sizePolicy().hasHeightForWidth())
        self.setting_required_dungeons.setSizePolicy(sizePolicy6)

        self.required_dungeons_layout.addWidget(self.setting_required_dungeons)


        self.verticalLayout_13.addLayout(self.required_dungeons_layout)

        self.setting_dungeons_include_sky_keep = RandoTriStateCheckBox(self.beat_the_game_group_box)
        self.setting_dungeons_include_sky_keep.setObjectName(u"setting_dungeons_include_sky_keep")

        self.verticalLayout_13.addWidget(self.setting_dungeons_include_sky_keep)

        self.setting_empty_unrequired_dungeons = RandoTriStateCheckBox(self.beat_the_game_group_box)
        self.setting_empty_unrequired_dungeons.setObjectName(u"setting_empty_unrequired_dungeons")

        self.verticalLayout_13.addWidget(self.setting_empty_unrequired_dungeons)

        self.setting_skip_horde = RandoTriStateCheckBox(self.beat_the_game_group_box)
        self.setting_skip_horde.setObjectName(u"setting_skip_horde")

        self.verticalLayout_13.addWidget(self.setting_skip_horde)

        self.setting_skip_g3 = RandoTriStateCheckBox(self.beat_the_game_group_box)
        self.setting_skip_g3.setObjectName(u"setting_skip_g3")

        self.verticalLayout_13.addWidget(self.setting_skip_g3)

        self.setting_skip_demise = RandoTriStateCheckBox(self.beat_the_game_group_box)
        self.setting_skip_demise.setObjectName(u"setting_skip_demise")

        self.verticalLayout_13.addWidget(self.setting_skip_demise)

        self.beat_the_game_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_13.addItem(self.beat_the_game_vspacer)


        self.gridLayout_9.addWidget(self.beat_the_game_group_box, 0, 0, 1, 1)

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

        self.setting_burn_traps = RandoTriStateCheckBox(self.hint_placements_group_box)
        self.setting_burn_traps.setObjectName(u"setting_burn_traps")

        self.verticalLayout_24.addWidget(self.setting_burn_traps)

        self.setting_curse_traps = RandoTriStateCheckBox(self.hint_placements_group_box)
        self.setting_curse_traps.setObjectName(u"setting_curse_traps")

        self.verticalLayout_24.addWidget(self.setting_curse_traps)

        self.setting_noise_traps = RandoTriStateCheckBox(self.hint_placements_group_box)
        self.setting_noise_traps.setObjectName(u"setting_noise_traps")

        self.verticalLayout_24.addWidget(self.setting_noise_traps)

        self.setting_health_traps = RandoTriStateCheckBox(self.hint_placements_group_box)
        self.setting_health_traps.setObjectName(u"setting_health_traps")

        self.verticalLayout_24.addWidget(self.setting_health_traps)

        self.setting_groose_traps = RandoTriStateCheckBox(self.hint_placements_group_box)
        self.setting_groose_traps.setObjectName(u"setting_groose_traps")

        self.verticalLayout_24.addWidget(self.setting_groose_traps)

        self.hint_placements_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_24.addItem(self.hint_placements_vspacer)


        self.gridLayout_9.addWidget(self.hint_placements_group_box, 0, 2, 1, 1)

        self.gridLayout_9.setColumnStretch(0, 1)
        self.gridLayout_9.setColumnStretch(1, 1)
        self.gridLayout_9.setColumnStretch(2, 1)
        self.gridLayout_9.setColumnStretch(3, 1)
        self.tab_widget.addTab(self.gameplay_tab, "")
        self.world_tab = QWidget()
        self.world_tab.setObjectName(u"world_tab")
        sizePolicy1.setHeightForWidth(self.world_tab.sizePolicy().hasHeightForWidth())
        self.world_tab.setSizePolicy(sizePolicy1)
        self.gridLayout_2 = QGridLayout(self.world_tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.open_world_group_box = QGroupBox(self.world_tab)
        self.open_world_group_box.setObjectName(u"open_world_group_box")
        self.verticalLayout_14 = QVBoxLayout(self.open_world_group_box)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.setting_unlock_all_groosenator_destinations = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_unlock_all_groosenator_destinations.setObjectName(u"setting_unlock_all_groosenator_destinations")

        self.verticalLayout_14.addWidget(self.setting_unlock_all_groosenator_destinations)

        self.setting_open_thunderhead = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_open_thunderhead.setObjectName(u"setting_open_thunderhead")

        self.verticalLayout_14.addWidget(self.setting_open_thunderhead)

        self.open_lake_floria_label = QLabel(self.open_world_group_box)
        self.open_lake_floria_label.setObjectName(u"open_lake_floria_label")

        self.verticalLayout_14.addWidget(self.open_lake_floria_label)

        self.setting_open_lake_floria = QComboBox(self.open_world_group_box)
        self.setting_open_lake_floria.setObjectName(u"setting_open_lake_floria")

        self.verticalLayout_14.addWidget(self.setting_open_lake_floria)

        self.setting_open_batreaux_shed = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_open_batreaux_shed.setObjectName(u"setting_open_batreaux_shed")

        self.verticalLayout_14.addWidget(self.setting_open_batreaux_shed)

        self.setting_shortcut_ios_bridge_complete = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_shortcut_ios_bridge_complete.setObjectName(u"setting_shortcut_ios_bridge_complete")

        self.verticalLayout_14.addWidget(self.setting_shortcut_ios_bridge_complete)

        self.setting_shortcut_spiral_log_to_btt = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_shortcut_spiral_log_to_btt.setObjectName(u"setting_shortcut_spiral_log_to_btt")

        self.verticalLayout_14.addWidget(self.setting_shortcut_spiral_log_to_btt)

        self.setting_shortcut_logs_near_machi = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_shortcut_logs_near_machi.setObjectName(u"setting_shortcut_logs_near_machi")

        self.verticalLayout_14.addWidget(self.setting_shortcut_logs_near_machi)

        self.setting_shortcut_faron_log_to_floria = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_shortcut_faron_log_to_floria.setObjectName(u"setting_shortcut_faron_log_to_floria")

        self.verticalLayout_14.addWidget(self.setting_shortcut_faron_log_to_floria)

        self.setting_shortcut_deep_woods_log_before_tightrope = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_shortcut_deep_woods_log_before_tightrope.setObjectName(u"setting_shortcut_deep_woods_log_before_tightrope")

        self.verticalLayout_14.addWidget(self.setting_shortcut_deep_woods_log_before_tightrope)

        self.setting_shortcut_deep_woods_log_before_temple = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_shortcut_deep_woods_log_before_temple.setObjectName(u"setting_shortcut_deep_woods_log_before_temple")

        self.verticalLayout_14.addWidget(self.setting_shortcut_deep_woods_log_before_temple)

        self.setting_shortcut_eldin_entrance_boulder = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_shortcut_eldin_entrance_boulder.setObjectName(u"setting_shortcut_eldin_entrance_boulder")

        self.verticalLayout_14.addWidget(self.setting_shortcut_eldin_entrance_boulder)

        self.setting_shortcut_eldin_ascent_boulder = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_shortcut_eldin_ascent_boulder.setObjectName(u"setting_shortcut_eldin_ascent_boulder")

        self.verticalLayout_14.addWidget(self.setting_shortcut_eldin_ascent_boulder)

        self.setting_shortcut_vs_flames = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_shortcut_vs_flames.setObjectName(u"setting_shortcut_vs_flames")

        self.verticalLayout_14.addWidget(self.setting_shortcut_vs_flames)

        self.setting_shortcut_lanayru_bars = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_shortcut_lanayru_bars.setObjectName(u"setting_shortcut_lanayru_bars")

        self.verticalLayout_14.addWidget(self.setting_shortcut_lanayru_bars)

        self.setting_shortcut_west_wall_minecart = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_shortcut_west_wall_minecart.setObjectName(u"setting_shortcut_west_wall_minecart")

        self.verticalLayout_14.addWidget(self.setting_shortcut_west_wall_minecart)

        self.setting_shortcut_sand_oasis_minecart = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_shortcut_sand_oasis_minecart.setObjectName(u"setting_shortcut_sand_oasis_minecart")

        self.verticalLayout_14.addWidget(self.setting_shortcut_sand_oasis_minecart)

        self.setting_shortcut_minecart_before_caves = RandoTriStateCheckBox(self.open_world_group_box)
        self.setting_shortcut_minecart_before_caves.setObjectName(u"setting_shortcut_minecart_before_caves")

        self.verticalLayout_14.addWidget(self.setting_shortcut_minecart_before_caves)

        self.open_world_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_14.addItem(self.open_world_vspacer)


        self.gridLayout_2.addWidget(self.open_world_group_box, 0, 0, 1, 1)

        self.open_dungeons_group_box = QGroupBox(self.world_tab)
        self.open_dungeons_group_box.setObjectName(u"open_dungeons_group_box")
        self.verticalLayout_25 = QVBoxLayout(self.open_dungeons_group_box)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.setting_open_earth_temple = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_open_earth_temple.setObjectName(u"setting_open_earth_temple")

        self.verticalLayout_25.addWidget(self.setting_open_earth_temple)

        self.open_lmf_label = QLabel(self.open_dungeons_group_box)
        self.open_lmf_label.setObjectName(u"open_lmf_label")

        self.verticalLayout_25.addWidget(self.open_lmf_label)

        self.setting_open_lmf = QComboBox(self.open_dungeons_group_box)
        self.setting_open_lmf.setObjectName(u"setting_open_lmf")

        self.verticalLayout_25.addWidget(self.setting_open_lmf)

        self.line = QFrame(self.open_dungeons_group_box)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_25.addWidget(self.line)

        self.setting_shortcut_skyview_boards = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_shortcut_skyview_boards.setObjectName(u"setting_shortcut_skyview_boards")

        self.verticalLayout_25.addWidget(self.setting_shortcut_skyview_boards)

        self.setting_shortcut_skyview_bars = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_shortcut_skyview_bars.setObjectName(u"setting_shortcut_skyview_bars")

        self.verticalLayout_25.addWidget(self.setting_shortcut_skyview_bars)

        self.setting_shortcut_earth_temple_bridge = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_shortcut_earth_temple_bridge.setObjectName(u"setting_shortcut_earth_temple_bridge")

        self.verticalLayout_25.addWidget(self.setting_shortcut_earth_temple_bridge)

        self.setting_shortcut_lmf_wind_gates = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_shortcut_lmf_wind_gates.setObjectName(u"setting_shortcut_lmf_wind_gates")

        self.verticalLayout_25.addWidget(self.setting_shortcut_lmf_wind_gates)

        self.setting_shortcut_lmf_boxes = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_shortcut_lmf_boxes.setObjectName(u"setting_shortcut_lmf_boxes")

        self.verticalLayout_25.addWidget(self.setting_shortcut_lmf_boxes)

        self.setting_shortcut_lmf_bars_to_west_side = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_shortcut_lmf_bars_to_west_side.setObjectName(u"setting_shortcut_lmf_bars_to_west_side")

        self.verticalLayout_25.addWidget(self.setting_shortcut_lmf_bars_to_west_side)

        self.setting_shortcut_ac_bridge = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_shortcut_ac_bridge.setObjectName(u"setting_shortcut_ac_bridge")

        self.verticalLayout_25.addWidget(self.setting_shortcut_ac_bridge)

        self.setting_shortcut_ac_water_vents = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_shortcut_ac_water_vents.setObjectName(u"setting_shortcut_ac_water_vents")

        self.verticalLayout_25.addWidget(self.setting_shortcut_ac_water_vents)

        self.setting_shortcut_sandship_windows = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_shortcut_sandship_windows.setObjectName(u"setting_shortcut_sandship_windows")

        self.verticalLayout_25.addWidget(self.setting_shortcut_sandship_windows)

        self.setting_shortcut_sandship_brig_bars = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_shortcut_sandship_brig_bars.setObjectName(u"setting_shortcut_sandship_brig_bars")

        self.verticalLayout_25.addWidget(self.setting_shortcut_sandship_brig_bars)

        self.setting_shortcut_fs_outside_bars = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_shortcut_fs_outside_bars.setObjectName(u"setting_shortcut_fs_outside_bars")

        self.verticalLayout_25.addWidget(self.setting_shortcut_fs_outside_bars)

        self.setting_shortcut_fs_lava_flow = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_shortcut_fs_lava_flow.setObjectName(u"setting_shortcut_fs_lava_flow")

        self.verticalLayout_25.addWidget(self.setting_shortcut_fs_lava_flow)

        self.setting_shortcut_sky_keep_sv_room_bars = RandoTriStateCheckBox(self.open_dungeons_group_box)
        self.setting_shortcut_sky_keep_sv_room_bars.setObjectName(u"setting_shortcut_sky_keep_sv_room_bars")

        self.verticalLayout_25.addWidget(self.setting_shortcut_sky_keep_sv_room_bars)

        self.shortcuts_vspacer = QSpacerItem(20, 148, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_25.addItem(self.shortcuts_vspacer)


        self.gridLayout_2.addWidget(self.open_dungeons_group_box, 0, 1, 1, 1)

        self.entrance_randomization_group_box = QGroupBox(self.world_tab)
        self.entrance_randomization_group_box.setObjectName(u"entrance_randomization_group_box")
        self.verticalLayout_17 = QVBoxLayout(self.entrance_randomization_group_box)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.setting_randomize_door_entrances = RandoTriStateCheckBox(self.entrance_randomization_group_box)
        self.setting_randomize_door_entrances.setObjectName(u"setting_randomize_door_entrances")

        self.verticalLayout_17.addWidget(self.setting_randomize_door_entrances)

        self.setting_randomize_interior_entrances = RandoTriStateCheckBox(self.entrance_randomization_group_box)
        self.setting_randomize_interior_entrances.setObjectName(u"setting_randomize_interior_entrances")

        self.verticalLayout_17.addWidget(self.setting_randomize_interior_entrances)

        self.setting_randomize_overworld_entrances = RandoTriStateCheckBox(self.entrance_randomization_group_box)
        self.setting_randomize_overworld_entrances.setObjectName(u"setting_randomize_overworld_entrances")

        self.verticalLayout_17.addWidget(self.setting_randomize_overworld_entrances)

        self.setting_randomize_dungeon_entrances = RandoTriStateCheckBox(self.entrance_randomization_group_box)
        self.setting_randomize_dungeon_entrances.setObjectName(u"setting_randomize_dungeon_entrances")

        self.verticalLayout_17.addWidget(self.setting_randomize_dungeon_entrances)

        self.setting_randomize_trial_gate_entrances = RandoTriStateCheckBox(self.entrance_randomization_group_box)
        self.setting_randomize_trial_gate_entrances.setObjectName(u"setting_randomize_trial_gate_entrances")

        self.verticalLayout_17.addWidget(self.setting_randomize_trial_gate_entrances)

        self.random_starting_spawn_label = QLabel(self.entrance_randomization_group_box)
        self.random_starting_spawn_label.setObjectName(u"random_starting_spawn_label")

        self.verticalLayout_17.addWidget(self.random_starting_spawn_label)

        self.setting_random_starting_spawn = QComboBox(self.entrance_randomization_group_box)
        self.setting_random_starting_spawn.setObjectName(u"setting_random_starting_spawn")

        self.verticalLayout_17.addWidget(self.setting_random_starting_spawn)

        self.setting_limit_starting_spawn = RandoTriStateCheckBox(self.entrance_randomization_group_box)
        self.setting_limit_starting_spawn.setObjectName(u"setting_limit_starting_spawn")

        self.verticalLayout_17.addWidget(self.setting_limit_starting_spawn)

        self.setting_random_starting_statues = RandoTriStateCheckBox(self.entrance_randomization_group_box)
        self.setting_random_starting_statues.setObjectName(u"setting_random_starting_statues")

        self.verticalLayout_17.addWidget(self.setting_random_starting_statues)

        self.setting_decouple_double_doors = RandoTriStateCheckBox(self.entrance_randomization_group_box)
        self.setting_decouple_double_doors.setObjectName(u"setting_decouple_double_doors")

        self.verticalLayout_17.addWidget(self.setting_decouple_double_doors)

        self.setting_decouple_entrances = RandoTriStateCheckBox(self.entrance_randomization_group_box)
        self.setting_decouple_entrances.setObjectName(u"setting_decouple_entrances")

        self.verticalLayout_17.addWidget(self.setting_decouple_entrances)

        self.entrance_randomization_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.entrance_randomization_vspacer)


        self.gridLayout_2.addWidget(self.entrance_randomization_group_box, 0, 2, 1, 1)

        self.mixed_entrance_pools_group_box = QGroupBox(self.world_tab)
        self.mixed_entrance_pools_group_box.setObjectName(u"mixed_entrance_pools_group_box")
        sizePolicy.setHeightForWidth(self.mixed_entrance_pools_group_box.sizePolicy().hasHeightForWidth())
        self.mixed_entrance_pools_group_box.setSizePolicy(sizePolicy)
        self.verticalLayout_28 = QVBoxLayout(self.mixed_entrance_pools_group_box)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.mixed_entrance_pools_list_label = QLabel(self.mixed_entrance_pools_group_box)
        self.mixed_entrance_pools_list_label.setObjectName(u"mixed_entrance_pools_list_label")
        self.mixed_entrance_pools_list_label.setTextFormat(Qt.TextFormat.RichText)
        self.mixed_entrance_pools_list_label.setWordWrap(True)
        self.mixed_entrance_pools_list_label.setOpenExternalLinks(True)
        self.mixed_entrance_pools_list_label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse)

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

        self.mixed_entrance_pools_vspacer1 = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_28.addItem(self.mixed_entrance_pools_vspacer1)

        self.mixed_entrance_pools_hline = QFrame(self.mixed_entrance_pools_group_box)
        self.mixed_entrance_pools_hline.setObjectName(u"mixed_entrance_pools_hline")
        self.mixed_entrance_pools_hline.setFrameShape(QFrame.Shape.HLine)
        self.mixed_entrance_pools_hline.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_28.addWidget(self.mixed_entrance_pools_hline)

        self.mixed_entrance_pools_vspacer2 = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_28.addItem(self.mixed_entrance_pools_vspacer2)

        self.mixed_entrance_pools_explainer_label = QLabel(self.mixed_entrance_pools_group_box)
        self.mixed_entrance_pools_explainer_label.setObjectName(u"mixed_entrance_pools_explainer_label")
        sizePolicy3.setHeightForWidth(self.mixed_entrance_pools_explainer_label.sizePolicy().hasHeightForWidth())
        self.mixed_entrance_pools_explainer_label.setSizePolicy(sizePolicy3)
        self.mixed_entrance_pools_explainer_label.setTextFormat(Qt.TextFormat.RichText)
        self.mixed_entrance_pools_explainer_label.setWordWrap(True)
        self.mixed_entrance_pools_explainer_label.setOpenExternalLinks(True)
        self.mixed_entrance_pools_explainer_label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.verticalLayout_28.addWidget(self.mixed_entrance_pools_explainer_label)

        self.mixed_entrance_pools_vspacer3 = QSpacerItem(20, 3, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_28.addItem(self.mixed_entrance_pools_vspacer3)


        self.gridLayout_2.addWidget(self.mixed_entrance_pools_group_box, 0, 3, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.tab_widget.addTab(self.world_tab, "")
        self.locations_tab = QWidget()
        self.locations_tab.setObjectName(u"locations_tab")
        sizePolicy1.setHeightForWidth(self.locations_tab.sizePolicy().hasHeightForWidth())
        self.locations_tab.setSizePolicy(sizePolicy1)
        self.gridLayout_3 = QGridLayout(self.locations_tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.locations_button_layout = QVBoxLayout()
        self.locations_button_layout.setObjectName(u"locations_button_layout")
        self.individual_locations_top_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.locations_button_layout.addItem(self.individual_locations_top_vspacer)

        self.include_location_button = QPushButton(self.locations_tab)
        self.include_location_button.setObjectName(u"include_location_button")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.include_location_button.sizePolicy().hasHeightForWidth())
        self.include_location_button.setSizePolicy(sizePolicy8)

        self.locations_button_layout.addWidget(self.include_location_button)

        self.individual_locations_middle_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.locations_button_layout.addItem(self.individual_locations_middle_vspacer)

        self.exclude_location_button = QPushButton(self.locations_tab)
        self.exclude_location_button.setObjectName(u"exclude_location_button")
        sizePolicy8.setHeightForWidth(self.exclude_location_button.sizePolicy().hasHeightForWidth())
        self.exclude_location_button.setSizePolicy(sizePolicy8)

        self.locations_button_layout.addWidget(self.exclude_location_button)

        self.individual_locations_bottom_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.locations_button_layout.addItem(self.individual_locations_bottom_vspacer)

        self.locations_reset_button = QPushButton(self.locations_tab)
        self.locations_reset_button.setObjectName(u"locations_reset_button")

        self.locations_button_layout.addWidget(self.locations_reset_button)


        self.gridLayout_3.addLayout(self.locations_button_layout, 0, 1, 1, 1)

        self.shuffles_group_box = QGroupBox(self.locations_tab)
        self.shuffles_group_box.setObjectName(u"shuffles_group_box")
        sizePolicy.setHeightForWidth(self.shuffles_group_box.sizePolicy().hasHeightForWidth())
        self.shuffles_group_box.setSizePolicy(sizePolicy)
        self.verticalLayout_10 = QVBoxLayout(self.shuffles_group_box)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.beedle_shop_shuffle_label = QLabel(self.shuffles_group_box)
        self.beedle_shop_shuffle_label.setObjectName(u"beedle_shop_shuffle_label")
        self.beedle_shop_shuffle_label.setEnabled(False)

        self.verticalLayout_10.addWidget(self.beedle_shop_shuffle_label)

        self.setting_beedle_shop_shuffle = QComboBox(self.shuffles_group_box)
        self.setting_beedle_shop_shuffle.setObjectName(u"setting_beedle_shop_shuffle")
        self.setting_beedle_shop_shuffle.setEnabled(False)

        self.verticalLayout_10.addWidget(self.setting_beedle_shop_shuffle)

        self.rupee_shuffle_label = QLabel(self.shuffles_group_box)
        self.rupee_shuffle_label.setObjectName(u"rupee_shuffle_label")

        self.verticalLayout_10.addWidget(self.rupee_shuffle_label)

        self.setting_rupee_shuffle = QComboBox(self.shuffles_group_box)
        self.setting_rupee_shuffle.setObjectName(u"setting_rupee_shuffle")

        self.verticalLayout_10.addWidget(self.setting_rupee_shuffle)

        self.setting_underground_rupee_shuffle = RandoTriStateCheckBox(self.shuffles_group_box)
        self.setting_underground_rupee_shuffle.setObjectName(u"setting_underground_rupee_shuffle")

        self.verticalLayout_10.addWidget(self.setting_underground_rupee_shuffle)

        self.setting_goddess_chest_shuffle = RandoTriStateCheckBox(self.shuffles_group_box)
        self.setting_goddess_chest_shuffle.setObjectName(u"setting_goddess_chest_shuffle")

        self.verticalLayout_10.addWidget(self.setting_goddess_chest_shuffle)

        self.setting_gratitude_crystal_shuffle = RandoTriStateCheckBox(self.shuffles_group_box)
        self.setting_gratitude_crystal_shuffle.setObjectName(u"setting_gratitude_crystal_shuffle")

        self.verticalLayout_10.addWidget(self.setting_gratitude_crystal_shuffle)

        self.setting_stamina_fruit_shuffle = RandoTriStateCheckBox(self.shuffles_group_box)
        self.setting_stamina_fruit_shuffle.setObjectName(u"setting_stamina_fruit_shuffle")

        self.verticalLayout_10.addWidget(self.setting_stamina_fruit_shuffle)

        self.setting_hidden_item_shuffle = RandoTriStateCheckBox(self.shuffles_group_box)
        self.setting_hidden_item_shuffle.setObjectName(u"setting_hidden_item_shuffle")

        self.verticalLayout_10.addWidget(self.setting_hidden_item_shuffle)

        self.setting_tadtone_shuffle = RandoTriStateCheckBox(self.shuffles_group_box)
        self.setting_tadtone_shuffle.setObjectName(u"setting_tadtone_shuffle")

        self.verticalLayout_10.addWidget(self.setting_tadtone_shuffle)

        self.npc_closet_shuffle_label = QLabel(self.shuffles_group_box)
        self.npc_closet_shuffle_label.setObjectName(u"npc_closet_shuffle_label")

        self.verticalLayout_10.addWidget(self.npc_closet_shuffle_label)

        self.setting_npc_closet_shuffle = QComboBox(self.shuffles_group_box)
        self.setting_npc_closet_shuffle.setObjectName(u"setting_npc_closet_shuffle")

        self.verticalLayout_10.addWidget(self.setting_npc_closet_shuffle)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.trial_treasure_shuffle_label = QLabel(self.shuffles_group_box)
        self.trial_treasure_shuffle_label.setObjectName(u"trial_treasure_shuffle_label")
        sizePolicy.setHeightForWidth(self.trial_treasure_shuffle_label.sizePolicy().hasHeightForWidth())
        self.trial_treasure_shuffle_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_8.addWidget(self.trial_treasure_shuffle_label)

        self.setting_trial_treasure_shuffle = QSpinBox(self.shuffles_group_box)
        self.setting_trial_treasure_shuffle.setObjectName(u"setting_trial_treasure_shuffle")
        sizePolicy6.setHeightForWidth(self.setting_trial_treasure_shuffle.sizePolicy().hasHeightForWidth())
        self.setting_trial_treasure_shuffle.setSizePolicy(sizePolicy6)

        self.horizontalLayout_8.addWidget(self.setting_trial_treasure_shuffle)


        self.verticalLayout_10.addLayout(self.horizontalLayout_8)

        self.shuffles_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

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
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.excluded_locations_free_search.sizePolicy().hasHeightForWidth())
        self.excluded_locations_free_search.setSizePolicy(sizePolicy9)
        self.excluded_locations_free_search.setClearButtonEnabled(True)

        self.excluded_locations_filter_layout.addWidget(self.excluded_locations_free_search)


        self.verticalLayout_18.addLayout(self.excluded_locations_filter_layout)

        self.excluded_locations_list_view = QListView(self.excluded_locations_group_box)
        self.excluded_locations_list_view.setObjectName(u"excluded_locations_list_view")
        self.excluded_locations_list_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.excluded_locations_list_view.setProperty(u"showDropIndicator", False)
        self.excluded_locations_list_view.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
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
        sizePolicy9.setHeightForWidth(self.included_locations_free_search.sizePolicy().hasHeightForWidth())
        self.included_locations_free_search.setSizePolicy(sizePolicy9)
        self.included_locations_free_search.setClearButtonEnabled(True)

        self.included_locations_filter_layout.addWidget(self.included_locations_free_search)


        self.verticalLayout_9.addLayout(self.included_locations_filter_layout)

        self.included_locations_list_view = QListView(self.included_locations_group_box)
        self.included_locations_list_view.setObjectName(u"included_locations_list_view")
        self.included_locations_list_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.included_locations_list_view.setProperty(u"showDropIndicator", False)
        self.included_locations_list_view.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
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
        sizePolicy1.setHeightForWidth(self.inventory_tab.sizePolicy().hasHeightForWidth())
        self.inventory_tab.setSizePolicy(sizePolicy1)
        self.gridLayout_4 = QGridLayout(self.inventory_tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.randomized_items_group_box = QGroupBox(self.inventory_tab)
        self.randomized_items_group_box.setObjectName(u"randomized_items_group_box")
        sizePolicy.setHeightForWidth(self.randomized_items_group_box.sizePolicy().hasHeightForWidth())
        self.randomized_items_group_box.setSizePolicy(sizePolicy)
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
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.randomized_items_list_view.sizePolicy().hasHeightForWidth())
        self.randomized_items_list_view.setSizePolicy(sizePolicy10)
        self.randomized_items_list_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.randomized_items_list_view.setProperty(u"showDropIndicator", False)
        self.randomized_items_list_view.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
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
        sizePolicy10.setHeightForWidth(self.starting_items_list_view.sizePolicy().hasHeightForWidth())
        self.starting_items_list_view.setSizePolicy(sizePolicy10)
        self.starting_items_list_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.starting_items_list_view.setProperty(u"showDropIndicator", False)
        self.starting_items_list_view.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.starting_items_list_view.setSelectionRectVisible(False)

        self.verticalLayout_11.addWidget(self.starting_items_list_view)


        self.gridLayout_4.addWidget(self.starting_items_group_box, 0, 2, 1, 1)

        self.inventory_button_layout = QVBoxLayout()
        self.inventory_button_layout.setObjectName(u"inventory_button_layout")
        self.inventory_button_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.starting_items_top_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.inventory_button_layout.addItem(self.starting_items_top_vspacer)

        self.randomize_item_button = QPushButton(self.inventory_tab)
        self.randomize_item_button.setObjectName(u"randomize_item_button")
        sizePolicy8.setHeightForWidth(self.randomize_item_button.sizePolicy().hasHeightForWidth())
        self.randomize_item_button.setSizePolicy(sizePolicy8)

        self.inventory_button_layout.addWidget(self.randomize_item_button)

        self.starting_items_middle_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.inventory_button_layout.addItem(self.starting_items_middle_vspacer)

        self.start_with_item_button = QPushButton(self.inventory_tab)
        self.start_with_item_button.setObjectName(u"start_with_item_button")
        sizePolicy8.setHeightForWidth(self.start_with_item_button.sizePolicy().hasHeightForWidth())
        self.start_with_item_button.setSizePolicy(sizePolicy8)

        self.inventory_button_layout.addWidget(self.start_with_item_button)

        self.starting_items_bottom_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.inventory_button_layout.addItem(self.starting_items_bottom_vspacer)

        self.inventory_reset_button = QPushButton(self.inventory_tab)
        self.inventory_reset_button.setObjectName(u"inventory_reset_button")

        self.inventory_button_layout.addWidget(self.inventory_reset_button)


        self.gridLayout_4.addLayout(self.inventory_button_layout, 0, 1, 1, 1)

        self.item_settings_group_box = QGroupBox(self.inventory_tab)
        self.item_settings_group_box.setObjectName(u"item_settings_group_box")
        sizePolicy.setHeightForWidth(self.item_settings_group_box.sizePolicy().hasHeightForWidth())
        self.item_settings_group_box.setSizePolicy(sizePolicy)
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
        sizePolicy6.setHeightForWidth(self.setting_random_starting_tablet_count.sizePolicy().hasHeightForWidth())
        self.setting_random_starting_tablet_count.setSizePolicy(sizePolicy6)
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
        sizePolicy6.setHeightForWidth(self.setting_random_starting_item_count.sizePolicy().hasHeightForWidth())
        self.setting_random_starting_item_count.setSizePolicy(sizePolicy6)

        self.random_starting_item_count_layout.addWidget(self.setting_random_starting_item_count)


        self.verticalLayout_29.addLayout(self.random_starting_item_count_layout)

        self.starting_hearts_layout = QHBoxLayout()
        self.starting_hearts_layout.setObjectName(u"starting_hearts_layout")
        self.starting_hearts_label = QLabel(self.item_settings_group_box)
        self.starting_hearts_label.setObjectName(u"starting_hearts_label")

        self.starting_hearts_layout.addWidget(self.starting_hearts_label)

        self.setting_starting_hearts = QSpinBox(self.item_settings_group_box)
        self.setting_starting_hearts.setObjectName(u"setting_starting_hearts")
        sizePolicy6.setHeightForWidth(self.setting_starting_hearts.sizePolicy().hasHeightForWidth())
        self.setting_starting_hearts.setSizePolicy(sizePolicy6)

        self.starting_hearts_layout.addWidget(self.setting_starting_hearts)


        self.verticalLayout_29.addLayout(self.starting_hearts_layout)

        self.item_settings_vspacer = QSpacerItem(20, 137, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_29.addItem(self.item_settings_vspacer)


        self.gridLayout_4.addWidget(self.item_settings_group_box, 0, 3, 1, 1)

        self.gridLayout_4.setColumnStretch(0, 6)
        self.gridLayout_4.setColumnStretch(1, 1)
        self.gridLayout_4.setColumnStretch(2, 6)
        self.gridLayout_4.setColumnStretch(3, 4)
        self.tab_widget.addTab(self.inventory_tab, "")
        self.hints_tab = QWidget()
        self.hints_tab.setObjectName(u"hints_tab")
        sizePolicy1.setHeightForWidth(self.hints_tab.sizePolicy().hasHeightForWidth())
        self.hints_tab.setSizePolicy(sizePolicy1)
        self.gridLayout_8 = QGridLayout(self.hints_tab)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.included_hint_locations_group_box = QGroupBox(self.hints_tab)
        self.included_hint_locations_group_box.setObjectName(u"included_hint_locations_group_box")
        sizePolicy.setHeightForWidth(self.included_hint_locations_group_box.sizePolicy().hasHeightForWidth())
        self.included_hint_locations_group_box.setSizePolicy(sizePolicy)
        self.verticalLayout_26 = QVBoxLayout(self.included_hint_locations_group_box)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.included_hint_locations_free_search = QLineEdit(self.included_hint_locations_group_box)
        self.included_hint_locations_free_search.setObjectName(u"included_hint_locations_free_search")
        self.included_hint_locations_free_search.setClearButtonEnabled(True)

        self.verticalLayout_26.addWidget(self.included_hint_locations_free_search)

        self.included_hint_locations_list_view = QListView(self.included_hint_locations_group_box)
        self.included_hint_locations_list_view.setObjectName(u"included_hint_locations_list_view")
        sizePolicy10.setHeightForWidth(self.included_hint_locations_list_view.sizePolicy().hasHeightForWidth())
        self.included_hint_locations_list_view.setSizePolicy(sizePolicy10)
        self.included_hint_locations_list_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.included_hint_locations_list_view.setProperty(u"showDropIndicator", False)
        self.included_hint_locations_list_view.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.included_hint_locations_list_view.setSelectionRectVisible(False)

        self.verticalLayout_26.addWidget(self.included_hint_locations_list_view)


        self.gridLayout_8.addWidget(self.included_hint_locations_group_box, 0, 0, 1, 1)

        self.hints_button_layout = QVBoxLayout()
        self.hints_button_layout.setObjectName(u"hints_button_layout")
        self.hints_button_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.hints_top_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.hints_button_layout.addItem(self.hints_top_vspacer)

        self.include_hint_location_button = QPushButton(self.hints_tab)
        self.include_hint_location_button.setObjectName(u"include_hint_location_button")
        sizePolicy8.setHeightForWidth(self.include_hint_location_button.sizePolicy().hasHeightForWidth())
        self.include_hint_location_button.setSizePolicy(sizePolicy8)

        self.hints_button_layout.addWidget(self.include_hint_location_button)

        self.hints_middle_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.hints_button_layout.addItem(self.hints_middle_vspacer)

        self.exclude_hint_location_button = QPushButton(self.hints_tab)
        self.exclude_hint_location_button.setObjectName(u"exclude_hint_location_button")
        sizePolicy8.setHeightForWidth(self.exclude_hint_location_button.sizePolicy().hasHeightForWidth())
        self.exclude_hint_location_button.setSizePolicy(sizePolicy8)

        self.hints_button_layout.addWidget(self.exclude_hint_location_button)

        self.hints_bottom_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

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
        sizePolicy10.setHeightForWidth(self.excluded_hint_locations_list_view.sizePolicy().hasHeightForWidth())
        self.excluded_hint_locations_list_view.setSizePolicy(sizePolicy10)
        self.excluded_hint_locations_list_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.excluded_hint_locations_list_view.setProperty(u"showDropIndicator", False)
        self.excluded_hint_locations_list_view.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.excluded_hint_locations_list_view.setSelectionRectVisible(False)

        self.verticalLayout_27.addWidget(self.excluded_hint_locations_list_view)


        self.gridLayout_8.addWidget(self.excluded_hint_locations_group_box, 0, 2, 1, 1)

        self.hints_group_box = QGroupBox(self.hints_tab)
        self.hints_group_box.setObjectName(u"hints_group_box")
        self.verticalLayout_23 = QVBoxLayout(self.hints_group_box)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.setting_gossip_stone_hints = RandoTriStateCheckBox(self.hints_group_box)
        self.setting_gossip_stone_hints.setObjectName(u"setting_gossip_stone_hints")

        self.verticalLayout_23.addWidget(self.setting_gossip_stone_hints)

        self.setting_fi_hints = RandoTriStateCheckBox(self.hints_group_box)
        self.setting_fi_hints.setObjectName(u"setting_fi_hints")

        self.verticalLayout_23.addWidget(self.setting_fi_hints)

        self.setting_impa_sot_hint = RandoTriStateCheckBox(self.hints_group_box)
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
        sizePolicy6.setHeightForWidth(self.setting_path_hints.sizePolicy().hasHeightForWidth())
        self.setting_path_hints.setSizePolicy(sizePolicy6)

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
        sizePolicy6.setHeightForWidth(self.setting_barren_hints.sizePolicy().hasHeightForWidth())
        self.setting_barren_hints.setSizePolicy(sizePolicy6)

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
        sizePolicy6.setHeightForWidth(self.setting_location_hints.sizePolicy().hasHeightForWidth())
        self.setting_location_hints.setSizePolicy(sizePolicy6)

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
        sizePolicy6.setHeightForWidth(self.setting_item_hints.sizePolicy().hasHeightForWidth())
        self.setting_item_hints.setSizePolicy(sizePolicy6)

        self.item_hints_layout.addWidget(self.setting_item_hints)


        self.verticalLayout_23.addLayout(self.item_hints_layout)

        self.setting_always_hints = RandoTriStateCheckBox(self.hints_group_box)
        self.setting_always_hints.setObjectName(u"setting_always_hints")

        self.verticalLayout_23.addWidget(self.setting_always_hints)

        self.setting_cryptic_hint_text = RandoTriStateCheckBox(self.hints_group_box)
        self.setting_cryptic_hint_text.setObjectName(u"setting_cryptic_hint_text")

        self.verticalLayout_23.addWidget(self.setting_cryptic_hint_text)

        self.chest_size_matches_contents_label = QLabel(self.hints_group_box)
        self.chest_size_matches_contents_label.setObjectName(u"chest_size_matches_contents_label")

        self.verticalLayout_23.addWidget(self.chest_size_matches_contents_label)

        self.setting_chest_type_matches_contents = QComboBox(self.hints_group_box)
        self.setting_chest_type_matches_contents.setObjectName(u"setting_chest_type_matches_contents")

        self.verticalLayout_23.addWidget(self.setting_chest_type_matches_contents)

        self.setting_small_keys_in_fancy_chests = RandoTriStateCheckBox(self.hints_group_box)
        self.setting_small_keys_in_fancy_chests.setObjectName(u"setting_small_keys_in_fancy_chests")

        self.verticalLayout_23.addWidget(self.setting_small_keys_in_fancy_chests)

        self.hints_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_23.addItem(self.hints_vspacer)


        self.gridLayout_8.addWidget(self.hints_group_box, 0, 3, 1, 1)

        self.gridLayout_8.setColumnStretch(0, 6)
        self.gridLayout_8.setColumnStretch(1, 1)
        self.gridLayout_8.setColumnStretch(2, 6)
        self.gridLayout_8.setColumnStretch(3, 4)
        self.tab_widget.addTab(self.hints_tab, "")
        self.logic_tab = QWidget()
        self.logic_tab.setObjectName(u"logic_tab")
        sizePolicy1.setHeightForWidth(self.logic_tab.sizePolicy().hasHeightForWidth())
        self.logic_tab.setSizePolicy(sizePolicy1)
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

        self.logic_rules_hspacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.logic_rules_hspacer)


        self.gridLayout_5.addWidget(self.logic_rules_group_box, 0, 0, 1, 1)

        self.tricks_group_box = QGroupBox(self.logic_tab)
        self.tricks_group_box.setObjectName(u"tricks_group_box")
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.tricks_group_box.sizePolicy().hasHeightForWidth())
        self.tricks_group_box.setSizePolicy(sizePolicy11)
        self.gridLayout_6 = QGridLayout(self.tricks_group_box)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.precise_items_group_box = QGroupBox(self.tricks_group_box)
        self.precise_items_group_box.setObjectName(u"precise_items_group_box")
        sizePolicy.setHeightForWidth(self.precise_items_group_box.sizePolicy().hasHeightForWidth())
        self.precise_items_group_box.setSizePolicy(sizePolicy)
        self.verticalLayout_20 = QVBoxLayout(self.precise_items_group_box)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.setting_logic_advanced_lizalfos_combat = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_advanced_lizalfos_combat.setObjectName(u"setting_logic_advanced_lizalfos_combat")

        self.verticalLayout_20.addWidget(self.setting_logic_advanced_lizalfos_combat)

        self.setting_logic_long_ranged_skyward_strikes = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_long_ranged_skyward_strikes.setObjectName(u"setting_logic_long_ranged_skyward_strikes")

        self.verticalLayout_20.addWidget(self.setting_logic_long_ranged_skyward_strikes)

        self.setting_logic_skyview_precise_slingshot = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_skyview_precise_slingshot.setObjectName(u"setting_logic_skyview_precise_slingshot")

        self.verticalLayout_20.addWidget(self.setting_logic_skyview_precise_slingshot)

        self.setting_logic_lmf_ceiling_precise_slingshot = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_lmf_ceiling_precise_slingshot.setObjectName(u"setting_logic_lmf_ceiling_precise_slingshot")

        self.verticalLayout_20.addWidget(self.setting_logic_lmf_ceiling_precise_slingshot)

        self.setting_logic_tot_slingshot = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_tot_slingshot.setObjectName(u"setting_logic_tot_slingshot")

        self.verticalLayout_20.addWidget(self.setting_logic_tot_slingshot)

        self.setting_logic_bomb_throws = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_bomb_throws.setObjectName(u"setting_logic_bomb_throws")

        self.verticalLayout_20.addWidget(self.setting_logic_bomb_throws)

        self.setting_logic_lanayru_mine_quick_bomb = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_lanayru_mine_quick_bomb.setObjectName(u"setting_logic_lanayru_mine_quick_bomb")

        self.verticalLayout_20.addWidget(self.setting_logic_lanayru_mine_quick_bomb)

        self.setting_logic_cactus_bomb_whip = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_cactus_bomb_whip.setObjectName(u"setting_logic_cactus_bomb_whip")

        self.verticalLayout_20.addWidget(self.setting_logic_cactus_bomb_whip)

        self.setting_logic_beedles_shop_with_bombs = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_beedles_shop_with_bombs.setObjectName(u"setting_logic_beedles_shop_with_bombs")

        self.verticalLayout_20.addWidget(self.setting_logic_beedles_shop_with_bombs)

        self.setting_logic_bird_nest_item_from_beedles_shop = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_bird_nest_item_from_beedles_shop.setObjectName(u"setting_logic_bird_nest_item_from_beedles_shop")

        self.verticalLayout_20.addWidget(self.setting_logic_bird_nest_item_from_beedles_shop)

        self.setting_logic_precise_beetle = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_precise_beetle.setObjectName(u"setting_logic_precise_beetle")

        self.verticalLayout_20.addWidget(self.setting_logic_precise_beetle)

        self.setting_logic_skippers_fast_clawshots = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_skippers_fast_clawshots.setObjectName(u"setting_logic_skippers_fast_clawshots")

        self.verticalLayout_20.addWidget(self.setting_logic_skippers_fast_clawshots)

        self.setting_logic_lmf_whip_switch = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_lmf_whip_switch.setObjectName(u"setting_logic_lmf_whip_switch")

        self.verticalLayout_20.addWidget(self.setting_logic_lmf_whip_switch)

        self.setting_logic_lmf_whip_armos_room_timeshift_stone = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_lmf_whip_armos_room_timeshift_stone.setObjectName(u"setting_logic_lmf_whip_armos_room_timeshift_stone")

        self.verticalLayout_20.addWidget(self.setting_logic_lmf_whip_armos_room_timeshift_stone)

        self.setting_logic_lmf_minecart_jump = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_lmf_minecart_jump.setObjectName(u"setting_logic_lmf_minecart_jump")

        self.verticalLayout_20.addWidget(self.setting_logic_lmf_minecart_jump)

        self.setting_logic_present_bow_switches = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_present_bow_switches.setObjectName(u"setting_logic_present_bow_switches")

        self.verticalLayout_20.addWidget(self.setting_logic_present_bow_switches)

        self.setting_logic_skykeep_vineclip = RandoTriStateCheckBox(self.precise_items_group_box)
        self.setting_logic_skykeep_vineclip.setObjectName(u"setting_logic_skykeep_vineclip")

        self.verticalLayout_20.addWidget(self.setting_logic_skykeep_vineclip)

        self.precise_items_vspacer = QSpacerItem(20, 87, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_20.addItem(self.precise_items_vspacer)


        self.gridLayout_6.addWidget(self.precise_items_group_box, 0, 0, 1, 1)

        self.dives_and_jumps_group_box = QGroupBox(self.tricks_group_box)
        self.dives_and_jumps_group_box.setObjectName(u"dives_and_jumps_group_box")
        sizePolicy.setHeightForWidth(self.dives_and_jumps_group_box.sizePolicy().hasHeightForWidth())
        self.dives_and_jumps_group_box.setSizePolicy(sizePolicy)
        self.verticalLayout_19 = QVBoxLayout(self.dives_and_jumps_group_box)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.setting_logic_volcanic_island_dive = RandoTriStateCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_volcanic_island_dive.setObjectName(u"setting_logic_volcanic_island_dive")

        self.verticalLayout_19.addWidget(self.setting_logic_volcanic_island_dive)

        self.setting_logic_east_island_dive = RandoTriStateCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_east_island_dive.setObjectName(u"setting_logic_east_island_dive")

        self.verticalLayout_19.addWidget(self.setting_logic_east_island_dive)

        self.setting_logic_beedles_island_cage_chest_dive = RandoTriStateCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_beedles_island_cage_chest_dive.setObjectName(u"setting_logic_beedles_island_cage_chest_dive")

        self.verticalLayout_19.addWidget(self.setting_logic_beedles_island_cage_chest_dive)

        self.setting_logic_gravestone_jump = RandoTriStateCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_gravestone_jump.setObjectName(u"setting_logic_gravestone_jump")

        self.verticalLayout_19.addWidget(self.setting_logic_gravestone_jump)

        self.setting_logic_waterfall_cave_jump = RandoTriStateCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_waterfall_cave_jump.setObjectName(u"setting_logic_waterfall_cave_jump")

        self.verticalLayout_19.addWidget(self.setting_logic_waterfall_cave_jump)

        self.setting_logic_early_lake_floria = RandoTriStateCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_early_lake_floria.setObjectName(u"setting_logic_early_lake_floria")

        self.verticalLayout_19.addWidget(self.setting_logic_early_lake_floria)

        self.setting_logic_skyview_coiled_rupee_jump = RandoTriStateCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_skyview_coiled_rupee_jump.setObjectName(u"setting_logic_skyview_coiled_rupee_jump")

        self.verticalLayout_19.addWidget(self.setting_logic_skyview_coiled_rupee_jump)

        self.setting_logic_ac_lever_jump_trick = RandoTriStateCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_ac_lever_jump_trick.setObjectName(u"setting_logic_ac_lever_jump_trick")

        self.verticalLayout_19.addWidget(self.setting_logic_ac_lever_jump_trick)

        self.setting_logic_ac_chest_after_whip_hooks_jump = RandoTriStateCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_ac_chest_after_whip_hooks_jump.setObjectName(u"setting_logic_ac_chest_after_whip_hooks_jump")

        self.verticalLayout_19.addWidget(self.setting_logic_ac_chest_after_whip_hooks_jump)

        self.setting_logic_sandship_jump_to_stern = RandoTriStateCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_sandship_jump_to_stern.setObjectName(u"setting_logic_sandship_jump_to_stern")

        self.verticalLayout_19.addWidget(self.setting_logic_sandship_jump_to_stern)

        self.setting_logic_fs_pillar_jump = RandoTriStateCheckBox(self.dives_and_jumps_group_box)
        self.setting_logic_fs_pillar_jump.setObjectName(u"setting_logic_fs_pillar_jump")

        self.verticalLayout_19.addWidget(self.setting_logic_fs_pillar_jump)

        self.dives_and_jumps_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_19.addItem(self.dives_and_jumps_vspacer)


        self.gridLayout_6.addWidget(self.dives_and_jumps_group_box, 0, 1, 1, 1)

        self.glitches_group_box = QGroupBox(self.tricks_group_box)
        self.glitches_group_box.setObjectName(u"glitches_group_box")
        sizePolicy.setHeightForWidth(self.glitches_group_box.sizePolicy().hasHeightForWidth())
        self.glitches_group_box.setSizePolicy(sizePolicy)
        self.verticalLayout_21 = QVBoxLayout(self.glitches_group_box)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.setting_logic_stuttersprint = RandoTriStateCheckBox(self.glitches_group_box)
        self.setting_logic_stuttersprint.setObjectName(u"setting_logic_stuttersprint")

        self.verticalLayout_21.addWidget(self.setting_logic_stuttersprint)

        self.setting_logic_et_slope_stuttersprint = RandoTriStateCheckBox(self.glitches_group_box)
        self.setting_logic_et_slope_stuttersprint.setObjectName(u"setting_logic_et_slope_stuttersprint")

        self.verticalLayout_21.addWidget(self.setting_logic_et_slope_stuttersprint)

        self.setting_logic_brakeslide = RandoTriStateCheckBox(self.glitches_group_box)
        self.setting_logic_brakeslide.setObjectName(u"setting_logic_brakeslide")

        self.verticalLayout_21.addWidget(self.setting_logic_brakeslide)

        self.setting_logic_tot_skip_brakeslide = RandoTriStateCheckBox(self.glitches_group_box)
        self.setting_logic_tot_skip_brakeslide.setObjectName(u"setting_logic_tot_skip_brakeslide")

        self.verticalLayout_21.addWidget(self.setting_logic_tot_skip_brakeslide)

        self.glitches_vspacer = QSpacerItem(20, 399, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_21.addItem(self.glitches_vspacer)


        self.gridLayout_6.addWidget(self.glitches_group_box, 0, 2, 1, 1)

        self.miscellaneous_group_box = QGroupBox(self.tricks_group_box)
        self.miscellaneous_group_box.setObjectName(u"miscellaneous_group_box")
        sizePolicy.setHeightForWidth(self.miscellaneous_group_box.sizePolicy().hasHeightForWidth())
        self.miscellaneous_group_box.setSizePolicy(sizePolicy)
        self.verticalLayout_22 = QVBoxLayout(self.miscellaneous_group_box)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.setting_logic_faron_woods_with_groosenator = RandoTriStateCheckBox(self.miscellaneous_group_box)
        self.setting_logic_faron_woods_with_groosenator.setObjectName(u"setting_logic_faron_woods_with_groosenator")

        self.verticalLayout_22.addWidget(self.setting_logic_faron_woods_with_groosenator)

        self.setting_logic_itemless_first_timeshift_stone = RandoTriStateCheckBox(self.miscellaneous_group_box)
        self.setting_logic_itemless_first_timeshift_stone.setObjectName(u"setting_logic_itemless_first_timeshift_stone")

        self.verticalLayout_22.addWidget(self.setting_logic_itemless_first_timeshift_stone)

        self.setting_logic_fire_node_without_hook_beetle = RandoTriStateCheckBox(self.miscellaneous_group_box)
        self.setting_logic_fire_node_without_hook_beetle.setObjectName(u"setting_logic_fire_node_without_hook_beetle")

        self.verticalLayout_22.addWidget(self.setting_logic_fire_node_without_hook_beetle)

        self.setting_logic_skyview_spider_roll = RandoTriStateCheckBox(self.miscellaneous_group_box)
        self.setting_logic_skyview_spider_roll.setObjectName(u"setting_logic_skyview_spider_roll")

        self.verticalLayout_22.addWidget(self.setting_logic_skyview_spider_roll)

        self.setting_logic_et_keese_skyward_strike = RandoTriStateCheckBox(self.miscellaneous_group_box)
        self.setting_logic_et_keese_skyward_strike.setObjectName(u"setting_logic_et_keese_skyward_strike")

        self.verticalLayout_22.addWidget(self.setting_logic_et_keese_skyward_strike)

        self.setting_logic_et_bombless_scaldera = RandoTriStateCheckBox(self.miscellaneous_group_box)
        self.setting_logic_et_bombless_scaldera.setObjectName(u"setting_logic_et_bombless_scaldera")

        self.verticalLayout_22.addWidget(self.setting_logic_et_bombless_scaldera)

        self.setting_logic_lmf_bellowsless_moldarach = RandoTriStateCheckBox(self.miscellaneous_group_box)
        self.setting_logic_lmf_bellowsless_moldarach.setObjectName(u"setting_logic_lmf_bellowsless_moldarach")

        self.verticalLayout_22.addWidget(self.setting_logic_lmf_bellowsless_moldarach)

        self.setting_logic_sandship_itemless_spume = RandoTriStateCheckBox(self.miscellaneous_group_box)
        self.setting_logic_sandship_itemless_spume.setObjectName(u"setting_logic_sandship_itemless_spume")

        self.verticalLayout_22.addWidget(self.setting_logic_sandship_itemless_spume)

        self.setting_logic_sandship_no_combination_hint = RandoTriStateCheckBox(self.miscellaneous_group_box)
        self.setting_logic_sandship_no_combination_hint.setObjectName(u"setting_logic_sandship_no_combination_hint")

        self.verticalLayout_22.addWidget(self.setting_logic_sandship_no_combination_hint)

        self.setting_logic_fs_practice_sword_ghirahim_2 = RandoTriStateCheckBox(self.miscellaneous_group_box)
        self.setting_logic_fs_practice_sword_ghirahim_2.setObjectName(u"setting_logic_fs_practice_sword_ghirahim_2")

        self.verticalLayout_22.addWidget(self.setting_logic_fs_practice_sword_ghirahim_2)

        self.miscellaneous_vspacer = QSpacerItem(20, 237, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_22.addItem(self.miscellaneous_vspacer)


        self.gridLayout_6.addWidget(self.miscellaneous_group_box, 0, 3, 1, 1)

        self.gridLayout_6.setColumnStretch(0, 1)
        self.gridLayout_6.setColumnStretch(1, 1)
        self.gridLayout_6.setColumnStretch(2, 1)
        self.gridLayout_6.setColumnStretch(3, 1)

        self.gridLayout_5.addWidget(self.tricks_group_box, 1, 0, 1, 1)

        self.tab_widget.addTab(self.logic_tab, "")
        self.cosmetics_tab = QWidget()
        self.cosmetics_tab.setObjectName(u"cosmetics_tab")
        self.horizontalLayout_2 = QHBoxLayout(self.cosmetics_tab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.environment_cosmetics_group_box = QGroupBox(self.cosmetics_tab)
        self.environment_cosmetics_group_box.setObjectName(u"environment_cosmetics_group_box")
        self.verticalLayout_33 = QVBoxLayout(self.environment_cosmetics_group_box)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.setting_starry_skies = RandoTriStateCheckBox(self.environment_cosmetics_group_box)
        self.setting_starry_skies.setObjectName(u"setting_starry_skies")

        self.verticalLayout_33.addWidget(self.setting_starry_skies)

        self.daytime_sky_color_label = QLabel(self.environment_cosmetics_group_box)
        self.daytime_sky_color_label.setObjectName(u"daytime_sky_color_label")

        self.verticalLayout_33.addWidget(self.daytime_sky_color_label)

        self.setting_daytime_sky_color = QComboBox(self.environment_cosmetics_group_box)
        self.setting_daytime_sky_color.setObjectName(u"setting_daytime_sky_color")

        self.verticalLayout_33.addWidget(self.setting_daytime_sky_color)

        self.nighttime_sky_color_label = QLabel(self.environment_cosmetics_group_box)
        self.nighttime_sky_color_label.setObjectName(u"nighttime_sky_color_label")

        self.verticalLayout_33.addWidget(self.nighttime_sky_color_label)

        self.setting_nighttime_sky_color = QComboBox(self.environment_cosmetics_group_box)
        self.setting_nighttime_sky_color.setObjectName(u"setting_nighttime_sky_color")

        self.verticalLayout_33.addWidget(self.setting_nighttime_sky_color)

        self.daytime_cloud_color_label = QLabel(self.environment_cosmetics_group_box)
        self.daytime_cloud_color_label.setObjectName(u"daytime_cloud_color_label")

        self.verticalLayout_33.addWidget(self.daytime_cloud_color_label)

        self.setting_daytime_cloud_color = QComboBox(self.environment_cosmetics_group_box)
        self.setting_daytime_cloud_color.setObjectName(u"setting_daytime_cloud_color")

        self.verticalLayout_33.addWidget(self.setting_daytime_cloud_color)

        self.nighttime_cloud_color_label = QLabel(self.environment_cosmetics_group_box)
        self.nighttime_cloud_color_label.setObjectName(u"nighttime_cloud_color_label")

        self.verticalLayout_33.addWidget(self.nighttime_cloud_color_label)

        self.setting_nighttime_cloud_color = QComboBox(self.environment_cosmetics_group_box)
        self.setting_nighttime_cloud_color.setObjectName(u"setting_nighttime_cloud_color")

        self.verticalLayout_33.addWidget(self.setting_nighttime_cloud_color)

        self.environment_cosmetics_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_33.addItem(self.environment_cosmetics_vspacer)


        self.horizontalLayout_2.addWidget(self.environment_cosmetics_group_box)

        self.player_cosmetics_group_box = QGroupBox(self.cosmetics_tab)
        self.player_cosmetics_group_box.setObjectName(u"player_cosmetics_group_box")
        self.verticalLayout_37 = QVBoxLayout(self.player_cosmetics_group_box)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.setting_tunic_swap = RandoTriStateCheckBox(self.player_cosmetics_group_box)
        self.setting_tunic_swap.setObjectName(u"setting_tunic_swap")

        self.verticalLayout_37.addWidget(self.setting_tunic_swap)

        self.setting_lightning_skyward_strike = RandoTriStateCheckBox(self.player_cosmetics_group_box)
        self.setting_lightning_skyward_strike.setObjectName(u"setting_lightning_skyward_strike")

        self.verticalLayout_37.addWidget(self.setting_lightning_skyward_strike)

        self.player_cosmetics_hline = QFrame(self.player_cosmetics_group_box)
        self.player_cosmetics_hline.setObjectName(u"player_cosmetics_hline")
        self.player_cosmetics_hline.setFrameShape(QFrame.Shape.HLine)
        self.player_cosmetics_hline.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_37.addWidget(self.player_cosmetics_hline)

        self.player_cosmetics_texture_gude_label = QLabel(self.player_cosmetics_group_box)
        self.player_cosmetics_texture_gude_label.setObjectName(u"player_cosmetics_texture_gude_label")
        self.player_cosmetics_texture_gude_label.setTextFormat(Qt.TextFormat.RichText)
        self.player_cosmetics_texture_gude_label.setWordWrap(True)
        self.player_cosmetics_texture_gude_label.setOpenExternalLinks(True)
        self.player_cosmetics_texture_gude_label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.verticalLayout_37.addWidget(self.player_cosmetics_texture_gude_label)

        self.player_cosmetics_vspacer = QSpacerItem(20, 545, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_37.addItem(self.player_cosmetics_vspacer)


        self.horizontalLayout_2.addWidget(self.player_cosmetics_group_box)

        self.audio_cosmetics_group_box = QGroupBox(self.cosmetics_tab)
        self.audio_cosmetics_group_box.setObjectName(u"audio_cosmetics_group_box")
        self.verticalLayout_35 = QVBoxLayout(self.audio_cosmetics_group_box)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.setting_remove_enemy_music = RandoTriStateCheckBox(self.audio_cosmetics_group_box)
        self.setting_remove_enemy_music.setObjectName(u"setting_remove_enemy_music")

        self.verticalLayout_35.addWidget(self.setting_remove_enemy_music)

        self.low_health_beeping_speed_label = QLabel(self.audio_cosmetics_group_box)
        self.low_health_beeping_speed_label.setObjectName(u"low_health_beeping_speed_label")

        self.verticalLayout_35.addWidget(self.low_health_beeping_speed_label)

        self.setting_low_health_beeping_speed = QComboBox(self.audio_cosmetics_group_box)
        self.setting_low_health_beeping_speed.setObjectName(u"setting_low_health_beeping_speed")

        self.verticalLayout_35.addWidget(self.setting_low_health_beeping_speed)

        self.audio_cosmetics_vspacer = QSpacerItem(20, 545, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_35.addItem(self.audio_cosmetics_vspacer)


        self.horizontalLayout_2.addWidget(self.audio_cosmetics_group_box)

        self.text_cosmetics_group_box = QGroupBox(self.cosmetics_tab)
        self.text_cosmetics_group_box.setObjectName(u"text_cosmetics_group_box")
        self.verticalLayout_36 = QVBoxLayout(self.text_cosmetics_group_box)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.language_label = QLabel(self.text_cosmetics_group_box)
        self.language_label.setObjectName(u"language_label")

        self.verticalLayout_36.addWidget(self.language_label)

        self.setting_language = QComboBox(self.text_cosmetics_group_box)
        self.setting_language.setObjectName(u"setting_language")

        self.verticalLayout_36.addWidget(self.setting_language)

        self.text_cosmetics_vspacer = QSpacerItem(20, 522, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_36.addItem(self.text_cosmetics_vspacer)


        self.horizontalLayout_2.addWidget(self.text_cosmetics_group_box)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 1)
        self.tab_widget.addTab(self.cosmetics_tab, "")
        self.advanced_tab = QWidget()
        self.advanced_tab.setObjectName(u"advanced_tab")
        sizePolicy1.setHeightForWidth(self.advanced_tab.sizePolicy().hasHeightForWidth())
        self.advanced_tab.setSizePolicy(sizePolicy1)
        self.horizontalLayout_4 = QHBoxLayout(self.advanced_tab)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.file_setup_group_box = QGroupBox(self.advanced_tab)
        self.file_setup_group_box.setObjectName(u"file_setup_group_box")
        sizePolicy.setHeightForWidth(self.file_setup_group_box.sizePolicy().hasHeightForWidth())
        self.file_setup_group_box.setSizePolicy(sizePolicy)
        self.verticalLayout_31 = QVBoxLayout(self.file_setup_group_box)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.config_generate_spoiler_log = QCheckBox(self.file_setup_group_box)
        self.config_generate_spoiler_log.setObjectName(u"config_generate_spoiler_log")

        self.verticalLayout_31.addWidget(self.config_generate_spoiler_log)

        self.utils_hline = QFrame(self.file_setup_group_box)
        self.utils_hline.setObjectName(u"utils_hline")
        self.utils_hline.setFrameShape(QFrame.Shape.HLine)
        self.utils_hline.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_31.addWidget(self.utils_hline)

        self.open_folders_label = QLabel(self.file_setup_group_box)
        self.open_folders_label.setObjectName(u"open_folders_label")

        self.verticalLayout_31.addWidget(self.open_folders_label)

        self.open_output_folder_button = QPushButton(self.file_setup_group_box)
        self.open_output_folder_button.setObjectName(u"open_output_folder_button")

        self.verticalLayout_31.addWidget(self.open_output_folder_button)

        self.open_extract_folder_button = QPushButton(self.file_setup_group_box)
        self.open_extract_folder_button.setObjectName(u"open_extract_folder_button")

        self.verticalLayout_31.addWidget(self.open_extract_folder_button)

        self.open_spoiler_logs_folder_button = QPushButton(self.file_setup_group_box)
        self.open_spoiler_logs_folder_button.setObjectName(u"open_spoiler_logs_folder_button")

        self.verticalLayout_31.addWidget(self.open_spoiler_logs_folder_button)

        self.utils_hline_2 = QFrame(self.file_setup_group_box)
        self.utils_hline_2.setObjectName(u"utils_hline_2")
        self.utils_hline_2.setFrameShape(QFrame.Shape.HLine)
        self.utils_hline_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_31.addWidget(self.utils_hline_2)

        self.output_label = QLabel(self.file_setup_group_box)
        self.output_label.setObjectName(u"output_label")
        sizePolicy.setHeightForWidth(self.output_label.sizePolicy().hasHeightForWidth())
        self.output_label.setSizePolicy(sizePolicy)

        self.verticalLayout_31.addWidget(self.output_label)

        self.config_output = QLineEdit(self.file_setup_group_box)
        self.config_output.setObjectName(u"config_output")
        self.config_output.setReadOnly(True)

        self.verticalLayout_31.addWidget(self.config_output)

        self.output_button_layout = QHBoxLayout()
        self.output_button_layout.setObjectName(u"output_button_layout")
        self.reset_output_button = QPushButton(self.file_setup_group_box)
        self.reset_output_button.setObjectName(u"reset_output_button")

        self.output_button_layout.addWidget(self.reset_output_button)

        self.browse_output_button = QPushButton(self.file_setup_group_box)
        self.browse_output_button.setObjectName(u"browse_output_button")

        self.output_button_layout.addWidget(self.browse_output_button)


        self.verticalLayout_31.addLayout(self.output_button_layout)

        self.utils_hline_3 = QFrame(self.file_setup_group_box)
        self.utils_hline_3.setObjectName(u"utils_hline_3")
        self.utils_hline_3.setFrameShape(QFrame.Shape.HLine)
        self.utils_hline_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_31.addWidget(self.utils_hline_3)

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

        self.file_setup_vspacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_31.addItem(self.file_setup_vspacer)


        self.horizontalLayout_4.addWidget(self.file_setup_group_box)

        self.plandomizer_group_box = QGroupBox(self.advanced_tab)
        self.plandomizer_group_box.setObjectName(u"plandomizer_group_box")
        sizePolicy.setHeightForWidth(self.plandomizer_group_box.sizePolicy().hasHeightForWidth())
        self.plandomizer_group_box.setSizePolicy(sizePolicy)
        self.verticalLayout_30 = QVBoxLayout(self.plandomizer_group_box)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.plandomizer_warning_label = QLabel(self.plandomizer_group_box)
        self.plandomizer_warning_label.setObjectName(u"plandomizer_warning_label")
        self.plandomizer_warning_label.setTextFormat(Qt.TextFormat.RichText)
        self.plandomizer_warning_label.setWordWrap(True)
        self.plandomizer_warning_label.setOpenExternalLinks(True)
        self.plandomizer_warning_label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse)

        self.verticalLayout_30.addWidget(self.plandomizer_warning_label)

        self.config_use_plandomizer = QCheckBox(self.plandomizer_group_box)
        self.config_use_plandomizer.setObjectName(u"config_use_plandomizer")

        self.verticalLayout_30.addWidget(self.config_use_plandomizer)

        self.selected_plandomizer_file_label = QLabel(self.plandomizer_group_box)
        self.selected_plandomizer_file_label.setObjectName(u"selected_plandomizer_file_label")

        self.verticalLayout_30.addWidget(self.selected_plandomizer_file_label)

        self.selected_plandomizer_file_combo_box = QComboBox(self.plandomizer_group_box)
        self.selected_plandomizer_file_combo_box.setObjectName(u"selected_plandomizer_file_combo_box")
        sizePolicy7.setHeightForWidth(self.selected_plandomizer_file_combo_box.sizePolicy().hasHeightForWidth())
        self.selected_plandomizer_file_combo_box.setSizePolicy(sizePolicy7)
        self.selected_plandomizer_file_combo_box.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.selected_plandomizer_file_combo_box.setMinimumContentsLength(1)

        self.verticalLayout_30.addWidget(self.selected_plandomizer_file_combo_box)

        self.open_plandomizer_folder_button = QPushButton(self.plandomizer_group_box)
        self.open_plandomizer_folder_button.setObjectName(u"open_plandomizer_folder_button")

        self.verticalLayout_30.addWidget(self.open_plandomizer_folder_button)

        self.plandomizer_vspacer = QSpacerItem(20, 369, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_30.addItem(self.plandomizer_vspacer)


        self.horizontalLayout_4.addWidget(self.plandomizer_group_box)

        self.random_settings_group_box = QGroupBox(self.advanced_tab)
        self.random_settings_group_box.setObjectName(u"random_settings_group_box")
        sizePolicy.setHeightForWidth(self.random_settings_group_box.sizePolicy().hasHeightForWidth())
        self.random_settings_group_box.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.random_settings_group_box)

        self.other_settings_group_box = QGroupBox(self.advanced_tab)
        self.other_settings_group_box.setObjectName(u"other_settings_group_box")
        sizePolicy.setHeightForWidth(self.other_settings_group_box.sizePolicy().hasHeightForWidth())
        self.other_settings_group_box.setSizePolicy(sizePolicy)
        self.verticalLayout_32 = QVBoxLayout(self.other_settings_group_box)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.setting_enable_back_in_time = RandoTriStateCheckBox(self.other_settings_group_box)
        self.setting_enable_back_in_time.setObjectName(u"setting_enable_back_in_time")

        self.verticalLayout_32.addWidget(self.setting_enable_back_in_time)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_32.addItem(self.verticalSpacer)


        self.horizontalLayout_4.addWidget(self.other_settings_group_box)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 1)
        self.horizontalLayout_4.setStretch(2, 1)
        self.horizontalLayout_4.setStretch(3, 1)
        self.tab_widget.addTab(self.advanced_tab, "")
        self.tracker_tab = QWidget()
        self.tracker_tab.setObjectName(u"tracker_tab")
        self.tracker_tab.setStyleSheet(u"background: black;\n"
"\n"
"QPushButton {\n"
"  background: gray;\n"
"}")
        self.gridLayout = QGridLayout(self.tracker_tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(3)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.inventory_layout = QVBoxLayout()
        self.inventory_layout.setObjectName(u"inventory_layout")
        self.dungeon_inventory_layout = QHBoxLayout()
        self.dungeon_inventory_layout.setSpacing(2)
        self.dungeon_inventory_layout.setObjectName(u"dungeon_inventory_layout")
        self.dungeon_sv_layout = QVBoxLayout()
        self.dungeon_sv_layout.setSpacing(1)
        self.dungeon_sv_layout.setObjectName(u"dungeon_sv_layout")
        self.dungeon_sv_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.dungeon_sv_keys_layout = QHBoxLayout()
        self.dungeon_sv_keys_layout.setSpacing(1)
        self.dungeon_sv_keys_layout.setObjectName(u"dungeon_sv_keys_layout")
        self.dungeon_sv_keys_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)

        self.dungeon_sv_layout.addLayout(self.dungeon_sv_keys_layout)


        self.dungeon_inventory_layout.addLayout(self.dungeon_sv_layout)

        self.dungeon_et_layout = QVBoxLayout()
        self.dungeon_et_layout.setSpacing(1)
        self.dungeon_et_layout.setObjectName(u"dungeon_et_layout")
        self.dungeon_et_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.dungeon_et_keys_layout = QHBoxLayout()
        self.dungeon_et_keys_layout.setSpacing(1)
        self.dungeon_et_keys_layout.setObjectName(u"dungeon_et_keys_layout")

        self.dungeon_et_layout.addLayout(self.dungeon_et_keys_layout)


        self.dungeon_inventory_layout.addLayout(self.dungeon_et_layout)

        self.dungeon_lmf_layout = QVBoxLayout()
        self.dungeon_lmf_layout.setSpacing(1)
        self.dungeon_lmf_layout.setObjectName(u"dungeon_lmf_layout")
        self.dungeon_lmf_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.dungeon_lmf_keys_layout = QHBoxLayout()
        self.dungeon_lmf_keys_layout.setSpacing(1)
        self.dungeon_lmf_keys_layout.setObjectName(u"dungeon_lmf_keys_layout")

        self.dungeon_lmf_layout.addLayout(self.dungeon_lmf_keys_layout)


        self.dungeon_inventory_layout.addLayout(self.dungeon_lmf_layout)

        self.dungeon_ac_layout = QVBoxLayout()
        self.dungeon_ac_layout.setSpacing(1)
        self.dungeon_ac_layout.setObjectName(u"dungeon_ac_layout")
        self.dungeon_ac_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.dungeon_ac_keys_layout = QHBoxLayout()
        self.dungeon_ac_keys_layout.setSpacing(1)
        self.dungeon_ac_keys_layout.setObjectName(u"dungeon_ac_keys_layout")

        self.dungeon_ac_layout.addLayout(self.dungeon_ac_keys_layout)


        self.dungeon_inventory_layout.addLayout(self.dungeon_ac_layout)

        self.dungeon_ssh_layout = QVBoxLayout()
        self.dungeon_ssh_layout.setSpacing(1)
        self.dungeon_ssh_layout.setObjectName(u"dungeon_ssh_layout")
        self.dungeon_ssh_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.dungeon_ssh_keys_layout = QHBoxLayout()
        self.dungeon_ssh_keys_layout.setSpacing(1)
        self.dungeon_ssh_keys_layout.setObjectName(u"dungeon_ssh_keys_layout")

        self.dungeon_ssh_layout.addLayout(self.dungeon_ssh_keys_layout)


        self.dungeon_inventory_layout.addLayout(self.dungeon_ssh_layout)

        self.dungeon_fs_layout = QVBoxLayout()
        self.dungeon_fs_layout.setSpacing(1)
        self.dungeon_fs_layout.setObjectName(u"dungeon_fs_layout")
        self.dungeon_fs_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.dungeon_fs_keys_layout = QHBoxLayout()
        self.dungeon_fs_keys_layout.setSpacing(1)
        self.dungeon_fs_keys_layout.setObjectName(u"dungeon_fs_keys_layout")

        self.dungeon_fs_layout.addLayout(self.dungeon_fs_keys_layout)


        self.dungeon_inventory_layout.addLayout(self.dungeon_fs_layout)

        self.dungeon_sk_layout = QVBoxLayout()
        self.dungeon_sk_layout.setSpacing(1)
        self.dungeon_sk_layout.setObjectName(u"dungeon_sk_layout")
        self.dungeon_sk_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.dungeon_sk_keys_layout = QHBoxLayout()
        self.dungeon_sk_keys_layout.setSpacing(1)
        self.dungeon_sk_keys_layout.setObjectName(u"dungeon_sk_keys_layout")
        self.dungeon_sk_keys_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)

        self.dungeon_sk_layout.addLayout(self.dungeon_sk_keys_layout)


        self.dungeon_inventory_layout.addLayout(self.dungeon_sk_layout)


        self.inventory_layout.addLayout(self.dungeon_inventory_layout)

        self.middle_inventory_layout = QGridLayout()
        self.middle_inventory_layout.setObjectName(u"middle_inventory_layout")
        self.inventory_b_wheel_layout = QGridLayout()
        self.inventory_b_wheel_layout.setSpacing(1)
        self.inventory_b_wheel_layout.setObjectName(u"inventory_b_wheel_layout")

        self.middle_inventory_layout.addLayout(self.inventory_b_wheel_layout, 0, 1, 1, 1)

        self.inventory_sword_layout = QVBoxLayout()
        self.inventory_sword_layout.setObjectName(u"inventory_sword_layout")

        self.middle_inventory_layout.addLayout(self.inventory_sword_layout, 0, 0, 1, 1)

        self.inventory_tablet_layout = QVBoxLayout()
        self.inventory_tablet_layout.setObjectName(u"inventory_tablet_layout")

        self.middle_inventory_layout.addLayout(self.inventory_tablet_layout, 0, 2, 1, 1)

        self.middle_inventory_layout.setColumnStretch(0, 2)
        self.middle_inventory_layout.setColumnStretch(1, 10)
        self.middle_inventory_layout.setColumnStretch(2, 4)

        self.inventory_layout.addLayout(self.middle_inventory_layout)

        self.lower_inventory_layout = QGridLayout()
        self.lower_inventory_layout.setSpacing(1)
        self.lower_inventory_layout.setObjectName(u"lower_inventory_layout")

        self.inventory_layout.addLayout(self.lower_inventory_layout)

        self.inventory_layout.setStretch(0, 1)
        self.inventory_layout.setStretch(1, 3)
        self.inventory_layout.setStretch(2, 3)

        self.gridLayout.addLayout(self.inventory_layout, 0, 0, 1, 1)

        self.tracker_info_layout = QVBoxLayout()
        self.tracker_info_layout.setObjectName(u"tracker_info_layout")
        self.tracker_info_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.tracker_info_top_half_layout = QVBoxLayout()
        self.tracker_info_top_half_layout.setObjectName(u"tracker_info_top_half_layout")
        self.tracker_statistics_grid = QGridLayout()
        self.tracker_statistics_grid.setObjectName(u"tracker_statistics_grid")
        self.tracker_statistics_grid.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.tracker_stats_remaining_label = QLabel(self.tracker_tab)
        self.tracker_stats_remaining_label.setObjectName(u"tracker_stats_remaining_label")

        self.tracker_statistics_grid.addWidget(self.tracker_stats_remaining_label, 2, 1, 1, 1)

        self.tracker_stats_remaining = QLabel(self.tracker_tab)
        self.tracker_stats_remaining.setObjectName(u"tracker_stats_remaining")
        sizePolicy2.setHeightForWidth(self.tracker_stats_remaining.sizePolicy().hasHeightForWidth())
        self.tracker_stats_remaining.setSizePolicy(sizePolicy2)
        self.tracker_stats_remaining.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.tracker_statistics_grid.addWidget(self.tracker_stats_remaining, 2, 0, 1, 1)

        self.tracker_stats_checked = QLabel(self.tracker_tab)
        self.tracker_stats_checked.setObjectName(u"tracker_stats_checked")
        sizePolicy2.setHeightForWidth(self.tracker_stats_checked.sizePolicy().hasHeightForWidth())
        self.tracker_stats_checked.setSizePolicy(sizePolicy2)
        self.tracker_stats_checked.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.tracker_statistics_grid.addWidget(self.tracker_stats_checked, 0, 0, 1, 1)

        self.tracker_stats_accessible = QLabel(self.tracker_tab)
        self.tracker_stats_accessible.setObjectName(u"tracker_stats_accessible")
        sizePolicy2.setHeightForWidth(self.tracker_stats_accessible.sizePolicy().hasHeightForWidth())
        self.tracker_stats_accessible.setSizePolicy(sizePolicy2)
        self.tracker_stats_accessible.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.tracker_statistics_grid.addWidget(self.tracker_stats_accessible, 1, 0, 1, 1)

        self.tracker_stats_accessible_label = QLabel(self.tracker_tab)
        self.tracker_stats_accessible_label.setObjectName(u"tracker_stats_accessible_label")
        sizePolicy12 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.tracker_stats_accessible_label.sizePolicy().hasHeightForWidth())
        self.tracker_stats_accessible_label.setSizePolicy(sizePolicy12)

        self.tracker_statistics_grid.addWidget(self.tracker_stats_accessible_label, 1, 1, 1, 1)

        self.tracker_stats_checked_label = QLabel(self.tracker_tab)
        self.tracker_stats_checked_label.setObjectName(u"tracker_stats_checked_label")

        self.tracker_statistics_grid.addWidget(self.tracker_stats_checked_label, 0, 1, 1, 1)

        self.tracker_statistics_grid.setColumnStretch(0, 4)
        self.tracker_statistics_grid.setColumnStretch(1, 50)

        self.tracker_info_top_half_layout.addLayout(self.tracker_statistics_grid)

        self.start_new_tracker_button = QPushButton(self.tracker_tab)
        self.start_new_tracker_button.setObjectName(u"start_new_tracker_button")
        sizePolicy13 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.start_new_tracker_button.sizePolicy().hasHeightForWidth())
        self.start_new_tracker_button.setSizePolicy(sizePolicy13)

        self.tracker_info_top_half_layout.addWidget(self.start_new_tracker_button)

        self.set_random_settings_button = QPushButton(self.tracker_tab)
        self.set_random_settings_button.setObjectName(u"set_random_settings_button")
        sizePolicy13.setHeightForWidth(self.set_random_settings_button.sizePolicy().hasHeightForWidth())
        self.set_random_settings_button.setSizePolicy(sizePolicy13)

        self.tracker_info_top_half_layout.addWidget(self.set_random_settings_button)

        self.set_starting_entrance_button = QPushButton(self.tracker_tab)
        self.set_starting_entrance_button.setObjectName(u"set_starting_entrance_button")
        sizePolicy13.setHeightForWidth(self.set_starting_entrance_button.sizePolicy().hasHeightForWidth())
        self.set_starting_entrance_button.setSizePolicy(sizePolicy13)

        self.tracker_info_top_half_layout.addWidget(self.set_starting_entrance_button)

        self.check_all_button = QPushButton(self.tracker_tab)
        self.check_all_button.setObjectName(u"check_all_button")

        self.tracker_info_top_half_layout.addWidget(self.check_all_button)

        self.check_all_in_logic_button = QPushButton(self.tracker_tab)
        self.check_all_in_logic_button.setObjectName(u"check_all_in_logic_button")

        self.tracker_info_top_half_layout.addWidget(self.check_all_in_logic_button)

        self.uncheck_all_button = QPushButton(self.tracker_tab)
        self.uncheck_all_button.setObjectName(u"uncheck_all_button")

        self.tracker_info_top_half_layout.addWidget(self.uncheck_all_button)

        self.set_hints_button = QPushButton(self.tracker_tab)
        self.set_hints_button.setObjectName(u"set_hints_button")

        self.tracker_info_top_half_layout.addWidget(self.set_hints_button)

        self.toggle_sphere_tracking_button = TrackerToggleSTButton(self.tracker_tab)
        self.toggle_sphere_tracking_button.setObjectName(u"toggle_sphere_tracking_button")

        self.tracker_info_top_half_layout.addWidget(self.toggle_sphere_tracking_button)

        self.tracker_sphere_tracking_label = QLabel(self.tracker_tab)
        self.tracker_sphere_tracking_label.setObjectName(u"tracker_sphere_tracking_label")

        self.tracker_info_top_half_layout.addWidget(self.tracker_sphere_tracking_label)

        self.cancel_sphere_tracking_button = QPushButton(self.tracker_tab)
        self.cancel_sphere_tracking_button.setObjectName(u"cancel_sphere_tracking_button")

        self.tracker_info_top_half_layout.addWidget(self.cancel_sphere_tracking_button)

        self.tracker_info_layout_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.tracker_info_top_half_layout.addItem(self.tracker_info_layout_spacer)


        self.tracker_info_layout.addLayout(self.tracker_info_top_half_layout)

        self.tracker_info_bottom_half = QVBoxLayout()
        self.tracker_info_bottom_half.setObjectName(u"tracker_info_bottom_half")
        self.tracker_notes_label = QLabel(self.tracker_tab)
        self.tracker_notes_label.setObjectName(u"tracker_notes_label")

        self.tracker_info_bottom_half.addWidget(self.tracker_notes_label)

        self.tracker_notes_textedit = QTextEdit(self.tracker_tab)
        self.tracker_notes_textedit.setObjectName(u"tracker_notes_textedit")

        self.tracker_info_bottom_half.addWidget(self.tracker_notes_textedit)


        self.tracker_info_layout.addLayout(self.tracker_info_bottom_half)

        self.tracker_info_layout.setStretch(0, 55)
        self.tracker_info_layout.setStretch(1, 45)

        self.gridLayout.addLayout(self.tracker_info_layout, 0, 2, 1, 1)

        self.tracker_map_layout = QVBoxLayout()
        self.tracker_map_layout.setObjectName(u"tracker_map_layout")
        self.map_widget = QWidget(self.tracker_tab)
        self.map_widget.setObjectName(u"map_widget")
        sizePolicy14 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.map_widget.sizePolicy().hasHeightForWidth())
        self.map_widget.setSizePolicy(sizePolicy14)
        self.map_widget.setMinimumSize(QSize(546, 300))

        self.tracker_map_layout.addWidget(self.map_widget)

        self.tracker_locations_info_layout = QHBoxLayout()
        self.tracker_locations_info_layout.setObjectName(u"tracker_locations_info_layout")

        self.tracker_map_layout.addLayout(self.tracker_locations_info_layout)

        self.tracker_locations_scroll_area = QScrollArea(self.tracker_tab)
        self.tracker_locations_scroll_area.setObjectName(u"tracker_locations_scroll_area")
        sizePolicy15 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        sizePolicy15.setHorizontalStretch(0)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.tracker_locations_scroll_area.sizePolicy().hasHeightForWidth())
        self.tracker_locations_scroll_area.setSizePolicy(sizePolicy15)
        self.tracker_locations_scroll_area.setMaximumSize(QSize(546, 16777215))
        self.tracker_locations_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.tracker_locations_scroll_area.setLineWidth(0)
        self.tracker_locations_scroll_area.setWidgetResizable(True)
        self.tracker_locations_scroll_widget = QWidget()
        self.tracker_locations_scroll_widget.setObjectName(u"tracker_locations_scroll_widget")
        self.tracker_locations_scroll_widget.setGeometry(QRect(0, 0, 100, 30))
        self.tracker_locations_scroll_widget.setMaximumSize(QSize(546, 16777215))
        self.tracker_locations_scroll_layout = QHBoxLayout(self.tracker_locations_scroll_widget)
        self.tracker_locations_scroll_layout.setSpacing(0)
        self.tracker_locations_scroll_layout.setObjectName(u"tracker_locations_scroll_layout")
        self.tracker_locations_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.tracker_locations_scroll_area.setWidget(self.tracker_locations_scroll_widget)

        self.tracker_map_layout.addWidget(self.tracker_locations_scroll_area)


        self.gridLayout.addLayout(self.tracker_map_layout, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.tab_widget.addTab(self.tracker_tab, "")

        self.verticalLayout_2.addWidget(self.tab_widget)

        self.settings_descriptions_layout = QHBoxLayout()
        self.settings_descriptions_layout.setObjectName(u"settings_descriptions_layout")
        self.settings_current_option_description_label = QLabel(self.central_widget)
        self.settings_current_option_description_label.setObjectName(u"settings_current_option_description_label")
        sizePolicy16 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy16.setHorizontalStretch(0)
        sizePolicy16.setVerticalStretch(0)
        sizePolicy16.setHeightForWidth(self.settings_current_option_description_label.sizePolicy().hasHeightForWidth())
        self.settings_current_option_description_label.setSizePolicy(sizePolicy16)
        self.settings_current_option_description_label.setMinimumSize(QSize(0, 64))
        self.settings_current_option_description_label.setTextFormat(Qt.TextFormat.RichText)
        self.settings_current_option_description_label.setWordWrap(True)

        self.settings_descriptions_layout.addWidget(self.settings_current_option_description_label)

        self.settings_default_option_description_label = QLabel(self.central_widget)
        self.settings_default_option_description_label.setObjectName(u"settings_default_option_description_label")
        sizePolicy16.setHeightForWidth(self.settings_default_option_description_label.sizePolicy().hasHeightForWidth())
        self.settings_default_option_description_label.setSizePolicy(sizePolicy16)
        self.settings_default_option_description_label.setMinimumSize(QSize(0, 64))
        self.settings_default_option_description_label.setWordWrap(True)

        self.settings_descriptions_layout.addWidget(self.settings_default_option_description_label)


        self.verticalLayout_2.addLayout(self.settings_descriptions_layout)

        self.footer_grid_layout = QGridLayout()
        self.footer_grid_layout.setObjectName(u"footer_grid_layout")
        self.setting_string_label = QLabel(self.central_widget)
        self.setting_string_label.setObjectName(u"setting_string_label")

        self.footer_grid_layout.addWidget(self.setting_string_label, 0, 0, 1, 1)

        self.about_button = QPushButton(self.central_widget)
        self.about_button.setObjectName(u"about_button")

        self.footer_grid_layout.addWidget(self.about_button, 2, 0, 1, 1)

        self.new_seed_button = QPushButton(self.central_widget)
        self.new_seed_button.setObjectName(u"new_seed_button")

        self.footer_grid_layout.addWidget(self.new_seed_button, 1, 2, 1, 1)

        self.copy_setting_string_button = QPushButton(self.central_widget)
        self.copy_setting_string_button.setObjectName(u"copy_setting_string_button")

        self.footer_grid_layout.addWidget(self.copy_setting_string_button, 0, 2, 1, 1)

        self.reset_settings_to_default_hlayout = QHBoxLayout()
        self.reset_settings_to_default_hlayout.setObjectName(u"reset_settings_to_default_hlayout")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.layout_label = QLabel(self.central_widget)
        self.layout_label.setObjectName(u"layout_label")

        self.horizontalLayout_7.addWidget(self.layout_label)

        self.reset_settings_to_default_button = QPushButton(self.central_widget)
        self.reset_settings_to_default_button.setObjectName(u"reset_settings_to_default_button")
        sizePolicy6.setHeightForWidth(self.reset_settings_to_default_button.sizePolicy().hasHeightForWidth())
        self.reset_settings_to_default_button.setSizePolicy(sizePolicy6)

        self.horizontalLayout_7.addWidget(self.reset_settings_to_default_button)

        self.hash_label = QLabel(self.central_widget)
        self.hash_label.setObjectName(u"hash_label")
        self.hash_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.hash_label)


        self.reset_settings_to_default_hlayout.addLayout(self.horizontalLayout_7)


        self.footer_grid_layout.addLayout(self.reset_settings_to_default_hlayout, 2, 1, 1, 1)

        self.seed_line_edit = QLineEdit(self.central_widget)
        self.seed_line_edit.setObjectName(u"seed_line_edit")

        self.footer_grid_layout.addWidget(self.seed_line_edit, 1, 1, 1, 1)

        self.setting_string_layout = QHBoxLayout()
        self.setting_string_layout.setObjectName(u"setting_string_layout")
        self.setting_string_line_edit = QLineEdit(self.central_widget)
        self.setting_string_line_edit.setObjectName(u"setting_string_line_edit")
        sizePolicy7.setHeightForWidth(self.setting_string_line_edit.sizePolicy().hasHeightForWidth())
        self.setting_string_line_edit.setSizePolicy(sizePolicy7)
        self.setting_string_line_edit.setReadOnly(True)

        self.setting_string_layout.addWidget(self.setting_string_line_edit)

        self.paste_setting_string_button = QPushButton(self.central_widget)
        self.paste_setting_string_button.setObjectName(u"paste_setting_string_button")
        self.paste_setting_string_button.setEnabled(True)
        sizePolicy14.setHeightForWidth(self.paste_setting_string_button.sizePolicy().hasHeightForWidth())
        self.paste_setting_string_button.setSizePolicy(sizePolicy14)
        self.paste_setting_string_button.setMinimumSize(QSize(80, 0))

        self.setting_string_layout.addWidget(self.paste_setting_string_button)


        self.footer_grid_layout.addLayout(self.setting_string_layout, 0, 1, 1, 1)

        self.seed_label = QLabel(self.central_widget)
        self.seed_label.setObjectName(u"seed_label")

        self.footer_grid_layout.addWidget(self.seed_label, 1, 0, 1, 1)

        self.randomize_button = QPushButton(self.central_widget)
        self.randomize_button.setObjectName(u"randomize_button")
        sizePolicy13.setHeightForWidth(self.randomize_button.sizePolicy().hasHeightForWidth())
        self.randomize_button.setSizePolicy(sizePolicy13)

        self.footer_grid_layout.addWidget(self.randomize_button, 2, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.footer_grid_layout)

        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)

        self.tab_widget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"The Legend of Zelda: Skyward Sword HD Randomizer", None))
        self.how_to_group_box.setTitle(QCoreApplication.translate("main_window", u"How to Randomize the Game", None))
        self.how_to_extract_group_box.setTitle(QCoreApplication.translate("main_window", u"Extract the Game", None))
        self.how_to_extract_label.setText(QCoreApplication.translate("main_window", u"<html><head/><body><p>Before generating a seed, you need to have a valid extract of the vanilla version of the game.</p><p>Please follow our handy setup guides for the <a href=\"https://docs.google.com/document/d/1VXNME7SVD5EU7NNn9dQ15_Q9-v9OJAHOX-hSor0n2dg\"><span style=\" text-decoration: underline; color:#9a0089;\">Nintendo Switch console</span></a> or for <a href=\"https://docs.google.com/document/d/1HHQRXND0n-ZrmhEl4eXjzMANQ-xHK3pKKXPQqSbwXwY\"><span style=\" text-decoration: underline; color:#9a0089;\">emulator</span></a>.</p><p>For additional help with this process, please join the <a href=\"https://discord.gg/nNbpfH5jyG\"><span style=\" text-decoration: underline; color:#9a0089;\">Discord Server</span></a> or ask on <a href=\"https://github.com/mint-choc-chip-skyblade/sshd-rando/issues\"><span style=\" text-decoration: underline; color:#9a0089;\">GitHub</span></a>.</p></body></html>", None))
        self.how_to_left_arrow_label.setText(QCoreApplication.translate("main_window", u"\u279c", None))
        self.useful_choose_settings_group_box.setTitle(QCoreApplication.translate("main_window", u"Choosing your Settings", None))
        self.choose_settings_label.setText(QCoreApplication.translate("main_window", u"<html><head/><body><p><span style=\" font-weight:700;\">Quick start: </span>You can select one of the settings presets below to jump straight in!</p><p>Don't worry if there's too much going on, the default settings are perfect for beginners.</p><p>Alternatively, you can customize every setting yourself. There's lots of buttons and switches, so get stuck in!</p></body></html>", None))
        self.how_to_middle_arrow_label.setText(QCoreApplication.translate("main_window", u"\u279c", None))
        self.how_to_generate_group_box.setTitle(QCoreApplication.translate("main_window", u"Generate a Seed", None))
        self.how_to_generate_label.setText(QCoreApplication.translate("main_window", u"<html><head/><body><p>Once you're ready, click the <span style=\" font-family:'Courier New';\">Randomize</span> button in the bottom right.</p><p>The program will begin to generate a game patch that will allow you to play the randomizer.</p><p>If you encounter a problem, don't hesitate to ask for help! You can join the <a href=\"https://discord.gg/nNbpfH5jyG\"><span style=\" text-decoration: underline; color:#9a0089;\">Discord Server</span></a> or ask on <a href=\"https://github.com/mint-choc-chip-skyblade/sshd-rando/issues\"><span style=\" text-decoration: underline; color:#9a0089;\">GitHub</span></a>!</p></body></html>", None))
        self.how_to_right_arrow_label.setText(QCoreApplication.translate("main_window", u"\u279c", None))
        self.how_to_running_group_box.setTitle(QCoreApplication.translate("main_window", u"Running the Seed", None))
        self.how_to_running_label.setText(QCoreApplication.translate("main_window", u"<html><head/><body><p>You can play the randomizer either on a modded Nintendo Switch console or on an emulator.</p><p>Please follow the instructions in our setup guides for <a href=\"https://docs.google.com/document/d/1VXNME7SVD5EU7NNn9dQ15_Q9-v9OJAHOX-hSor0n2dg\"><span style=\" text-decoration: underline; color:#9a0089;\">Nintendo Switch console</span></a> or for <a href=\"https://docs.google.com/document/d/1HHQRXND0n-ZrmhEl4eXjzMANQ-xHK3pKKXPQqSbwXwY\"><span style=\" text-decoration: underline; color:#9a0089;\">emulator</span></a> to find instructions on running the randomizer patch.</p></body></html>", None))
        self.useful_info_group_box.setTitle(QCoreApplication.translate("main_window", u"Useful Information", None))
        self.guides_label.setText(QCoreApplication.translate("main_window", u"<html><head/><body><p>Guides</p><p>\u279c <a href=\"https://docs.google.com/document/d/1VXNME7SVD5EU7NNn9dQ15_Q9-v9OJAHOX-hSor0n2dg\"><span style=\" text-decoration: underline; color:#9a0089;\">Setup Guide (Console)</span></a><br/>\u279c <a href=\"https://docs.google.com/document/d/1HHQRXND0n-ZrmhEl4eXjzMANQ-xHK3pKKXPQqSbwXwY\"><span style=\" text-decoration: underline; color:#9a0089;\">Setup Guide (Emulator)</span></a><br/>\u279c <a href=\"https://docs.google.com/document/d/1bb6GoCBFVREc-wHscRBTfZrftN1OA639iML2azdXqXE\"><span style=\" text-decoration: underline; color:#9a0089;\">Location Guide</span></a><br/>\u279c <a href=\"https://docs.google.com/document/d/1Dm0jhwXWIvPLuvl-JoRqocTKjXM_jRRmryYqpQMO_6w\"><span style=\" text-decoration: underline; color:#9a0089;\">Tricks Guide</span></a><br/>\u279c <a href=\"https://docs.google.com/document/d/1Eq1rXcjwRpVjp-5ugpQAsjmZy5QuGi7KAOkvpWoQkqc\"><span style=\" text-decoration: underline; color:#9a0089;\">Texture Replacement Guide</span></a></p></body></html>", None))
        self.community_label.setText(QCoreApplication.translate("main_window", u"<html><head/><body><p>Community</p><p><span style=\" font-weight:700;\">\u279c </span><a href=\"https://discord.gg/nNbpfH5jyG\"><span style=\" text-decoration: underline; color:#9a0089;\">Discord Server</span></a><br/><span style=\" font-weight:700;\">\u279c </span><a href=\"https://github.com/mint-choc-chip-skyblade/sshd-rando/issues\"><span style=\" text-decoration: underline; color:#9a0089;\">Report a Bug</span></a><br/><span style=\" font-weight:700;\">\u279c </span><a href=\"https://github.com/mint-choc-chip-skyblade/sshd-rando\"><span style=\" text-decoration: underline; color:#9a0089;\">GitHub</span></a></p></body></html>", None))
        self.accessibility_group_box.setTitle(QCoreApplication.translate("main_window", u"Accessibility", None))
        self.theming_group_box.setTitle(QCoreApplication.translate("main_window", u"Theming", None))
        self.theme_mode_label.setText(QCoreApplication.translate("main_window", u"Theme Mode:", None))
        self.theme_presets_label.setText(QCoreApplication.translate("main_window", u"Theme Presets", None))
        self.use_custom_theme_check_box.setText(QCoreApplication.translate("main_window", u"Use Custom Theme", None))
        self.customize_theme_button.setText(QCoreApplication.translate("main_window", u"Customize Theme", None))
        self.theming_fonts.setTitle(QCoreApplication.translate("main_window", u"Fonts", None))
        self.font_family_label.setText(QCoreApplication.translate("main_window", u"Font Family", None))
        self.font_family_combo_box.setPlaceholderText(QCoreApplication.translate("main_window", u"Select Font Family", None))
        self.font_size_label.setText(QCoreApplication.translate("main_window", u"Font Size", None))
        self.font_reset_button.setText(QCoreApplication.translate("main_window", u"Reset", None))
        self.presets_group_box.setTitle(QCoreApplication.translate("main_window", u"Presets", None))
        self.selected_preset_label.setText(QCoreApplication.translate("main_window", u"Selected Preset:", None))
        self.presets_delete_button.setText(QCoreApplication.translate("main_window", u"Delete", None))
        self.presets_save_new_button.setText(QCoreApplication.translate("main_window", u"Save New", None))
        self.presets_apply_button.setText(QCoreApplication.translate("main_window", u"Apply", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.getting_started_tab), QCoreApplication.translate("main_window", u"Getting Started", None))
        self.dungeons_group_box.setTitle(QCoreApplication.translate("main_window", u"Dungeon Items", None))
        self.small_keys_label.setText(QCoreApplication.translate("main_window", u"Small Keys", None))
        self.boss_keys_label.setText(QCoreApplication.translate("main_window", u"Boss Keys", None))
        self.map_mode_label.setText(QCoreApplication.translate("main_window", u"Dungeon Maps", None))
        self.lanayru_caves_keys_label.setText(QCoreApplication.translate("main_window", u"Lanayru Caves Small Key", None))
        self.boss_key_puzzles_label.setText(QCoreApplication.translate("main_window", u"Boss Key Puzzles", None))
        self.tweaks_group_box.setTitle(QCoreApplication.translate("main_window", u"Tweaks", None))
        self.setting_spawn_hearts.setText(QCoreApplication.translate("main_window", u"Spawn Hearts and Heart Flowers", None))
        self.setting_upgraded_skyward_strike.setText(QCoreApplication.translate("main_window", u"Upgraded Skyward Strike", None))
        self.setting_faster_air_meter_depletion.setText(QCoreApplication.translate("main_window", u"Faster Air Meter Depletion", None))
        self.damage_multiplier_label.setText(QCoreApplication.translate("main_window", u"Damage Multiplier", None))
        self.ammo_availability_label.setText(QCoreApplication.translate("main_window", u"Ammo Availability", None))
        self.peatrice_conversations_label.setText(QCoreApplication.translate("main_window", u"Peatrice Conversations", None))
        self.setting_random_bottle_contents.setText(QCoreApplication.translate("main_window", u"Random Bottle Contents", None))
        self.setting_full_wallet_upgrades.setText(QCoreApplication.translate("main_window", u"Full Wallet Upgrades", None))
        self.setting_skip_harp_playing.setText(QCoreApplication.translate("main_window", u"Skip Harp Playing", None))
        self.random_trial_object_positions_label.setText(QCoreApplication.translate("main_window", u"Random Trial Object Positions", None))
        self.beat_the_game_group_box.setTitle(QCoreApplication.translate("main_window", u"Beat the Game", None))
        self.got_sword_requirement_label.setText(QCoreApplication.translate("main_window", u"Gate of Time Sword Requirement", None))
        self.required_dungeons_label.setText(QCoreApplication.translate("main_window", u"Required Dungeons", None))
        self.setting_dungeons_include_sky_keep.setText(QCoreApplication.translate("main_window", u"Include Sky Keep as a Dungeon", None))
        self.setting_empty_unrequired_dungeons.setText(QCoreApplication.translate("main_window", u"Barren Unrequired Dungeons", None))
        self.setting_skip_horde.setText(QCoreApplication.translate("main_window", u"Skip The Horde Fight", None))
        self.setting_skip_g3.setText(QCoreApplication.translate("main_window", u"Skip Ghirahim 3 Fight", None))
        self.setting_skip_demise.setText(QCoreApplication.translate("main_window", u"Skip Demise Fight", None))
        self.hint_placements_group_box.setTitle(QCoreApplication.translate("main_window", u"Traps", None))
        self.trap_mode_label.setText(QCoreApplication.translate("main_window", u"Trap Mode", None))
        self.trappable_items_label.setText(QCoreApplication.translate("main_window", u"Trappable Items", None))
        self.setting_burn_traps.setText(QCoreApplication.translate("main_window", u"Burn Traps", None))
        self.setting_curse_traps.setText(QCoreApplication.translate("main_window", u"Curse Traps", None))
        self.setting_noise_traps.setText(QCoreApplication.translate("main_window", u"Noise Traps", None))
        self.setting_health_traps.setText(QCoreApplication.translate("main_window", u"Health Traps", None))
        self.setting_groose_traps.setText(QCoreApplication.translate("main_window", u"Groose Traps", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.gameplay_tab), QCoreApplication.translate("main_window", u"Gameplay", None))
        self.open_world_group_box.setTitle(QCoreApplication.translate("main_window", u"Open World", None))
        self.setting_unlock_all_groosenator_destinations.setText(QCoreApplication.translate("main_window", u"Unlock all Groosenator Destinations", None))
        self.setting_open_thunderhead.setText(QCoreApplication.translate("main_window", u"Open Thunderhead", None))
        self.open_lake_floria_label.setText(QCoreApplication.translate("main_window", u"Open Lake Floria", None))
        self.setting_open_batreaux_shed.setText(QCoreApplication.translate("main_window", u"Open Batreaux's Shed", None))
        self.setting_shortcut_ios_bridge_complete.setText(QCoreApplication.translate("main_window", u"Isle of Songs Bridge Complete", None))
        self.setting_shortcut_spiral_log_to_btt.setText(QCoreApplication.translate("main_window", u"Sealed Spiral Log to Behind the Temple", None))
        self.setting_shortcut_logs_near_machi.setText(QCoreApplication.translate("main_window", u"Faron Woods Logs near Entry Bird Statue", None))
        self.setting_shortcut_faron_log_to_floria.setText(QCoreApplication.translate("main_window", u"Faron Woods Log to after Lake Floria", None))
        self.setting_shortcut_deep_woods_log_before_tightrope.setText(QCoreApplication.translate("main_window", u"Deep Woods Log before Tightrope", None))
        self.setting_shortcut_deep_woods_log_before_temple.setText(QCoreApplication.translate("main_window", u"Deep Woods Log before Temple", None))
        self.setting_shortcut_eldin_entrance_boulder.setText(QCoreApplication.translate("main_window", u"Eldin Volcano Entrance Boulder", None))
        self.setting_shortcut_eldin_ascent_boulder.setText(QCoreApplication.translate("main_window", u"Eldin Volcano Boulder near Ascent", None))
        self.setting_shortcut_vs_flames.setText(QCoreApplication.translate("main_window", u"Volcano Summit Flames", None))
        self.setting_shortcut_lanayru_bars.setText(QCoreApplication.translate("main_window", u"Lanayru Desert Bars near Stone Cache", None))
        self.setting_shortcut_west_wall_minecart.setText(QCoreApplication.translate("main_window", u"Lanayru Desert Minecart on West Wall", None))
        self.setting_shortcut_sand_oasis_minecart.setText(QCoreApplication.translate("main_window", u"Lanayru Desert Minecart in Sand Oasis", None))
        self.setting_shortcut_minecart_before_caves.setText(QCoreApplication.translate("main_window", u"Lanayru Desert Minecart before Lanayru Caves", None))
        self.open_dungeons_group_box.setTitle(QCoreApplication.translate("main_window", u"Open Dungeons", None))
        self.setting_open_earth_temple.setText(QCoreApplication.translate("main_window", u"Open Earth Temple", None))
        self.open_lmf_label.setText(QCoreApplication.translate("main_window", u"Open Lanyru Mining Facility", None))
        self.setting_shortcut_skyview_boards.setText(QCoreApplication.translate("main_window", u"Skyview Temple Boarded Shortcut", None))
        self.setting_shortcut_skyview_bars.setText(QCoreApplication.translate("main_window", u"Skyview Temple Bars before Boss Door", None))
        self.setting_shortcut_earth_temple_bridge.setText(QCoreApplication.translate("main_window", u"Earth Temple Pegs Bridge", None))
        self.setting_shortcut_lmf_wind_gates.setText(QCoreApplication.translate("main_window", u"Lanayru Mining Facility Wind Gates in Hub Room", None))
        self.setting_shortcut_lmf_boxes.setText(QCoreApplication.translate("main_window", u"Lanayru Mining Facility Pushable Boxes", None))
        self.setting_shortcut_lmf_bars_to_west_side.setText(QCoreApplication.translate("main_window", u"Lanayru Mining Facility Bars to West Side", None))
        self.setting_shortcut_ac_bridge.setText(QCoreApplication.translate("main_window", u"Ancient Cistern Bridge to Basement", None))
        self.setting_shortcut_ac_water_vents.setText(QCoreApplication.translate("main_window", u"Ancient Cistern Water Vents", None))
        self.setting_shortcut_sandship_windows.setText(QCoreApplication.translate("main_window", u"Sandship Windows below Life Boat", None))
        self.setting_shortcut_sandship_brig_bars.setText(QCoreApplication.translate("main_window", u"Sandship Bars before Brig", None))
        self.setting_shortcut_fs_outside_bars.setText(QCoreApplication.translate("main_window", u"Fire Sanctuary Bars between Outdoor Bridges", None))
        self.setting_shortcut_fs_lava_flow.setText(QCoreApplication.translate("main_window", u"Fire Sanctuary Skip Lava Chase", None))
        self.setting_shortcut_sky_keep_sv_room_bars.setText(QCoreApplication.translate("main_window", u"Sky Keep Bars in Skyview Room", None))
        self.entrance_randomization_group_box.setTitle(QCoreApplication.translate("main_window", u"Entrance Randomization", None))
        self.setting_randomize_door_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Door Entrances", None))
        self.setting_randomize_interior_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Interior Entrances", None))
        self.setting_randomize_overworld_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Overworld Entrances", None))
        self.setting_randomize_dungeon_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Dungeon Entrances", None))
        self.setting_randomize_trial_gate_entrances.setText(QCoreApplication.translate("main_window", u"Randomize Trial Gate Entrances", None))
        self.random_starting_spawn_label.setText(QCoreApplication.translate("main_window", u"Randomize Starting Spawn", None))
        self.setting_limit_starting_spawn.setText(QCoreApplication.translate("main_window", u"Limit Starting Spawn", None))
        self.setting_random_starting_statues.setText(QCoreApplication.translate("main_window", u"Random Starting Statues", None))
        self.setting_decouple_double_doors.setText(QCoreApplication.translate("main_window", u"Decouple Double Door Entrances", None))
        self.setting_decouple_entrances.setText(QCoreApplication.translate("main_window", u"Decouple Entrances", None))
        self.mixed_entrance_pools_group_box.setTitle(QCoreApplication.translate("main_window", u"Mixed Entrance Pools", None))
        self.mixed_entrance_pools_list_label.setText(QCoreApplication.translate("main_window", u"<html><head/><body><p><span style=\" font-weight:700;\">Defined Entrance Pools:</span><br/><br/>Pool 1: [] <br/>Pool 2: [] <br/>Pool 3: []</p></body></html>", None))
        self.highlighted_entrance_pool_label.setText(QCoreApplication.translate("main_window", u"Highlighted Entrance Pool:", None))
        self.selected_entrance_type_label.setText(QCoreApplication.translate("main_window", u"Selected Entrance Type:", None))
        self.add_entrance_type_button.setText(QCoreApplication.translate("main_window", u"Add Entrance Type", None))
        self.remove_entrance_type_button.setText(QCoreApplication.translate("main_window", u"Remove Entrance Type", None))
        self.mixed_entrance_pools_reset_button.setText(QCoreApplication.translate("main_window", u"Reset", None))
        self.mixed_entrance_pools_explainer_label.setText(QCoreApplication.translate("main_window", u"<html><head/><body><p><span style=\" font-weight:700;\">What are Mixed Entrance Pools?</span><br/><br/>Mixed entrance pools define how entrance types are shuffled together. By default, turning on an entrance randomizer setting will only shuffle the entrances of that type with each other. For example, randomizing dungeon entrances will only shuffle the dungeon entrances with each other. The Sandship entrance could <span style=\" font-style:italic;\">not</span> be shuffled to Wryna's House door or a trial gate entrance. <br/><br/>By defining mixed entrance pools, different entrance types can be shuffled together. For example, if a mixed pool was defined as this: [Dungeon, Door, Trial Gate], the Sandship entrance <span style=\" font-style:italic;\">could</span> be shuffled to Wryna's House door or a trial gate entrance.</p></body></html>", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.world_tab), QCoreApplication.translate("main_window", u"World", None))
        self.include_location_button.setText(QCoreApplication.translate("main_window", u"Include\n"
"<---", None))
        self.exclude_location_button.setText(QCoreApplication.translate("main_window", u"Exclude\n"
"--->", None))
        self.locations_reset_button.setText(QCoreApplication.translate("main_window", u"Reset", None))
        self.shuffles_group_box.setTitle(QCoreApplication.translate("main_window", u"Shuffles", None))
        self.beedle_shop_shuffle_label.setText(QCoreApplication.translate("main_window", u"Beedle's Airshop Shuffle", None))
        self.rupee_shuffle_label.setText(QCoreApplication.translate("main_window", u"Rupee Shuffle", None))
        self.setting_underground_rupee_shuffle.setText(QCoreApplication.translate("main_window", u"Underground Rupee Shuffle", None))
        self.setting_goddess_chest_shuffle.setText(QCoreApplication.translate("main_window", u"Goddess Chest Shuffle", None))
        self.setting_gratitude_crystal_shuffle.setText(QCoreApplication.translate("main_window", u"Gratitude Crystals Shuffle", None))
        self.setting_stamina_fruit_shuffle.setText(QCoreApplication.translate("main_window", u"Stamina Fruit Shuffle", None))
        self.setting_hidden_item_shuffle.setText(QCoreApplication.translate("main_window", u"Hidden Item Shuffle", None))
        self.setting_tadtone_shuffle.setText(QCoreApplication.translate("main_window", u"Tadtone Shuffle", None))
        self.npc_closet_shuffle_label.setText(QCoreApplication.translate("main_window", u"NPC Closets", None))
        self.trial_treasure_shuffle_label.setText(QCoreApplication.translate("main_window", u"Trial Treasure Shuffle", None))
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
        self.starting_hearts_label.setText(QCoreApplication.translate("main_window", u"Starting Hearts", None))
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
        self.chest_size_matches_contents_label.setText(QCoreApplication.translate("main_window", u"Chest Type Matches Contents (CTMC)", None))
        self.setting_small_keys_in_fancy_chests.setText(QCoreApplication.translate("main_window", u"Small Keys in Fancy Chests", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.hints_tab), QCoreApplication.translate("main_window", u"Hints", None))
        self.logic_rules_group_box.setTitle(QCoreApplication.translate("main_window", u"Logic", None))
        self.logic_rules_label.setText(QCoreApplication.translate("main_window", u"Logic Mode", None))
        self.tricks_group_box.setTitle(QCoreApplication.translate("main_window", u"Tricks", None))
        self.precise_items_group_box.setTitle(QCoreApplication.translate("main_window", u"Precise Items", None))
        self.setting_logic_advanced_lizalfos_combat.setText(QCoreApplication.translate("main_window", u"Advanced Lizalfos Combat", None))
        self.setting_logic_long_ranged_skyward_strikes.setText(QCoreApplication.translate("main_window", u"Long Range Skyward Strikes", None))
        self.setting_logic_skyview_precise_slingshot.setText(QCoreApplication.translate("main_window", u"Skyview Temple Precise Slingshot", None))
        self.setting_logic_lmf_ceiling_precise_slingshot.setText(QCoreApplication.translate("main_window", u"Lanayru Mining Facility Precise Slingshot", None))
        self.setting_logic_tot_slingshot.setText(QCoreApplication.translate("main_window", u"Temple of Time Precise Slingshot", None))
        self.setting_logic_bomb_throws.setText(QCoreApplication.translate("main_window", u"Precise Bomb Throws", None))
        self.setting_logic_lanayru_mine_quick_bomb.setText(QCoreApplication.translate("main_window", u"Lanayru Mine Quick Bomb", None))
        self.setting_logic_cactus_bomb_whip.setText(QCoreApplication.translate("main_window", u"Whip Bomb Flowers off Cacti", None))
        self.setting_logic_beedles_shop_with_bombs.setText(QCoreApplication.translate("main_window", u"Beedle's Airshop with Bombs", None))
        self.setting_logic_bird_nest_item_from_beedles_shop.setText(QCoreApplication.translate("main_window", u"Bird's Nest from Beedle's Airshop", None))
        self.setting_logic_precise_beetle.setText(QCoreApplication.translate("main_window", u"Precise Beetle Flying", None))
        self.setting_logic_skippers_fast_clawshots.setText(QCoreApplication.translate("main_window", u"Skipper's Retreat Fast Clawshots", None))
        self.setting_logic_lmf_whip_switch.setText(QCoreApplication.translate("main_window", u"Lanayru Mining Facility Whip Switch", None))
        self.setting_logic_lmf_whip_armos_room_timeshift_stone.setText(QCoreApplication.translate("main_window", u"Lanayru Mining Facility Whip Timeshift Stone", None))
        self.setting_logic_lmf_minecart_jump.setText(QCoreApplication.translate("main_window", u"Lanayru Mining Facility Ride on Minecart", None))
        self.setting_logic_present_bow_switches.setText(QCoreApplication.translate("main_window", u"Present Bow Switch Shots", None))
        self.setting_logic_skykeep_vineclip.setText(QCoreApplication.translate("main_window", u"Sky Keep Vine Clip", None))
        self.dives_and_jumps_group_box.setTitle(QCoreApplication.translate("main_window", u"Dives and Jumps", None))
        self.setting_logic_volcanic_island_dive.setText(QCoreApplication.translate("main_window", u"Volcanic Island Dive", None))
        self.setting_logic_east_island_dive.setText(QCoreApplication.translate("main_window", u"Inside the Thunderhead East Island Dive", None))
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
        self.setting_logic_faron_woods_with_groosenator.setText(QCoreApplication.translate("main_window", u"Faron Woods with Groosenator", None))
        self.setting_logic_itemless_first_timeshift_stone.setText(QCoreApplication.translate("main_window", u"Itemless First Timeshift Stone", None))
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
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.logic_tab), QCoreApplication.translate("main_window", u"Logic and Tricks", None))
        self.environment_cosmetics_group_box.setTitle(QCoreApplication.translate("main_window", u"Environment Cosmetics", None))
        self.setting_starry_skies.setText(QCoreApplication.translate("main_window", u"Starry Skies", None))
        self.daytime_sky_color_label.setText(QCoreApplication.translate("main_window", u"Daytime Sky Color", None))
        self.nighttime_sky_color_label.setText(QCoreApplication.translate("main_window", u"Nighttime Sky Color", None))
        self.daytime_cloud_color_label.setText(QCoreApplication.translate("main_window", u"Daytime Cloud Color", None))
        self.nighttime_cloud_color_label.setText(QCoreApplication.translate("main_window", u"Nighttime Cloud Color", None))
        self.player_cosmetics_group_box.setTitle(QCoreApplication.translate("main_window", u"Player Cosmetics", None))
        self.setting_tunic_swap.setText(QCoreApplication.translate("main_window", u"Tunic Swap", None))
        self.setting_lightning_skyward_strike.setText(QCoreApplication.translate("main_window", u"Lightning Skyward Strike", None))
        self.player_cosmetics_texture_gude_label.setText(QCoreApplication.translate("main_window", u"<html><head/><body><p>You can also edit the textures of Link and the Loftwing by following this <a href=\"https://docs.google.com/document/d/1Eq1rXcjwRpVjp-5ugpQAsjmZy5QuGi7KAOkvpWoQkqc\"><span style=\" text-decoration: underline; color:#9a0089;\">Texture Replacements Guide</span></a>. The same principles shown there can also be used with custom models.</p></body></html>", None))
        self.audio_cosmetics_group_box.setTitle(QCoreApplication.translate("main_window", u"Audio Cosmetics", None))
        self.setting_remove_enemy_music.setText(QCoreApplication.translate("main_window", u"Remove Enemy Music", None))
        self.low_health_beeping_speed_label.setText(QCoreApplication.translate("main_window", u"Low Health Beeping Speed", None))
        self.text_cosmetics_group_box.setTitle(QCoreApplication.translate("main_window", u"Text Cosmetics", None))
        self.language_label.setText(QCoreApplication.translate("main_window", u"In-Game Language", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.cosmetics_tab), QCoreApplication.translate("main_window", u"Cosmetics", None))
        self.file_setup_group_box.setTitle(QCoreApplication.translate("main_window", u"Extract and Output Utilities", None))
        self.config_generate_spoiler_log.setText(QCoreApplication.translate("main_window", u"Generate Spoiler Log", None))
        self.open_folders_label.setText(QCoreApplication.translate("main_window", u"Open Folders", None))
        self.open_output_folder_button.setText(QCoreApplication.translate("main_window", u"Open Output Folder", None))
        self.open_extract_folder_button.setText(QCoreApplication.translate("main_window", u"Open Extract Folder", None))
        self.open_spoiler_logs_folder_button.setText(QCoreApplication.translate("main_window", u"Open Spoiler Logs Folder", None))
        self.output_label.setText(QCoreApplication.translate("main_window", u"Output Path:", None))
        self.reset_output_button.setText(QCoreApplication.translate("main_window", u"Reset", None))
        self.browse_output_button.setText(QCoreApplication.translate("main_window", u"Browse", None))
        self.verify_extract_label.setText(QCoreApplication.translate("main_window", u"Verify Extracted Game Files:", None))
        self.verify_important_extract_button.setText(QCoreApplication.translate("main_window", u"Verify Important Files", None))
        self.verify_all_extract_button.setText(QCoreApplication.translate("main_window", u"Verify All Files", None))
        self.plandomizer_group_box.setTitle(QCoreApplication.translate("main_window", u"Plandomizer", None))
        self.plandomizer_warning_label.setText(QCoreApplication.translate("main_window", u"<html><head/><body><p><span style=\" font-weight:700;\">WARNING</span>: The plandomizer settings will automatically <span style=\" font-weight:700;\">TURN THEMSELVES OFF</span> when reopening this randomizer program!</p></body></html>", None))
        self.config_use_plandomizer.setText(QCoreApplication.translate("main_window", u"Use Plandomizer File", None))
        self.selected_plandomizer_file_label.setText(QCoreApplication.translate("main_window", u"Selected Plandomizer File:", None))
        self.open_plandomizer_folder_button.setText(QCoreApplication.translate("main_window", u"Open Plandomizer Folder", None))
        self.random_settings_group_box.setTitle(QCoreApplication.translate("main_window", u"Random Settings", None))
        self.other_settings_group_box.setTitle(QCoreApplication.translate("main_window", u"Other Settings", None))
        self.setting_enable_back_in_time.setText(QCoreApplication.translate("main_window", u"Enable Back in Time (BiT)", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.advanced_tab), QCoreApplication.translate("main_window", u"Advanced", None))
        self.tracker_stats_remaining_label.setText(QCoreApplication.translate("main_window", u"Locations Remaining", None))
        self.tracker_stats_remaining.setText("")
        self.tracker_stats_checked.setText("")
        self.tracker_stats_accessible.setText("")
        self.tracker_stats_accessible_label.setText(QCoreApplication.translate("main_window", u"Locations Accessible", None))
        self.tracker_stats_checked_label.setText(QCoreApplication.translate("main_window", u"Locations Checked", None))
        self.start_new_tracker_button.setText(QCoreApplication.translate("main_window", u"Start New Tracker", None))
        self.set_random_settings_button.setText(QCoreApplication.translate("main_window", u"Set Random Settings", None))
        self.set_starting_entrance_button.setText(QCoreApplication.translate("main_window", u"Set Starting Entrance", None))
        self.check_all_button.setText(QCoreApplication.translate("main_window", u"Check All", None))
        self.check_all_in_logic_button.setText(QCoreApplication.translate("main_window", u"Check All in Logic", None))
        self.uncheck_all_button.setText(QCoreApplication.translate("main_window", u"Uncheck All", None))
        self.set_hints_button.setText(QCoreApplication.translate("main_window", u"Set Hints", None))
        self.toggle_sphere_tracking_button.setText(QCoreApplication.translate("main_window", u"Enable Sphere Tracking", None))
        self.tracker_sphere_tracking_label.setText(QCoreApplication.translate("main_window", u"Sphere Tracking", None))
        self.cancel_sphere_tracking_button.setText(QCoreApplication.translate("main_window", u"Cancel Sphere Tracking for Location", None))
        self.tracker_notes_label.setText(QCoreApplication.translate("main_window", u"Notes", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tracker_tab), QCoreApplication.translate("main_window", u"Tracker", None))
        self.settings_current_option_description_label.setText(QCoreApplication.translate("main_window", u"Settings current option description", None))
        self.settings_default_option_description_label.setText(QCoreApplication.translate("main_window", u"Settings default option description", None))
        self.setting_string_label.setText(QCoreApplication.translate("main_window", u"Setting String", None))
        self.about_button.setText(QCoreApplication.translate("main_window", u"About", None))
        self.new_seed_button.setText(QCoreApplication.translate("main_window", u"New Seed", None))
        self.copy_setting_string_button.setText(QCoreApplication.translate("main_window", u"Copy", None))
        self.layout_label.setText("")
        self.reset_settings_to_default_button.setText(QCoreApplication.translate("main_window", u"Reset Settings to Default", None))
        self.hash_label.setText(QCoreApplication.translate("main_window", u"Hash:", None))
        self.paste_setting_string_button.setText(QCoreApplication.translate("main_window", u"Paste", None))
        self.seed_label.setText(QCoreApplication.translate("main_window", u"Seed:", None))
        self.randomize_button.setText(QCoreApplication.translate("main_window", u"Randomize", None))
    # retranslateUi

