# iTrade Python - Stock Trading Platform

A comprehensive stock trading platform built with Python Flask, featuring real-time market data, AI-powered news analysis, economic indicators, and a modern web interface.

## 🚀 Features

### 📊 **Stock Trading & Analysis**
- **Real-time Stock Data**: Live quotes from Yahoo Finance API
- **Stock Search**: Search and discover new stocks
- **Watchlist Management**: Add/remove stocks to personal watchlist
- **Stock Charts**: Interactive price charts with historical data
- **Stock Details**: Comprehensive stock information and metrics

### 📈 **Economic Data**
- **Federal Reserve Data**: CPI, interest rates, unemployment rates
- **Bond Yields**: 10-year Treasury yield tracking
- **Housing Market**: Home price index data
- **Interactive Charts**: Visualize economic trends
- **Real-time Updates**: Latest economic indicators

### 🤖 **AI-Powered News Analysis**
- **Financial News**: Latest market news from News API
- **Sentiment Analysis**: AI-powered news sentiment using OpenAI
- **Market Insights**: Bullish/bearish analysis
- **Risk Assessment**: Identify market risks and opportunities
- **Sector Analysis**: Analyze specific stock sectors

### 👤 **User Management**
- **User Registration**: Secure account creation
- **Email Verification**: Account verification system
- **Password Reset**: Forgot password functionality
- **Profile Management**: Update personal information
- **Security Features**: Password change and account deletion

### 🎨 **Modern UI/UX**
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Mode**: Toggle between light and dark themes
- **Real-time Updates**: Live data without page refresh
- **Interactive Charts**: Plotly-powered visualizations
- **Modern Styling**: Tailwind CSS with custom components

## 🛠️ Technology Stack

### **Backend**
- **Flask 3.0.0**: Web framework
- **SQLAlchemy 3.1.1**: Database ORM
- **Flask-Login 0.6.3**: User authentication
- **SQLite**: Database (default)

### **APIs & Data**
- **yfinance 0.2.28**: Yahoo Finance stock data
- **FRED API**: Federal Reserve economic data
- **News API**: Financial news
- **OpenAI API**: AI sentiment analysis
- **Plotly 5.18.0**: Interactive charts

### **Frontend**
- **HTML5**: Semantic markup
- **Tailwind CSS**: Utility-first CSS framework
- **JavaScript**: Interactive functionality
- **Jinja2**: Template engine

### **Development**
- **Python 3.8+**: Runtime environment
- **pip**: Package management
- **gunicorn**: Production server

## 📦 Installation

### **Prerequisites**
- Python 3.8 or higher
- pip package manager
- Git (for cloning)

### **Quick Start**

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/iTrade.git
   cd iTrade
   ```

2. **Run automated setup**
   ```bash
   python setup_python.py
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Configure environment variables**
   ```bash
   # Edit .env file with your API keys
   nano .env
   ```

5. **Run the application**
   ```bash
   python iTrade.py
   ```

6. **Access the application**
   ```
   http://localhost:5000
   ```

### **Manual Installation**

If the automated setup fails, try manual installation:

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements_simple.txt

# Test installation
python test_installation.py

# Run application
python iTrade.py
```

## 🔧 Configuration

### **Environment Variables**

Create a `.env` file in the project root:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development

# Database Configuration
DATABASE_URL=sqlite:///itrade.db

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password

# API Keys (Required)
FRED_API_KEY=your-fred-api-key
OPENAI_API_KEY=your-openai-api-key
NEWS_API_KEY=your-news-api-key
```

### **API Keys Setup**

1. **FRED API Key** (Free)
   - Visit: https://fred.stlouisfed.org/docs/api/api_key.html
   - Get free API key
   - Add to `.env`: `FRED_API_KEY=your-key`

2. **OpenAI API Key** (Paid)
   - Visit: https://platform.openai.com
   - Create account and get API key
   - Add to `.env`: `OPENAI_API_KEY=your-key`

3. **News API Key** (Free)
   - Visit: https://newsapi.org
   - Get free API key
   - Add to `.env`: `NEWS_API_KEY=your-key`

## 📁 Project Structure

```
iTrade/
├── iTrade.py                 # Main Flask application
├── requirements.txt          # Full dependencies
├── requirements_simple.txt   # Simplified dependencies
├── setup_python.py          # Automated setup script
├── test_installation.py     # Installation test
├── INSTALLATION_GUIDE.md    # Detailed installation guide
├── README_Python.md         # This file
├── .env                     # Environment variables
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── dashboard.html      # Dashboard page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── stock_detail.html   # Stock detail page
│   ├── watchlist.html      # Watchlist page
│   ├── news.html           # News page
│   ├── economic.html       # Economic data page
│   ├── profile.html        # Profile page
│   ├── forgot_password.html # Forgot password page
│   ├── reset_password.html # Reset password page
│   ├── 404.html           # 404 error page
│   └── 500.html           # 500 error page
└── static/                 # Static files
    ├── css/
    │   └── style.css      # Custom styles
    └── js/
        └── app.js         # Common JavaScript
```

