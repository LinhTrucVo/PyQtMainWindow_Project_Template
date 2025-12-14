"""
bico_qwindowthread_ui.py
========================

Defines the Bico_QWindowThread_UI class, a base class for UI logic associated with a worker thread.

.. uml::

   @startuml
   class Bico_QWindowThread_UI {
       +create(...)
       +getUIThreadHash()
       +getThread()
       +setThread(thread)
       +fromThreadHandling(mess, data)
       +fromThread(mess, data)
   }
   Bico_QWindowThread_UI --> Bico_QWindowThread
   @enduml
"""

from PySide6.QtCore import QMutex, Signal, Slot, QObject, QMetaObject, Qt, QCoreApplication, QThread
from PySide6.QtWidgets import QMainWindow


class UIFactory(QObject):
    """Helper class that lives in the main thread to create UI instances safely."""
    
    def __init__(self):
        super().__init__()
        self.created_ui = None  # Store the last created UI for BlockingQueuedConnection
        self.pending_params = None  # Store parameters to avoid Q_ARG issues
    
    @Slot()
    def createUI(self):
        """
        Create a new UI in the main thread using pending parameters.
        This slot takes no arguments to avoid Q_ARG type issues.
        Parameters are stored in self.pending_params before calling.
        """
        if self.pending_params is None:
            return
        
        custom_class, obj_name, thread, parent = self.pending_params
        
        # Create UI directly (we're already in main thread)
        self.created_ui = custom_class(obj_name, thread, parent)
        
        # Clear pending params
        self.pending_params = None
        
        return self.created_ui


class Bico_QWindowThread_UI(QMainWindow):
    """
    Base class for window UI logic in a threaded application.

    :cvar UI_NAME_PREFIX: Prefix for UI object names.
    :cvar ui_thread_hash: Dictionary of UI thread instances.
    :cvar ui_thread_hash_mutex: Mutex for UI thread hash access.
    :cvar toThread: Signal for sending messages to the thread.
    :cvar TERMINATE: Signal for UI termination.
    :ivar _thread: Reference to the associated worker thread.
    """

    UI_NAME_PREFIX = "ui_"
    ui_thread_hash = {}
    ui_thread_hash_mutex = QMutex()
    _ui_factory = None
    toThread = Signal(str, "QVariant")
    TERMINATE = Signal()

    def __init__(self, obj_name="", thread=None, parent=None):
        """
        Initialize the UI window.

        :param obj_name: Name for this UI instance.
        :param thread: Associated worker thread.
        :param parent: Parent widget.
        """
        QMainWindow.__init__(self, parent)
        self.setObjectName(__class__.UI_NAME_PREFIX + obj_name)
        __class__.ui_thread_hash_mutex.lock()
        __class__.ui_thread_hash[__class__.UI_NAME_PREFIX + obj_name] = self
        __class__.ui_thread_hash_mutex.unlock()
        self.TERMINATE.connect(lambda: __class__.selfRemove(__class__.UI_NAME_PREFIX + obj_name))
        self._thread = thread
        if (self._thread != None):
            if (self._thread.getUi() == None):
                self._thread.setUi(self)
                self.toThread.connect(self._thread.fromUI)
                self._thread.toUI.connect(self.fromThread)

    def __del__(self):
        """
        Destructor for UI window.
        """
        pass

    def show(self):
        """
        Show the UI window and start the thread if not running.
        """
        QMainWindow.show(self)
        if (self._thread != None):
            if (self._thread.isRunning() == False):
                self._thread.start()

    def create(custom_class=None, obj_name="", thread=None, parent=None):
        """
        Factory method to create and register a new UI instance.
        Automatically handles thread-safety by using QMetaObject.invokeMethod 
        to create in main thread when called from a worker thread.

        :param custom_class: The UI class to instantiate.
        :param obj_name: UI instance name.
        :param thread: Associated worker thread.
        :param parent: Parent widget.
        :return: UI instance or None if already exists.
        """
        if (__class__.ui_thread_hash.get(__class__.UI_NAME_PREFIX + obj_name) != None):
            return None
        
        # Check if we're in the main thread
        main_thread = QCoreApplication.instance().thread()
        current_thread = QThread.currentThread()
        
        if current_thread == main_thread:
            # We're in the main thread, create directly
            return custom_class(obj_name, thread, parent)
        else:
            # We're in a worker thread, use QMetaObject.invokeMethod to create in main thread
            # Store parameters in the factory object first (avoids Q_ARG type issues)
            factory = Bico_QWindowThread_UI.getUIFactory()
            factory.created_ui = None
            factory.pending_params = (custom_class, obj_name, thread, parent)
            
            # Use BlockingQueuedConnection to wait for the UI to be created
            # Call with no arguments - parameters are already stored
            QMetaObject.invokeMethod(
                factory,
                "createUI",
                Qt.BlockingQueuedConnection
            )
            
            # Return the created UI
            return factory.created_ui

    @staticmethod
    def initializeFactory():
        """
        Initialize UI factory in the main thread.
        This MUST be called from the main thread before any worker threads are created.
        """
        if Bico_QWindowThread_UI._ui_factory is None:
            Bico_QWindowThread_UI._ui_factory = UIFactory()

    @staticmethod
    def getUIFactory():
        """
        Get the UI factory instance.

        :return: UIFactory instance.
        """
        return Bico_QWindowThread_UI._ui_factory

    def getUIThreadHash():
        """
        Get the dictionary of all registered UI threads.

        :return: Dictionary of UI thread instances.
        """
        return __class__.ui_thread_hash

    def getThread(self):
        """
        Get the associated worker thread.

        :return: Thread instance.
        """
        return self._thread

    def setThread(self, thread):
        """
        Set the associated worker thread.

        :param thread: Thread instance.
        """
        self._thread = thread

    def fromThreadHandling(self, mess, data):
        """
        Virtual method to be implemented in the subclass.
        Handles messages sent from the worker thread.

        :param mess: Message type.
        :param data: Message data.
        :return: 0 by default.
        """
        return 0

    @Slot(str)
    def selfRemove(obj_name):
        """
        Remove a UI thread from the registry.

        :param obj_name: Name of the UI thread to remove.
        """
        ui = __class__.ui_thread_hash.get(obj_name)
        if ui is None:
            return
        
        __class__.ui_thread_hash_mutex.lock()
        __class__.ui_thread_hash.pop(obj_name).deleteLater()
        __class__.ui_thread_hash_mutex.unlock()

    @Slot(str, "QVariant")
    def fromThread(self, mess, data):
        """
        Handle messages sent from the worker thread.

        :param mess: Message type.
        :param data: Message data.
        """
        self.fromThreadHandling(mess, data)