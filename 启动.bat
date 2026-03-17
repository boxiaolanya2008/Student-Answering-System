@echo off
chcp 65001 >nul
echo ================================================
echo          学生答题系统 - 一键启动
echo ================================================
echo.

:: 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [1/4] 检查 Python 环境... ✓
echo.

:: 安装依赖
echo [2/4] 正在安装 Python 依赖包...
python -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo [错误] 依赖安装失败，请检查网络连接
    pause
    exit /b 1
)
echo [依赖安装完成] ✓
echo.

:: 初始化数据库
echo [3/4] 初始化数据库...
python database.py
if errorlevel 1 (
    echo [警告] 数据库可能已存在，继续启动...
)
echo.

:: 启动 Flask 应用
echo [4/4] 启动服务器...
echo.
echo ================================================
echo  服务器即将启动...
echo  访问地址：http://localhost:5000
echo  示例账号：2024001 / 123456
echo ================================================
echo.
echo 按 Ctrl+C 可停止服务器
echo.

python app.py

pause
