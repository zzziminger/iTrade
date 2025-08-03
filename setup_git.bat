@echo off
echo 🚀 Setting up Git connection to GitHub repository...

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

REM Add remote origin
echo 🔗 Adding remote origin...
git remote add origin https://github.com/QO2021/iTrade.git

REM Check if remote was added successfully
git remote -v

echo.
echo 📋 Next steps:
echo 1. Add your files: git add .
echo 2. Commit changes: git commit -m "Initial commit"
echo 3. Push to GitHub: git push -u origin main
echo.
echo 💡 If you get authentication errors, you may need to:
echo    - Set up GitHub authentication (Personal Access Token)
echo    - Or use GitHub CLI: gh auth login
echo.
pause 