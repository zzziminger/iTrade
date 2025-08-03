# iTrade Deployment Guide

This guide will help you deploy the iTrade application to various platforms.

## 🚀 Quick Deployment Options

### Option 1: Deploy to Vercel (Recommended)

1. **Fork/Clone the Repository**
   ```bash
   git clone https://github.com/QO2021/iTrade.git
   cd iTrade
   ```

2. **Deploy Backend to Railway/Heroku**
   - Create account on [Railway](https://railway.app) or [Heroku](https://heroku.com)
   - Connect your GitHub repository
   - Set environment variables (see `.env.example`)
   - Deploy the `server` directory

3. **Deploy Frontend to Vercel**
   - Create account on [Vercel](https://vercel.com)
   - Import your GitHub repository
   - Set build settings:
     - Framework Preset: `Create React App`
     - Root Directory: `client`
     - Build Command: `npm run build`
     - Output Directory: `build`
   - Add environment variable: `REACT_APP_API_URL` (your backend URL)

### Option 2: Deploy to Netlify

1. **Deploy Backend** (same as above)
2. **Deploy Frontend to Netlify**
   - Create account on [Netlify](https://netlify.com)
   - Connect your GitHub repository
   - Set build settings:
     - Build command: `cd client && npm run build`
     - Publish directory: `client/build`

### Option 3: Deploy to Heroku (Full Stack)

1. **Create Heroku App**
   ```bash
   heroku create your-itrade-app
   ```

2. **Set Environment Variables**
   ```bash
   heroku config:set NODE_ENV=production
   heroku config:set MONGODB_URI=your-mongodb-uri
   heroku config:set JWT_SECRET=your-jwt-secret
   # ... add all other environment variables
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

## 🔧 Environment Setup

### Required Environment Variables

Create a `.env` file in the root directory:

```env
# Server Configuration
PORT=5000
NODE_ENV=development

# MongoDB Connection
MONGODB_URI=mongodb://localhost:27017/itrade

# JWT Secret
JWT_SECRET=your-super-secret-jwt-key-here

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password

# OpenAI API
OPENAI_API_KEY=your-openai-api-key

# Yahoo Finance API
YAHOO_FINANCE_API_KEY=your-yahoo-api-key

# FRED API
FRED_API_KEY=your-fred-api-key

# News API
NEWS_API_KEY=your-news-api-key

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
```

### API Keys Setup

1. **OpenAI API Key**
   - Visit [OpenAI Platform](https://platform.openai.com)
   - Create account and get API key
   - Used for news sentiment analysis

2. **FRED API Key**
   - Visit [FRED API](https://fred.stlouisfed.org/docs/api/api_key.html)
   - Get free API key
   - Used for economic data

3. **News API Key**
   - Visit [News API](https://newsapi.org)
   - Get free API key
   - Used for financial news

4. **Email Setup (Gmail)**
   - Enable 2-factor authentication
   - Generate app password
   - Used for password reset emails

## 📦 Local Development

### Prerequisites
- Node.js (v16 or higher)
- MongoDB (local or Atlas)
- npm or yarn

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/QO2021/iTrade.git
   cd iTrade
   ```

2. **Install Dependencies**
   ```bash
   # Install backend dependencies
   npm install

   # Install frontend dependencies
   cd client
   npm install
   cd ..
   ```

3. **Environment Setup**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Start Development Servers**
   ```bash
   # Start backend (from root directory)
   npm run dev

   # Start frontend (in another terminal)
   cd client
   npm start
   ```

5. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 🗄️ Database Setup

### MongoDB Atlas (Recommended for Production)

1. Create account on [MongoDB Atlas](https://mongodb.com/atlas)
2. Create new cluster
3. Get connection string
4. Add to environment variables

### Local MongoDB

```bash
# Install MongoDB
# macOS: brew install mongodb-community
# Ubuntu: sudo apt install mongodb

# Start MongoDB
mongod

# Create database
mongo
use itrade
```

## 🔒 Security Considerations

1. **Environment Variables**
   - Never commit `.env` files
   - Use different keys for development/production
   - Rotate keys regularly

2. **CORS Configuration**
   - Update CORS settings for production domains
   - Restrict to specific origins

3. **Rate Limiting**
   - Adjust rate limits based on usage
   - Monitor API usage

4. **SSL/HTTPS**
   - Always use HTTPS in production
   - Configure SSL certificates

## 📊 Monitoring & Analytics

### Recommended Tools

1. **Application Monitoring**
   - [Sentry](https://sentry.io) for error tracking
   - [LogRocket](https://logrocket.com) for session replay

2. **Performance Monitoring**
   - [Google Analytics](https://analytics.google.com)
   - [Vercel Analytics](https://vercel.com/analytics)

3. **API Monitoring**
   - [UptimeRobot](https://uptimerobot.com)
   - [Pingdom](https://pingdom.com)

## 🚀 Production Checklist

- [ ] Environment variables configured
- [ ] Database connection established
- [ ] API keys secured
- [ ] CORS settings updated
- [ ] SSL certificate installed
- [ ] Error monitoring setup
- [ ] Performance monitoring setup
- [ ] Backup strategy implemented
- [ ] Documentation updated
- [ ] Testing completed

## 📞 Support

For deployment issues:
1. Check the logs in your hosting platform
2. Verify environment variables
3. Test API endpoints
4. Check database connectivity

## 🔗 Useful Links

- [Vercel Documentation](https://vercel.com/docs)
- [Heroku Documentation](https://devcenter.heroku.com)
- [Netlify Documentation](https://docs.netlify.com)
- [MongoDB Atlas](https://docs.atlas.mongodb.com)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FRED API Documentation](https://fred.stlouisfed.org/docs/api) 