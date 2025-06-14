Installation
============

Requirements
-----------

* Python 3.8 or higher
* PySide6 or PyQt6
* Windows 10 or higher (for Windows-specific features)

Installation Steps
----------------

1. Clone the repository:

.. code-block:: bash

    git clone https://github.com/yourusername/PyQtMainWindow_Project_Template.git
    cd PyQtMainWindow_Project_Template

2. Create a virtual environment (recommended):

.. code-block:: bash

    # Using venv
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    source .venv/bin/activate  # On Linux/Mac

    # Or using conda
    conda create --name PyQtMainWindow_Project_Template_env python=3.11 -y
    conda activate PyQtMainWindow_Project_Template_env

3. Install dependencies:

.. code-block:: bash

    pip install -r requirements.txt

4. Build the project:

.. code-block:: bash

    # On Windows
    build.bat

    # On Linux/Mac
    ./build.sh

Project Structure
---------------

::

    PyQtMainWindow_Project_Template/
    ├── docs/                    # Documentation
    ├── src/                     # Source code
    │   ├── Client_Code/        # Client implementation
    │   └── Template_Material/  # Core template classes
    ├── build/                   # Build output
    ├── dist/                    # Distribution files
    ├── .vscode/                # VS Code configuration
    ├── build.bat               # Windows build script
    ├── main.spec              # PyInstaller spec file
    └── requirements.txt        # Project dependencies

Development Setup
---------------

1. Install development dependencies:

.. code-block:: bash

    pip install -r requirements-dev.txt

2. Set up pre-commit hooks:

.. code-block:: bash

    pre-commit install

3. Configure your IDE:
   - For VS Code, the configuration is included in the `.vscode` directory
   - For other IDEs, ensure you have Python and Qt development tools installed

Building Documentation
--------------------

To build the documentation locally:

.. code-block:: bash

    cd docs
    make html

The documentation will be available in `docs/_build/html/`.

Troubleshooting
--------------

Common issues and solutions:

1. **Qt DLL not found**
   - Ensure PySide6/PyQt6 is properly installed
   - Check if Qt DLLs are in your system PATH

2. **Build errors**
   - Make sure all dependencies are installed
   - Check if you have the correct Python version
   - Verify that your Qt installation is complete

3. **Import errors**
   - Ensure you're using the correct virtual environment
   - Check if all required packages are installed
   - Verify your PYTHONPATH includes the project root 