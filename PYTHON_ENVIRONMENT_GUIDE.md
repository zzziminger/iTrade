# Python Environment Setup Guide for iTrade

This guide will help you choose and set up the right Python environment for your iTrade project.

## 🐍 Python Version Options

### **Recommended: Python 3.11**
- **Best compatibility** with all dependencies
- **Stable and well-tested**
- **Full pandas support**
- **Recommended for production**

### **Alternative: Python 3.10**
- **Good compatibility**
- **Stable performance**
- **Widely supported**

### **Latest: Python 3.13**
- **Newest features**
- **Some compatibility issues** with pandas
- **Use `requirements_simple.txt`** (without pandas)

## 🔍 Check Your Current Python Version

### **Windows**
```bash
python --version
# or
python3 --version
```

### **macOS/Linux**
```bash
python3 --version
# or
python --version
```

## 📦 Environment Management Options

### **Option 1: Virtual Environment (Recommended)**

#### **Create Virtual Environment**
```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

#### **Activate Virtual Environment**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### **Install Dependencies**
```bash
# For Python 3.11 or 3.10 (with pandas)
pip install -r requirements.txt

# For Python 3.13 (without pandas)
pip install -r requirements_simple.txt
```

### **Option 2: Conda Environment**

#### **Install Anaconda/Miniconda**
- Download from: https://docs.conda.io/en/latest/miniconda.html

#### **Create Conda Environment**
```bash
# Create environment with Python 3.11
conda create -n itrade python=3.11

# Activate environment
conda activate itrade

# Install dependencies
pip install -r requirements.txt
```

### **Option 3: pyenv (Advanced)**

#### **Install pyenv**
```bash
# macOS
brew install pyenv

# Linux
curl https://pyenv.run | bash

# Windows (using pyenv-win)
pip install pyenv-win
```

#### **Install Python Version**
```bash
# List available versions
pyenv install --list

# Install Python 3.11.7
pyenv install 3.11.7

# Set local version
pyenv local 3.11.7

# Create virtual environment
python -m venv venv
```

## 🛠️ Environment Setup Scripts

### **Windows Setup Script**
```batch
@echo off
echo 🐍 Setting up Python environment for iTrade...

REM Check Python version
python --version
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

echo ✅ Environment setup complete!
echo.
echo 🚀 To activate the environment:
echo    venv\Scripts\activate
echo.
echo 🏃 To run the application:
echo    python iTrade.py
pause
```

### **macOS/Linux Setup Script**
```bash
#!/bin/bash

echo "🐍 Setting up Python environment for iTrade..."

# Check Python version
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Environment setup complete!"
echo ""
echo "🚀 To activate the environment:"
echo "   source venv/bin/activate"
echo ""
echo "🏃 To run the application:"
echo "   python iTrade.py"
```

## 🔧 Environment Configuration

### **VS Code Configuration**

#### **Select Python Interpreter**
1. Open VS Code
2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
3. Type "Python: Select Interpreter"
4. Choose your virtual environment:
   - `./venv/Scripts/python.exe` (Windows)
   - `./venv/bin/python` (macOS/Linux)

#### **Create `.vscode/settings.json`**
```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
}
```

### **PyCharm Configuration**

#### **Set Project Interpreter**
1. Go to `File > Settings > Project > Python Interpreter`
2. Click the gear icon
3. Select "Add"
4. Choose "Existing Environment"
5. Browse to your virtual environment:
   - `venv/Scripts/python.exe` (Windows)
   - `venv/bin/python` (macOS/Linux)

## 📋 Environment Checklist

### **Before Starting**
- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] Environment activated
- [ ] Dependencies installed
- [ ] API keys configured

### **Testing Your Environment**
```bash
# Test Python version
python --version

# Test imports
python -c "import flask; print('Flask OK')"
python -c "import yfinance; print('yfinance OK')"
python -c "import plotly; print('plotly OK')"

# Test application
python iTrade.py
```

## 🚨 Troubleshooting

### **Common Issues**

#### **Issue: "No module named 'flask'"`
**Solution:**
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

#### **Issue: "pandas installation fails"**
**Solution:**
```bash
# Use simplified requirements
pip install -r requirements_simple.txt
```

#### **Issue: "Python not found"**
**Solution:**
1. Install Python from https://python.org
2. Add Python to PATH during installation
3. Restart terminal/command prompt

#### **Issue: "Permission denied"**
**Solution:**
```bash
# macOS/Linux
sudo python3 -m venv venv

# Or use user installation
pip install --user -r requirements.txt
```

### **Environment-Specific Issues**

#### **Windows Issues**
```bash
# If virtual environment activation fails
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# If pip is not recognized
python -m pip install --upgrade pip
```

#### **macOS Issues**
```bash
# If python3 not found
brew install python

# If pip not found
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

#### **Linux Issues**
```bash
# Install Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip

# Create virtual environment
python3.11 -m venv venv
```

## 🎯 Recommended Setup

### **For Development**
```bash
# 1. Install Python 3.11
# 2. Create virtual environment
python -m venv venv

# 3. Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Test installation
python test_installation.py

# 6. Run application
python iTrade.py
```

### **For Production (Vercel)**
- Use Python 3.11 (specified in `runtime.txt`)
- Dependencies listed in `requirements.txt`
- Environment variables set in Vercel dashboard

## 📊 Environment Comparison

| Environment | Pros | Cons | Best For |
|-------------|------|------|----------|
| Virtual Environment | Lightweight, isolated | Manual activation | Development |
| Conda | Easy package management | Larger size | Data science |
| pyenv | Multiple Python versions | Complex setup | Advanced users |
| System Python | No setup required | Conflicts possible | Quick testing |

## 🔄 Switching Environments

### **Deactivate Current Environment**
```bash
deactivate
```

### **Activate Different Environment**
```bash
# Virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Conda environment
conda activate itrade

# pyenv environment
pyenv local 3.11.7
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
Set these in Vercel dashboard:
- `FLASK_ENV=production`
- `SECRET_KEY=your-prod-secret-key`
- `FRED_API_KEY=your-fred-api-key`
- `OPENAI_API_KEY=your-openai-api-key`
- `NEWS_API_KEY=your-news-api-key`

---

**Choose the environment that best fits your needs and follow the setup guide above!** 🚀 