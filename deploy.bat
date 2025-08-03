@echo off
echo 🚀 Preparing iTrade for Vercel deployment...

REM Check if git is initialized
if not exist ".git" (
    echo ❌ Git repository not found. Please initialize git first:
    echo    git init
    echo    git add .
    echo    git commit -m "Initial commit"
    pause
    exit /b 1
)

REM Check if remote origin exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo ❌ No remote origin found. Please add your GitHub repository:
    echo    git remote add origin https://github.com/yourusername/iTrade.git
    pause
    exit /b 1
)

REM Add all files
echo 📁 Adding files to git...
git add .

REM Commit changes
echo 💾 Committing changes...
git commit -m "Prepare for Vercel deployment - %date% %time%"

REM Push to GitHub
echo 📤 Pushing to GitHub...
git push origin main

echo ✅ Repository updated successfully!
echo.
echo 🎯 Next steps:
echo 1. Go to https://vercel.com
echo 2. Sign in with your GitHub account
echo 3. Click 'New Project'
echo 4. Import your iTrade repository
echo 5. Configure environment variables:
echo    - FRED_API_KEY=your-fred-api-key
echo    - OPENAI_API_KEY=your-openai-api-key
echo    - NEWS_API_KEY=your-news-api-key
echo    - SECRET_KEY=your-secret-key
echo 6. Click 'Deploy'
echo.
echo 🌐 Your app will be live at: https://your-project-name.vercel.app
pause 