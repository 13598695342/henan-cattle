@echo off
title Cattle Data - Full Auto Update

echo =========================================
echo   Cattle Data - Full Auto Update
echo =========================================
echo.

cd /d "%~dp0"

echo [1/5] Updating data...
python data_update.py
if %errorlevel% neq 0 (
    echo Update failed!
    pause
    exit /b 1
)
echo   OK

echo.
echo [2/5] Commit to GitHub...
git add -A
git commit -m "Auto update %date% %time%" 2>nul
if %errorlevel% neq 0 (
    echo No changes to commit
) else (
    echo   OK - Committed
)

echo.
echo [3/5] Push to GitHub...
git push origin master 2>nul
if %errorlevel% neq 0 (
    echo   Warning: Push failed (network issue)
) else (
    echo   OK - Pushed
)

echo.
echo [4/5] Push to Gitee...
git push gitee master 2>nul
if %errorlevel% neq 0 (
    echo   Warning: Push failed (network issue)
) else (
    echo   OK - Pushed
)

echo.
echo [5/5] Done!
echo.
echo =========================================
echo   All Done!
echo =========================================
echo.
echo Website: https://dulcet-daifuku-4f5ffe.netlify.app/
echo.
pause
