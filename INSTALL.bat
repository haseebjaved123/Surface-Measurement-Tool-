@echo off
title Install Dependencies
cd /d "%~dp0"

echo.
echo Installing Surface Measurement Tool dependencies...
echo.

if exist ".venv\Scripts\python.exe" (
  set "PYTHON_CMD=.venv\Scripts\python.exe"
  echo Using Python from .venv
) else (
  set "PYTHON_CMD=python"
  echo Using system Python
)

echo.
"%PYTHON_CMD%" -m pip install -r requirements.txt

echo.
if errorlevel 1 (
  echo Install failed. Make sure Python is installed from python.org
) else (
  echo Done. You can now double-click RUN.bat to start the app.
)
echo.
pause
