"""
Task1_Data.py
======================

Example data object for demonstration of data passing between threads.

.. uml::

   @startuml
   class Task1_Data {
       +getData_1()
       +setData_1(data)
       +getData_2()
       +setData_2(data)
   }
   @enduml
"""

class Task1_Data:
    """
    Example data object for use in sample window threads.

    :ivar data_1: First data attribute.
    :ivar data_2: Second data attribute.
    """

    def __init__(self):
        """
        Initialize the data object with default values.
        """
        self.data_1 = 50
        self.data_2 = 100

    def getData_1(self):
        """
        Get the first data attribute.

        :return: Value of data_1.
        """
        return self.data_1

    def setData_1(self, data):
        """
        Set the first data attribute.

        :param data: Value to set.
        """
        self.data_1 = data

    def getData_2(self):
        """
        Get the second data attribute.

        :return: Value of data_2.
        """
        return self.data_2

    def setData_2(self, data):
        """
        Set the second data attribute.

        :param data: Value to set.
        """
        self.data_2 = data