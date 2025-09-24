Usage Guide
===========

This guide explains how to use the PyQtMainWindow Project Template to create multi-threaded Qt applications.

Basic Concepts
--------------

The template provides several key components:

1. **Bico_QWindowThread**: Manages window threads and their lifecycle
2. **Bico_QMutexQueue**: Thread-safe message queue for inter-thread communication
3. **Bico_QWindowThread_UI**: UI thread management and window creation

Creating a New Window
---------------------

Here's a basic example of creating a new window:

.. code-block:: python

    from PySide6.QtWidgets import QApplication, QMainWindow
    from PyQtLib_Project_Template import Bico_QWindowThread
    from PyQtLib_Project_Template import Bico_QMutexQueue

    class MyWindow(QMainWindow):
        def __init__(self, input_queue, output_queue):
            super().__init__()
            self.input_queue = input_queue
            self.output_queue = output_queue
            self.setWindowTitle("My Window")
            # Add your UI setup here

    # Create the application
    app = QApplication(sys.argv)
    Bico_QWindowThread.setMainApp(app)

    # Create input and output queues
    input_queue = Bico_QMutexQueue()
    output_queue = Bico_QMutexQueue()

    # Create and start the window thread
    window_thread = Bico_QWindowThread.create(
        MyWindow,
        input_queue,
        1,  # input queue size
        output_queue,
        1,  # output queue size
        "my_window"
    )
    window_thread.start()

Thread Communication
--------------------

To send messages between threads:

.. code-block:: python

    # In the main thread
    output_queue.put({"type": "update", "data": "Hello from main thread"})

    # In the window thread
    while True:
        message = input_queue.get()
        if message:
            # Process the message
            if message["type"] == "update":
                print(message["data"])

Multiple Windows
----------------

To create multiple windows:

.. code-block:: python

    # Create first window
    window1 = Bico_QWindowThread.create(
        MyWindow,
        Bico_QMutexQueue(),
        1,
        Bico_QMutexQueue(),
        1,
        "window1"
    )
    window1.start()

    # Create second window
    window2 = Bico_QWindowThread.create(
        MyWindow,
        Bico_QMutexQueue(),
        1,
        Bico_QMutexQueue(),
        1,
        "window2"
    )
    window2.start()

Window Management
-----------------

Access and manage windows:

.. code-block:: python

    # Get all window threads
    threads = Bico_QWindowThread.getThreadHash()

    # Access a specific window
    window = threads["my_window"]

    # Close a window
    window.quit()
    window.wait()

Best Practices
--------------

1. **Queue Management**
   - Always check queue size before sending messages
   - Use appropriate queue sizes for your use case
   - Clear queues when no longer needed

2. **Thread Safety**
   - Use mutex-protected queues for thread communication
   - Avoid direct access to shared resources
   - Handle thread termination properly

3. **Resource Management**
   - Clean up resources when windows are closed
   - Monitor memory usage with multiple windows
   - Use appropriate window closing strategies

4. **Error Handling**
   - Implement proper error handling in threads
   - Use try-except blocks for queue operations
   - Log errors appropriately

Example Applications
--------------------

1. **Simple Window**
   - Basic window creation and management
   - Single thread communication

2. **Multiple Windows**
   - Multiple window management
   - Inter-window communication

3. **Complex UI**
   - Advanced UI components
   - Multiple thread synchronization

For more examples, check the `examples` directory in the project repository.