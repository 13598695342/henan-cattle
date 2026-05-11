@echo off
title Cattle Data - Full Auto Update

echo =========================================
echo   Cattle Data - Full Auto Update
echo =========================================
echo.

echo Current Time: %date% %time%
echo.

cd /d "%~dp0"

echo [1/5] Updating data...
echo Started at: %time%
python data_update.py
if %errorlevel% neq 0 (
    echo Update failed!
    pause
    exit /b 1
)
echo   Completed at: %time%
echo   OK - Data updated!

echo.
echo [2/5] Commit to GitHub...
echo Started at: %time%
git add -A
git commit -m "Auto update %date% %time%" 2>nul
if %errorlevel% neq 0 (
    echo No changes to commit
) else (
    echo   Completed at: %time%
    echo   OK - Committed
)

echo.
echo [3/5] Push to GitHub...
echo Started at: %time%
git push origin master 2>nul
if %errorlevel% neq 0 (
    echo   Warning: GitHub push failed (network issue)
) else (
    echo   Completed at: %time%
    echo   OK - Pushed to GitHub
)

echo.
echo [4/5] Push to Gitee...
echo Started at: %time%
git push gitee master 2>nul
if %errorlevel% neq 0 (
    echo   Warning: Gitee push failed (network issue)
) else (
    echo   Completed at: %time%
    echo   OK - Pushed to Gitee
)

echo.
echo [5/5] Finished!
echo Finished at: %time%
echo.
echo =========================================
echo   All Done!
echo =========================================
echo.
echo Website: https://dulcet-daifuku-4f5ffe.netlify.app/
echo.
echo Scheduled task runs daily at 09:00 AM
echo.
pause
