@echo off
chcp 65001 >nul
set "ROOT=%~dp0"
set "LOGFILE=%ROOT%runs\test_log.txt"
set "PY=%ROOT%venv\Scripts\python.exe"
set "SCRIPT=%ROOT%scripts\test_single.py"
set "PS1=%ROOT%scripts\pick_image.ps1"
set "PSOUT=%TEMP%\picker_output.txt"

del "%PSOUT%" >nul 2>&1
echo [%date% %time%] Started. Arg: [%~1] >> "%LOGFILE%"

REM Case 1: an image was dragged onto the .bat icon
if not "%~1"=="" (
    if exist "%~f1" (
        "%PY%" "%SCRIPT%" "%~f1" >> "%LOGFILE%" 2>&1
        echo [%date% %time%] Dragged-file finished, exit %errorlevel% >> "%LOGFILE%"
        goto :done
    )
)

REM Case 2: double-click -> show a file picker
echo Opening image picker...
powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%" "%PSOUT%" >> "%LOGFILE%" 2>&1
echo [%date% %time%] Picker finished, exit %errorlevel% >> "%LOGFILE%"

set "PICKED="
if exist "%PSOUT%" (
    for /f "usebackq delims=" %%i in ("%PSOUT%") do set "PICKED=%%i"
)

if not defined PICKED (
    echo No image selected. Nothing to do.
    echo [%date% %time%] No file selected >> "%LOGFILE%"
    pause
    exit /b
)

echo [%date% %time%] Processing: %PICKED% >> "%LOGFILE%"
"%PY%" "%SCRIPT%" "%PICKED%" >> "%LOGFILE%" 2>&1
echo [%date% %time%] Finished, exit %errorlevel% >> "%LOGFILE%"

:done
echo.
echo Done. Result saved in runs\detections\ . Details in runs\test_log.txt
pause