@echo off
echo ========================================
echo   Bridgette Safe Cleanup Script
echo ========================================
echo.

echo [1/4] Stopping all Python processes...
taskkill /f /im python.exe 2>nul
if %errorlevel% == 0 (
    echo ✅ Python processes stopped
) else (
    echo ⚠️ No Python processes found or already stopped
)

echo.
echo [2/4] Waiting for file handles to release...
timeout /t 3 /nobreak >nul

echo.
echo [3/4] Cleaning uploaded files...
if exist "backend\uploaded_files\bank1\*" (
    echo   Cleaning bank1 files...
    del /q "backend\uploaded_files\bank1\*" 2>nul
    echo   ✅ Bank1 files cleaned
) else (
    echo   ⚠️ No bank1 files found
)

if exist "backend\uploaded_files\bank2\*" (
    echo   Cleaning bank2 files...
    del /q "backend\uploaded_files\bank2\*" 2>nul
    echo   ✅ Bank2 files cleaned
) else (
    echo   ⚠️ No bank2 files found
)

echo.
echo [4/4] Cleaning temporary JSON files...
if exist "backend\temp_json_files\*" (
    echo   Cleaning JSON files...
    del /q "backend\temp_json_files\*" 2>nul
    echo   ✅ JSON files cleaned
) else (
    echo   ⚠️ No JSON files found
)

echo.
echo ========================================
echo   ✅ Cleanup Complete!
echo ========================================
echo.
echo You can now restart the application.
echo.
pause
