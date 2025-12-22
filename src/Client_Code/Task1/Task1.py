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
    count = 0

    def __init__(self, qin=None, qin_owner=0, qout=None, qout_owner=0, obj_name="", ui=None, parent=None):
        """
        Initialize Task1 thread with message handlers.
        
        Parameters
        ----------
        qin : Bico_QMutexQueue, optional
            Input queue for the thread.
        qin_owner : int, optional
            Ownership flag for input queue.
        qout : Bico_QMutexQueue, optional
            Output queue for the thread.
        qout_owner : int, optional
            Ownership flag for output queue.
        obj_name : str
            Name/identifier for the thread object.
        ui : Bico_QWindowThread_UI, optional
            UI thread associated with this window thread.
        parent : QObject, optional
            Parent QObject for parent-child relationship.
        """
        # Call parent class __init__
        super().__init__(qin, qin_owner, qout, qout_owner, obj_name, ui, parent)
        
        # Message handler dictionary - cleaner than if-else chains
        self.message_handlers = {
            "terminate": self._handle_terminate,
            "mess_from_ui": self._handle_mess_from_ui,
            "create": self._handle_create,
            "create_child": self._handle_create_child,
            "from_another_thread": self._handle_from_another_thread,
        }

    def cleanupChildren(self):
        """
        Cleanup child threads before this thread is destroyed.
        """
        # Get all children from this QObject's children() and terminate them
        child_list = self.children()
        for child in child_list:
            thread = child
            mess_data = Bico_QMessData("terminate", "")
            thread.qinEnqueue(mess_data)
            
            # Wait for child thread to finish
            if thread.isRunning():
                thread.wait(5000)  # Wait up to 5 seconds

    def MainTask(self):
        """
        Main logic for the sample window thread.

        Processes messages from the input queue and demonstrates inter-thread communication.

        :return: 1 to continue running, 0 to terminate.
        """
        continue_to_run = 1
        input, result = self.qinDequeue()

        if result:
            mess = input.mess()
            data = input.data()
            
            # Use the message handler dictionary from __init__
            handler = self.message_handlers.get(mess)
            if handler:
                continue_to_run = handler(data, input)

        print("Hello from " + self.objectName())
        print("Num of running thread: " + str(len(Bico_QWindowThread.getThreadHash())))
        print("Num of running UI: " + str(len(Bico_QWindowThread_UI.getUIThreadHash())))
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


    def _handle_terminate(self, data, input_msg_queue):
        """Handle terminate message."""
        self.cleanupChildren()
        return 0  # Signal to stop running

    def _handle_mess_from_ui(self, data, input_msg_queue):
        """Handle mess_from_ui message."""
        print("From UI: " + self.objectName() + " mess_from_ui " + str(data))
        self.toUI.emit("change_button_text", str(random.randint(0, 2147483647)))
        return 1

    def _handle_create(self, data, input_msg_queue):
        """Handle create message to create sibling thread."""
        print(self.objectName() + " create ")
        # Create and start a new window thread with its UI (as sibling)
        __class__.count = __class__.count + 1
        thread_name = "task_" + str(__class__.count)
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
        return 1

    def _handle_create_child(self, data, input_msg_queue):
        """Handle create_child message to create child thread."""
        print(self.objectName() + " create_child ")
        # Create and start a new window thread with its UI (as child of this thread)
        __class__.count = __class__.count + 1
        thread_name = "child_task_" + str(__class__.count)
        Bico_QWindowThread.create(
            Task1,
            Bico_QMutexQueue(),
            1,
            Bico_QMutexQueue(),
            1,
            thread_name,
            Bico_QWindowThread_UI.create(Task1_UI, thread_name),
            self
        )
        Bico_QWindowThread.getThreadHash()[thread_name].start()
        return 1

    def _handle_from_another_thread(self, data, input_msg_queue):
        """Handle from_another_thread message."""
        print(self.objectName() + " from_another_thread: " + input_msg_queue.src() + " - " + str(data))
        return 1