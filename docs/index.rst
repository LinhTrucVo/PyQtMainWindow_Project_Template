Welcome to PyQtMainWindow Project Template's documentation!
===========================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   architecture
   usag
   api
   contributing

Introduction
------------

PyQtMainWindow Project Template is a modern template for PyQt/PySide6 projects with multi-threaded window management. 
It provides a robust foundation for building desktop applications with multiple windows and threads.

Features
--------

* Multi-threaded window management
* Thread-safe message queue system
* Clean separation of UI and business logic
* Easy-to-use window creation and management
* Thread synchronization utilities

Quick Start
-----------

.. code-block:: python

    from PySide6.QtWidgets import QApplication
    from PyQtLib_Project_Template import Bico_QWindowThread
    from PyQtLib_Project_Template import Bico_QMutexQueue

    app = QApplication(sys.argv)
    Bico_QWindowThread.setMainApp(app)

    # Create and start a window thread
    Bico_QWindowThread.create(
        YourWindowClass,
        Bico_QMutexQueue(),
        1,
        Bico_QMutexQueue(),
        1,
        "window_name"
    )
    Bico_QWindowThread.getThreadHash()["window_name"].start()

Architecture Overview
---------------------

The project follows a modular architecture with clear separation of concerns:

* **Core Framework**: Thread and window management
* **Communication Layer**: Thread-safe message queues
* **UI Layer**: Window and UI component management
* **Client Implementation**: Custom window and UI components

For detailed architecture documentation, see the :doc:`architecture` section.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`