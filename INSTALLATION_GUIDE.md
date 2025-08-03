# iTrade Python Installation Guide

This guide will help you install the iTrade Python application, especially if you encounter issues with pandas and Python 3.13.

## 🚀 Quick Installation

### Option 1: Automated Setup (Recommended)

```bash
python setup_python.py
```

### Option 2: Manual Installation

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements_simple.txt

# 4. Test installation
python test_installation.py

# 5. Run the application
python iTrade.py
```

## 🔧 Troubleshooting

### Issue: pandas installation fails on Python 3.13

**Problem**: pandas 2.1.1 is not compatible with Python 3.13.

**Solution**: Use the simplified requirements file that doesn't include pandas:

```bash
pip install -r requirements_simple.txt
```

### Issue: Visual Studio Build Tools required

**Problem**: Some packages require C++ build tools on Windows.

**Solution**: 
1. Install Visual Studio Build Tools
2. Or use pre-compiled wheels:

```bash
pip install --only-binary=all -r requirements_simple.txt
```

### Issue: yfinance installation fails

**Problem**: yfinance dependency issues.

**Solution**: Install yfinance separately:

```bash
pip install yfinance --upgrade
```

### Issue: FRED API key not working

**Problem**: FRED API requires authentication.

**Solution**: 
1. Get free API key from [FRED](https://fred.stlouisfed.org/docs/api/api_key.html)
2. Add to your `.env` file:

```env
FRED_API_KEY=your-fred-api-key
```

## 📦 Alternative Installation Methods

### Method 1: Minimal Installation

If you only want basic functionality:

```bash
pip install Flask Flask-SQLAlchemy Flask-Login yfinance plotly requests
```

### Method 2: Conda Installation

If you use Anaconda:

```bash
conda create -n itrade python=3.11
conda activate itrade
pip install -r requirements.txt
```

### Method 3: Docker Installation

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements_simple.txt .
RUN pip install -r requirements_simple.txt

COPY . .
EXPOSE 5000

CMD ["python", "iTrade.py"]
```

## 🧪 Testing Your Installation

After installation, run the test script:

```bash
python test_installation.py
```

This will verify that all required modules are working correctly.

## 🔑 Required API Keys

Before running the application, you need these API keys:

### 1. FRED API Key (Free)
- Visit: https://fred.stlouisfed.org/docs/api/api_key.html
- Get free API key
- Add to `.env`: `FRED_API_KEY=your-key`

### 2. OpenAI API Key (Paid)
- Visit: https://platform.openai.com
- Create account and get API key
- Add to `.env`: `OPENAI_API_KEY=your-key`

### 3. News API Key (Free)
- Visit: https://newsapi.org
- Get free API key
- Add to `.env`: `NEWS_API_KEY=your-key`

### 4. Email Configuration (Optional)
For password reset functionality:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
```

## 🚀 Running the Application

### Development Mode

```bash
python iTrade.py
```

Access at: http://localhost:5000

### Production Mode

```bash
gunicorn -w 4 -b 0.0.0.0:8000 iTrade:app
```

## 📁 Project Structure

```
iTrade/
├── iTrade.py              # Main application
├── requirements.txt        # Full dependencies
├── requirements_simple.txt # Simplified dependencies
├── setup_python.py        # Automated setup
├── test_installation.py   # Installation test
├── templates/             # HTML templates
├── static/               # Static files
└── .env                  # Environment variables
```

## 🔍 Common Issues and Solutions

### Issue: "ModuleNotFoundError: No module named 'pandas'"

**Solution**: The application works without pandas. Use `requirements_simple.txt`:

```bash
pip install -r requirements_simple.txt
```

### Issue: "yfinance not found"

**Solution**: Install yfinance separately:

```bash
pip install yfinance
```

### Issue: "Flask-Login not found"

**Solution**: Install Flask-Login:

```bash
pip install Flask-Login
```

### Issue: Database errors

**Solution**: The database will be created automatically on first run. If issues persist:

```bash
# Remove existing database
rm itrade.db

# Run the application (database will be recreated)
python iTrade.py
```

## 📞 Getting Help

If you encounter issues:

1. **Check Python version**: Ensure you're using Python 3.8+
2. **Use virtual environment**: Always use a virtual environment
3. **Test installation**: Run `python test_installation.py`
4. **Check API keys**: Ensure all API keys are set in `.env`
5. **Check logs**: Look for error messages in the console

## 🎯 Next Steps

After successful installation:

1. **Configure API keys** in `.env` file
2. **Run the application**: `python iTrade.py`
3. **Access the web interface**: http://localhost:5000
4. **Register an account** and start using iTrade!

---

**iTrade Python** - Your trusted platform for smart trading decisions. 