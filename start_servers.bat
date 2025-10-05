@echo off
echo Starting Bridgette Application...

echo Starting Backend Server...
cd /d "%~dp0\backend"
start "Backend" python app.py

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
cd /d "%~dp0\frontend"
start "Frontend" python -m http.server 8080

echo Waiting for frontend to start...
timeout /t 3 /nobreak >nul

echo Opening application in browser...
start http://localhost:8080/index.html

echo.
echo Both servers are now running:
echo - Backend: http://localhost:5001
echo - Frontend: http://localhost:8080
echo.
echo Press any key to close this window...
pause >nul
