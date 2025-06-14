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

import sys
import os

from PySide6.QtCore import QMutex, Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow

from Template_Material.bico_qwindowthread import Bico_QWindowThread
from Template_Material.bico_qmutexqueue import Bico_QMutexQueue
from Template_Material.bico_qmessdata import Bico_QMessData


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

    def closeEvent(self, event):
        """
        Handle the window close event by requesting thread termination.

        :param event: QCloseEvent
        """
        event.ignore()
        self.toThread.emit("terminate", "")

    def create(custom_class=None, obj_name="", thread=None, parent=None):
        """
        Factory method to create and register a new UI instance.

        :param custom_class: The UI class to instantiate.
        :param obj_name: UI instance name.
        :param thread: Associated worker thread.
        :param parent: Parent widget.
        :return: UI instance or None if already exists.
        """
        if (__class__.ui_thread_hash.get(obj_name) == None):
            return custom_class(obj_name, thread, parent)
        else:
            return None

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
        __class__.ui_thread_hash_mutex.lock()
        __class__.ui_thread_hash.pop(obj_name)
        __class__.ui_thread_hash_mutex.unlock()

    @Slot(str, "QVariant")
    def fromThread(self, mess, data):
        """
        Handle messages sent from the worker thread.

        :param mess: Message type.
        :param data: Message data.
        """
        self.fromThreadHandling(mess, data)