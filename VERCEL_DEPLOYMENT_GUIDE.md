# Vercel Deployment Guide for iTrade Flask App

## ✅ Current Configuration Status

### **File Structure (All Correct)**
```
✅ app.py                    - Main Flask application
✅ requirements.txt          - Python dependencies
✅ vercel.json              - Vercel configuration
✅ Procfile                 - Production server config
✅ runtime.txt              - Python version (3.11)
✅ templates/index.html     - Landing page
✅ static/css/hero.css      - Custom styles
```

### **Configuration Files**

#### **vercel.json** ✅
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production",
    "FLASK_APP": "app.py"
  },
  "functions": {
    "app.py": {
      "maxDuration": 30
    }
  }
}
```

#### **requirements.txt** ✅
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
yfinance==0.2.28
plotly==5.18.0
fredapi==0.5.1
openai==1.12.0
newsapi-python==0.2.6
requests==2.31.0
python-dotenv==1.0.1
gunicorn==21.2.0
numpy<2
```

#### **Procfile** ✅
```
web: gunicorn app:app
```

#### **runtime.txt** ✅
```
python-3.11
```

## 🚀 Deployment Steps

### **1. GitHub Repository Setup**
```bash
# Ensure your repository is up to date
git add .
git commit -m "Update Vercel configuration"
git push origin main
```

### **2. Vercel Dashboard Setup**
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository: `QO2021/iTrade`
4. Configure project settings:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (default)
   - **Build Command**: Leave empty (auto-detected)
   - **Output Directory**: Leave empty (auto-detected)

### **3. Environment Variables**
Add these in Vercel Dashboard → Settings → Environment Variables:

```env
FLASK_ENV=production
FLASK_APP=app.py
SECRET_KEY=your-super-secret-key-here
FRED_API_KEY=your-fred-api-key
OPENAI_API_KEY=your-openai-api-key
NEWS_API_KEY=your-news-api-key
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
```

### **4. Deploy**
Click "Deploy" in Vercel Dashboard

## 🔧 Troubleshooting

### **Common Issues & Solutions**

#### **Issue 1: "Function not found"**
**Solution**: Ensure `app.py` exists and has the correct Flask app instance
```python
app = Flask(__name__)
# ... your routes ...

if __name__ == '__main__':
    app.run()
```

#### **Issue 2: "Module not found"**
**Solution**: Check requirements.txt includes all dependencies
```bash
pip freeze > requirements.txt
```

#### **Issue 3: "Build failed"**
**Solution**: Check Python version compatibility
```txt
# runtime.txt
python-3.11
```

#### **Issue 4: "Static files not found"**
**Solution**: Ensure static files are in the correct directory
```
static/
├── css/
│   └── hero.css
└── js/
    └── app.js
```

#### **Issue 5: "Database errors"**
**Solution**: Use SQLite for Vercel (already configured)
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///itrade.db'
```

## 📊 Monitoring Deployment

### **Vercel Dashboard**
- **Functions**: Check if `app.py` is listed
- **Build Logs**: Look for any errors during build
- **Function Logs**: Check runtime errors

### **Common Build Log Messages**
```
✅ Installing dependencies...
✅ Building application...
✅ Deploying to Vercel...
```

### **Common Error Messages**
```
❌ ModuleNotFoundError: No module named 'flask'
❌ ImportError: cannot import name 'app'
❌ 404: Function not found
```

## 🎯 Best Practices

### **1. File Naming**
- ✅ Use `app.py` as main file
- ✅ Keep `vercel.json` in root directory
- ✅ Include `requirements.txt` in root

### **2. Dependencies**
- ✅ Pin specific versions in requirements.txt
- ✅ Include all necessary packages
- ✅ Test locally before deploying

### **3. Environment Variables**
- ✅ Set all required environment variables
- ✅ Use production values
- ✅ Keep secrets secure

### **4. Static Files**
- ✅ Place in `static/` directory
- ✅ Reference with `url_for('static', filename='...')`
- ✅ Include in Git repository

## 🔍 Debugging Commands

### **Local Testing**
```bash
# Test Flask app locally
python app.py

# Test with gunicorn
gunicorn app:app

# Check requirements
pip list
```

### **Vercel CLI (Optional)**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from command line
vercel

# Check deployment status
vercel ls
```

## 📱 Expected Result

After successful deployment, your app should be available at:
```
https://i-trade-five.vercel.app
```

The landing page should display:
- ✅ Futuristic financial data visualization background
- ✅ Animated elements and effects
- ✅ Responsive design
- ✅ Working navigation
- ✅ Login/Register functionality

## 🆘 If Still Having Issues

1. **Check Vercel Build Logs**: Look for specific error messages
2. **Verify File Structure**: Ensure all files are in the correct locations
3. **Test Locally**: Run `python app.py` to ensure it works locally
4. **Check Dependencies**: Ensure all packages are in requirements.txt
5. **Environment Variables**: Verify all required env vars are set in Vercel

## 📞 Support

If you continue to have issues:
1. Check the [Vercel Documentation](https://vercel.com/docs)
2. Review the [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
3. Check the [Vercel Community](https://github.com/vercel/vercel/discussions)

---

**Your iTrade application is properly configured for Vercel deployment!** 🚀 