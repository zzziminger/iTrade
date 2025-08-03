<<<<<<< HEAD
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

# Initialize API clients
try:
    fred = Fred(api_key=FRED_API_KEY)
except Exception as e:
    logger.warning(f"FRED API not initialized: {e}")
    fred = None

try:
    openai.api_key = OPENAI_API_KEY
except Exception as e:
    logger.warning(f"OpenAI API not initialized: {e}")

try:
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
except Exception as e:
    logger.warning(f"News API not initialized: {e}")
    newsapi = None

# Database Models
=======
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_wtf import FlaskForm
from flask_mail import Mail, Message
from wtforms import StringField, PasswordField, EmailField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import yfinance as yf
import requests
import os
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.utils
import json
from fredapi import Fred
from bs4 import BeautifulSoup
import secrets
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///itrade.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# API Keys
FRED_API_KEY = os.environ.get('FRED_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
mail = Mail(app)

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

<<<<<<< HEAD
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
    """Get economic data from FRED"""
    if not fred:
        return {}
    
    try:
        indicators = {
            'cpi': 'CPIAUCSL',  # Consumer Price Index
            'interest_rate': 'FEDFUNDS',  # Federal Funds Rate
            'unemployment': 'UNRATE',  # Unemployment Rate
            'bond_yield_10y': 'GS10',  # 10-Year Treasury Yield
            'house_price_index': 'CSUSHPISA'  # House Price Index
        }
        
        data = {}
        for key, series_id in indicators.items():
            try:
                series = fred.get_series(series_id, limit=12)
                if not series.empty:
                    # Convert pandas Series to list of dictionaries
                    series_data = []
                    for index, value in series.items():
                        series_data.append({
                            'date': index.strftime('%Y-%m-%d'),
                            'value': float(value)
                        })
                    
                    data[key] = {
                        'latest_value': float(series.iloc[-1]),
                        'previous_value': float(series.iloc[-2]) if len(series) > 1 else None,
                        'data': series_data
                    }
            except Exception as e:
                logger.error(f"Error getting {key} data: {e}")
        
        return data
    except Exception as e:
        logger.error(f"Error getting economic data: {e}")
        return {}

def get_financial_news():
    """Get financial news from News API"""
    if not newsapi:
        return []
    
    try:
        news = newsapi.get_top_headlines(
            category='business',
            language='en',
            country='us',
            page_size=20
        )
        return news.get('articles', [])
    except Exception as e:
        logger.error(f"Error getting news: {e}")
        return []

def analyze_news_sentiment(articles, symbol=None):
    """Analyze news sentiment using OpenAI"""
    if not openai.api_key:
        return None
    
    try:
        if not articles:
            return None
        
        # Prepare articles text
        articles_text = ""
        for article in articles[:5]:  # Limit to 5 articles
            articles_text += f"Title: {article.get('title', '')}\n"
            articles_text += f"Description: {article.get('description', '')}\n"
            articles_text += f"Content: {article.get('content', '')}\n\n"
        
        prompt = f"""
        Analyze the following financial news articles{' for ' + symbol if symbol else ''}:
        
        {articles_text}
        
        Provide analysis in JSON format with the following structure:
        {{
            "sentiment": "bullish/bearish/neutral",
            "confidence": 0.85,
            "key_themes": ["theme1", "theme2"],
            "risk_factors": ["risk1", "risk2"],
            "opportunities": ["opportunity1", "opportunity2"],
            "recommendation": "buy/hold/sell"
        }}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial analyst. Provide accurate, balanced analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        analysis_text = response.choices[0].message.content
        return json.loads(analysis_text)
    except Exception as e:
        logger.error(f"Error analyzing news sentiment: {e}")
        return None

# Routes
@app.route('/')
@login_required
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
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
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')
=======
# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', 
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', 
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class TradeForm(FlaskForm):
    symbol = StringField('Stock Symbol', validators=[DataRequired()])
    action = SelectField('Action', choices=[('BUY', 'Buy'), ('SELL', 'Sell')], validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Execute Trade')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return render_template('register.html', form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', 'error')
            return render_template('register.html', form=form)
        
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_reset_email(user.email, token)
            flash('Password reset email sent!', 'info')
            return redirect(url_for('login'))
        flash('Email not found', 'error')
    return render_template('forgot_password.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    if not user or user.reset_token_expiry < datetime.utcnow():
        flash('Invalid or expired reset token', 'error')
        return redirect(url_for('login'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()
        flash('Password reset successful!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
>>>>>>> 747f760ebec52577853952b2f681bb4da40fbd43

@app.route('/logout')
@login_required
def logout():
<<<<<<< HEAD
    """User logout"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/stocks/quote/<symbol>')
@login_required
def get_stock_quote(symbol):
    """Get stock quote"""
    data = get_stock_data(symbol)
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Stock not found'}), 404

@app.route('/api/stocks/search')
@login_required
def search_stocks():
    """Search stocks"""
    query = request.args.get('query', '').upper()
    if len(query) < 2:
        return jsonify({'stocks': []})
    
    # Simple search - in production, use a proper stock database
    common_stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'AMD', 'INTC']
    results = [stock for stock in common_stocks if query in stock]
    
    stocks_data = []
    for symbol in results[:10]:  # Limit to 10 results
        data = get_stock_data(symbol)
        if data:
            stocks_data.append({
                'symbol': symbol,
                'name': data['name'],
                'price': data['price']
            })
    
    return jsonify({'stocks': stocks_data})

