# 🚀 iTrade - Advanced Stock Trading Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Vercel-black.svg)](https://vercel.com)

> **Professional stock trading platform with real-time data, AI-powered insights, and modern UI**

## 🌟 **Features**

### **📊 Real-Time Market Data**
- **Live Stock Prices** - Real-time quotes from Yahoo Finance API
- **Market Indices** - S&P 500, Dow Jones, NASDAQ live data
- **Interactive Charts** - Plotly.js powered price charts
- **Technical Analysis** - RSI, MACD, Moving Averages
- **Volume & Market Cap** - Comprehensive stock metrics

### **📈 Economic Indicators**
- **CPI Data** - Consumer Price Index trends
- **Interest Rates** - Federal Reserve rates
- **Unemployment** - Employment statistics
- **GDP Data** - Economic growth indicators
- **Real-time Updates** - Live economic data

### **🤖 AI-Powered Analysis**
- **Market Sentiment** - OpenAI-powered analysis
- **News Impact** - AI assessment of market news
- **Trend Predictions** - Machine learning insights
- **Risk Assessment** - Automated risk analysis

### **📰 Financial News**
- **Real-time News** - Live financial updates
- **Stock-specific News** - Company-specific articles
- **Market Analysis** - Expert insights and reports
- **Economic Policy** - Federal Reserve updates

### **🎨 Modern UI/UX**
- **Glass Morphism** - Translucent design elements
- **Responsive Design** - Works on all devices
- **Smooth Animations** - Floating elements and transitions
- **Dark Theme** - Professional dark interface
- **Interactive Elements** - Hover effects and feedback

### **👤 User Management**
- **Secure Authentication** - Flask-Login integration
- **User Registration** - Email verification ready
- **Profile Management** - User preferences and settings
- **Session Handling** - Secure session management

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.11 or higher
- Git
- pip (Python package manager)

### **Installation**

1. **Clone the repository**
   ```bash
   git clone https://github.com/QO2021/iTrade.git
   cd iTrade
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   # Create .env file
   echo "SECRET_KEY=your-secret-key-here" > .env
   echo "FRED_API_KEY=your-fred-api-key" >> .env
   echo "NEWS_API_KEY=your-news-api-key" >> .env
   echo "OPENAI_API_KEY=your-openai-api-key" >> .env
   ```

5. **Run the application**
   ```bash
   python index.py
   ```

6. **Open your browser**
   ```
   http://localhost:5000
   ```

## 🏗️ **Project Structure**

```
iTrade/
├── index.py                 # Main Flask application
├── api_integration.py       # Real API integrations
├── requirements.txt         # Python dependencies
├── vercel.json             # Vercel deployment config
├── templates/              # HTML templates
│   ├── index.html          # Landing page
│   ├── login.html          # Login form
│   ├── register.html       # Registration form
│   ├── dashboard.html      # Main dashboard
│   ├── stock_detail.html   # Stock analysis page
│   └── [other templates]   # Additional pages
├── static/                 # Static assets
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Images and icons
└── README.md              # This file
```

## 🔧 **API Integrations**

### **Yahoo Finance API** ✅
- **Status:** Active (No API key required)
- **Features:** Real-time stock data, historical charts
- **Rate Limit:** Generous free tier
- **Data:** Stock prices, volume, market cap, P/E ratios

### **FRED API** (Federal Reserve Economic Data)
- **Status:** Ready (API key required)
- **Features:** Economic indicators and trends
- **Rate Limit:** 120 requests/minute (free)
- **Data:** CPI, Interest Rates, Unemployment, GDP

### **News API**
- **Status:** Ready (API key required)
- **Features:** Financial news and market updates
- **Rate Limit:** 1,000 requests/day (free)
- **Data:** Real-time financial news

### **OpenAI API**
- **Status:** Ready (API key required)
- **Features:** AI-powered market analysis
- **Rate Limit:** $5 free credit monthly
- **Data:** Market sentiment analysis

## 🚀 **Deployment**

### **Vercel Deployment (Recommended)**

1. **Fork/Clone** this repository
2. **Connect** to Vercel: https://vercel.com/dashboard
3. **Import** the `QO2021/iTrade` project
4. **Configure** environment variables (optional)
5. **Deploy** with one click

