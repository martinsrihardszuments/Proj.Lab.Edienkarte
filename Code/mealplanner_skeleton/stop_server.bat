@echo off
REM Quick launcher to stop MealPlanner Server
REM This script stops the server from the root directory
cd /d "%~dp0"
call setup\stop_server.bat
