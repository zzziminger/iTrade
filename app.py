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
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
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
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get some popular stocks
    popular_stocks = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
    stock_data = []
    
    for symbol in popular_stocks:
        data = get_stock_data(symbol, '1d')
        if data:
            stock_data.append(data)
    
    return render_template('dashboard.html', stocks=stock_data)

@app.route('/stock/<symbol>')
@login_required
def stock_detail(symbol):
    stock_data = get_stock_data(symbol, '1mo')
    if not stock_data:
        flash('Stock not found')
        return redirect(url_for('dashboard'))
    
    # Create chart
    if stock_data['historical_data']:
        dates = [item['Date'] for item in stock_data['historical_data']]
        prices = [item['Close'] for item in stock_data['historical_data']]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines', name=symbol))
        fig.update_layout(title=f'{symbol} Stock Price', xaxis_title='Date', yaxis_title='Price')
        
        chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        chart_json = None
    
    return render_template('stock_detail.html', stock=stock_data, chart_json=chart_json)

@app.route('/watchlist')
@login_required
def watchlist():
    user_watchlist = Watchlist.query.filter_by(user_id=current_user.id).all()
    watchlist_data = []
    
    for item in user_watchlist:
        data = get_stock_data(item.symbol, '1d')
        if data:
            watchlist_data.append(data)
    
    return render_template('watchlist.html', stocks=watchlist_data)

@app.route('/add_to_watchlist/<symbol>')
@login_required
def add_to_watchlist(symbol):
    existing = Watchlist.query.filter_by(user_id=current_user.id, symbol=symbol).first()
    if not existing:
        watchlist_item = Watchlist(user_id=current_user.id, symbol=symbol)
        db.session.add(watchlist_item)
        db.session.commit()
        flash(f'{symbol} added to watchlist')
    else:
        flash(f'{symbol} is already in your watchlist')
    
    return redirect(url_for('watchlist'))

@app.route('/remove_from_watchlist/<symbol>')
@login_required
def remove_from_watchlist(symbol):
    item = Watchlist.query.filter_by(user_id=current_user.id, symbol=symbol).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f'{symbol} removed from watchlist')
    
    return redirect(url_for('watchlist'))

@app.route('/news')
@login_required
def news():
    news_data = get_news_analysis()
    return render_template('news.html', news=news_data)

@app.route('/economic')
@login_required
def economic():
    economic_data = get_economic_data()
    return render_template('economic.html', data=economic_data)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate reset token
            token = secrets.token_urlsafe(32)
            user.password_reset_token = token
            db.session.commit()
            
            # Send email
            reset_url = url_for('reset_password', token=token, _external=True)
            body = f"""
            <h2>Password Reset Request</h2>
            <p>Click the link below to reset your password:</p>
            <a href="{reset_url}">Reset Password</a>
            <p>If you didn't request this, please ignore this email.</p>
            """
            
            if send_email(email, 'Password Reset Request', body):
                flash('Password reset email sent!')
            else:
                flash('Error sending email. Please try again.')
        else:
            flash('Email not found')
    
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(password_reset_token=token).first()
    
    if not user:
        flash('Invalid or expired reset token')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password = request.form['password']
        user.set_password(password)
        user.password_reset_token = None
        db.session.commit()
        flash('Password updated successfully!')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')

# API Routes
@app.route('/api/stock_search')
def stock_search():
    query = request.args.get('q', '').upper()
    if len(query) < 1:
        return jsonify([])
    
    # Simple stock search - you could enhance this with a stock database
    common_stocks = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 'NVDA', 'NFLX', 'AMD', 'INTC']
    results = [stock for stock in common_stocks if query in stock]
    
    return jsonify(results)

@app.route('/api/stock_data/<symbol>')
def api_stock_data(symbol):
    data = get_stock_data(symbol, '1mo')
    return jsonify(data)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 