@app.route('/api/stocks/watchlist')
@login_required
def get_watchlist():
    """Get user watchlist"""
    watchlist_items = Watchlist.query.filter_by(user_id=current_user.id).all()
    stocks_data = []
    
    for item in watchlist_items:
        data = get_stock_data(item.symbol)
        if data:
            stocks_data.append(data)
    
    return jsonify({'watchlist': stocks_data})

@app.route('/api/stocks/watchlist', methods=['POST'])
@login_required
def add_to_watchlist():
    """Add stock to watchlist"""
    data = request.get_json()
    symbol = data.get('symbol', '').upper()
    
    if not symbol:
        return jsonify({'error': 'Symbol required'}), 400
    
    # Check if already in watchlist
    existing = Watchlist.query.filter_by(user_id=current_user.id, symbol=symbol).first()
    if existing:
        return jsonify({'error': 'Stock already in watchlist'}), 400
    
    # Verify stock exists
    stock_data = get_stock_data(symbol)
    if not stock_data:
        return jsonify({'error': 'Stock not found'}), 404
    
    watchlist_item = Watchlist(user_id=current_user.id, symbol=symbol)
    db.session.add(watchlist_item)
    db.session.commit()
    
    return jsonify({'message': 'Added to watchlist'})

@app.route('/api/stocks/watchlist/<symbol>', methods=['DELETE'])
@login_required
def remove_from_watchlist(symbol):
    """Remove stock from watchlist"""
    watchlist_item = Watchlist.query.filter_by(user_id=current_user.id, symbol=symbol.upper()).first()
    if watchlist_item:
        db.session.delete(watchlist_item)
        db.session.commit()
        return jsonify({'message': 'Removed from watchlist'})
    else:
        return jsonify({'error': 'Stock not in watchlist'}), 404

@app.route('/api/economic/indicators')
@login_required
def get_economic_indicators():
    """Get economic indicators"""
    data = get_economic_data()
    return jsonify({'indicators': data})

@app.route('/api/news/financial')
@login_required
def get_financial_news_api():
    """Get financial news"""
    news = get_financial_news()
    return jsonify({'articles': news})

@app.route('/api/news/analyze-sentiment', methods=['POST'])
@login_required
def analyze_news_sentiment_api():
    """Analyze news sentiment"""
    data = request.get_json()
    articles = data.get('articles', [])
    symbol = data.get('symbol')
    
    analysis = analyze_news_sentiment(articles, symbol)
    if analysis:
        return jsonify({'analysis': analysis})
    else:
        return jsonify({'error': 'Analysis failed'}), 500
=======
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
>>>>>>> 747f760ebec52577853952b2f681bb4da40fbd43

@app.route('/stock/<symbol>')
@login_required
def stock_detail(symbol):
<<<<<<< HEAD
    """Stock detail page"""
    return render_template('stock_detail.html', symbol=symbol)

@app.route('/watchlist')
@login_required
def watchlist_page():
    """Watchlist page"""
    return render_template('watchlist.html')

@app.route('/news')
@login_required
def news_page():
    """News page"""
    return render_template('news.html')

@app.route('/economic')
@login_required
def economic_page():
    """Economic data page"""
    return render_template('economic.html')

