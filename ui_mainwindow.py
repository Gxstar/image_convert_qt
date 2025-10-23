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
        MainWindow.resize(783, 660)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
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
        self.addImages = QPushButton(self.inputBox)
        self.addImages.setObjectName(u"addImages")

        self.verticalLayout.addWidget(self.addImages)

        self.addDirs = QPushButton(self.inputBox)
        self.addDirs.setObjectName(u"addDirs")

        self.verticalLayout.addWidget(self.addDirs)


        self.left.addWidget(self.inputBox)

        self.outputBox = QGroupBox(self.centralwidget)
        self.outputBox.setObjectName(u"outputBox")
        self.verticalLayout_4 = QVBoxLayout(self.outputBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.format = QVBoxLayout()
        self.format.setSpacing(4)
        self.format.setObjectName(u"format")
        self.outFormatTitle = QLabel(self.outputBox)
        self.outFormatTitle.setObjectName(u"outFormatTitle")

        self.format.addWidget(self.outFormatTitle)

        self.formatSelection = QComboBox(self.outputBox)
        self.formatSelection.setObjectName(u"formatSelection")
        self.formatSelection.setAcceptDrops(False)

        self.format.addWidget(self.formatSelection)


        self.verticalLayout_4.addLayout(self.format)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.outDirTitle = QLabel(self.outputBox)
        self.outDirTitle.setObjectName(u"outDirTitle")

        self.horizontalLayout_5.addWidget(self.outDirTitle)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.outDirSelect = QToolButton(self.outputBox)
        self.outDirSelect.setObjectName(u"outDirSelect")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderNew))
        self.outDirSelect.setIcon(icon)

        self.horizontalLayout_5.addWidget(self.outDirSelect)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.outputBox)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.horizontalLayout.setStretch(0, 8)

        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_5)

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


        self.verticalLayout_4.addLayout(self.quality)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.isReplace = QCheckBox(self.outputBox)
        self.isReplace.setObjectName(u"isReplace")

        self.verticalLayout_4.addWidget(self.isReplace)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


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
        self.right.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.right)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.toolbarWidget = QWidget(self.right)
        self.toolbarWidget.setObjectName(u"toolbarWidget")
        self.toolbarWidget.setStyleSheet(u"")
        self.horizontalLayout_4 = QHBoxLayout(self.toolbarWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.selectedNum = QLCDNumber(self.toolbarWidget)
        self.selectedNum.setObjectName(u"selectedNum")
        self.selectedNum.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.selectedNum)

        self.labelSelectedNum = QLabel(self.toolbarWidget)
        self.labelSelectedNum.setObjectName(u"labelSelectedNum")
        self.labelSelectedNum.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.labelSelectedNum)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.clearSelected = QToolButton(self.toolbarWidget)
        self.clearSelected.setObjectName(u"clearSelected")
        self.clearSelected.setStyleSheet(u"")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.clearSelected.setIcon(icon1)

        self.horizontalLayout_4.addWidget(self.clearSelected)

        self.clearAll = QToolButton(self.toolbarWidget)
        self.clearAll.setObjectName(u"clearAll")
        self.clearAll.setStyleSheet(u"")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditClear))
        self.clearAll.setIcon(icon2)

        self.horizontalLayout_4.addWidget(self.clearAll)


        self.verticalLayout_3.addWidget(self.toolbarWidget)

        self.imageList = QListView(self.right)
        self.imageList.setObjectName(u"imageList")
        self.imageList.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.imageList)


        self.horizontalLayout_3.addWidget(self.right)

        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(u"")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 783, 33))
        self.menubar.setStyleSheet(u"")
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
        self.outDirSelect.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u76ee\u5f55", None))
        self.qualityTitle.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u8d28\u91cf", None))
        self.qualityShow.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>100</p></body></html>", None))
        self.isReplace.setText(QCoreApplication.translate("MainWindow", u"\u662f\u5426\u66ff\u6362\u540c\u540d\u6587\u4ef6", None))
        self.run.setText(QCoreApplication.translate("MainWindow", u"\u6267\u884c", None))
        self.right.setTitle(QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u9884\u89c8", None))
        self.labelSelectedNum.setText(QCoreApplication.translate("MainWindow", u"\u5f20\u5df2\u9009", None))
#if QT_CONFIG(tooltip)
        self.clearSelected.setToolTip(QCoreApplication.translate("MainWindow", u"\u6e05\u9664\u9009\u4e2d\u56fe\u7247", None))
#endif // QT_CONFIG(tooltip)
        self.clearSelected.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664\u5df2\u9009", None))
#if QT_CONFIG(tooltip)
        self.clearAll.setToolTip(QCoreApplication.translate("MainWindow", u"\u6e05\u9664\u6240\u6709\u56fe\u7247", None))
#endif // QT_CONFIG(tooltip)
        self.clearAll.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664\u6240\u6709", None))
    # retranslateUi

