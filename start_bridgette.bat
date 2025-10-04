@echo off
echo Starting Bridgette Application...
echo.

echo Starting Backend Server (Python Flask)...
start "Backend Server" cmd /k "cd backend && python app.py"

echo Starting Frontend Server (Node.js)...
start "Frontend Server" cmd /k "npm run dev:frontend"

echo.
echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause > nul
