"""
Task1.py
============================

Sample implementation of a window thread for demonstration purposes.

.. uml::

   @startuml
   class Task1 {
       +MainTask()
   }
   Task1 --|> Bico_QWindowThread
   @enduml
"""

from PySide6.QtWidgets import QPushButton

from lib import Bico_QMessData
from lib import Bico_QWindowThread
from .Data_Object.Task1_Data import Task1_Data


class Task1(Bico_QWindowThread):
    """
    Example subclass of Bico_QWindowThread for demonstration.

    Implements the main task logic for the sample window thread.

    :cvar i: Counter for demonstration.
    :cvar ex_data_obj: Example data object.
    """

    i = 0
    ex_data_obj = Task1_Data()

    def MainTask(self):
        """
        Main logic for the sample window thread.

        Processes messages from the input queue and demonstrates inter-thread communication.

        :return: 1 to continue running, 0 to terminate.
        """
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
        self.msleep(100)

        if ((self.objectName() == "task_1") and (Bico_QWindowThread.getThreadHash().get("task_0") != None)):
            self.i += 1
            mess_data = Bico_QMessData("from_another_thread", self.i)
            mess_data.setSrc(self.objectName())
            Bico_QWindowThread.getThreadHash().get("task_0").qinEnqueue(mess_data)
            self.msleep(236)

            # internally delete a thread
            # mess_data = Bico_QMessData("terminate", "")
            # mess_data.setSrc(self.objectName())
            # Bico_QWindowThread.getThreadHash().get("task_0").qinEnqueue(mess_data)

        return continue_to_run