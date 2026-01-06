@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
title MealPlanner Database Setup

REM Navigate to project root (parent of setup folder)
cd /d "%~dp0.."

echo === MealPlanner Database Setup ===

where python >nul 2>&1
if errorlevel 1 (
  where py >nul 2>&1
  if errorlevel 1 (
    echo [ERROR] Python not found in PATH. Please install Python 3.11+ and try again.
    pause
    exit /b 1
  ) else (
    set "PYEXE=py -3"
  )
) else (
  set "PYEXE=python"
)

if not exist ".venv\Scripts\python.exe" (
  echo ==> Creating virtual environment (.venv)
  %PYEXE% -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
  )
)

call ".venv\Scripts\activate.bat"

echo ==> Installing requirements
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo ==> Creating database schema
python manage.py migrate

if errorlevel 1 (
  echo [ERROR] Failed to create database
  pause
  exit /b 1
)

echo.
echo Database created successfully!
echo Database file: db.sqlite3
echo.

set /p SEED="Do you want to seed demo data? (y/n): "
if /i "%SEED%"=="y" (
  echo ==> Seeding demo data
  python manage.py seed
  echo Demo data seeded!
)

echo.
echo Database setup complete!
pause
