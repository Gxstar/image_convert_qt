# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGroupBox,
    QHBoxLayout, QLCDNumber, QLabel, QLineEdit,
    QListView, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QStatusBar,
    QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"/* \u4e3b\u7a97\u53e3\u80cc\u666f */\n"
"QWidget#centralwidget {\n"
"	background-color: #F0F2F5;\n"
"	font-family: \"Segoe UI\", \"Microsoft YaHei\";\n"
"}\n"
"\n"
"/* \u5206\u7ec4\u6846\u6837\u5f0f */\n"
"QGroupBox {\n"
"    font-weight: 500;\n"
"    border: 1px solid #E1E5EB;\n"
"    border-radius: 8px;\n"
"    margin-top: 1ex; /* \u4e3a\u6807\u9898\u7559\u51fa\u7a7a\u95f4 */\n"
"    background-color: #FAFBFD;\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\";\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 5px 0 5px;\n"
"    color: #5A6475;\n"
"}\n"
"\n"
"/* \u6309\u94ae\u901a\u7528\u6837\u5f0f */\n"
"QPushButton {\n"
"    background-color: #5B8DB8;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 10px 16px;\n"
"    font-weight: 500;\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\";\n"
"    min-height: 24px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #4A7A9F;\n"
"}\n"
"\n"
"QPushB"
                        "utton:pressed {\n"
"    background-color: #3D6785;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #8997A5;\n"
"}\n"
"\n"
"/* \u6807\u7b7e\u6837\u5f0f */\n"
"QLabel {\n"
"    color: #5A6475;\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\";\n"
"}\n"
"\n"
"/* \u7ec4\u5408\u6846\u6837\u5f0f */\n"
"QComboBox {\n"
"    padding: 8px 12px;\n"
"    border: 1px solid #D4D9E0;\n"
"    border-radius: 6px;\n"
"    background-color: #FAFBFD;\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\";\n"
"    min-height: 24px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border-color: #5B8DB8;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/icons/down_arrow.png);\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    margin-right: 8px;\n"
"}\n"
"\n"
"/* \u8f93\u5165\u6846\u6837\u5f0f */\n"
"QLineEdit {\n"
"    padding: 8px 12px;\n"
"    border: 1px solid #D4D9E0;\n"
"    border-radius: 6px;\n"
"    background-color"
                        ": #FAFBFD;\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\";\n"
"    selection-background-color: #5B8DB8;\n"
"    selection-color: white;\n"
"    min-height: 24px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: #5B8DB8;\n"
"    outline: none;\n"
"}\n"
"\n"
"/* \u6ed1\u5757\u6837\u5f0f */\n"
"QSlider::groove:horizontal {\n"
"    height: 6px;\n"
"    background: #E1E5EB;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #5B8DB8;\n"
"    border: none;\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    margin: -6px 0;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background: #8997A5;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"/* \u590d\u9009\u6846\u6837\u5f0f */\n"
"QCheckBox {\n"
"    color: #5A6475;\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\";\n"
"    spacing: 8px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"}\n"
"\n"
"/* \u5217\u8868\u89c6\u56fe\u6837\u5f0f */\n"
"QList"
                        "View {\n"
