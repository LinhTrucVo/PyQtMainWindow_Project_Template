"""
bico_qmutexqueue.py
===================

Defines Bico_QMutexQueue, a thread-safe queue for inter-thread communication.

.. uml::

   @startuml
   class Bico_QMutexQueue {
       +enqueue(item)
       +enqueueToBack(item)
       +dequeue()
       +dequeueFromFront()
   }
   @enduml
"""

from PySide6.QtCore import QMutex, QMutexLocker
from collections import deque

class Bico_QMutexQueue(deque):
    """
    Thread-safe queue using QMutex for synchronization.
    Inherits from collections.deque.
    """
    def __init__(self, items = []):
        """
        Initialize the queue.

        :param items: Optional initial items.
        """
        deque.__init__(self, items)
        self._mutex = QMutex()

    def enqueue(self, item):
        """Add an item to the queue (thread-safe)."""
        self._mutex.lock()
        self.append(item)
        self._mutex.unlock()

    def enqueueToBack(self, item):
        """Add an item to the back of the queue (thread-safe)."""
        self._mutex.lock()
        self.appendleft(item)
        self._mutex.unlock()

    def dequeue(self):
        """
        Remove and return an item from the front of the queue (thread-safe).

        :return: (item, success_flag)
        """
        self._mutex.lock()
        if len(self) > 0:
            item = self.popleft()
            sucessful = 1
        else:
            item = None
            sucessful = 0
        self._mutex.unlock()
        return item, sucessful

    def dequeueFromFront(self):
        """
        Remove and return an item from the back of the queue (thread-safe).

        :return: (item, success_flag)
        """
        self._mutex.lock()
        if len(self) > 0:
            item = self.pop()
            sucessful = 1
        else:
            item = None
            sucessful = 0
        self._mutex.unlock()
        return item, sucessful