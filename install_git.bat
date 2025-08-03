@echo off
echo 🚀 Installing Git and setting up GitHub connection...

echo.
echo 📦 Step 1: Installing Git...
echo Please download Git from: https://git-scm.com/downloads
echo Make sure to check "Add Git to PATH" during installation
echo.
echo After installing Git, restart this script.
echo.
pause

REM Check if Git is now available
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is still not available. Please install Git first.
    echo Download from: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo ✅ Git found:
git --version

echo.
echo 🔗 Step 2: Setting up GitHub connection...
echo.

REM Initialize Git repository
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
) else (
    echo ✅ Git repository already exists
)

REM Add remote origin
echo 🔗 Adding remote origin...
git remote add origin https://github.com/QO2021/iTrade.git

REM Check remote
echo 📋 Current remotes:
git remote -v

echo.
echo 📋 Step 3: Next steps after Git installation:
echo 1. Add your files: git add .
echo 2. Commit changes: git commit -m "Update iTrade with Python 3.12 compatibility"
echo 3. Push to GitHub: git push -u origin main
echo.
echo 💡 If you get authentication errors, you may need to:
echo    - Set up GitHub authentication (Personal Access Token)
echo    - Or use GitHub CLI: gh auth login
echo.
pause 