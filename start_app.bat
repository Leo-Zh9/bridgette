@echo off
echo Starting Bridgette Full Stack Application...
echo.

echo Starting Python Backend Server...
start "Backend Server" cmd /k "cd backend && python app.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npx http-server -p 3005 -o"

echo.
echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3005
echo.
echo Press any key to exit...
pause > nul

