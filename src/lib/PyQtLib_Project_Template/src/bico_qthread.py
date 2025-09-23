"""
bico_qthread.py
===============

Defines Bico_QThread, a base class for thread logic with input/output queues.

.. uml::

   @startuml
   class Bico_QThread {
       - _qin: Bico_QMutexQueue
       - _qout: Bico_QMutexQueue
       +qin()
       +setQin(qin)
       +qout()
       +setQout(qout)
       +qinEnqueue(item)
       +qinEnqueueToBack(item)
       +qinDequeue()
       +qinDequeueFromFront()
       +qoutEnqueue(item)
       +qoutEnqueueToBack(item)
   }
   @enduml
"""

from .bico_qmessdata import Bico_QMessData
from .bico_qmutexqueue import Bico_QMutexQueue

class Bico_QThread:
    """
    Base class for thread logic with input/output queues.
    """
    def __init__(self, qin:Bico_QMutexQueue = None, qin_owner:bool = False, qout:Bico_QMutexQueue = None, qout_owner:bool = False):
        """
        :param qin: Input queue
        :param qin_owner: Ownership flag for input queue
        :param qout: Output queue
        :param qout_owner: Ownership flag for output queue
        """
        self._qin = qin
        self._qin_owner = qin_owner
        self._qout = qout
        self._qout_owner = qout_owner

    def qin(self) -> Bico_QMutexQueue:
        """Get the input queue."""
        return self._qin

    def setQin(self, qin:Bico_QMutexQueue):
        """Set the input queue."""
        self._qin = qin

    def qout(self) -> Bico_QMutexQueue:
        """Get the output queue."""
        return self._qout

    def setQout(self, qout:Bico_QMutexQueue):
        """Set the output queue."""
        self._qout = qout

    def qinEnqueue(self, item):
        """Enqueue an item to the input queue."""
        if not (self._qin == None):
            self._qin.enqueue(item)
            return 1
        return 0

    def qinEnqueueToBack(self, item):
        """Enqueue an item to the back of the input queue."""
        if not (self._qin == None):
            self._qin.enqueueToBack(item)
            return 1
        return 0

    def qinDequeue(self):
        """Dequeue an item from the input queue."""
        if not (self._qin == None):
            return self._qin.dequeue()
        return None, 0

    def qinDequeueFromFront(self):
        """Dequeue an item from the front of the input queue."""
        if not (self._qin == None):
            return self._qin.dequeueFromFront()
        return None, 0

    def qoutEnqueue(self, item):
        """Enqueue an item to the output queue."""
        if not (self._qout == None):
            self._qout.enqueue(item)
            return 1
        return 0

    def qoutEnqueueToBack(self, item):
        """Enqueue an item to the back of the output queue."""
        if not (self._qout == None):
            self._qout.enqueueToBack(item)
            return 1
        return 0
