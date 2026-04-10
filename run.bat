@echo off
REM =============================================================================
REM   Student Attendance & Engagement Tracker - Windows Startup Script
REM   Double-click this file to start the application
REM =============================================================================

cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     🎓 STUDENT ATTENDANCE & ENGAGEMENT TRACKER                ║
echo ║                                                                ║
echo ║              Starting Application...                          ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    echo    Download from: https://www.python.org
    pause
    exit /b 1
)

echo ✅ Python found!
echo.

REM Run the universal launcher
python run.py
pause
