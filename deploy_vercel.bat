@echo off
echo ========================================
echo iTrade - Vercel Deployment Script
echo ========================================

echo.
echo 1. Adding files to Git...
git add .

echo.
echo 2. Committing changes...
git commit -m "Deploy lightweight version for Vercel (fix 250MB limit)"

echo.
echo 3. Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo Deployment completed!
echo ========================================
echo.
echo Your app should now deploy successfully on Vercel.
echo Check: https://vercel.com/dashboard
echo.
pause 