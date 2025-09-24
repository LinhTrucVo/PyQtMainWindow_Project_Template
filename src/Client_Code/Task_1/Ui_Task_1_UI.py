# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Task_1_UI.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
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
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QWidget)

"""
Ui_Task_1_UI module.
Auto-generated UI class for the sample window UI.
"""

class Ui_Task_1_UI(object):
    def setupUi(self, Task_1_UI):
        if not Task_1_UI.objectName():
            Task_1_UI.setObjectName(u"Task_1_UI")
        Task_1_UI.resize(474, 334)
        self.centralwidget = QWidget(Task_1_UI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(190, 50, 81, 41))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(190, 130, 81, 41))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(190, 200, 81, 41))
        Task_1_UI.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Task_1_UI)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 474, 22))
        Task_1_UI.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Task_1_UI)
        self.statusbar.setObjectName(u"statusbar")
        Task_1_UI.setStatusBar(self.statusbar)

        self.retranslateUi(Task_1_UI)

        QMetaObject.connectSlotsByName(Task_1_UI)
    # setupUi

    def retranslateUi(self, Task_1_UI):
        Task_1_UI.setWindowTitle(QCoreApplication.translate("Task_1_UI", u"Bico_QWidgetThread_UI_Example", None))
        self.pushButton.setText(QCoreApplication.translate("Task_1_UI", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("Task_1_UI", u"1", None))
        self.pushButton_3.setText(QCoreApplication.translate("Task_1_UI", u"2", None))
    # retranslateUi

