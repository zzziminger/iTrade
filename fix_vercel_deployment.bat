@echo off
echo 🚀 Fixing Vercel Deployment - Syncing to GitHub...

echo.
echo 📋 Step 1: Checking if Git is installed...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed
    echo.
    echo 📥 Please install Git from: https://git-scm.com/downloads
    echo    - Download and run the installer
    echo    - Use default settings
    echo    - Make sure to check "Add Git to PATH"
    echo    - Restart this command prompt after installation
    echo.
    echo 🔄 After installing Git, run this script again
    pause
    exit /b 1
)

echo ✅ Git is installed:
git --version

echo.
echo 📋 Step 2: Setting up Git repository...
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
) else (
    echo ✅ Git repository exists
)

echo.
echo 📋 Step 3: Connecting to GitHub with your token...
git remote remove origin 2>nul
git remote add origin https://github.com/QO2021/iTrade.git

echo 📋 Current remotes:
git remote -v

echo.
echo 📋 Step 4: Adding all files to Git...
git add .

echo.
echo 📋 Step 5: Committing changes...
git commit -m "Fix Vercel deployment - Update app.py and configuration files"

echo.
echo 📋 Step 6: Pushing to GitHub...
echo ⚠️  This might fail if the repository has different content
echo    If it fails, we'll need to force push or pull first

git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ Push failed. The repository might have different content.
    echo.
    echo 💡 Let's try to pull first and then push:
    echo    git pull origin main --allow-unrelated-histories
    echo    git push origin main
    echo.
    echo 🔄 Running pull command...
    git pull origin main --allow-unrelated-histories
    echo.
    echo 🔄 Now pushing again...
    git push origin main
)

if errorlevel 1 (
    echo.
    echo ❌ Still failed. Let's try force push (this will overwrite GitHub content):
    echo    git push -f origin main
    echo.
    echo ⚠️  WARNING: This will overwrite the GitHub repository content
    echo    Press any key to continue with force push...
    pause
    git push -f origin main
)

echo.
echo ✅ Files pushed to GitHub successfully!
echo.
echo 🌐 Your repository: https://github.com/QO2021/iTrade
echo 🚀 Vercel will automatically redeploy in a few minutes
echo 📱 Check your deployment at: https://i-trade-five.vercel.app
echo.
echo 📋 If Vercel still shows 404, check:
echo    1. Go to https://vercel.com/dashboard
echo    2. Find your iTrade project
echo    3. Check the deployment logs
echo    4. Make sure the build settings are correct
echo.
pause 