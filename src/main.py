"""
main.py
=======

Entry point for the PyQtMainWindow Project Template.

This script initializes the QApplication, sets up the main application context,
creates and starts multiple window threads using the core framework.

.. uml::

   @startuml
   actor User
   User -> main.py : start application
   main.py -> Bico_QWindowThread : setMainApp(app)
   main.py -> Bico_QWindowThread : create(...)
   main.py -> Bico_QWindowThread : getThreadHash()["task_0"].start()
   main.py -> Bico_QWindowThread : getThreadHash()["task_1"].start()
   @enduml
"""

import sys
from PySide6.QtWidgets import QApplication

from lib import Bico_QMutexQueue
from lib import Bico_QWindowThread
from lib import Bico_QWindowThread_UI
from Client_Code.Task1.Task1 import Task1
from Client_Code.Task1.Task1_UI import Task1_UI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Register the main application with the thread manager
    Bico_QWindowThread.setMainApp(app)

# -------------------------------------------------------------------
    # Create and start two window threads with their UIs
    Bico_QWindowThread.create(
        Task1,
        Bico_QMutexQueue(),
        1,
        Bico_QMutexQueue(),
        1,
        "task_0",
        Bico_QWindowThread_UI.create(Task1_UI, "ui0")
    )
    Bico_QWindowThread.getThreadHash()["task_0"].start()
# -------------------------------------------------------------------

# -------------------------------------------------------------------
    # Bico_QWindowThread_UI.create(
    #     Bico_QWindowThread_Sample_UI, 
    #     "ui0", 
    #     Bico_QWindowThread.create(
    #         Bico_QWindowThread_Sample,
    #         Bico_QMutexQueue(),
    #         1,
    #         Bico_QMutexQueue(),
    #         1,
    #         "task_0"
    #     )
    # )    
    # Bico_QWindowThread_UI.getUIThreadHash()["ui0"].show()
# -------------------------------------------------------------------



    sys.exit(app.exec())
