@echo off
echo 🚀 Pushing iTrade to GitHub repository...

REM Check if Git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/downloads
    echo Make sure to add Git to PATH during installation
    pause
    exit /b 1
)

echo ✅ Git found:
git --version

REM Initialize Git repository if not already done
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
) else (
    echo ✅ Git repository already exists
)

REM Configure Git with token
echo 🔗 Setting up GitHub connection with token...
git remote remove origin 2>nul
git remote add origin https://github.com/QO2021/iTrade.git

REM Check remote
echo 📋 Current remotes:
git remote -v

REM Add all files
echo 📁 Adding files to Git...
git add .

REM Check status
echo 📊 Git status:
git status

REM Commit changes
echo 💾 Committing changes...
git commit -m "Update iTrade with Python 3.12 compatibility and Vercel deployment"

REM Push to GitHub
echo 📤 Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo ❌ Push failed. This might be because:
    echo    - The repository already has content
    echo    - You need to pull first
    echo    - The token might have expired
    echo.
    echo 💡 Try these solutions:
    echo    1. git pull origin main --allow-unrelated-histories
    echo    2. Then: git push origin main
    echo    3. Or create a new repository
) else (
    echo ✅ Successfully pushed to GitHub!
    echo 🌐 Your code is now available at: https://github.com/QO2021/iTrade
)

echo.
pause 