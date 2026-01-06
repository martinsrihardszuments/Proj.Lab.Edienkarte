@echo off
REM Quick launcher for MealPlanner Server
REM This script starts the server from the root directory
cd /d "%~dp0"
call setup\start_server.bat
