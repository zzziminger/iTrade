#!/bin/bash

# iTrade Vercel Deployment Script

echo "🚀 Preparing iTrade for Vercel deployment..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No remote origin found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/yourusername/iTrade.git"
    exit 1
fi

# Add all files
echo "📁 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Prepare for Vercel deployment - $(date)"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo "✅ Repository updated successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Go to https://vercel.com"
echo "2. Sign in with your GitHub account"
echo "3. Click 'New Project'"
echo "4. Import your iTrade repository"
echo "5. Configure environment variables:"
echo "   - FRED_API_KEY=your-fred-api-key"
echo "   - OPENAI_API_KEY=your-openai-api-key"
echo "   - NEWS_API_KEY=your-news-api-key"
echo "   - SECRET_KEY=your-secret-key"
echo "6. Click 'Deploy'"
echo ""
echo "🌐 Your app will be live at: https://your-project-name.vercel.app" 