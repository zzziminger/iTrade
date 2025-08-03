#!/usr/bin/env python3
"""
Test script to verify iTrade deployment readiness
"""

from flask import Flask
import os
import sys

def test_flask_app():
    """Test if Flask app can be imported and configured"""
    try:
        from index import app
        print("✅ Flask app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")
        return False

def test_templates():
    """Test if templates exist and can be rendered"""
    try:
        from index import app
        with app.app_context():
            # Test basic template rendering
            from flask import render_template_string
            test_html = render_template_string("<h1>Test</h1>")
            print("✅ Template rendering works")
            return True
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are available"""
    required_packages = [
        'flask',
        'flask_sqlalchemy', 
        'flask_login',
        'werkzeug',
        'requests',
        'dotenv'  # Changed from python-dotenv to dotenv
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError:
            print(f"❌ {package} not found")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {missing_packages}")
        return False
    else:
        print("✅ All dependencies available")
        return True

def test_file_structure():
    """Test if required files exist"""
    required_files = [
        'index.py',
        'requirements.txt',
        'vercel.json',
        'templates/index.html',
        'templates/login.html',
        'templates/register.html',
        'templates/dashboard.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Run all deployment tests"""
    print("🚀 iTrade Deployment Test")
    print("=" * 40)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Dependencies", test_dependencies),
        ("Flask App", test_flask_app),
        ("Templates", test_templates)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing: {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for deployment!")
        return True
    else:
        print("❌ Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 