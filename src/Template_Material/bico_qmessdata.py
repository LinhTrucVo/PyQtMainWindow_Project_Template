"""
bico_qmessdata.py
=================

Defines the Bico_QMessData class, a simple data structure for passing messages
between threads in the application.

.. uml::

   @startuml
   class Bico_QMessData {
       - _src: str
       - _dst: str
       - _mess: str
       - _data: any
       + src()
       + setSrc(src)
       + dst()
       + setDst(dst)
       + mess()
       + setMess(mess)
       + data()
       + setData(data)
   }
   @enduml
"""

class Bico_QMessData:
    """
    Message data structure for inter-thread communication.

    :param args: Can be (mess, data) or (src, dst, mess, data)
    """
    def __init__(self, *args):
        if(len(args) == 2):
            self._src = ""
            self._dst = ""
            self._mess = args[0]
            self._data = args[1]
        elif(len(args) == 4):
            self._src = args[0]
            self._dst = args[1]
            self._mess = args[2]
            self._data = args[3]
        else:
            self._src = ""
            self._dst = ""
            self._mess = ""
            self._data = ""

    def src(self):
        """Get the source of the message."""
        return self._src

    def setSrc(self, src):
        """Set the source of the message."""
        self._src = src

    def dst(self):
        """Get the destination of the message."""
        return self._dst

    def setDst(self, dst):
        """Set the destination of the message."""
        self._dst = dst

    def mess(self):
        """Get the message type."""
        return self._mess

    def setMess(self, mess):
        """Set the message type."""
        self._mess = mess

    def data(self):
        """Get the message data."""
        return self._data

    def setData(self, data):
        """Set the message data."""
        self._data = data

    def __str__(self):
        """String representation for debugging."""
        return "Bico_QMessData{src: " + self.src() + ", dst: " + self.dst() + ", mess: " + self.mess() + ", data: " + str(self.data()) + "}"