@app.route('/profile')
@login_required
def profile_page():
    """Profile page"""
    return render_template('profile.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page"""
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate reset token
            token = secrets.token_urlsafe(32)
            user.password_reset_token = token
            db.session.commit()
            
            # Send email (in production, implement proper email sending)
            flash('Password reset link sent to your email', 'success')
        else:
            flash('Email not found', 'error')
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password page"""
    user = User.query.filter_by(password_reset_token=token).first()
    
    if not user:
        flash('Invalid or expired reset token', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
        else:
            user.set_password(password)
            user.password_reset_token = None
            db.session.commit()
            flash('Password reset successful', 'success')
            return redirect(url_for('login'))
    
    return render_template('reset_password.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
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
=======
    try:
        stock = yf.Ticker(symbol.upper())
        info = stock.info
        hist = stock.history(period="1mo")
        
        # Create price chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            name=symbol.upper()
        ))
        fig.update_layout(
            title=f'{symbol.upper()} Stock Price',
            yaxis_title='Price ($)',
            xaxis_title='Date',
            template='plotly_dark'
        )
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Get sector analysis
        sector_analysis = get_sector_analysis(info.get('sector', ''))
        
        # Get economic indicators
        economic_data = get_economic_indicators()
        
        return render_template('stock_detail.html', 
                             stock_info=info, 
                             graphJSON=graphJSON, 
                             symbol=symbol.upper(),
                             sector_analysis=sector_analysis,
                             economic_data=economic_data)
    except Exception as e:
        flash(f'Error fetching stock data: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/trade', methods=['GET', 'POST'])
@login_required
def trade():
    form = TradeForm()
    if form.validate_on_submit():
        try:
            symbol = form.symbol.data.upper()
            action = form.action.data
            quantity = int(form.quantity.data)
            
            # Get current price
            stock = yf.Ticker(symbol)
            current_price = stock.info.get('currentPrice', 0)
            
            if current_price == 0:
                flash('Invalid stock symbol', 'error')
                return render_template('trade.html', form=form)
            
            # Execute trade (simplified - in real app, you'd integrate with broker API)
            trade = Trade(
                user_id=current_user.id,
                symbol=symbol,
                action=action,
                quantity=quantity,
                price=current_price
            )
            db.session.add(trade)
            db.session.commit()
            
            flash(f'Trade executed: {action} {quantity} shares of {symbol} at ${current_price:.2f}', 'success')
            return redirect(url_for('portfolio'))
        except ValueError:
            flash('Invalid quantity', 'error')
        except Exception as e:
            flash(f'Error executing trade: {str(e)}', 'error')
    
    return render_template('trade.html', form=form)

@app.route('/portfolio')
@login_required
def portfolio():
    trades = Trade.query.filter_by(user_id=current_user.id).order_by(Trade.timestamp.desc()).all()
    return render_template('portfolio.html', trades=trades)

@app.route('/api/stock_search')
@login_required
def stock_search():
    query = request.args.get('q', '')
    if len(query) < 1:
        return jsonify([])
    
    try:
        # Simple stock search (in production, use a proper stock search API)
        suggestions = []
        common_stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'AMD', 'INTC', 'NFLX']
        for stock in common_stocks:
            if query.upper() in stock:
                suggestions.append({'symbol': stock, 'name': stock})
        return jsonify(suggestions[:5])
    except:
        return jsonify([])

def send_reset_email(email, token):
    try:
        msg = Message(
            'Password Reset - iTrade.com',
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        reset_url = url_for('reset_password', token=token, _external=True)
        msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request, please ignore this email.
'''
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

def get_economic_indicators():
    indicators = {}
    if fred:
        try:
            # Get recent economic data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            
            cpi_data = fred.get_series('CPIAUCSL', start_date, end_date)
            unemployment_data = fred.get_series('UNRATE', start_date, end_date)
            interest_rate_data = fred.get_series('FEDFUNDS', start_date, end_date)
            bond_yield_data = fred.get_series('GS10', start_date, end_date)
            house_price_data = fred.get_series('CSUSHPINSA', start_date, end_date)
            
            if len(cpi_data) > 0:
                indicators['cpi'] = cpi_data.iloc[-1]
            if len(unemployment_data) > 0:
                indicators['unemployment'] = unemployment_data.iloc[-1]
            if len(interest_rate_data) > 0:
                indicators['interest_rate'] = interest_rate_data.iloc[-1]
            if len(bond_yield_data) > 0:
                indicators['bond_yield'] = bond_yield_data.iloc[-1]
            if len(house_price_data) > 0:
                indicators['house_price'] = house_price_data.iloc[-1]
        except Exception as e:
            print(f"Error fetching economic data: {e}")
    return indicators

def get_sector_analysis(sector):
    if not OPENAI_API_KEY or not sector:
        return "Sector analysis not available"
    
    try:
        # Get recent news and analyze sector trends
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        prompt = f"""Analyze the current market sentiment and trends for the {sector} sector. 
        Consider recent news, market conditions, and provide a brief analysis of whether 
        this sector is likely to perform well in the short term. Keep response under 200 words."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial analyst providing market insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting sector analysis: {e}")
        return "Sector analysis temporarily unavailable"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
>>>>>>> 747f760ebec52577853952b2f681bb4da40fbd43
