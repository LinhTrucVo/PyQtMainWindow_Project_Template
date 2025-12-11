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
from lib import Bico_QMutexQueue
from lib import Bico_QWindowThread_UI
from .Data_Object.Task1_Data import Task1_Data
from .Task1_UI import Task1_UI
import random


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
            elif (mess == "mess_from_ui"):
                print("From UI: " + self.objectName() + " " + mess + " " + str(data))
                self.toUI.emit("change_button_text", str(random.randint(0, 2147483647)))
            elif (mess == "create"):
                print(self.objectName() + " " + mess + " ")
                # Create and start two window threads with their UIs
                thread_name = "task_" + str(random.randint(1000, 9999))
                Bico_QWindowThread.create(
                    Task1,
                    Bico_QMutexQueue(),
                    1,
                    Bico_QMutexQueue(),
                    1,
                    thread_name,
                    Bico_QWindowThread_UI.create(Task1_UI, thread_name)
                )
                Bico_QWindowThread.getThreadHash()[thread_name].start()
            elif (mess == "create_child"):
                print(self.objectName() + " " + mess + " ")
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
            self.msleep(236)

            # internally delete a thread
            # mess_data = Bico_QMessData("terminate", "")
            # mess_data.setSrc(self.objectName())
            # Bico_QWindowThread.getThreadHash().get("task_0").qinEnqueue(mess_data)

        return continue_to_run