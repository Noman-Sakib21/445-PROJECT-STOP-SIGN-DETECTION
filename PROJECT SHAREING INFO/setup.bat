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
echo Project folder: %PROJECT%
echo.

REM ---- Check Python is installed ----
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is NOT installed or not on PATH.
    echo.
    echo Please install Python 3.10 or newer from https://www.python.org/downloads/
    echo IMPORTANT: tick "Add Python to PATH" during installation.
    echo.
    echo Then run this setup again.
    pause
    exit /b 1
)
echo [OK] Python found.
python --version
echo.

REM ---- Create virtual environment ----
if exist "%PROJECT%\venv\Scripts\python.exe" (
    echo [SKIP] venv already exists.
) else (
    echo Creating virtual environment...
    python -m venv "%PROJECT%\venv"
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
