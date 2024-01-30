# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'custom_theme_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QDoubleSpinBox, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QPlainTextEdit, QProgressBar, QPushButton,
    QRadioButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QTabWidget, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_CustomThemeDialog(object):
    def setupUi(self, CustomThemeDialog):
        if not CustomThemeDialog.objectName():
            CustomThemeDialog.setObjectName(u"CustomThemeDialog")
        CustomThemeDialog.resize(630, 635)
        self.verticalLayout = QVBoxLayout(CustomThemeDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.custom_theme_tabWidget = QTabWidget(CustomThemeDialog)
        self.custom_theme_tabWidget.setObjectName(u"custom_theme_tabWidget")
        self.custom_colors_tab = QWidget()
        self.custom_colors_tab.setObjectName(u"custom_colors_tab")
        self.verticalLayout_2 = QVBoxLayout(self.custom_colors_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.vlay_widget = QVBoxLayout()
        self.vlay_widget.setObjectName(u"vlay_widget")
        self.hlay_widget_catergory = QHBoxLayout()
        self.hlay_widget_catergory.setObjectName(u"hlay_widget_catergory")
        self.widget_category_label = QLabel(self.custom_colors_tab)
        self.widget_category_label.setObjectName(u"widget_category_label")

        self.hlay_widget_catergory.addWidget(self.widget_category_label)

        self.widget_category_choice = QComboBox(self.custom_colors_tab)
        self.widget_category_choice.setObjectName(u"widget_category_choice")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_category_choice.sizePolicy().hasHeightForWidth())
        self.widget_category_choice.setSizePolicy(sizePolicy)

        self.hlay_widget_catergory.addWidget(self.widget_category_choice)

        self.hspace_widget_category = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hlay_widget_catergory.addItem(self.hspace_widget_category)


        self.vlay_widget.addLayout(self.hlay_widget_catergory)

        self.hlay_widgets = QHBoxLayout()
        self.hlay_widgets.setObjectName(u"hlay_widgets")
        self.vlay_widget_name = QVBoxLayout()
        self.vlay_widget_name.setObjectName(u"vlay_widget_name")
        self.vlay_widget_name.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.widget_name_label = QLabel(self.custom_colors_tab)
        self.widget_name_label.setObjectName(u"widget_name_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_name_label.sizePolicy().hasHeightForWidth())
        self.widget_name_label.setSizePolicy(sizePolicy1)
        self.widget_name_label.setMinimumSize(QSize(0, 0))
        self.widget_name_label.setTextFormat(Qt.MarkdownText)

        self.vlay_widget_name.addWidget(self.widget_name_label)

        self.vspace_widget_name = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_widget_name.addItem(self.vspace_widget_name)


        self.hlay_widgets.addLayout(self.vlay_widget_name)

        self.vlay_color_light = QVBoxLayout()
        self.vlay_color_light.setObjectName(u"vlay_color_light")
        self.color_light_label = QLabel(self.custom_colors_tab)
        self.color_light_label.setObjectName(u"color_light_label")
        self.color_light_label.setTextFormat(Qt.MarkdownText)

        self.vlay_color_light.addWidget(self.color_light_label)

        self.vspace_color_light = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_color_light.addItem(self.vspace_color_light)


        self.hlay_widgets.addLayout(self.vlay_color_light)

        self.vlay_color_dark = QVBoxLayout()
        self.vlay_color_dark.setObjectName(u"vlay_color_dark")
        self.color_dark_label = QLabel(self.custom_colors_tab)
        self.color_dark_label.setObjectName(u"color_dark_label")
        self.color_dark_label.setFrameShadow(QFrame.Plain)
        self.color_dark_label.setTextFormat(Qt.MarkdownText)

        self.vlay_color_dark.addWidget(self.color_dark_label)

        self.vspace_color_dark = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_color_dark.addItem(self.vspace_color_dark)


        self.hlay_widgets.addLayout(self.vlay_color_dark)


        self.vlay_widget.addLayout(self.hlay_widgets)


        self.verticalLayout_2.addLayout(self.vlay_widget)

        self.custom_theme_tabWidget.addTab(self.custom_colors_tab, "")
        self.demo_widgets_tab = QWidget()
        self.demo_widgets_tab.setObjectName(u"demo_widgets_tab")
        self.horizontalLayout_2 = QHBoxLayout(self.demo_widgets_tab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.vlay_demo_left = QVBoxLayout()
        self.vlay_demo_left.setObjectName(u"vlay_demo_left")
        self.demo_group_box = QGroupBox(self.demo_widgets_tab)
        self.demo_group_box.setObjectName(u"demo_group_box")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.demo_group_box.sizePolicy().hasHeightForWidth())
        self.demo_group_box.setSizePolicy(sizePolicy2)
        self.verticalLayout_3 = QVBoxLayout(self.demo_group_box)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.vlay_demo_group_box = QVBoxLayout()
        self.vlay_demo_group_box.setObjectName(u"vlay_demo_group_box")
        self.demo_label = QLabel(self.demo_group_box)
        self.demo_label.setObjectName(u"demo_label")
        sizePolicy1.setHeightForWidth(self.demo_label.sizePolicy().hasHeightForWidth())
        self.demo_label.setSizePolicy(sizePolicy1)

        self.vlay_demo_group_box.addWidget(self.demo_label)

        self.demo_line_3 = QFrame(self.demo_group_box)
        self.demo_line_3.setObjectName(u"demo_line_3")
        self.demo_line_3.setFrameShape(QFrame.HLine)
        self.demo_line_3.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.demo_line_3)

        self.demo_checkBox = QCheckBox(self.demo_group_box)
        self.demo_checkBox.setObjectName(u"demo_checkBox")

        self.vlay_demo_group_box.addWidget(self.demo_checkBox)

        self.demo_line_2 = QFrame(self.demo_group_box)
        self.demo_line_2.setObjectName(u"demo_line_2")
        self.demo_line_2.setFrameShape(QFrame.HLine)
        self.demo_line_2.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.demo_line_2)

        self.demo_radioButton = QRadioButton(self.demo_group_box)
        self.demo_radioButton.setObjectName(u"demo_radioButton")

        self.vlay_demo_group_box.addWidget(self.demo_radioButton)

        self.demo_line = QFrame(self.demo_group_box)
        self.demo_line.setObjectName(u"demo_line")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.demo_line.sizePolicy().hasHeightForWidth())
        self.demo_line.setSizePolicy(sizePolicy3)
        self.demo_line.setFrameShape(QFrame.HLine)
        self.demo_line.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.demo_line)

        self.demo_spinBox = QSpinBox(self.demo_group_box)
        self.demo_spinBox.setObjectName(u"demo_spinBox")

        self.vlay_demo_group_box.addWidget(self.demo_spinBox)

        self.demo_line_10 = QFrame(self.demo_group_box)
        self.demo_line_10.setObjectName(u"demo_line_10")
        self.demo_line_10.setFrameShape(QFrame.HLine)
        self.demo_line_10.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.demo_line_10)

        self.demo_doubleSpinBox = QDoubleSpinBox(self.demo_group_box)
        self.demo_doubleSpinBox.setObjectName(u"demo_doubleSpinBox")

        self.vlay_demo_group_box.addWidget(self.demo_doubleSpinBox)

        self.demo_line_9 = QFrame(self.demo_group_box)
        self.demo_line_9.setObjectName(u"demo_line_9")
        self.demo_line_9.setFrameShape(QFrame.HLine)
        self.demo_line_9.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.demo_line_9)

        self.demo_pushButton = QPushButton(self.demo_group_box)
        self.demo_pushButton.setObjectName(u"demo_pushButton")

        self.vlay_demo_group_box.addWidget(self.demo_pushButton)

        self.demo_line_8 = QFrame(self.demo_group_box)
        self.demo_line_8.setObjectName(u"demo_line_8")
        self.demo_line_8.setFrameShape(QFrame.HLine)
        self.demo_line_8.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.demo_line_8)

        self.demo_comboBox = QComboBox(self.demo_group_box)
        self.demo_comboBox.setObjectName(u"demo_comboBox")

        self.vlay_demo_group_box.addWidget(self.demo_comboBox)

        self.demo_line_7 = QFrame(self.demo_group_box)
        self.demo_line_7.setObjectName(u"demo_line_7")
        self.demo_line_7.setFrameShape(QFrame.HLine)
        self.demo_line_7.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.demo_line_7)

        self.demo_lineEdit = QLineEdit(self.demo_group_box)
        self.demo_lineEdit.setObjectName(u"demo_lineEdit")

        self.vlay_demo_group_box.addWidget(self.demo_lineEdit)

        self.demo_line_6 = QFrame(self.demo_group_box)
        self.demo_line_6.setObjectName(u"demo_line_6")
        self.demo_line_6.setFrameShape(QFrame.HLine)
        self.demo_line_6.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.demo_line_6)

        self.demo_horizontalSlider = QSlider(self.demo_group_box)
        self.demo_horizontalSlider.setObjectName(u"demo_horizontalSlider")
        self.demo_horizontalSlider.setOrientation(Qt.Horizontal)

        self.vlay_demo_group_box.addWidget(self.demo_horizontalSlider)

        self.demo_line_5 = QFrame(self.demo_group_box)
        self.demo_line_5.setObjectName(u"demo_line_5")
        self.demo_line_5.setFrameShape(QFrame.HLine)
        self.demo_line_5.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.demo_line_5)

        self.demo_progressBar = QProgressBar(self.demo_group_box)
        self.demo_progressBar.setObjectName(u"demo_progressBar")
        self.demo_progressBar.setValue(24)

        self.vlay_demo_group_box.addWidget(self.demo_progressBar)

        self.demo_line_4 = QFrame(self.demo_group_box)
        self.demo_line_4.setObjectName(u"demo_line_4")
        self.demo_line_4.setFrameShape(QFrame.HLine)
        self.demo_line_4.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.demo_line_4)

        self.demo_dialogButtonBox = QDialogButtonBox(self.demo_group_box)
        self.demo_dialogButtonBox.setObjectName(u"demo_dialogButtonBox")
        self.demo_dialogButtonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.demo_dialogButtonBox.setCenterButtons(True)

        self.vlay_demo_group_box.addWidget(self.demo_dialogButtonBox)

        self.vspace_demo = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_demo_group_box.addItem(self.vspace_demo)


        self.verticalLayout_3.addLayout(self.vlay_demo_group_box)


        self.vlay_demo_left.addWidget(self.demo_group_box)


        self.horizontalLayout_2.addLayout(self.vlay_demo_left)

        self.demo_line_separator_left = QFrame(self.demo_widgets_tab)
        self.demo_line_separator_left.setObjectName(u"demo_line_separator_left")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.demo_line_separator_left.sizePolicy().hasHeightForWidth())
        self.demo_line_separator_left.setSizePolicy(sizePolicy4)
        self.demo_line_separator_left.setFrameShape(QFrame.VLine)
        self.demo_line_separator_left.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.demo_line_separator_left)

        self.demo_vslider = QSlider(self.demo_widgets_tab)
        self.demo_vslider.setObjectName(u"demo_vslider")
        self.demo_vslider.setOrientation(Qt.Vertical)

        self.horizontalLayout_2.addWidget(self.demo_vslider)

        self.demo_line_separator_right = QFrame(self.demo_widgets_tab)
        self.demo_line_separator_right.setObjectName(u"demo_line_separator_right")
        sizePolicy4.setHeightForWidth(self.demo_line_separator_right.sizePolicy().hasHeightForWidth())
        self.demo_line_separator_right.setSizePolicy(sizePolicy4)
        self.demo_line_separator_right.setFrameShape(QFrame.VLine)
        self.demo_line_separator_right.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.demo_line_separator_right)

        self.vlay_demo_right = QVBoxLayout()
        self.vlay_demo_right.setObjectName(u"vlay_demo_right")
        self.demo_textEdit = QTextEdit(self.demo_widgets_tab)
        self.demo_textEdit.setObjectName(u"demo_textEdit")

        self.vlay_demo_right.addWidget(self.demo_textEdit)

        self.demo_line_11 = QFrame(self.demo_widgets_tab)
        self.demo_line_11.setObjectName(u"demo_line_11")
        self.demo_line_11.setFrameShape(QFrame.HLine)
        self.demo_line_11.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_right.addWidget(self.demo_line_11)

        self.demo_plainTextEdit = QPlainTextEdit(self.demo_widgets_tab)
        self.demo_plainTextEdit.setObjectName(u"demo_plainTextEdit")

        self.vlay_demo_right.addWidget(self.demo_plainTextEdit)


        self.horizontalLayout_2.addLayout(self.vlay_demo_right)

        self.custom_theme_tabWidget.addTab(self.demo_widgets_tab, "")

        self.verticalLayout.addWidget(self.custom_theme_tabWidget)

        self.widget_description = QLabel(CustomThemeDialog)
        self.widget_description.setObjectName(u"widget_description")
        self.widget_description.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.widget_description.sizePolicy().hasHeightForWidth())
        self.widget_description.setSizePolicy(sizePolicy2)
        self.widget_description.setWordWrap(True)

        self.verticalLayout.addWidget(self.widget_description)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.restore_defaults_button = QPushButton(CustomThemeDialog)
        self.restore_defaults_button.setObjectName(u"restore_defaults_button")

        self.horizontalLayout.addWidget(self.restore_defaults_button)

        self.bbox_theme = QDialogButtonBox(CustomThemeDialog)
        self.bbox_theme.setObjectName(u"bbox_theme")
        self.bbox_theme.setOrientation(Qt.Horizontal)
        self.bbox_theme.setStandardButtons(QDialogButtonBox.Close|QDialogButtonBox.Save)
        self.bbox_theme.setCenterButtons(False)

        self.horizontalLayout.addWidget(self.bbox_theme)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(CustomThemeDialog)
        self.bbox_theme.rejected.connect(CustomThemeDialog.reject)
        self.bbox_theme.clicked.connect(CustomThemeDialog.update)

        self.custom_theme_tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CustomThemeDialog)
    # setupUi

    def retranslateUi(self, CustomThemeDialog):
        CustomThemeDialog.setWindowTitle(QCoreApplication.translate("CustomThemeDialog", u"Customize Randomizer Theme", None))
        self.widget_category_label.setText(QCoreApplication.translate("CustomThemeDialog", u"Widget Category", None))
        self.widget_name_label.setText(QCoreApplication.translate("CustomThemeDialog", u"_**Widget Name**_", None))
        self.color_light_label.setText(QCoreApplication.translate("CustomThemeDialog", u"_**Color (Light Theme)**_", None))
        self.color_dark_label.setText(QCoreApplication.translate("CustomThemeDialog", u"_**Color (Dark Theme)**_", None))
        self.custom_theme_tabWidget.setTabText(self.custom_theme_tabWidget.indexOf(self.custom_colors_tab), QCoreApplication.translate("CustomThemeDialog", u"Custom Colors", None))
        self.demo_group_box.setTitle(QCoreApplication.translate("CustomThemeDialog", u"GroupBox", None))
        self.demo_label.setText(QCoreApplication.translate("CustomThemeDialog", u"QLabel", None))
        self.demo_checkBox.setText(QCoreApplication.translate("CustomThemeDialog", u"CheckBox", None))
        self.demo_radioButton.setText(QCoreApplication.translate("CustomThemeDialog", u"RadioButton", None))
        self.demo_pushButton.setText(QCoreApplication.translate("CustomThemeDialog", u"PushButton", None))
        self.demo_comboBox.setCurrentText("")
        self.demo_comboBox.setPlaceholderText(QCoreApplication.translate("CustomThemeDialog", u"ComboBox", None))
        self.demo_lineEdit.setText(QCoreApplication.translate("CustomThemeDialog", u"LineEdit", None))
        self.demo_textEdit.setHtml(QCoreApplication.translate("CustomThemeDialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">TextEdit</p></body></html>", None))
        self.demo_plainTextEdit.setPlainText(QCoreApplication.translate("CustomThemeDialog", u"PlainTextEdit", None))
        self.custom_theme_tabWidget.setTabText(self.custom_theme_tabWidget.indexOf(self.demo_widgets_tab), QCoreApplication.translate("CustomThemeDialog", u"Demo Widgets", None))
        self.widget_description.setText("")
        self.restore_defaults_button.setText(QCoreApplication.translate("CustomThemeDialog", u"Restore Defaults", None))
    # retranslateUi

