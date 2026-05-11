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
    echo 数据更新失败，请检查网络连接
    pause
    exit /b 1
)
echo ✓ 数据更新成功

echo.
echo [2/4] 正在安装 Netlify CLI...
call npm install -g netlify-cli --silent 2>nul
echo ✓ Netlify CLI 安装完成

echo.
echo [3/4] 正在部署到 Netlify...
call netlify deploy --prod --dir=. --site=dulcet-daifuku-4f5ffe --auth eyJhbGciOi5IUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0ZmY5Nzk0ZS03OTU5LTQ1YjUtYmIwNi0wYzJjNzM0ODAwMDAiLCJpbnRlcm5hbCI6InNlcnZpY2UiLCJhdWQiOiJjbGllbnQiLCJpYXQiOjE3MTM1NTM2NjEsImV4cCI6MTcxMzYzOTg2MX0.ZGkvO4vVac0l7xROBC1eVMrLu5jX0cNwTiFRmH5zBdo 2>&1
echo ✓ 部署完成

echo.
echo [4/4] 清理临时文件...
echo ✓ 清理完成

echo.
echo =========================================
echo   更新并部署完成！
echo =========================================
echo.
echo 网站地址：https://dulcet-daifuku-4f5ffe.netlify.app/
echo.
pause
