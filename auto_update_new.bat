@echo off
chcp 65001 >nul
title 河南牛价数据 - 自动更新

echo =========================================
echo   河南牛价数据 - 自动更新
echo =========================================
echo.

cd /d "%~dp0"

echo [1/2] 正在获取最新数据...
python data_update.py
if %errorlevel% neq 0 (
    echo.
    echo 数据更新失败，请检查网络连接
    echo.
    pause
    exit /b 1
)
echo   ✓ 数据更新成功

echo.
echo [2/2] 部署提示
echo.
echo   请打开浏览器访问:
echo   https://app.netlify.com/drop
echo.
echo   然后把文件夹拖进去即可
echo.

echo =========================================
echo   完成！
echo =========================================
echo.
echo 网站地址: https://dulcet-daifuku-4f5ffe.netlify.app/
echo.
pause
