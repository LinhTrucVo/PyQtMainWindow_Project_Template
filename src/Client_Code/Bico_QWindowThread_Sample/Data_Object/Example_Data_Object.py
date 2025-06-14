"""
Example_Data_Object module.
Defines a sample data object for demonstration and testing purposes.
"""

class Example_Data_Object:
    """
    A sample data object class for use in window thread communication.
    """
    def __init__(self, value=None):
        """
        Initialize the Example_Data_Object.

        Parameters
        ----------
        value : any, optional
            The value to store in the data object.
        """
        self.value = value

    def get_value(self):
        """
        Get the value stored in the data object.

        Returns
        -------
        any
            The stored value.
        """
        return self.value

    def getData_1(self):
        return self.data_1

    def setData_1(self, data):
        self.data_1 = data

    def getData_2(self):
        return self.data_2

    def setData_2(self, data):
        self.data_2 = data