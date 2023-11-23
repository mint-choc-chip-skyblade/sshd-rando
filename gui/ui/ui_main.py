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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(1000, 800)
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.verticalLayout_2 = QVBoxLayout(self.central_widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setObjectName(u"tab_widget")
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
        self.horizontalLayout_2 = QHBoxLayout(self.useful_info_group_box)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.useful_info_label = QLabel(self.useful_info_group_box)
        self.useful_info_label.setObjectName(u"useful_info_label")

        self.horizontalLayout_2.addWidget(self.useful_info_label)


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
        self.tab_widget.addTab(self.world_tab, "")
        self.logic_tab = QWidget()
        self.logic_tab.setObjectName(u"logic_tab")
        self.tab_widget.addTab(self.logic_tab, "")
        self.inventory_tab = QWidget()
        self.inventory_tab.setObjectName(u"inventory_tab")
        self.tab_widget.addTab(self.inventory_tab, "")
        self.cosmetic_tab = QWidget()
        self.cosmetic_tab.setObjectName(u"cosmetic_tab")
        self.tab_widget.addTab(self.cosmetic_tab, "")
        self.advanced_tab = QWidget()
        self.advanced_tab.setObjectName(u"advanced_tab")
        self.tab_widget.addTab(self.advanced_tab, "")
        self.accessibility_tab = QWidget()
        self.accessibility_tab.setObjectName(u"accessibility_tab")
        self.verticalLayout_3 = QVBoxLayout(self.accessibility_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tab_widget.addTab(self.accessibility_tab, "")

        self.verticalLayout_2.addWidget(self.tab_widget)

        self.seed_layout = QHBoxLayout()
        self.seed_layout.setObjectName(u"seed_layout")
        self.seed_label = QLabel(self.central_widget)
        self.seed_label.setObjectName(u"seed_label")

        self.seed_layout.addWidget(self.seed_label)

        self.seed_line_edit = QLineEdit(self.central_widget)
        self.seed_line_edit.setObjectName(u"seed_line_edit")

        self.seed_layout.addWidget(self.seed_line_edit)

        self.new_seed_button = QPushButton(self.central_widget)
        self.new_seed_button.setObjectName(u"new_seed_button")

        self.seed_layout.addWidget(self.new_seed_button)

        self.copy_seed_button = QPushButton(self.central_widget)
        self.copy_seed_button.setObjectName(u"copy_seed_button")

        self.seed_layout.addWidget(self.copy_seed_button)


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
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.randomize_button.sizePolicy().hasHeightForWidth())
        self.randomize_button.setSizePolicy(sizePolicy5)

        self.footer_layout.addWidget(self.randomize_button)


        self.verticalLayout_2.addLayout(self.footer_layout)

        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)

        self.tab_widget.setCurrentIndex(0)


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
        self.useful_info_label.setText(QCoreApplication.translate("main_window", u"TODO:<br><br>\n"
"\n"
"Discord Server: https::/discord.com<br>\n"
"Report a Bug: https::/github.com/mint-choc-chip-skyblade/ssdh-rando/issues<br>\n"
"Location Guide: ???", None))
        self.file_setup_group_box.setTitle(QCoreApplication.translate("main_window", u"File Setup", None))
        self.extract_label.setText(QCoreApplication.translate("main_window", u"Extract", None))
        self.extract_button.setText(QCoreApplication.translate("main_window", u"Browse", None))
        self.output_label.setText(QCoreApplication.translate("main_window", u"Output", None))
        self.output_button.setText(QCoreApplication.translate("main_window", u"Browse", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.getting_started_tab), QCoreApplication.translate("main_window", u"Getting Started", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.world_tab), QCoreApplication.translate("main_window", u"World", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.logic_tab), QCoreApplication.translate("main_window", u"Logic", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.inventory_tab), QCoreApplication.translate("main_window", u"Inventory", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.cosmetic_tab), QCoreApplication.translate("main_window", u"Cosmetic", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.advanced_tab), QCoreApplication.translate("main_window", u"Advanced", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.accessibility_tab), QCoreApplication.translate("main_window", u"Accessibility", None))
        self.seed_label.setText(QCoreApplication.translate("main_window", u"Seed:", None))
        self.new_seed_button.setText(QCoreApplication.translate("main_window", u"New Seed", None))
        self.copy_seed_button.setText(QCoreApplication.translate("main_window", u"Copy Seed", None))
        self.about_button.setText(QCoreApplication.translate("main_window", u"About", None))
        self.reset_button.setText(QCoreApplication.translate("main_window", u"Reset Settings to Default", None))
        self.randomize_button.setText(QCoreApplication.translate("main_window", u"Randomize", None))
    # retranslateUi

