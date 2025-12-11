"""
Task1_UI.py
===============================

Sample UI implementation for a window thread.

.. uml::

   @startuml
   class Task1_UI {
       +moreUISetup()
       +fromThreadHandling(mess, data)
       +on_pushButton_clicked()
       +on_pushButton_2_clicked()
       +on_pushButton_3_clicked()
   }
   Task1_UI --|> Bico_QWindowThread_UI
   @enduml
"""

from PySide6.QtCore import QSize, Slot

from lib import Bico_QWindowThread_UI
from .Ui_Task1_UI import Ui_Task1_UI


class Task1_UI(Bico_QWindowThread_UI):
    """
    Example subclass of Bico_QWindowThread_UI for demonstration.

    Implements UI logic and event handlers for the sample window.
    """

    def __init__(self, obj_name="", thread=None, parent=None):
        """
        Initialize the sample UI window.

        :param obj_name: Name for this UI instance.
        :param thread: Associated worker thread.
        :param parent: Parent widget.
        """
        Bico_QWindowThread_UI.__init__(self, obj_name, thread, parent)
        self.ui = Ui_Task1_UI()
        self.ui.setupUi(self)
        self.moreUISetup()

    def closeEvent(self, event):
        """
        Handle the window close event by requesting thread termination.

        :param event: QCloseEvent
        """
        event.ignore()
        self.toThread.emit("terminate", "")

    def moreUISetup(self):
        """
        Additional UI setup logic.
        """
        self.ui.pushButton.resize(QSize(100, 50))

    def fromThreadHandling(self, mess, data):
        """
        Handle messages sent from the worker thread.

        :param mess: Message type.
        :param data: Message data.
        """
        if(mess == "show"):
            self.show()
        elif (mess == "hide"):
            self.hide()
        elif (mess == "terminate"):
            self.TERMINATE.emit()
        elif (mess == "change_button_text"):
            self.ui.pushButton.setText(data)

    @Slot()
    def on_pushButton_clicked(self):
        """
        Handler for the first push button click event.
        """
        self.toThread.emit("mess_from_ui", "button_clicked")

    @Slot()
    def on_pushButton_2_clicked(self):
        """
        Handler for the second push button click event.
        """
        self.toThread.emit("create", "")

    @Slot()
    def on_pushButton_3_clicked(self):
        """
        Handler for the third push button click event.
        """
        self.toThread.emit("create_child", "")
