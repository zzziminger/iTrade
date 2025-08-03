@echo off
echo 🐍 Setting up Python environment for iTrade...

REM Check Python version
python --version
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+
    echo Download from: https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv" (
    echo 📦 Virtual environment already exists
    echo 🔄 Activating virtual environment...
    call venv\Scripts\activate
) else (
    echo 📦 Creating virtual environment...
    python -m venv venv
    
    echo 🔄 Activating virtual environment...
    call venv\Scripts\activate
)

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ⚠️ Some dependencies failed to install
    echo 📥 Trying simplified requirements...
    pip install -r requirements_simple.txt
)

echo ✅ Environment setup complete!
echo.
echo 🚀 To activate the environment:
echo    venv\Scripts\activate
echo.
echo 🏃 To run the application:
echo    python iTrade.py
echo.
echo 🧪 To test the installation:
echo    python test_installation.py
pause 