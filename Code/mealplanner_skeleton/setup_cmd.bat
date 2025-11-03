@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
title MealPlanner Setup (CMD)

cd /d "%~dp0"

echo === MealPlanner setup starting (CMD) ===

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
) else (
  echo ==> Virtual environment exists
)

call ".venv\Scripts\activate.bat"

echo ==> Installing requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ==> Making migrations
python manage.py makemigrations core
echo ==> Applying migrations
python manage.py migrate

echo ==> Seeding demo data
python manage.py seed

echo ==> Starting server on http://127.0.0.1:8000/
start "" http://127.0.0.1:8000/
python manage.py runserver 0.0.0.0:8000

endlocal
