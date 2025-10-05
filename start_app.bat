@echo off
echo Starting Bridgette Full Stack Application...
echo.

REM Get the directory where this batch file is located
cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo Starting Python Backend Server...
start "Backend Server" cmd /k "cd /d %CD%\backend && python app.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo Starting Frontend Server (Python HTTP Server)...
start "Frontend Server" cmd /k "cd /d %CD%\frontend && python -m http.server 8080"

echo.
echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8080
echo.
echo Opening application in browser...
timeout /t 5 /nobreak > nul
start http://localhost:8080/index.html
echo.
echo Press any key to exit...
pause > nul

