@echo off
chcp 65001 >nul
title Surface Measurement Tool - Launcher
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8

echo.
echo ========================================
echo  Surface Measurement Tool - Full App
echo  (OCR + Web Server)
echo ========================================
echo.

if exist ".venv\Scripts\python.exe" (
  set "PYTHON_CMD=.venv\Scripts\python.exe"
) else (
  set "PYTHON_CMD=python"
)

"%PYTHON_CMD%" -c "import flask" 2>nul
if errorlevel 1 (
  echo Installing dependencies (first time)...
  "%PYTHON_CMD%" -m pip install -r requirements.txt
  if errorlevel 1 (
    echo Failed. Install Python from python.org and try again.
    pause
    exit /b 1
  )
  echo.
)

echo Starting server in new window...
start "Surface Measurement - Server" cmd /k ""%PYTHON_CMD%" server.py"

echo Waiting for server to start (first run can take ~20 sec)...
timeout /t 15 /nobreak >nul

echo Opening browser...
start "" "http://127.0.0.1:8000"

echo.
echo Server is running in the other window.
echo Close that window to stop the server.
echo You can close this window now.
pause
