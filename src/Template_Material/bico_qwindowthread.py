"""
Bico_QWindowThread Module
=========================

This module provides a thread-safe window management system for PyQt/PySide6 applications.
It allows creating and managing multiple windows in separate threads with proper synchronization.

Main Classes:
- Bico_QWindowThread: Manages window threads and their lifecycle.
- Bico_QThread: Base thread class for custom threaded tasks.
- Bico_QMutexQueue: Thread-safe message queue for inter-thread communication.
- Bico_QWindowThread_UI: Manages UI thread and window integration.
- Bico_QMessData: Message data structure for thread communication.

Usage:
------
Import and use Bico_QWindowThread to create and manage window threads in your PyQt/PySide6 application.

Example:
    from Template_Material.bico_qwindowthread import Bico_QWindowThread
    Bico_QWindowThread.create(...)
"""

import sys
import os

from PySide6.QtCore import QThread, QMutex, Signal, Slot
from PySide6.QtWidgets import QApplication

from Template_Material.bico_qthread import Bico_QThread
from Template_Material.bico_qmutexqueue import Bico_QMutexQueue
from Template_Material.bico_qmessdata import Bico_QMessData


class Bico_QWindowThread(QThread, Bico_QThread):
    thread_hash = {}
    thread_hash_mutex = QMutex()
    main_app = None
    toUI = Signal(str, "QVariant")

    def __init__(self, qin=None, qin_owner=0, qout=None, qout_owner=0, obj_name="", ui=None, parent=None):
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
        if not __class__.thread_hash:
            if __class__.main_app != None:
                __class__.main_app.exit(0)

    def start(self, priority=QThread.InheritPriority):
        QThread.start(self, priority)
        if (self._ui != None):
            if (self._ui.isHidden()):
                self._ui.show()

    # Virtual method which will be implemented in the subclass
    def MainTask(self):
        return 0

    def run(self):
        while True:
            if(not self.MainTask()):  
                break

    def create(custom_class=None, qin=None, qin_owner=0, qout=None, qout_owner=0, obj_name="", ui=None, parent=None):
        if (__class__.thread_hash.get(obj_name) == None):
            return custom_class(qin, qin_owner, qout, qout_owner, obj_name, ui, parent)
        else:
            return None

    def remove(obj_name=""):
        if (__class__.thread_hash.get(obj_name) != None):
            mess_data = Bico_QMessData("terminate", "")
            __class__.thread_hash[obj_name].qinEnqueue(mess_data)
            return 1
        return 0

    def getThreadHash():
        return __class__.thread_hash

    def getMainApp():
        return __class__.main_app

    def setMainApp(app):
        __class__.main_app = app

    def getUi(self):
        return self._ui

    def setUi(self, ui):
        self._ui = ui

    @Slot(str)
    def selfRemove(obj_name):
        if (__class__.thread_hash.get(obj_name)._ui != None):
            __class__.thread_hash.get(obj_name)._ui.setThread(None)
            __class__.thread_hash.get(obj_name)._ui = None
            __class__.thread_hash.get(obj_name).toUI.emit("terminate", "")
        __class__.thread_hash_mutex.lock()
        __class__.thread_hash.pop(obj_name)
        __class__.thread_hash_mutex.unlock()

    @Slot(str, "QVariant")
    def fromUI(self, mess, data):
        mess_data = Bico_QMessData()
        mess_data.setMess(mess)
        mess_data.setData(data)
        self.qinEnqueue(mess_data)
