@echo off
echo 🐍 Setting up Python 3.11 environment for iTrade...

REM Check if Python 3.11 exists
if exist "C:\Users\ouqin\AppData\Local\Programs\Python\Python311\python.exe" (
    echo ✅ Found Python 3.11
    set PYTHON_PATH=C:\Users\ouqin\AppData\Local\Programs\Python\Python311\python.exe
) else (
    echo ❌ Python 3.11 not found at expected location
    echo Please install Python 3.11 from https://python.org
    pause
    exit /b 1
)

REM Remove old virtual environment
if exist "venv" (
    echo 🗑️ Removing old virtual environment...
    rmdir /s /q venv
)

REM Create new virtual environment with Python 3.11
echo 📦 Creating new virtual environment with Python 3.11...
"%PYTHON_PATH%" -m venv venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate

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

echo ✅ Python 3.11 environment setup complete!
echo.
echo 🚀 To activate the environment:
echo    venv\Scripts\activate
echo.
echo 🏃 To run the application:
echo    python iTrade.py
echo.
echo 🧪 To test the installation:
echo    python test_installation.py
echo.
echo 📊 Python version:
python --version
pause 