# Manual Git Setup for iTrade GitHub Repository

This guide will help you manually set up Git and connect to the [iTrade GitHub repository](https://github.com/QO2021/iTrade.git).

## 🚀 Step 1: Install Git

### **Download Git**
1. Go to: https://git-scm.com/downloads
2. Download the Windows version
3. Run the installer
4. **Important**: Check "Add Git to PATH" during installation
5. Restart your command prompt

### **Verify Installation**
```bash
git --version
# Should show: git version 2.x.x
```

## 🔗 Step 2: Set Up GitHub Connection

### **Initialize Git Repository**
```bash
# Initialize Git repository
git init

# Add remote origin
git remote add origin https://github.com/QO2021/iTrade.git

# Verify remote
git remote -v
```

### **Configure Git (First Time Only)**
```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

## 📦 Step 3: Sync Your Code

### **Add Your Files**
```bash
# Add all files
git add .

# Check what will be committed
git status
```

### **Commit Your Changes**
```bash
# Commit with a descriptive message
git commit -m "Update iTrade with Python 3.12 compatibility and enhanced features"
```

### **Push to GitHub**
```bash
# Push to GitHub (first time)
git push -u origin main

# Future pushes
git push
```

## 🔐 Step 4: GitHub Authentication

### **Option 1: Personal Access Token (Recommended)**
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`
4. Copy the token
5. Use token as password when pushing

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

## 📋 Repository Structure Comparison

### **Your Local Files:**
```
iTrade/
├── app.py                 # Main Flask application (renamed from iTrade.py)
├── requirements.txt       # Updated dependencies
├── templates/            # Complete HTML templates
├── static/              # CSS and JavaScript files
├── vercel.json          # Vercel deployment config
├── runtime.txt          # Python version
├── Procfile            # Start command
├── .gitignore          # Git ignore rules
├── setup_git.bat       # Git setup script
├── GITHUB_SYNC_GUIDE.md # This guide
└── MANUAL_GIT_SETUP.md # Manual setup guide
```

### **GitHub Repository Files:**
```
iTrade/
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── README.md           # Project documentation
├── templates/          # Jinja2 templates
├── static/            # Static assets
├── instance/          # Instance-specific files
└── run.sh             # Run script
```

## 🔄 Sync Strategies

### **Strategy 1: Update GitHub with Your Local Code**
```bash
# Your local code is more advanced
git add .
git commit -m "Update iTrade with Python 3.12 compatibility and Vercel deployment"
git push origin main
```

### **Strategy 2: Merge Both Versions**
```bash
# Fetch GitHub changes
git fetch origin

# Merge changes
git merge origin/main

# Resolve conflicts if any
# Then commit and push
git add .
git commit -m "Merge local and GitHub changes"
git push origin main
```

### **Strategy 3: Start Fresh from GitHub**
```bash
# Backup your current files
# Then clone fresh from GitHub
git clone https://github.com/QO2021/iTrade.git
cd iTrade
```

## 🚨 Troubleshooting

### **Issue: "Git not found"**
**Solution:**
1. Install Git from https://git-scm.com/downloads
2. Make sure to check "Add to PATH"
3. Restart command prompt

### **Issue: "Authentication failed"**
**Solution:**
```bash
# Use Personal Access Token
git remote set-url origin https://YOUR_TOKEN@github.com/QO2021/iTrade.git
```

### **Issue: "Repository not found"**
**Solution:**
1. Check URL: `https://github.com/QO2021/iTrade.git`
2. Ensure you have access to the repository
3. Verify your GitHub account permissions

### **Issue: "Permission denied"**
**Solution:**
```bash
# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📊 Current Status

### **✅ Your Local Environment:**
- Python 3.12.6 (excellent compatibility)
- All dependencies installed and working
- Application ready to run
- Vercel deployment configuration complete
- File structure matches GitHub

### **✅ Ready for GitHub:**
- `app.py` (main application)
- `requirements.txt` (updated dependencies)
- Complete templates and static files
- Deployment configuration
- Documentation

## 🎯 Quick Commands

### **After Git Installation:**
```bash
# Initialize repository
git init

# Add remote
git remote add origin https://github.com/QO2021/iTrade.git

# Add files
git add .

# Commit
git commit -m "Update iTrade with Python 3.12 compatibility"

# Push
git push -u origin main
```

### **Check Status:**
```bash
# Check Git status
git status

# Check remote
git remote -v

# Check commits
git log --oneline
```

---

**Your iTrade application is ready to sync with GitHub!** 🚀

Follow the steps above to connect your local code to the GitHub repository. 