### **Environment Variables**

```bash
FLASK_ENV=production
FLASK_APP=index.py
SECRET_KEY=your-secret-key-here
FRED_API_KEY=your-fred-api-key
NEWS_API_KEY=your-news-api-key
OPENAI_API_KEY=your-openai-api-key
```

### **Other Deployment Options**

- **Heroku:** Use `Procfile` and `runtime.txt`
- **Railway:** Direct GitHub integration
- **DigitalOcean:** App Platform deployment
- **AWS:** Elastic Beanstalk or Lambda

## 📊 **Features Demo**

### **Landing Page**
- Beautiful glass morphism design
- Animated floating elements
- Call-to-action buttons
- Responsive layout

### **Dashboard**
- Real-time market indices
- Live stock data tables
- Interactive price charts
- Economic indicators
- Financial news feed

### **Stock Analysis**
- Detailed stock information
- Technical analysis indicators
- Historical price charts
- Stock-specific news
- Trading interface

### **User Management**
- Secure login/registration
- Password strength validation
- User profile management
- Session handling

## 🛠️ **Technology Stack**

### **Backend**
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **Flask-Login** - Authentication
- **Werkzeug** - Security utilities

### **Frontend**
- **Tailwind CSS** - Utility-first CSS
- **Font Awesome** - Icons
- **Plotly.js** - Interactive charts
- **JavaScript** - Dynamic interactions

### **APIs**
- **Yahoo Finance** - Stock data
- **FRED** - Economic data
- **News API** - Financial news
- **OpenAI** - AI analysis

### **Deployment**
- **Vercel** - Serverless deployment
- **GitHub** - Version control
- **Python** - Runtime environment

## 🔒 **Security Features**

- **Password Hashing** - Secure password storage
- **Session Management** - Secure user sessions
- **CSRF Protection** - Cross-site request forgery protection
- **Input Validation** - Form data validation
- **Error Handling** - Graceful error management

## 📱 **Responsive Design**

- **Mobile First** - Optimized for mobile devices
- **Tablet Support** - Responsive tablet layout
- **Desktop Experience** - Full desktop features
- **Touch Friendly** - Touch-optimized interface

## 🎨 **UI/UX Features**

### **Design System**
- **Glass Morphism** - Modern translucent effects
- **Gradient Backgrounds** - Beautiful color transitions
- **Smooth Animations** - 60fps animations
- **Hover Effects** - Interactive feedback

### **Color Scheme**
- **Primary:** Blue gradients (#667eea to #764ba2)
- **Success:** Green (#10B981)
- **Warning:** Yellow (#F59E0B)
- **Error:** Red (#EF4444)
- **Neutral:** Gray scale

### **Typography**
- **Headings:** Bold, large text
- **Body:** Readable, medium weight
- **Captions:** Small, muted text
- **Font:** System fonts for performance

## 🤝 **Contributing**

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### **Development Setup**

```bash
# Clone the repository
git clone https://github.com/QO2021/iTrade.git

# Install development dependencies
pip install -r requirements.txt

# Run tests
python test_deployment.py

# Start development server
python index.py
```

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Yahoo Finance** - Stock data API
- **Federal Reserve** - Economic data
- **News API** - Financial news
- **OpenAI** - AI analysis capabilities
- **Vercel** - Deployment platform
- **Tailwind CSS** - UI framework
- **Plotly.js** - Charting library

## 📞 **Support**

- **Issues:** [GitHub Issues](https://github.com/QO2021/iTrade/issues)
- **Documentation:** [Wiki](https://github.com/QO2021/iTrade/wiki)
- **Discussions:** [GitHub Discussions](https://github.com/QO2021/iTrade/discussions)

## 🚀 **Live Demo**

Visit the live application: [iTrade on Vercel](https://your-project-name.vercel.app)

---

**Made with ❤️ by the iTrade Team**

[![GitHub stars](https://img.shields.io/github/stars/QO2021/iTrade?style=social)](https://github.com/QO2021/iTrade)
[![GitHub forks](https://img.shields.io/github/forks/QO2021/iTrade?style=social)](https://github.com/QO2021/iTrade)
[![GitHub issues](https://img.shields.io/github/issues/QO2021/iTrade)](https://github.com/QO2021/iTrade/issues)