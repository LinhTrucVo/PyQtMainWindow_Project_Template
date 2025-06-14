@echo off
REM filepath: c:\Users\bico\Desktop\PyQtQuick_Project_Template\build.bat

REM ==========================================
REM Build script for application and docs
REM Usage:
REM   build.bat           - build both app and docs
REM   build.bat --app     - build only the application
REM   build.bat --docs    - build only the documentation
REM   build.bat --help    - show this help message
REM ==========================================

setlocal

REM Show help
if "%1"=="--help" (
    echo Build script usage:
    echo   build.bat           - build both app and docs
    echo   build.bat --app     - build only the application
    echo   build.bat --docs    - build only the documentation
    echo   build.bat --help    - show this help message
    exit /b 0
)

REM Build only app
if "%1"=="--app" (
    echo Building application...
    pyinstaller main.spec
    exit /b %ERRORLEVEL%
)

REM Build only docs
if "%1"=="--docs" (
    echo Building documentation...
    sphinx-build -b html docs docs/_build
    exit /b %ERRORLEVEL%
)

REM Default: build both
echo Building documentation...
sphinx-build -b html docs docs/_build
if errorlevel 1 exit /b %ERRORLEVEL%

echo Building application...
pyinstaller main.spec
exit /b %ERRORLEVEL%