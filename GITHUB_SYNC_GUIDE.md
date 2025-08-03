# GitHub Repository Sync Guide

This guide will help you sync your local iTrade code with the GitHub repository at [https://github.com/QO2021/iTrade.git](https://github.com/QO2021/iTrade.git).

## 🚀 Quick Setup

### **Option 1: Automated Setup**
```bash
# Run the Git setup script
.\setup_git.bat
```

### **Option 2: Manual Setup**

#### **Step 1: Install Git (if not installed)**
1. Download Git from: https://git-scm.com/downloads
2. Install with default settings
3. Make sure to check "Add Git to PATH"
4. Restart your terminal/command prompt

#### **Step 2: Initialize Git Repository**
```bash
# Initialize Git repository
git init

# Add remote origin
git remote add origin https://github.com/QO2021/iTrade.git

# Verify remote
git remote -v
```

#### **Step 3: Sync with GitHub**
```bash
# Add all files
git add .

# Commit changes
git commit -m "Update iTrade application with Python 3.12 compatibility"

# Push to GitHub
git push -u origin main
```

## 📋 GitHub Repository Structure

Based on the [GitHub repository](https://github.com/QO2021/iTrade.git), your local structure should match:

```
iTrade/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # Project documentation
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Landing page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # Trading dashboard
│   ├── stock_detail.html # Stock information page
│   ├── trade.html        # Trading interface
│   └── portfolio.html    # Portfolio management
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── app.js        # JavaScript functionality
└── instance/             # Instance-specific files
    └── itrade.db         # SQLite database (created automatically)
```

## 🔄 Syncing Strategies

### **Strategy 1: Push Local Changes to GitHub**
If you want to update the GitHub repository with your local changes:

```bash
# Add all files
git add .

# Commit changes
git commit -m "Update iTrade with Python 3.12 compatibility and Vercel deployment"

# Push to GitHub
git push origin main
```

### **Strategy 2: Pull from GitHub**
If you want to get the latest changes from GitHub:

```bash
# Fetch latest changes
git fetch origin

# Pull changes
git pull origin main
```

### **Strategy 3: Merge Both Versions**
If you want to combine local and remote changes:

```bash
# Fetch remote changes
git fetch origin

# Merge remote changes
git merge origin/main

# Resolve any conflicts manually
# Then commit and push
git add .
git commit -m "Merge local and remote changes"
git push origin main
```

## 🔧 Key Differences to Address

### **File Name Changes**
- **Local**: `iTrade.py` (main application)
- **GitHub**: `app.py` (main application)

### **Template Structure**
- **Local**: Comprehensive templates with all features
- **GitHub**: Basic templates

### **Dependencies**
- **Local**: Updated for Python 3.12 compatibility
- **GitHub**: May have older versions

## 📝 Recommended Actions

### **1. Update Main Application File**
```bash
# Rename iTrade.py to app.py to match GitHub
ren iTrade.py app.py
```

### **2. Update Requirements**
Make sure your `requirements.txt` includes all necessary dependencies:

```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
yfinance==0.2.28
plotly==5.18.0
fredapi==0.5.1
openai==1.12.0
newsapi-python==0.2.6
requests==2.31.0
python-dotenv==1.0.1
gunicorn==21.2.0
```

### **3. Update README**
Update your README.md to match the GitHub structure and include your improvements.

### **4. Environment Variables**
Create `.env.example` file:

```env
SECRET_KEY=your-super-secret-key-here
FRED_API_KEY=your-fred-api-key
OPENAI_API_KEY=your-openai-api-key
NEWS_API_KEY=your-news-api-key
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## 🔐 GitHub Authentication

### **Option 1: Personal Access Token**
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate new token with repo permissions
3. Use token as password when pushing

### **Option 2: GitHub CLI**
```bash
# Install GitHub CLI
winget install GitHub.cli

# Login
gh auth login
```

### **Option 3: SSH Keys**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to GitHub
# Copy public key to GitHub Settings > SSH and GPG keys
```

## 🚨 Troubleshooting

### **Issue: "Authentication failed"**
**Solution:**
```bash
# Use Personal Access Token
git remote set-url origin https://YOUR_TOKEN@github.com/QO2021/iTrade.git
```

### **Issue: "Repository not found"**
**Solution:**
1. Check repository URL: `https://github.com/QO2021/iTrade.git`
2. Ensure you have access to the repository
3. Verify your GitHub account has proper permissions

### **Issue: "Merge conflicts"**
**Solution:**
```bash
# See conflicts
git status

# Edit conflicted files manually
# Then add and commit
git add .
git commit -m "Resolve merge conflicts"
```

## 📊 Current Status

### **Your Local Environment:**
- ✅ Python 3.12.6 (excellent compatibility)
- ✅ All dependencies installed
- ✅ Application working perfectly
- ✅ Vercel deployment ready

### **GitHub Repository:**
- ✅ Public repository available
- ✅ Basic Flask application structure
- ✅ Templates and static files
- ⚠️ May need updates for latest dependencies

## 🎯 Next Steps

1. **Install Git** (if not already installed)
2. **Run setup script**: `.\setup_git.bat`
3. **Choose sync strategy** (push local changes or pull from GitHub)
4. **Update file names** to match GitHub structure
5. **Push changes** to GitHub repository

---

**Your iTrade application is ready to sync with GitHub!** 🚀

Choose your preferred sync strategy and follow the steps above. 