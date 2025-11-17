@echo off
setlocal
title Stop Django Server

REM ==== Settings ====
set PORT=8000

echo.
echo === Stopping any server listening on port %PORT% ===

REM Find the process ID using the specified port
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%PORT%') do (
    set PID=%%a
)

if not defined PID (
    echo [INFO] No process found on port %PORT%. Server is not running.
    goto :end
)

REM Kill the process
echo Found process with PID %PID%. Terminating...
taskkill /PID %PID% /F >nul 2>&1

if %errorlevel%==0 (
    echo [OK] Server on port %PORT% has been stopped.
) else (
    echo [WARN] Could not terminate process with PID %PID% (may require admin rights).
)

:end
echo.
pause
endlocal