"    border: 1px solid #D4D9E0;\n"
"    border-radius: 6px;\n"
"    background-color: #FAFBFD;\n"
"    alternate-background-color: #F0F2F5;\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\";\n"
"}\n"
"\n"
"QListView::item {\n"
"    padding: 6px 8px;\n"
"}\n"
"\n"
"QListView::item:selected {\n"
"    background-color: #5B8DB8;\n"
"    color: white;\n"
"}\n"
"\n"
"/* LCD\u6570\u5b57\u663e\u793a\u6837\u5f0f */\n"
"QLCDNumber {\n"
"    color: #5B8DB8;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.left = QVBoxLayout()
        self.left.setSpacing(12)
        self.left.setObjectName(u"left")
        self.inputBox = QGroupBox(self.centralwidget)
        self.inputBox.setObjectName(u"inputBox")
        self.verticalLayout = QVBoxLayout(self.inputBox)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_5)

        self.addImages = QPushButton(self.inputBox)
        self.addImages.setObjectName(u"addImages")

        self.verticalLayout.addWidget(self.addImages)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.addDirs = QPushButton(self.inputBox)
        self.addDirs.setObjectName(u"addDirs")

        self.verticalLayout.addWidget(self.addDirs)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)


        self.left.addWidget(self.inputBox)

        self.outputBox = QGroupBox(self.centralwidget)
        self.outputBox.setObjectName(u"outputBox")
        self.verticalLayout_2 = QVBoxLayout(self.outputBox)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_7)

        self.format = QVBoxLayout()
        self.format.setSpacing(4)
        self.format.setObjectName(u"format")
        self.outFormatTitle = QLabel(self.outputBox)
        self.outFormatTitle.setObjectName(u"outFormatTitle")

        self.format.addWidget(self.outFormatTitle)

        self.formatSelection = QComboBox(self.outputBox)
        self.formatSelection.setObjectName(u"formatSelection")

        self.format.addWidget(self.formatSelection)


        self.verticalLayout_2.addLayout(self.format)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.outdir = QVBoxLayout()
        self.outdir.setSpacing(4)
        self.outdir.setObjectName(u"outdir")
        self.outDirTitle = QLabel(self.outputBox)
        self.outDirTitle.setObjectName(u"outDirTitle")

        self.outdir.addWidget(self.outDirTitle)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.outputBox)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.outputBox)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 2)

        self.outdir.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.outdir)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.quality = QVBoxLayout()
        self.quality.setSpacing(4)
        self.quality.setObjectName(u"quality")
        self.qualityTitle = QLabel(self.outputBox)
        self.qualityTitle.setObjectName(u"qualityTitle")

        self.quality.addWidget(self.qualityTitle)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.qualityValue = QSlider(self.outputBox)
        self.qualityValue.setObjectName(u"qualityValue")
        self.qualityValue.setMaximum(100)
        self.qualityValue.setValue(100)
        self.qualityValue.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_2.addWidget(self.qualityValue)

        self.qualityShow = QLabel(self.outputBox)
        self.qualityShow.setObjectName(u"qualityShow")
        self.qualityShow.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.qualityShow)

        self.horizontalLayout_2.setStretch(0, 6)
        self.horizontalLayout_2.setStretch(1, 1)

        self.quality.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.quality)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.isReplace = QCheckBox(self.outputBox)
        self.isReplace.setObjectName(u"isReplace")

        self.verticalLayout_2.addWidget(self.isReplace)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_8)


        self.left.addWidget(self.outputBox)

        self.run = QPushButton(self.centralwidget)
        self.run.setObjectName(u"run")
        self.run.setMinimumSize(QSize(0, 44))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setWeight(QFont.Medium)
        self.run.setFont(font)

        self.left.addWidget(self.run)


        self.horizontalLayout_3.addLayout(self.left)

        self.right = QGroupBox(self.centralwidget)
        self.right.setObjectName(u"right")
        self.right.setStyleSheet(u"QGroupBox#right {\n"
"     background-color: #FFFFFF;\n"
"     border: 1px solid #E1E5EB;\n"
"     border-radius: 8px;\n"
"     margin-top: 1ex;\n"
" }\n"
"\n"
" QGroupBox#right::title {\n"
"     subcontrol-origin: margin;\n"
"     left: 10px;\n"
"     padding: 0 5px 0 5px;\n"
"     color: #5A6475;\n"
"     font-weight: 500;\n"
" }")
        self.verticalLayout_3 = QVBoxLayout(self.right)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.toolbarWidget = QWidget(self.right)
        self.toolbarWidget.setObjectName(u"toolbarWidget")
        self.toolbarWidget.setStyleSheet(u"QWidget#toolbarWidget {\n"
"    background-color: #E9EEF5;\n"
"    border: 1px solid #D4D9E0;\n"
"    border-radius: 6px;\n"
"    padding: 8px;\n"
"}")
        self.horizontalLayout_4 = QHBoxLayout(self.toolbarWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.selectedNum = QLCDNumber(self.toolbarWidget)
        self.selectedNum.setObjectName(u"selectedNum")
        self.selectedNum.setStyleSheet(u"QLCDNumber {\n"
"    color: #4285F4;\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}")

        self.horizontalLayout_4.addWidget(self.selectedNum)

        self.labelSelectedNum = QLabel(self.toolbarWidget)
        self.labelSelectedNum.setObjectName(u"labelSelectedNum")
        self.labelSelectedNum.setStyleSheet(u"QLabel {\n"
"    color: #5A6475;\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\";\n"
"    font-weight: 500;\n"
"}")

        self.horizontalLayout_4.addWidget(self.labelSelectedNum)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.clearSelected = QToolButton(self.toolbarWidget)
        self.clearSelected.setObjectName(u"clearSelected")
        self.clearSelected.setStyleSheet(u"/* --- \u5de5\u5177\u680f\u6309\u94ae QSS --- */\n"
"\n"
"QToolButton {\n"
"    /* \u57fa\u7840\u6837\u5f0f */\n"
"    background-color: #5B8DB8;        /* \u67d4\u548c\u84dd\u8272\u80cc\u666f */\n"
"    color: #FFFFFF;                   /* \u767d\u8272\u6587\u5b57 */\n"
"    border: none;                     /* \u65e0\u8fb9\u6846 */\n"
"    border-radius: 6px;               /* \u5706\u6da6\u8fb9\u89d2 */\n"
"    padding: 8px 16px;                /* \u8212\u9002\u5185\u8fb9\u8ddd */\n"
"    font-weight: 500;                 /* \u4e2d\u7b49\u5b57\u4f53\u7c97\u7ec6 */\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\"; /* \u73b0\u4ee3\u5b57\u4f53 */\n"
"    min-width: 80px;\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    /* \u9f20\u6807\u60ac\u505c\u72b6\u6001 */\n"
"    background-color: #4A7A9F;        /* \u6df1\u4e00\u53f7\u7684\u60ac\u505c\u8272 */\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    /* \u9f20\u6807\u6309\u4e0b\u72b6\u6001 */\n"
"    background-color: #3D6785;        /* \u66f4\u6df1\u7684\u6309\u4e0b"
                        "\u8272 */\n"
"}\n"
"\n"
"QToolButton:disabled {\n"
"    /* \u7981\u7528\u72b6\u6001 */\n"
"    background-color: #8997A5;        /* \u6d45\u7070\u8272\u7981\u7528\u72b6\u6001 */\n"
"    color: #CED4DA;\n"
"}\n"
"")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.clearSelected.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.clearSelected)

        self.clearAll = QToolButton(self.toolbarWidget)
        self.clearAll.setObjectName(u"clearAll")
        self.clearAll.setStyleSheet(u"/* --- \u5de5\u5177\u680f\u6309\u94ae QSS --- */\n"
"\n"
"QToolButton {\n"
"    /* \u57fa\u7840\u6837\u5f0f */\n"
"    background-color: #5B8DB8;        /* \u67d4\u548c\u84dd\u8272\u80cc\u666f */\n"
"    color: #FFFFFF;                   /* \u767d\u8272\u6587\u5b57 */\n"
"    border: none;                     /* \u65e0\u8fb9\u6846 */\n"
"    border-radius: 6px;               /* \u5706\u6da6\u8fb9\u89d2 */\n"
"    padding: 8px 16px;                /* \u8212\u9002\u5185\u8fb9\u8ddd */\n"
"    font-weight: 500;                 /* \u4e2d\u7b49\u5b57\u4f53\u7c97\u7ec6 */\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\"; /* \u73b0\u4ee3\u5b57\u4f53 */\n"
"    min-width: 80px;\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    /* \u9f20\u6807\u60ac\u505c\u72b6\u6001 */\n"
"    background-color: #4A7A9F;        /* \u6df1\u4e00\u53f7\u7684\u60ac\u505c\u8272 */\n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    /* \u9f20\u6807\u6309\u4e0b\u72b6\u6001 */\n"
"    background-color: #3D6785;        /* \u66f4\u6df1\u7684\u6309\u4e0b"
                        "\u8272 */\n"
"}\n"
"\n"
"QToolButton:disabled {\n"
"    /* \u7981\u7528\u72b6\u6001 */\n"
"    background-color: #8997A5;        /* \u6d45\u7070\u8272\u7981\u7528\u72b6\u6001 */\n"
"    color: #CED4DA;\n"
"}\n"
"")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditClear))
        self.clearAll.setIcon(icon1)

        self.horizontalLayout_4.addWidget(self.clearAll)


        self.verticalLayout_3.addWidget(self.toolbarWidget)

        self.imageList = QListView(self.right)
        self.imageList.setObjectName(u"imageList")
        self.imageList.setStyleSheet(u"QListView {\n"
"    border: 1px solid #D4D9E0;\n"
"    border-radius: 6px;\n"
"    background-color: #FAFBFD;\n"
"    alternate-background-color: #F0F2F5;\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\";\n"
"    margin-top: 8px;\n"
"}\n"
"\n"
"QListView::item {\n"
"    padding: 6px 8px;\n"
"    border-bottom: 1px solid #E1E5EB;\n"
"}\n"
"\n"
"QListView::item:selected {\n"
"    background-color: #4285F4;\n"
"    color: white;\n"
"}")

        self.verticalLayout_3.addWidget(self.imageList)


        self.horizontalLayout_3.addWidget(self.right)

        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(u"QStatusBar {\n"
"    background-color: #F0F2F5;\n"
"    border-top: 1px solid #E1E5EB;\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\";\n"
"}\n"
"\n"
"QStatusBar::item {\n"
"    border: none;\n"
"}")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 30))
        self.menubar.setStyleSheet(u"QMenuBar {\n"
"    background-color: #FFFFFF;\n"
"    border-bottom: 1px solid #E1E5EB;\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\";\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"    background: transparent;\n"
"    padding: 6px 12px;\n"
"    color: #5A6475;\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"    background: #E9EEF5;\n"
"}\n"
"\n"
"QMenuBar::item:pressed {\n"
"    background: #5B8DB8;\n"
"    color: white;\n"
"}\n"
"\n"
"QMenu {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #E1E5EB;\n"
"    border-radius: 6px;\n"
"    padding: 4px 0px;\n"
"    font-family: \"Segoe UI\", \"Microsoft YaHei\";\n"
"}\n"
"\n"
"QMenu::item {\n"
"    padding: 6px 24px;\n"
"    color: #5A6475;\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"    background-color: #E9EEF5;\n"
"}\n"
"\n"
"QMenu::separator {\n"
"    height: 1px;\n"
"    background: #E1E5EB;\n"
"    margin: 4px 0px;\n"
"}")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.qualityValue.valueChanged.connect(self.qualityShow.setNum)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.inputBox.setTitle(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u56fe\u7247", None))
        self.addImages.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u56fe\u7247", None))
        self.addDirs.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.outputBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u9009\u9879", None))
        self.outFormatTitle.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u683c\u5f0f\u9009\u62e9", None))
        self.outDirTitle.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u8def\u5f84\u9009\u62e9", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u76ee\u5f55", None))
        self.qualityTitle.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u8d28\u91cf", None))
        self.qualityShow.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>100</p></body></html>", None))
        self.isReplace.setText(QCoreApplication.translate("MainWindow", u"\u662f\u5426\u66ff\u6362\u540c\u540d\u6587\u4ef6", None))
        self.run.setText(QCoreApplication.translate("MainWindow", u"\u6267\u884c", None))
        self.right.setTitle(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u9884\u89c8", None))
        self.labelSelectedNum.setText(QCoreApplication.translate("MainWindow", u"\u5f20\u5df2\u9009", None))
        self.clearSelected.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664\u5df2\u9009", None))
        self.clearAll.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664\u6240\u6709", None))
    # retranslateUi

