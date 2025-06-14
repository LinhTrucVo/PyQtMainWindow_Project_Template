import sys
from PySide6.QtWidgets import QApplication

from Template_Material.bico_qmutexqueue import Bico_QMutexQueue
from Template_Material.bico_qwindowthread import Bico_QWindowThread
from Template_Material.bico_qwindowthread_ui import Bico_QWindowThread_UI
from Client_Code.Bico_QWindowThread_Sample.Bico_QWindowThread_Sample import Bico_QWindowThread_Sample
from Client_Code.Bico_QWindowThread_Sample.Bico_QWindowThread_Sample_UI import Bico_QWindowThread_Sample_UI


"""
Main entry point for the PyQtMainWindow Project Template.
Initializes the QApplication and sets up window threads and UIs.
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    Bico_QWindowThread.setMainApp(app)

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
