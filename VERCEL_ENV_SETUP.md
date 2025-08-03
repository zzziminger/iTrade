# Vercel Environment Variables Setup

## 🔑 **API Keys Configuration**

Your iTrade application is now deployed on Vercel! To enable full functionality with real-time data, you need to configure the following environment variables in your Vercel dashboard.

## 📋 **Required Environment Variables**

### **1. Flask Secret Key**
```
SECRET_KEY=your-secret-key-here
```

### **2. OpenAI API Key (for AI analysis)**
```
OPENAI_API_KEY=your-openai-api-key
```

### **3. FRED API Key (Federal Reserve Economic Data)**
```
FRED_API_KEY=your-fred-api-key
```

### **4. News API Key (Financial News)**
```
NEWS_API_KEY=your-news-api-key
```

## 🚀 **How to Set Environment Variables in Vercel**

### **Step 1: Access Vercel Dashboard**
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Sign in with your GitHub account
3. Find your iTrade project

### **Step 2: Configure Environment Variables**
1. Click on your project
2. Go to **Settings** tab
3. Click **Environment Variables**
4. Add each variable with your actual API keys

### **Step 3: Deploy Changes**
1. After adding all variables, click **Save**
2. Go to **Deployments** tab
3. Click **Redeploy** to apply the new environment variables

## 🧪 **Test Your Configuration**

After setting the environment variables, test these endpoints:

### **Health Check**
```
GET /health
```
Should return database status and API availability.

### **Stock Data**
```
GET /api/stock/AAPL
```
Should return real stock data from Yahoo Finance.

### **Economic Data**
```
GET /api/economic
```
Should return real economic indicators from FRED.

### **News Data**
```
GET /api/news
```
Should return real financial news from News API.

### **AI Sentiment**
```
GET /api/sentiment
```
Should return AI-powered market sentiment analysis.

## 🔒 **Security Notes**

- ✅ **Environment variables are encrypted** in Vercel
- ✅ **Not visible** in client-side code
- ✅ **Automatically rotated** by Vercel
- ✅ **Accessible only** to your deployment

## 📊 **API Rate Limits**

| API | Rate Limit | Notes |
|-----|------------|-------|
| **Yahoo Finance** | Unlimited | No API key required |
| **FRED** | 120 requests/minute | Free tier |
| **News API** | 1,000 requests/day | Free tier |
| **OpenAI** | $5 free credit/month | Pay-as-you-go |

## 🚨 **Troubleshooting**

### **If APIs don't work:**
1. Check environment variables are set correctly
2. Verify API keys are valid
3. Check Vercel function logs for errors
4. Test with `/health` endpoint first

### **If deployment fails:**
1. Check Vercel build logs
2. Verify `requirements.txt` is up to date
3. Ensure `vercel.json` is properly configured

## 🎉 **Success Indicators**

Your setup is working when:
- ✅ `/health` returns `"status": "healthy"`
- ✅ Stock data shows real prices
- ✅ Economic data shows current indicators
- ✅ News feed shows recent articles
- ✅ Sentiment analysis provides AI insights

---

**Your iTrade application is now fully configured with real-time data! 🚀** 