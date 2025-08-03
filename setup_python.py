#!/usr/bin/env python3
"""
iTrade Python Setup Script
Automates the installation and setup process for the iTrade Python application.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Print the setup banner"""
    print("🚀 iTrade Python Setup Script")
    print("=" * 40)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print("✅ pip is available")
    except subprocess.CalledProcessError:
        print("❌ pip is not available. Please install pip first.")
        sys.exit(1)

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✅ Virtual environment created")
        except subprocess.CalledProcessError:
            print("❌ Failed to create virtual environment")
            sys.exit(1)
    else:
        print("✅ Virtual environment already exists")

def get_venv_python():
    """Get the Python executable from virtual environment"""
    if os.name == 'nt':  # Windows
        return Path("venv/Scripts/python.exe")
    else:  # Unix/Linux/macOS
        return Path("venv/bin/python")

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    venv_python = get_venv_python()
    
    try:
        # Try with the main requirements first
        subprocess.run([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("⚠️  Failed to install with main requirements, trying simplified version...")
        try:
            subprocess.run([str(venv_python), "-m", "pip", "install", "-r", "requirements_simple.txt"], 
                          check=True)
            print("✅ Dependencies installed successfully (simplified version)")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("💡 Try installing packages manually:")
            print("   pip install Flask Flask-SQLAlchemy Flask-Login yfinance plotly")
            sys.exit(1)

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("📝 Creating .env file from template...")
            shutil.copy(env_example, env_file)
            print("✅ .env file created")
            print("⚠️  Please edit .env file with your API keys")
        else:
            print("📝 Creating .env file...")
            with open(env_file, 'w') as f:
                f.write("""# Flask Configuration
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development

# Database Configuration
DATABASE_URL=sqlite:///itrade.db

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password

# API Keys
FRED_API_KEY=your-fred-api-key
OPENAI_API_KEY=your-openai-api-key
NEWS_API_KEY=your-news-api-key
""")
            print("✅ .env file created")
            print("⚠️  Please edit .env file with your API keys")
    else:
        print("✅ .env file already exists")

def create_directories():
    """Create necessary directories"""
    print("📁 Creating necessary directories...")
    
    directories = [
        "templates",
        "static",
        "static/css",
        "static/js",
        "static/images",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")

def check_database():
    """Check if database exists"""
    db_file = Path("itrade.db")
    if not db_file.exists():
        print("🗄️  Database will be created on first run")
    else:
        print("✅ Database file exists")

def print_next_steps():
    """Print next steps for the user"""
    print()
    print("🎉 Setup complete!")
    print()
    print("Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Activate virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source venv/bin/activate")
    print("3. Run the application:")
    print("   python iTrade.py")
    print("4. Open your browser and go to: http://localhost:5000")
    print()
    print("📚 For more information, see README_Python.md")

def main():
    """Main setup function"""
    print_banner()
    
    # Check prerequisites
    check_python_version()
    check_pip()
    
    # Setup
    create_virtual_environment()
    install_dependencies()
    create_env_file()
    create_directories()
    check_database()
    
    # Final instructions
    print_next_steps()

if __name__ == "__main__":
    main() 