@echo off
echo ========================================
echo 河南牛业数据 PWA 部署到 GitHub
echo ========================================
echo.

echo 步骤1: 请在浏览器中打开 GitHub 并登录
echo 网址: https://github.com/new
echo.
echo 步骤2: 创建新仓库
echo   - Repository name: henan-cattle
echo   - 选择 Public
echo   - 不要勾选任何初始化选项
echo   - 点击 Create repository
echo.
echo 步骤3: 创建完成后，复制仓库的 HTTPS 地址
echo   类似: https://github.com/你的用户名/henan-cattle.git
echo.
echo 步骤4: 回到这里，把地址告诉我
echo.
echo 或者你可以直接运行以下命令(需要先手动创建仓库):
echo.
echo   cd C:\Users\AFireBoy\Desktop\pydemo\henan-cattle-app
echo   git remote add origin https://github.com/你的用户名/henan-cattle.git
echo   git push -u origin master
echo.
pause
