"""
Bico_QWindowThread_Sample module.
Defines a sample window thread class for demonstration purposes.
"""

import sys, os
from PySide6.QtWidgets import QApplication, QPushButton

from Template_Material.bico_qmessdata import Bico_QMessData
from Template_Material.bico_qmutexqueue import Bico_QMutexQueue
from Template_Material.bico_qwindowthread import Bico_QWindowThread
from Client_Code.Bico_QWindowThread_Sample.Data_Object.Example_Data_Object import Example_Data_Object


class Bico_QWindowThread_Sample(Bico_QWindowThread):
    i = 0
    ex_data_obj = Example_Data_Object()

    def MainTask(self):
        continue_to_run = 1
        i = 0
        input, result = self.qinDequeue()

        if result:
            mess = input.mess()
            data = input.data()
            if (mess == "terminate"):     
                continue_to_run = 0
            elif (mess == "num1"):
                print(self.objectName() + " " + mess + " " + str(self.ex_data_obj.getData_1()))
            elif (mess == "num2"):
                print(self.objectName() + " " + mess + " " + str(self.ex_data_obj.getData_2()))
            elif (mess == "text"):
                print(self.objectName() + " " + mess + " " + data)
                self.getChildWidget(QPushButton, "pushButton_4").setText("44")
            elif (mess == "size"):
                print(self.objectName() + " " + mess + " " + str(data.width()) + " " + str(data.height()))
                self.getChildWidget(QPushButton, "pushButton_5").setText("55")
            elif (mess == "from_another_thread"):
                print(self.objectName() + " " + mess + ": "  + input.src() + " - " + str(data))

        print("Hello from " + self.objectName())
        print("Num of running thread: " + str(len(Bico_QWindowThread.getThreadHash())))
        self.msleep(1000)

        if ((self.objectName() == "task_1") and (Bico_QWindowThread.getThreadHash().get("task_0") != None)):
            self.i += 1
            mess_data = Bico_QMessData("from_another_thread", self.i)
            mess_data.setSrc(self.objectName())
            Bico_QWindowThread.getThreadHash().get("task_0").qinEnqueue(mess_data)
            self.msleep(2365)

            # internally delete a thread
            # mess_data = Bico_QMessData("terminate", "")
            # mess_data.setSrc(self.objectName())
            # Bico_QWindowThread.getThreadHash().get("task_0").qinEnqueue(mess_data)

        return continue_to_run