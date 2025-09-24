"""
bico_qwindowthread.py
=====================

Defines the Bico_QWindowThread class, which manages a worker thread with input/output queues and UI integration.

.. uml::

   @startuml
   class Bico_QWindowThread {
       +setMainApp(app)
       +create(...)
       +getThreadHash()
       +run()
       +MainTask()
       +fromUI(mess, data)
   }
   Bico_QWindowThread --> Bico_QMutexQueue
   Bico_QWindowThread --> Bico_QWindowThread_UI
   @enduml
"""

from PySide6.QtCore import QThread, QMutex, Signal, Slot

from .PyQtLib_Project_Template import Bico_QThread
from .PyQtLib_Project_Template import Bico_QMessData

class Bico_QWindowThread(QThread, Bico_QThread):
    """
    Worker thread class for window logic and communication.

    :cvar thread_hash: Dictionary of thread instances.
    :cvar thread_hash_mutex: Mutex for thread hash access.
    :cvar main_app: Reference to the QApplication instance.
    :cvar toUI: Signal for sending messages to the UI.

    :ivar _ui: Reference to the associated UI object.
    """

    thread_hash = {}
    thread_hash_mutex = QMutex()
    main_app = None
    toUI = Signal(str, "QVariant")

    def __init__(self, qin=None, qin_owner=0, qout=None, qout_owner=0, obj_name="", ui=None, parent=None):
        """
        Initialize the window thread.

        :param qin: Input queue.
        :param qin_owner: Ownership flag for input queue.
        :param qout: Output queue.
        :param qout_owner: Ownership flag for output queue.
        :param obj_name: Name for this thread instance.
        :param ui: Associated UI object.
        :param parent: Parent QObject.
        """
        QThread.__init__(self, parent)
        Bico_QThread.__init__(self, qin, qin_owner, qout, qout_owner)
        self.setObjectName(obj_name)
        __class__.thread_hash_mutex.lock()
        __class__.thread_hash[obj_name] = self
        __class__.thread_hash_mutex.unlock()
        self.finished.connect(lambda: __class__.selfRemove(obj_name))
        self._ui = ui
        if (self._ui != None):
            if self._ui.getThread() == None:
                self._ui.setThread(self)
            self.toUI.connect(self._ui.fromThread)
            self._ui.toThread.connect(self.fromUI)

    def __del__(self):
        """
        Destructor. Exits the application if all threads are finished.
        """
        if not __class__.thread_hash:
            if __class__.main_app != None:
                __class__.main_app.exit(0)

    def start(self, priority=QThread.InheritPriority):
        """
        Start the thread and show the UI if hidden.

        :param priority: Thread priority.
        """
        QThread.start(self, priority)
        if (self._ui != None):
            if (self._ui.isHidden()):
                self._ui.show()

    def MainTask(self):
        """
        Virtual method to be implemented in the subclass.
        Should return 0 to stop the thread, or 1 to continue.
        """
        return 0

    def run(self):
        """
        Main thread execution loop.
        Calls MainTask repeatedly until it returns 0.
        """
        while True:
            if(not self.MainTask()):  
                break

    def create(custom_class=None, qin=None, qin_owner=0, qout=None, qout_owner=0, obj_name="", ui=None, parent=None):
        """
        Factory method to create and register a new thread.

        :param custom_class: The thread class to instantiate.
        :param qin: Input queue.
        :param qin_owner: Ownership flag for input queue.
        :param qout: Output queue.
        :param qout_owner: Ownership flag for output queue.
        :param obj_name: Thread name.
        :param ui: Optional UI instance.
        :param parent: Parent QObject.
        :return: Thread instance or None if already exists.
        """
        if (__class__.thread_hash.get(obj_name) == None):
            return custom_class(qin, qin_owner, qout, qout_owner, obj_name, ui, parent)
        else:
            return None

    def remove(obj_name=""):
        """
        Request termination of a thread by name.

        :param obj_name: Name of the thread to remove.
        :return: 1 if removed, 0 if not found.
        """
        if (__class__.thread_hash.get(obj_name) != None):
            mess_data = Bico_QMessData("terminate", "")
            __class__.thread_hash[obj_name].qinEnqueue(mess_data)
            return 1
        return 0

    def getThreadHash():
        """
        Get the dictionary of all registered threads.

        :return: Dictionary of thread instances.
        """
        return __class__.thread_hash

    def getMainApp():
        """
        Get the QApplication instance.

        :return: QApplication instance.
        """
        return __class__.main_app

    def setMainApp(app):
        """
        Set the QApplication instance.

        :param app: QApplication instance.
        """
        __class__.main_app = app

    def getUi(self):
        """
        Get the associated UI object.

        :return: UI object.
        """
        return self._ui

    def setUi(self, ui):
        """
        Set the associated UI object.

        :param ui: UI object.
        """
        self._ui = ui

    @Slot(str)
    def selfRemove(obj_name):
        """
        Remove a thread from the registry and clean up its UI.

        :param obj_name: Name of the thread to remove.
        """
        if (__class__.thread_hash.get(obj_name)._ui != None):
            __class__.thread_hash.get(obj_name)._ui.setThread(None)
            __class__.thread_hash.get(obj_name)._ui = None
            __class__.thread_hash.get(obj_name).toUI.emit("terminate", "")
        __class__.thread_hash_mutex.lock()
        __class__.thread_hash.pop(obj_name)
        __class__.thread_hash_mutex.unlock()

    @Slot(str, "QVariant")
    def fromUI(self, mess, data):
        """
        Handle messages sent from the UI.

        :param mess: Message type.
        :param data: Message data.
        """
        mess_data = Bico_QMessData()
        mess_data.setMess(mess)
        mess_data.setData(data)
        self.qinEnqueue(mess_data)
