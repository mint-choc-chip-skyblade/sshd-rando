# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.verticalLayout_2 = QVBoxLayout(self.central_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setObjectName("tab_widget")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.tab_widget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tab_widget.addTab(self.tab_2, "")

        self.verticalLayout_2.addWidget(self.tab_widget)

        self.footer_layout = QHBoxLayout()
        self.footer_layout.setObjectName("footer_layout")
        self.about_button = QPushButton(self.central_widget)
        self.about_button.setObjectName("about_button")

        self.footer_layout.addWidget(self.about_button)

        self.footer_left_hspacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.footer_layout.addItem(self.footer_left_hspacer)

        self.reset_button = QPushButton(self.central_widget)
        self.reset_button.setObjectName("reset_button")

        self.footer_layout.addWidget(self.reset_button)

        self.footer_right_hspacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.footer_layout.addItem(self.footer_right_hspacer)

        self.randomize_button = QPushButton(self.central_widget)
        self.randomize_button.setObjectName("randomize_button")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.randomize_button.sizePolicy().hasHeightForWidth()
        )
        self.randomize_button.setSizePolicy(sizePolicy)

        self.footer_layout.addWidget(self.randomize_button)

        self.verticalLayout_2.addLayout(self.footer_layout)

        main_window.setCentralWidget(self.central_widget)

        self.retranslateUi(main_window)

        QMetaObject.connectSlotsByName(main_window)

    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(
            QCoreApplication.translate(
                "main_window", "The Legend of Zelda: Skyward Sword HD Randomizer", None
            )
        )
        self.tab_widget.setTabText(
            self.tab_widget.indexOf(self.tab),
            QCoreApplication.translate("main_window", "Tab 1", None),
        )
        self.tab_widget.setTabText(
            self.tab_widget.indexOf(self.tab_2),
            QCoreApplication.translate("main_window", "Tab 2", None),
        )
        self.about_button.setText(
            QCoreApplication.translate("main_window", "About", None)
        )
        self.reset_button.setText(
            QCoreApplication.translate("main_window", "Reset Settings to Default", None)
        )
        self.randomize_button.setText(
            QCoreApplication.translate("main_window", "Randomize", None)
        )

    # retranslateUi
