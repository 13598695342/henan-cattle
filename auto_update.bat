@echo off
title Cattle Data Auto Update

echo =========================================
echo   Cattle Data - Auto Update
echo =========================================
echo.

cd /d "%~dp0"

echo [1/2] Updating data...
python data_update.py
if %errorlevel% neq 0 (
    echo.
    echo Update failed! Check network connection.
    echo.
    pause
    exit /b 1
)
echo   OK - Data updated!

echo.
echo [2/2] Deploy to Netlify
echo.
echo   1. Open browser: https://app.netlify.com/drop
echo   2. Drag folder to the page
echo   3. Wait for deployment
echo.

echo =========================================
echo   Done!
echo =========================================
echo.
echo Website: https://dulcet-daifuku-4f5ffe.netlify.app/
echo.
pause
