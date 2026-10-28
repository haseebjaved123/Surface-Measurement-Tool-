@echo off
title Surface Measurement Tool - CLI (process images)
echo.
echo Processing images with OCR (command-line)...
echo Place images in 'input_images' folder, then run this.
echo.
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
python main.py
echo.
echo Check 'output_images' and 'results' for output.
pause
