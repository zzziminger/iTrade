import os
import sys
import traceback

# Debug: Print Python version and environment
print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("Current working directory:", os.getcwd())
print("Environment variables:")
for key, value in os.environ.items():
    if 'VERCEL' in key or 'FLASK' in key:
        print(f"  {key}: {value}")

try:
    # Try to import Flask
    print("\nTrying to import Flask...")
    from flask import Flask
    print("✅ Flask imported successfully")
    
    # Create simple app
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return {"message": "Debug: Flask is working!", "status": "success"}
    
    @app.route('/debug')
    def debug():
        return {
            "python_version": sys.version,
            "flask_version": Flask.__version__,
            "working_directory": os.getcwd(),
            "environment": {k: v for k, v in os.environ.items() if 'VERCEL' in k or 'FLASK' in k}
        }
    
    print("✅ Flask app created successfully")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Traceback:")
    traceback.print_exc()
    sys.exit(1)

if __name__ == '__main__':
    print("✅ Debug script completed successfully")
    app.run(debug=True) 