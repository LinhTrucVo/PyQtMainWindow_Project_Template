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

from PySide6.QtCore import QThread, QMutex, Signal, Slot, QObject, QMetaObject, Qt, Q_ARG
from PySide6.QtCore import QCoreApplication

from .PyQtLib_Project_Template import Bico_QThread
from .PyQtLib_Project_Template import Bico_QMessData
from .PyQtLib_Project_Template import Bico_QMutexQueue


class ThreadFactory(QObject):
    """Helper class that lives in the main thread to create new threads safely."""
    
    def __init__(self):
        super().__init__()
        self.created_thread = None  # Store the last created thread for BlockingQueuedConnection
        self.pending_params = None  # Store parameters to avoid Q_ARG issues
    
    @Slot()
    def createThread(self):
        """
        Create a new thread in the main thread using pending parameters.
        This slot takes no arguments to avoid Q_ARG type issues.
        Parameters are stored in self.pending_params before calling.
        """
        if self.pending_params is None:
            return
        
        custom_class, qin, qin_owner, qout, qout_owner, obj_name, ui, parent = self.pending_params
        
        # Create thread directly (we're already in main thread)
        self.created_thread = custom_class(qin, qin_owner, qout, qout_owner, obj_name, ui, parent)
        
        # Clear pending params
        self.pending_params = None
        
        return self.created_thread


class UIShower(QObject):
    """Helper class to show UI widgets in the main thread."""
    
    def __init__(self):
        super().__init__()
        self.pending_ui = None
    
    @Slot()
    def showUI(self):
        """Show a UI widget in the main thread."""
        if self.pending_ui is not None and self.pending_ui.isHidden():
            self.pending_ui.show()
            self.pending_ui = None


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
    _thread_factory = None
    _ui_shower = None
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
                # Check if we're in the main thread
                main_thread = QCoreApplication.instance().thread()
                current_thread = QThread.currentThread()
                
                if current_thread == main_thread:
                    # We're in main thread, show directly
                    self._ui.show()
                else:
                    # We're in a worker thread, use QMetaObject.invokeMethod to show in main thread
                    ui_shower = Bico_QWindowThread.getUIShower()
                    ui_shower.pending_ui = self._ui
                    QMetaObject.invokeMethod(
                        ui_shower,
                        "showUI",
                        Qt.BlockingQueuedConnection
                    )

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
        Automatically handles thread-safety by using QMetaObject.invokeMethod 
        to create in main thread when called from a worker thread.

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
        
        if (__class__.thread_hash.get(obj_name) != None):
            return None
        
        # Check if we're in the main thread
        main_thread = QCoreApplication.instance().thread()
        current_thread = QThread.currentThread()
        
        if current_thread == main_thread:
            # We're in the main thread, create directly
            return custom_class(qin, qin_owner, qout, qout_owner, obj_name, ui, parent)
        else:
            # We're in a worker thread, use QMetaObject.invokeMethod to create in main thread
            # Store parameters in the factory object first (avoids Q_ARG type issues)
            factory = Bico_QWindowThread.getThreadFactory()
            factory.created_thread = None
            factory.pending_params = (custom_class, qin, qin_owner, qout, qout_owner, obj_name, ui, parent)
            
            # Use BlockingQueuedConnection to wait for the thread to be created
            # Call with no arguments - parameters are already stored
            QMetaObject.invokeMethod(
                factory,
                "createThread",
                Qt.BlockingQueuedConnection
            )
            # Return the created thread
            return factory.created_thread

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

    @staticmethod
    def initializeFactories():
        """
        Initialize global factory instances in the main thread.
        This MUST be called from the main thread before any worker threads are created.
        """
        if Bico_QWindowThread._thread_factory is None:
            Bico_QWindowThread._thread_factory = ThreadFactory()
        if Bico_QWindowThread._ui_shower is None:
            Bico_QWindowThread._ui_shower = UIShower()

    @staticmethod
    def getThreadFactory():
        """
        Get the thread factory instance.

        :return: ThreadFactory instance.
        """
        return Bico_QWindowThread._thread_factory

    @staticmethod
    def getUIShower():
        """
        Get the UI shower instance.

        :return: UIShower instance.
        """
        return Bico_QWindowThread._ui_shower

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
            __class__.thread_hash.get(obj_name)._ui.TERMINATE.emit()
            __class__.thread_hash.get(obj_name)._ui = None
            
        __class__.thread_hash_mutex.lock()
        __class__.thread_hash.pop(obj_name).deleteLater()
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
