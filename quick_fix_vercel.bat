@echo off
echo 🚀 Quick Fix for Vercel 404 Error...

echo.
echo 📋 Step 1: Installing Git using winget...
winget install Git.Git --accept-source-agreements --accept-package-agreements

if errorlevel 1 (
    echo ❌ Failed to install Git via winget
    echo 📥 Please manually install Git from: https://git-scm.com/downloads
    echo    - Download and run the installer
    echo    - Use default settings
    echo    - Make sure to check "Add Git to PATH"
    echo    - Restart this command prompt after installation
    pause
    exit /b 1
)

echo ✅ Git installed successfully!

echo.
echo 📋 Step 2: Refreshing PATH...
call refreshenv

echo.
echo 📋 Step 3: Setting up Git repository...
git init
git remote add origin https://github.com/QO2021/iTrade.git

echo.
echo 📋 Step 4: Adding and committing files...
git add .
git commit -m "Fix Vercel deployment - Update app.py and configuration"

echo.
echo 📋 Step 5: Pushing to GitHub...
git push -f origin main

echo.
echo ✅ Done! Vercel should redeploy automatically.
echo 🌐 Check: https://i-trade-five.vercel.app
echo.
pause 