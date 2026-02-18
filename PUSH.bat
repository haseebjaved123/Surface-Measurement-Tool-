@echo off
title Push to GitHub
echo.
echo Checking Git...
if not exist .git (
  echo Initializing Git...
  git init
)
echo.
echo Adding files...
git add .
echo.
echo Committing...
git commit -m "Update Surface Measurement Tool" 2>nul || git commit -m "Update Surface Measurement Tool" --allow-empty
echo.
echo Pushing to GitHub...
git branch -M main 2>nul
git push -u origin main 2>nul || git push origin main 2>nul
if errorlevel 1 (
  echo.
  echo If this is your first time, run this in the same folder first:
  echo   git remote add origin https://github.com/haseebjaved123/Surface-Measurement-Tool-.git
  echo.
  echo Then run this script again. You may be asked to sign in to GitHub.
  echo.
) else (
  echo.
  echo Done. Your site will update at:
  echo https://haseebjaved123.github.io/Surface-Measurement-Tool-/
  echo.
)
pause
