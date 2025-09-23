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

from lib.PyQtLib_Project_Template.src.bico_qmutexqueue import Bico_QMutexQueue
from lib.bico_qwindowthread import Bico_QWindowThread
from lib.bico_qwindowthread_ui import Bico_QWindowThread_UI
from Client_Code.Bico_QWindowThread_Sample.Bico_QWindowThread_Sample import Bico_QWindowThread_Sample
from Client_Code.Bico_QWindowThread_Sample.Bico_QWindowThread_Sample_UI import Bico_QWindowThread_Sample_UI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Register the main application with the thread manager
    Bico_QWindowThread.setMainApp(app)

    # Create and start two window threads with their UIs
    Bico_QWindowThread.create(
        Bico_QWindowThread_Sample,
        Bico_QMutexQueue(),
        1,
        Bico_QMutexQueue(),
        1,
        "task_0",
        Bico_QWindowThread_UI.create(Bico_QWindowThread_Sample_UI, "ui0")
    )
    Bico_QWindowThread.getThreadHash()["task_0"].start()

    Bico_QWindowThread.create(
        Bico_QWindowThread_Sample,
        Bico_QMutexQueue(),
        1,
        Bico_QMutexQueue(),
        1,
        "task_1",
        Bico_QWindowThread_UI.create(Bico_QWindowThread_Sample_UI, "ui1")
    )
    Bico_QWindowThread.getThreadHash()["task_1"].start()




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

    # Bico_QWindowThread_UI.create(
    #     Bico_QWindowThread_Sample_UI, 
    #     "ui1", 
    #     Bico_QWindowThread.create(
    #         Bico_QWindowThread_Sample,
    #         Bico_QMutexQueue(),
    #         1,
    #         Bico_QMutexQueue(),
    #         1,
    #         "task_1"
    #     )
    # )    
    # Bico_QWindowThread_UI.getUIThreadHash()["ui1"].show()




    sys.exit(app.exec())
