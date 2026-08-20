@echo off
setlocal
chcp 65001 >nul
title Stop Sign Project - Setup

echo ==========================================
echo  Stop Sign Detection - One-Time Setup
echo ==========================================
echo.

REM ---- Locate this project folder ----
set "PROJECT=%~dp0.."
set "INSTALLER=%PROJECT%\python-3.14.7-amd64.exe"
echo Project folder: %PROJECT%
echo.

REM ---- Find a Python 3.11+ interpreter (py launcher first, then python) ----
set "PY="
set "PY_OK=0"

where py >nul 2>&1
if not errorlevel 1 (
    py -c "import sys; print(sys.executable)" >"%TEMP%\ssd_py.txt" 2>nul
    if not errorlevel 1 (
        for /f "usebackq delims=" %%i in ("%TEMP%\ssd_py.txt") do set "PY=%%i"
    )
)

if not defined PY (
    where python >nul 2>&1
    if not errorlevel 1 (
        python -c "import sys; print(sys.executable)" >"%TEMP%\ssd_py.txt" 2>nul
        if not errorlevel 1 (
            for /f "usebackq delims=" %%i in ("%TEMP%\ssd_py.txt") do set "PY=%%i"
        )
    )
)
del "%TEMP%\ssd_py.txt" >nul 2>&1

if defined PY (
    "%PY%" -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>&1
    if not errorlevel 1 set "PY_OK=1"
)

REM ---- If no usable Python found, install the bundled Python 3.14 silently ----
if not "%PY_OK%"=="1" (
    echo No usable Python 3.11+ found. Installing the bundled Python 3.14...
    echo.
    if not exist "%INSTALLER%" (
        echo [ERROR] python-3.14.7-amd64.exe was not found in the project folder.
        echo.
        echo Please put it back in the project folder, or download Python 3.14
        echo from https://www.python.org/downloads/ and run this setup again.
        echo.
        pause
        exit /b 1
    )
    "%INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1 Include_test=0 Include_doc=0 Include_pip=1
    echo Installer finished, exit code %errorlevel%.
    echo.

    if exist "%LocalAppData%\Programs\Python\Python314\python.exe" (
        set "PY=%LocalAppData%\Programs\Python\Python314\python.exe"
    ) else (
        echo [ERROR] Python was not found after running the installer.
        pause
        exit /b 1
    )
    "%PY%" -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] The installed Python is older than 3.11.
        pause
        exit /b 1
    )
    set "PY_OK=1"
)

if not "%PY_OK%"=="1" (
    echo [ERROR] Could not find or install a Python 3.11+ interpreter.
    pause
    exit /b 1
)

echo [OK] Python found: %PY%
"%PY%" --version
echo.

REM ---- Create virtual environment ----
if exist "%PROJECT%\venv\Scripts\python.exe" (
    echo [SKIP] venv already exists.
) else (
    echo Creating virtual environment...
    "%PY%" -m venv "%PROJECT%\venv"
    if errorlevel 1 (
        echo [ERROR] Failed to create venv.
        pause
        exit /b 1
    )
    echo [OK] venv created.
)
echo.

REM ---- Install CPU PyTorch + project dependencies ----
echo Installing packages (this takes a few minutes)...
"%PROJECT%\venv\Scripts\python.exe" -m pip install --upgrade pip
"%PROJECT%\venv\Scripts\python.exe" -m pip install torch==2.13.0 torchvision==0.28.0 --index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 (
    echo [ERROR] PyTorch install failed. Check your internet connection.
    pause
    exit /b 1
)
"%PROJECT%\venv\Scripts\python.exe" -m pip install ultralytics==8.4.115 opencv-python==5.0.0.93 numpy==2.4.4 PyYAML==6.0.3 matplotlib==3.11.1
if errorlevel 1 (
    echo [ERROR] Package install failed.
    pause
    exit /b 1
)
echo [OK] All packages installed.
echo.

echo ==========================================
echo  Setup complete! You can now:
echo   - Double-click test_photo.bat to test the model
echo   - Run:  venv\Scripts\python scripts\detect.py
echo ==========================================
pause