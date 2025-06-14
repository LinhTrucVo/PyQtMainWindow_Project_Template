from Template_Material.bico_qmessdata import Bico_QMessData
from Template_Material.bico_qmutexqueue import Bico_QMutexQueue

class Bico_QThread:
    def __init__(self, qin:Bico_QMutexQueue = None, qin_owner:bool = False, qout:Bico_QMutexQueue = None, qout_owner:bool = False):
        self._qin = qin
        self._qin_owner = qin_owner
        self._qout = qout
        self._qout_owner = qout_owner

    def qin(self) -> Bico_QMutexQueue:
        return self._qin

    def setQin(self, qin:Bico_QMutexQueue):
        self._qin = qin
    
    def qout(self) -> Bico_QMutexQueue:
        return self._qout

    def setQin(self, qout:Bico_QMutexQueue):
        self._qout = qout

    def qinEnqueue(self, item):
        if not (self._qin == None):
            self._qin.enqueue(item)
            return 1
        return 0

    def qinEnqueueToBack(self, item):
        if not (self._qin == None):
            self._qin.enqueueToBack(item)
            return 1
        return 0

    def qinDequeue(self):
        if not (self._qin == None):
            return self._qin.dequeue()
        return None, 0

    def qinDequeueFromFront(self):
        if not (self._qin == None):
            return self._qin.dequeueFromFront()
        return None, 0

    def qoutEnqueue(self, item):
        if not (self._qout == None):
            self._qout.enqueue(item)
            return 1
        return 0

    def qoutEnqueueToBack(self, item):
        if not (self._qout == None):
            self._qout.enqueueToBack(item)
            return 1
        return 0
