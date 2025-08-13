@echo off
echo ========================================
echo Learning Platform - Starting...
echo ========================================
echo.

echo Checking if Python is available...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Installing/updating packages...
pip install -r requirements.txt

echo.
echo Starting the Learning Platform...
echo.
echo 🌐 Open your browser and go to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause 