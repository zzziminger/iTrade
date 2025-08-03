#!/usr/bin/env python3
"""
iTrade - Python Stock Trading Platform
A comprehensive stock trading platform with real-time market data, AI-powered news analysis, and economic indicators.
"""

import os
import json
import requests
import sqlite3
import hashlib
import secrets
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import yfinance as yf
import plotly.graph_objs as go
import plotly.utils
from fredapi import Fred
import openai
from newsapi import NewsApiClient
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///itrade.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# API Keys (set these in environment variables)
FRED_API_KEY = os.environ.get('FRED_API_KEY', 'your-fred-api-key')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'your-openai-api-key')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', 'your-news-api-key')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USER = os.environ.get('EMAIL_USER', 'your-email@gmail.com')
EMAIL_PASS = os.environ.get('EMAIL_PASS', 'your-app-password')

# Initialize APIs
fred = Fred(api_key=FRED_API_KEY) if FRED_API_KEY else None

try:
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
except Exception as e:
    logger.warning(f"News API not initialized: {e}")
    newsapi = None

try:
    openai.api_key = OPENAI_API_KEY
except Exception as e:
    logger.warning(f"OpenAI API not initialized: {e}")

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(100))
    password_reset_token = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('watchlist', lazy=True))

# Trade model
class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    action = db.Column(db.String(4), nullable=False)  # BUY or SELL
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Utility Functions
def send_email(to_email, subject, body):
    """Send email using SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        return False

def get_stock_data(symbol, period='1mo'):
    """Get stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        info = stock.info
        
        # Convert pandas DataFrame to list of dictionaries
        historical_data = []
        if not hist.empty:
            for index, row in hist.iterrows():
                historical_data.append({
                    'Date': index.strftime('%Y-%m-%d'),
                    'Open': float(row['Open']),
                    'High': float(row['High']),
                    'Low': float(row['Low']),
                    'Close': float(row['Close']),
                    'Volume': int(row['Volume'])
                })
        
        current_price = float(hist['Close'].iloc[-1]) if not hist.empty else None
        previous_price = float(hist['Close'].iloc[-2]) if len(hist) > 1 else None
        
        change = current_price - previous_price if previous_price else 0
        change_percent = (change / previous_price * 100) if previous_price else 0
        
        return {
            'symbol': symbol,
            'price': current_price,
            'change': change,
            'change_percent': change_percent,
            'volume': int(hist['Volume'].iloc[-1]) if not hist.empty else 0,
            'high': float(hist['High'].iloc[-1]) if not hist.empty else None,
            'low': float(hist['Low'].iloc[-1]) if not hist.empty else None,
            'open': float(hist['Open'].iloc[-1]) if not hist.empty else None,
            'name': info.get('longName', symbol),
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('trailingPE'),
            'dividend_yield': info.get('dividendYield'),
            'historical_data': historical_data
        }
    except Exception as e:
        logger.error(f"Error getting stock data for {symbol}: {e}")
        return None

def get_economic_data():
    """Get economic data from FRED API"""
    if not fred:
        return None
    
    try:
        # Get various economic indicators
        indicators = {
            'CPI': 'CPIAUCSL',  # Consumer Price Index
            'Interest_Rate': 'FEDFUNDS',  # Federal Funds Rate
            'Unemployment': 'UNRATE',  # Unemployment Rate
            'GDP': 'GDP',  # Gross Domestic Product
            'Housing_Index': 'CSUSHPISA'  # Case-Shiller Home Price Index
        }
        
        data = {}
        for name, series_id in indicators.items():
            try:
                series = fred.get_series(series_id, limit=12)
                # Convert pandas Series to list of dictionaries
                data[name] = [
                    {
                        'date': str(index.date()),
                        'value': float(value)
                    }
                    for index, value in series.items()
                ]
            except Exception as e:
                logger.error(f"Error getting {name} data: {e}")
                data[name] = []
        
        return data
    except Exception as e:
        logger.error(f"Error getting economic data: {e}")
        return None

def get_news_analysis():
    """Get financial news and analyze with AI"""
    if not newsapi or not openai.api_key:
        return []
    
    try:
        # Get financial news
        news = newsapi.get_top_headlines(
            category='business',
            language='en',
            country='us',
            page_size=10
        )
        
        # Analyze with OpenAI
        if news['articles']:
            articles_text = "\n\n".join([
                f"Title: {article['title']}\nSummary: {article.get('description', 'No description')}"
                for article in news['articles'][:5]
            ])
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial analyst. Analyze the following news articles and provide insights on market sentiment and potential impacts on different sectors."},
                    {"role": "user", "content": articles_text}
                ],
                max_tokens=300
            )
            
            return {
                'articles': news['articles'][:5],
                'analysis': response.choices[0].message.content
            }
    except Exception as e:
        logger.error(f"Error getting news analysis: {e}")
    
    return []

# Routes
@app.route('/')
def home():
    return jsonify({
        "message": "iTrade API is working!",
        "status": "success",
        "version": "production"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "iTrade"
    })

@app.route('/test')
def test():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>iTrade - Stock Trading Platform</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container { 
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                text-align: center;
                color: white;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            h1 { margin-bottom: 20px; font-size: 2.5em; }
            .success { color: #4ade80; font-weight: bold; }
            .feature { margin: 10px 0; padding: 10px; background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 iTrade</h1>
            <p class="success">✅ Successfully Deployed on Vercel!</p>
            <p>Your stock trading platform is now live.</p>
            
            <div class="feature">
                <h3>📈 Stock Trading Features</h3>
                <p>Real-time stock data, watchlists, and trading tools</p>
            </div>
            
            <div class="feature">
                <h3>📊 Economic Data</h3>
                <p>CPI, interest rates, unemployment, and market indicators</p>
            </div>
            
            <div class="feature">
                <h3>📰 News & Analysis</h3>
                <p>Financial news feed and market sentiment analysis</p>
            </div>
            
            <div class="feature">
                <h3>👤 User Authentication</h3>
                <p>Secure login, registration, and user profiles</p>
            </div>
            
            <p style="margin-top: 30px; font-size: 0.9em; opacity: 0.8;">
                Built with Flask • Deployed on Vercel • Ready for production
            </p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/api/status')
def api_status():
    return jsonify({
        "service": "iTrade",
        "status": "operational",
        "version": "1.0.0",
        "features": [
            "User Authentication",
            "Stock Trading",
            "Economic Data",
            "News Feed",
            "Market Analysis"
        ]
    })

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template_string('<h1>404 - Page Not Found</h1>'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template_string('<h1>500 - Internal Server Error</h1>'), 500

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True) 