@echo off
REM Railway.app Quick Setup & Deploy Script for Windows
REM Run this from your student-tracker repository root

echo.
echo 🚀 Railway.app Deployment Setup
echo ================================
echo.

REM Step 1: Verify files exist
echo ✓ Checking configuration files...
if exist "Procfile" if exist "runtime.txt" if exist "requirements.txt" if exist ".streamlit\config.toml" (
    echo ✓ All configuration files present
) else (
    echo ✗ Missing files. Make sure you have:
    echo   - Procfile
    echo   - runtime.txt
    echo   - .streamlit\config.toml
    echo   - requirements.txt
    exit /b 1
)

REM Step 2: Add to git
echo.
echo 📝 Adding files to git...
git add Procfile runtime.txt requirements.txt .streamlit\

REM Step 3: Commit
echo 💾 Committing changes...
git commit -m "Add Railway.app deployment configuration"

REM Step 4: Push
echo.
echo 🔄 Pushing to GitHub...
git push origin main

echo.
echo ✅ Done! Railway.app will auto-deploy when it detects the push.
echo.
echo Next steps:
echo 1. Go to https://railway.app
echo 2. Click 'New Project' - 'Deploy from GitHub'
echo 3. Select your 'student-tracker' repository
echo 4. Click 'Deploy'
echo.
echo Your app will be live in 2-3 minutes! 🎉
echo.
pause
