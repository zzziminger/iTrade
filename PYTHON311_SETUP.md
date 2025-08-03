# Python 3.11 Setup Guide for iTrade

This guide will help you switch to Python 3.11 for better compatibility with all dependencies.

## 🐍 Why Python 3.11?

- **Better pandas compatibility** - No installation issues
- **Stable and well-tested** - Production ready
- **Full feature support** - All dependencies work perfectly
- **Recommended for Vercel** - Matches production environment

## 📦 Step 1: Install Python 3.11

### **Download Python 3.11**
1. Go to https://www.python.org/downloads/
2. Download Python 3.11.x (latest 3.11 version)
3. Run the installer
4. **Important**: Check "Add Python to PATH" during installation

### **Verify Installation**
```bash
python --version
# Should show: Python 3.11.x
```

## 🔧 Step 2: Set Up New Environment

### **Option A: Automated Setup (Recommended)**
```bash
# Run the setup script
.\setup_python311.bat
```

### **Option B: Manual Setup**
```bash
# 1. Remove old environment
rmdir /s /q venv

# 2. Create new environment with Python 3.11
python -m venv venv

# 3. Activate environment
venv\Scripts\activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Test installation
python test_installation.py
```

## 🚀 Step 3: Verify Setup

### **Check Python Version**
```bash
python --version
# Should show: Python 3.11.x
```

### **Test Installation**
```bash
python test_installation.py
```

### **Run Application**
```bash
python iTrade.py
```

## 🔍 Troubleshooting

### **Issue: "Python 3.11 not found"**
**Solution:**
1. Install Python 3.11 from https://python.org
2. Make sure to check "Add to PATH" during installation
3. Restart command prompt
4. Run setup script again

### **Issue: "Permission denied"**
**Solution:**
```bash
# Run as administrator or use user installation
pip install --user -r requirements.txt
```

### **Issue: "Virtual environment activation fails"**
**Solution:**
```bash
# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📊 Environment Comparison

| Feature | Python 3.13 | Python 3.11 |
|---------|-------------|-------------|
| pandas | ❌ Issues | ✅ Works |
| yfinance | ✅ Works | ✅ Works |
| Flask | ✅ Works | ✅ Works |
| Vercel | ⚠️ Limited | ✅ Full Support |
| Stability | ⚠️ New | ✅ Stable |

## 🎯 Benefits of Python 3.11

1. **Full pandas support** - No installation issues
2. **Better compatibility** - All packages work
3. **Production ready** - Stable for deployment
4. **Vercel optimized** - Matches production environment
5. **Wide support** - Most packages tested

## 📋 Quick Commands

### **Activate Environment**
```bash
venv\Scripts\activate
```

### **Check Version**
```bash
python --version
```

### **Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Test Installation**
```bash
python test_installation.py
```

### **Run Application**
```bash
python iTrade.py
```

## 🔄 Switching Between Python Versions

### **To Python 3.11**
```bash
# Use the setup script
.\setup_python311.bat
```

### **To Python 3.13**
```bash
# Use the original setup
.\setup_env.bat
```

## 📝 Environment Variables

### **Development (.env file)**
```env
FLASK_ENV=development
SECRET_KEY=your-dev-secret-key
FRED_API_KEY=your-fred-api-key
OPENAI_API_KEY=your-openai-api-key
NEWS_API_KEY=your-news-api-key
```

### **Production (Vercel)**
Set in Vercel dashboard:
- `FLASK_ENV=production`
- `SECRET_KEY=your-prod-secret-key`
- `FRED_API_KEY=your-fred-api-key`
- `OPENAI_API_KEY=your-openai-api-key`
- `NEWS_API_KEY=your-news-api-key`

---

**Python 3.11 is the recommended choice for iTrade!** 🚀

It provides the best compatibility and stability for all features. 