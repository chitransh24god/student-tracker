@echo off
REM ==============================================================================
REM   ONE-CLICK LAUNCHER - Student Attendance & Engagement Tracker
REM   Just double-click this file! Everything will run automatically
REM ==============================================================================

setlocal enabledelayedexpansion

cls

REM Color codes (Windows 10+)
REM Use this for colored output if supported

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                                                                        ║
echo ║      🎓  STUDENT ATTENDANCE ^& ENGAGEMENT TRACKER                      ║
echo ║                                                                        ║
echo ║              ONE-CLICK LAUNCHER                                       ║
echo ║                                                                        ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

REM Check for Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo ❌ ERROR: Python not found!
    echo.
    echo Please install Python 3.8 or higher:
    echo   👉 https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
echo ✅ Found: %PYTHON_VER%
echo.

REM Check if venv exists
echo [2/5] Checking virtual environment...
if not exist "venv" (
    echo   Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        color 0C
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created!
) else (
    echo ✅ Virtual environment found!
)
echo.

REM Activate venv
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    color 0C
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated!
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
if exist "requirements.txt" (
    python -m pip install --upgrade pip >nul 2>&1
    python -m pip install -q Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Werkzeug==2.3.7 python-dotenv==1.0.0 2>nul
    if errorlevel 1 (
        echo ⚠️  Installing packages individually...
        python -m pip install -q Flask
        python -m pip install -q Flask-SQLAlchemy
        python -m pip install -q Werkzeug
        python -m pip install -q python-dotenv
    )
    echo ✅ Dependencies installed!
) else (
    echo ❌ requirements.txt not found!
    pause
    exit /b 1
)
echo.

REM Start the app
echo [5/5] Starting application...
echo.
echo ═══════════════════════════════════════════════════════════════════════
echo.
echo 📱  APPLICATION STARTING...
echo.
echo 🌐  Open your browser and visit: http://127.0.0.1:5000
echo.
echo 👤  Demo Login:
echo    Email:    faculty@example.com
echo    Password: faculty123
echo.
echo ⏹️   Press CTRL+C to stop the server
echo.
echo ═══════════════════════════════════════════════════════════════════════
echo.

REM Run the Flask app
python app.py

REM Show message when exiting
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║           Application stopped. Press any key to exit...              ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

pause
