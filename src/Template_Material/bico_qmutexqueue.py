"""
Bico_QMutexQueue Module
=======================

This module provides a thread-safe queue implementation using Qt's mutex mechanism.
It is designed for safe communication between threads in PyQt/PySide6 applications.

Main Class:
- Bico_QMutexQueue: A mutex-protected queue for inter-thread messaging.

Usage:
------
Import and use Bico_QMutexQueue to safely pass messages between threads.

Example:
    from Template_Material.bico_qmutexqueue import Bico_QMutexQueue
    queue = Bico_QMutexQueue()
    queue.put(item)
    item = queue.get()

Classes
-------
Bico_QMutexQueue
    A thread-safe queue implementation using Qt's mutex for synchronization.
"""

from PySide6.QtCore import QMutex, QMutexLocker
from collections import deque

class Bico_QMutexQueue(deque):
    pass
    def __init__(self, items = []):
        deque.__init__(self, items)
        self._mutex = QMutex()

    def enqueue(self, item):
        self._mutex.lock()
        self.append(item)
        self._mutex.unlock()

    def enqueueToBack(self, item):
        self._mutex.lock()
        self.appendleft(item)
        self._mutex.unlock()
    
    def dequeue(self):
        self._mutex.lock()
        # if data available in queue
        if len(self) > 0:
            item = self.popleft()
            sucessful = 1
        else:
            item = None
            sucessful = 0
        self._mutex.unlock()
        return item, sucessful

    def dequeueFromFront(self):
        self._mutex.lock()
        # if data available in queue
        if len(self) > 0:
            item = self.pop()
            sucessful = 1
        else:
            item = None
            sucessful = 0
        self._mutex.unlock()
        return item, sucessful