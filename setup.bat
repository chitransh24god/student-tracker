@echo off
REM Quick Start Script for Student Attendance & Engagement Tracker (Windows)

echo ==================================
echo Student Tracker - Quick Start
echo ==================================
echo.

REM Check Python version
echo Checking Python version...
python --version

echo.
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo To run the application:
echo   1. Activate virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Run Flask application:
echo      python app.py
echo.
echo   3. Open browser and visit:
echo      http://127.0.0.1:5000
echo.
echo Demo Credentials:
echo   Email: faculty@example.com
echo   Password: faculty123
echo.
echo ==================================
pause
