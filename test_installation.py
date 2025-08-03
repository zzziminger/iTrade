#!/usr/bin/env python3
"""
Test script to verify iTrade installation
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    modules = [
        'flask',
        'flask_sqlalchemy', 
        'flask_login',
        'werkzeug',
        'yfinance',
        'plotly',
        'fredapi',
        'openai',
        'newsapi',
        'requests',
        'dotenv'
    ]
    
    failed_imports = []
    
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All imports successful!")
        return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test Flask app creation
        from flask import Flask
        app = Flask(__name__)
        print("✅ Flask app creation")
        
        # Test yfinance (basic test without API calls)
        import yfinance as yf
        print("✅ Yahoo Finance API")
        
        # Test plotly
        import plotly.graph_objs as go
        fig = go.Figure()
        print("✅ Plotly charts")
        
        print("\n✅ All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 iTrade Installation Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test functionality
    functionality_ok = test_basic_functionality()
    
    print("\n" + "=" * 40)
    if imports_ok and functionality_ok:
        print("🎉 All tests passed! iTrade is ready to run.")
        print("\nTo start the application:")
        print("python iTrade.py")
    else:
        print("❌ Some tests failed. Please check the installation.")
        print("\nTry running:")
        print("pip install -r requirements_simple.txt")

if __name__ == "__main__":
    main() 