## 🚀 Usage

### **Dashboard**
- View market overview
- Quick access to watchlist
- Recent news headlines
- Economic indicators

### **Stock Trading**
1. **Search Stocks**: Use the search bar to find stocks
2. **View Details**: Click on any stock for detailed information
3. **Add to Watchlist**: Click the star icon to add to watchlist
4. **Track Performance**: Monitor your watchlist stocks

### **Economic Data**
1. **Select Indicator**: Choose from CPI, interest rates, etc.
2. **View Charts**: Interactive charts with historical data
3. **Analyze Trends**: Compare current vs previous values
4. **Export Data**: Download data for further analysis

### **News Analysis**
1. **Browse News**: Latest financial news
2. **Sentiment Analysis**: AI-powered market sentiment
3. **Risk Assessment**: Identify market risks
4. **Sector Analysis**: Analyze specific sectors

### **User Management**
1. **Register**: Create new account
2. **Login**: Access your account
3. **Profile**: Update personal information
4. **Security**: Change password or delete account

## 🔍 API Endpoints

### **Authentication**
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout
- `POST /forgot-password` - Password reset request
- `POST /reset-password/<token>` - Password reset

### **Stock Data**
- `GET /api/stocks/quote/<symbol>` - Get stock quote
- `GET /api/stocks/search` - Search stocks
- `GET /api/stocks/watchlist` - Get user watchlist
- `POST /api/stocks/watchlist` - Add to watchlist
- `DELETE /api/stocks/watchlist/<symbol>` - Remove from watchlist

### **Economic Data**
- `GET /api/economic/indicators` - Get economic indicators

### **News**
- `GET /api/news/financial` - Get financial news
- `POST /api/news/analyze-sentiment` - Analyze news sentiment

### **User Management**
- `PUT /api/users/profile` - Update profile
- `POST /api/users/change-password` - Change password
- `DELETE /api/users/account` - Delete account

## 🧪 Testing

### **Test Installation**
```bash
python test_installation.py
```

### **Manual Testing**
1. **Start Application**: `python iTrade.py`
2. **Access Dashboard**: http://localhost:5000
3. **Register Account**: Create new user account
4. **Test Features**: Try all functionality
5. **Check Logs**: Monitor console for errors

## 🚀 Deployment

### **Development**
```bash
python iTrade.py
```

### **Production**
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 iTrade:app
```

### **Docker Deployment**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements_simple.txt .
RUN pip install -r requirements_simple.txt

COPY . .
EXPOSE 5000

CMD ["python", "iTrade.py"]
```

## 🔧 Troubleshooting

### **Common Issues**

1. **pandas installation fails**
   ```bash
   pip install -r requirements_simple.txt
   ```

2. **API keys not working**
   - Check `.env` file configuration
   - Verify API key validity
   - Check API rate limits

3. **Database errors**
   ```bash
   rm itrade.db
   python iTrade.py
   ```

4. **Port already in use**
   ```bash
   python iTrade.py --port 5001
   ```

### **Python Version Issues**

- **Python 3.13**: Use `requirements_simple.txt`
- **Python 3.11**: Use `requirements.txt`
- **Older versions**: Upgrade to Python 3.8+

## 📈 Performance

### **Optimizations**
- **Caching**: In-memory caching for API responses
- **Database**: SQLite for simplicity, PostgreSQL for production
- **Static Files**: CDN-ready static assets
- **Compression**: Gzip compression for responses

### **Monitoring**
- **Logging**: Comprehensive error logging
- **Health Checks**: Application health monitoring
- **Performance**: Response time tracking

## 🔒 Security

### **Features**
- **Password Hashing**: bcrypt password hashing
- **CSRF Protection**: Cross-site request forgery protection
- **Input Validation**: Server-side input validation
- **SQL Injection**: Parameterized queries
- **XSS Protection**: Content Security Policy

### **Best Practices**
- **HTTPS**: Use HTTPS in production
- **Environment Variables**: Secure API key storage
- **Regular Updates**: Keep dependencies updated
- **Security Headers**: Implement security headers

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature-name`
3. **Make changes**: Add your improvements
4. **Test thoroughly**: Ensure all tests pass
5. **Submit pull request**: Describe your changes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Yahoo Finance**: Stock data API
- **Federal Reserve**: Economic data
- **News API**: Financial news
- **OpenAI**: AI sentiment analysis
- **Flask**: Web framework
- **Tailwind CSS**: Styling framework

## 📞 Support

- **Documentation**: See INSTALLATION_GUIDE.md
- **Issues**: Report bugs on GitHub
- **Discussions**: Join community discussions
- **Email**: Contact for support

---

**iTrade Python** - Your trusted platform for smart trading decisions.

*Built with ❤️ using Python and Flask* 