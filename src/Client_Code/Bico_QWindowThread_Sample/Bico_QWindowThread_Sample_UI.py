"""
Bico_QWindowThread_Sample_UI module.
Defines a sample UI class for demonstration purposes.
"""

import sys
import os

from PySide6.QtCore import QSize, Slot
from PySide6.QtWidgets import QApplication

from Client_Code.Bico_QWindowThread_Sample.Data_Object.Example_Data_Object import Example_Data_Object
from Client_Code.Bico_QWindowThread_Sample.Ui_Bico_QWindowThread_Sample_UI import Ui_Bico_QWindowThread_Sample_UI
from Template_Material.bico_qwindowthread_ui import Bico_QWindowThread_UI
from Template_Material.bico_qmutexqueue import Bico_QMutexQueue
from Template_Material.bico_qmessdata import Bico_QMessData


class Bico_QWindowThread_Sample_UI(Bico_QWindowThread_UI):
    def __init__(self, obj_name="", thread=None, parent=None):
        Bico_QWindowThread_UI.__init__(self, obj_name, thread, parent)
        self.ui = Ui_Bico_QWindowThread_Sample_UI()
        self.ui.setupUi(self)
        self.moreUISetup()

    # more setting up when the ui started
    def moreUISetup(self):
        self.ui.pushButton.resize(QSize(100, 50))

    def fromThreadHandling(self, mess, data):
        if(mess == "show"):
            self.show()
        elif (mess == "hide"):
            self.hide()
        elif (mess == "terminate"):
            self.TERMINATE.emit()
        elif (mess == "change_button_text"):
            self.ui.pushButton.setText(data)

    @Slot()
    def on_pushButton_clicked(self):
        self.toThread.emit("mess_from_ui", "button_clicked")

    @Slot()
    def on_pushButton_2_clicked(self):
        self.toThread.emit("num1", "111")

    @Slot()
    def on_pushButton_3_clicked(self):
        self.toThread.emit("num2", "222")
