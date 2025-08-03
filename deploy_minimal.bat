@echo off
echo ========================================
echo iTrade - Minimal Vercel Deployment
echo ========================================

echo.
echo 1. Adding minimal files to Git...
git add iTrade_minimal.py requirements_minimal.txt vercel.json

echo.
echo 2. Committing minimal version...
git commit -m "Add minimal version for Vercel (under 250MB limit)"

echo.
echo 3. Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo Minimal deployment completed!
echo ========================================
echo.
echo Your minimal app should now deploy successfully on Vercel.
echo Size: Under 50MB (well under 250MB limit)
echo.
pause 