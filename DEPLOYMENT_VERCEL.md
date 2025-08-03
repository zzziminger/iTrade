# iTrade Vercel Deployment Guide

This guide will help you deploy your iTrade Python application to Vercel.

## 🚀 Quick Deployment

### Step 1: Prepare Your Repository

1. **Ensure all files are committed to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Verify these files exist in your repository:**
   - `iTrade.py` (main application)
   - `requirements.txt` (dependencies)
   - `vercel.json` (Vercel configuration)
   - `runtime.txt` (Python version)
   - `Procfile` (start command)
   - `.gitignore` (exclude unnecessary files)

### Step 2: Connect to Vercel

1. **Visit Vercel Dashboard**
   - Go to [vercel.com](https://vercel.com)
   - Sign in with your GitHub account

2. **Import Repository**
   - Click "New Project"
   - Select "Import Git Repository"
   - Choose your iTrade repository
   - Click "Import"

3. **Configure Project**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave empty)
   - **Build Command**: Leave empty (Vercel will auto-detect)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

### Step 3: Set Environment Variables

In your Vercel project settings, add these environment variables:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production

# Database Configuration (Vercel uses ephemeral storage)
DATABASE_URL=sqlite:///itrade.db

# API Keys (Required)
FRED_API_KEY=your-fred-api-key
OPENAI_API_KEY=your-openai-api-key
NEWS_API_KEY=your-news-api-key

# Optional Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
```

### Step 4: Deploy

1. **Click "Deploy"**
2. **Wait for build to complete**
3. **Your app will be live at**: `https://your-project-name.vercel.app`

## 🔧 Configuration Files

### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "iTrade.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "iTrade.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

### `requirements.txt`
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
```

### `runtime.txt`
```
python-3.11
```

### `Procfile`
```
web: gunicorn iTrade:app
```

## 📁 Project Structure for Vercel

```
iTrade/
├── iTrade.py              # Main Flask application
├── requirements.txt        # Python dependencies
├── vercel.json           # Vercel configuration
├── runtime.txt           # Python version
├── Procfile             # Start command
├── .gitignore           # Git ignore rules
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── watchlist.html
│   ├── news.html
│   ├── economic.html
│   ├── profile.html
│   ├── forgot_password.html
│   ├── reset_password.html
│   ├── 404.html
│   └── 500.html
└── static/              # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## 🔑 Environment Variables Setup

### Required API Keys

1. **FRED API Key** (Free)
   - Visit: https://fred.stlouisfed.org/docs/api/api_key.html
   - Get free API key
   - Add to Vercel: `FRED_API_KEY=your-key`

2. **OpenAI API Key** (Paid)
   - Visit: https://platform.openai.com
   - Create account and get API key
   - Add to Vercel: `OPENAI_API_KEY=your-key`

3. **News API Key** (Free)
   - Visit: https://newsapi.org
   - Get free API key
   - Add to Vercel: `NEWS_API_KEY=your-key`

### Setting Environment Variables in Vercel

1. **Go to Project Settings**
   - In your Vercel dashboard, click on your project
   - Go to "Settings" tab

2. **Environment Variables**
   - Click "Environment Variables"
   - Add each variable:
     - Name: `FRED_API_KEY`
     - Value: `your-fred-api-key`
     - Environment: Production, Preview, Development
   - Repeat for all required variables

3. **Redeploy**
   - After adding environment variables, redeploy your project

## 🚀 Deployment Commands

### Using Vercel CLI (Optional)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from command line**
   ```bash
   vercel
   ```

4. **Deploy to production**
   ```bash
   vercel --prod
   ```

## 🔍 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` for correct versions
   - Ensure all dependencies are listed
   - Check Python version in `runtime.txt`

2. **Environment Variables Not Working**
   - Verify variables are set in Vercel dashboard
   - Check variable names match your code
   - Redeploy after adding variables

3. **Database Issues**
   - Vercel uses ephemeral storage
   - Database will reset on each deployment
   - Consider using external database for production

4. **API Rate Limits**
   - Monitor API usage
   - Implement caching where possible
   - Consider upgrading API plans

### Debugging

1. **Check Build Logs**
   - In Vercel dashboard, go to "Deployments"
   - Click on failed deployment
   - Check build logs for errors

2. **Local Testing**
   ```bash
   # Test locally first
   python iTrade.py
   ```

3. **Environment Variable Testing**
   ```bash
   # Test with environment variables
   export FRED_API_KEY=your-key
   export OPENAI_API_KEY=your-key
   export NEWS_API_KEY=your-key
   python iTrade.py
   ```

## 📊 Monitoring

### Vercel Analytics
- **Function Logs**: Monitor serverless function execution
- **Performance**: Track response times
- **Errors**: Monitor application errors

### Custom Monitoring
- Add logging to your application
- Monitor API usage
- Track user interactions

## 🔄 Continuous Deployment

### Automatic Deployments
- Vercel automatically deploys on Git pushes
- Configure branch protection rules
- Set up preview deployments for pull requests

### Manual Deployments
- Use Vercel dashboard for manual deployments
- Rollback to previous versions if needed

## 🎯 Best Practices

1. **Environment Variables**
   - Never commit API keys to Git
   - Use Vercel environment variables
   - Keep secrets secure

2. **Database**
   - Use external database for production
   - Implement proper backup strategies
   - Consider using PostgreSQL or MongoDB

3. **Performance**
   - Implement caching strategies
   - Optimize API calls
   - Use CDN for static assets

4. **Security**
   - Keep dependencies updated
   - Implement proper authentication
   - Use HTTPS in production

## 📞 Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Vercel Support**: [vercel.com/support](https://vercel.com/support)
- **GitHub Issues**: Report bugs in your repository
- **Community**: Join Vercel community forums

---

**Your iTrade application is now ready for Vercel deployment!** 🚀

Follow the steps above to deploy your application and share the live URL with your users. 