"""
Bico_QWindowThread_UI Module
===========================

This module provides UI thread management for window creation and integration in PyQt/PySide6 applications.
It acts as a bridge between the main application and custom UI components, enabling dynamic UI updates from worker threads.

Main Class:
- Bico_QWindowThread_UI: Manages UI thread and window association.

Usage:
------
Import and use Bico_QWindowThread_UI to create and manage UI threads for your windows.

Example:
    from Template_Material.bico_qwindowthread_ui import Bico_QWindowThread_UI
    ui_thread = Bico_QWindowThread_UI.create(...)
"""
import sys
import os

module_path = os.path.abspath(os.path.join(os.getcwd(), "../../Common/Template_Material"))
sys.path.append(module_path)
current_path = os.getcwd()

from PySide6.QtCore import QMutex, Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow

from Template_Material.bico_qwindowthread import Bico_QWindowThread
from Template_Material.bico_qmutexqueue import Bico_QMutexQueue
from Template_Material.bico_qmessdata import Bico_QMessData


class Bico_QWindowThread_UI(QMainWindow):
    UI_NAME_PREFIX = "ui_"
    ui_thread_hash = {}
    ui_thread_hash_mutex = QMutex()
    toThread = Signal(str, "QVariant")
    TERMINATE = Signal()

    def __init__(self, obj_name="", thread=None, parent=None):
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
        pass

    def show(self):
        QMainWindow.show(self)
        if (self._thread != None):
            if (self._thread.isRunning() == False):
                self._thread.start()

    def closeEvent(self, event):
        event.ignore()
        self.toThread.emit("terminate", "")

    def create(custom_class=None, obj_name="", thread=None, parent=None):
        if (__class__.ui_thread_hash.get(obj_name) == None):
            return custom_class(obj_name, thread, parent)
        else:
            return None

    def getUIThreadHash():
        return __class__.ui_thread_hash

    def getThread(self):
        return self._thread

    def setThread(self, thread):
        self._thread = thread

    # Virtual method which will be implemented in the subclass
    def fromThreadHandling(self, mess, data):
        return 0


    @Slot(str)
    def selfRemove(obj_name):
        __class__.ui_thread_hash_mutex.lock()
        __class__.ui_thread_hash.pop(obj_name)
        __class__.ui_thread_hash_mutex.unlock()

    @Slot(str, "QVariant")
    def fromThread(self, mess, data):
        self.fromThreadHandling(mess, data)