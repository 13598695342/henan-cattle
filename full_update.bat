@echo off
chcp 65001 >nul
echo =========================================
echo   河南牛价数据 - 自动更新并部署
echo =========================================
echo.

cd /d "%~dp0"

echo [1/4] 正在获取最新数据...
python data_update.py
if %errorlevel% neq 0 (
    echo 数据更新失败
    pause
    exit /b 1
)
echo   ✓ 数据更新成功

echo.
echo [2/4] 正在安装 Netlify CLI...
call npm install -g netlify-cli --silent --registry=https://registry.npmmirror.com 2>nul
echo   ✓ 安装完成

echo.
echo [3/4] 正在部署到 Netlify...
call netlify deploy --prod --dir=. --site=dulcet-daifuku-4f5ffe 2>&1
echo   ✓ 部署完成

echo.
echo [4/4] 完成！
echo.
echo =========================================
echo   更新并部署完成！
echo =========================================
echo.
echo 网站地址：https://dulcet-daifuku-4f5ffe.netlify.app/
echo.
pause
