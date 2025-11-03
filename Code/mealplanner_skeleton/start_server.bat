@echo off
setlocal
title MealPlanner Start Server (CMD)

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [ERROR] .venv not found. Run setup_cmd.bat first.
  pause
  exit /b 1
)

call ".venv\Scripts\activate.bat"
echo Starting server at http://127.0.0.1:8000/
start "" http://127.0.0.1:8000/
python manage.py runserver 0.0.0.0:8000

endlocal
