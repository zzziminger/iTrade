import os
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import yfinance as yf
import plotly.graph_objs as go
import plotly.utils
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///itrade.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Environment variables
FRED_API_KEY = os.getenv('FRED_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize APIs
try:
    from fredapi import Fred
    fred = Fred(api_key=FRED_API_KEY) if FRED_API_KEY else None
except ImportError:
    fred = None
    logger.warning("FRED API not available")

try:
    from newsapi import NewsApiClient
    newsapi = NewsApiClient(api_key=NEWS_API_KEY) if NEWS_API_KEY else None
except ImportError:
    newsapi = None
    logger.warning("News API not available")

try:
    import openai
    openai.api_key = OPENAI_API_KEY
except ImportError:
    openai = None
    logger.warning("OpenAI API not available")

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_stock_data(symbol):
    """Get stock data without pandas dependency"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Get current price and basic info
        current_price = info.get('currentPrice', 0)
        previous_close = info.get('previousClose', 0)
        
        if current_price and previous_close:
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100
        else:
            change = 0
            change_percent = 0
        
        # Get historical data for chart
        hist = ticker.history(period="1mo")
        
        # Convert to list of dictionaries for JSON serialization
        chart_data = []
        for date, row in hist.iterrows():
            chart_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume'])
            })
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'previous_price': previous_close,
            'change': change,
            'change_percent': change_percent,
            'chart_data': chart_data,
            'info': {
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'volume': info.get('volume'),
                'avg_volume': info.get('averageVolume')
            }
        }
    except Exception as e:
        logger.error(f"Error getting stock data for {symbol}: {e}")
        return None

def get_economic_data():
    """Get economic data without pandas dependency"""
    if not fred:
        return []
    
    try:
        # Get economic indicators
        indicators = {
            'CPI': 'CPIAUCSL',
            'Interest Rate': 'FEDFUNDS',
            'Unemployment': 'UNRATE',
            'GDP': 'GDP'
        }
        
        data = []
        for name, series_id in indicators.items():
            try:
                series = fred.get_series(series_id, limit=12)
                if not series.empty:
                    # Convert to list of dictionaries
                    values = []
                    for date, value in series.items():
                        values.append({
                            'date': date.strftime('%Y-%m-%d'),
                            'value': float(value)
                        })
                    
                    data.append({
                        'name': name,
                        'series_id': series_id,
                        'values': values,
                        'latest_value': float(series.iloc[-1]),
                        'latest_date': series.index[-1].strftime('%Y-%m-%d')
                    })
            except Exception as e:
                logger.error(f"Error getting {name} data: {e}")
                continue
        
        return data
    except Exception as e:
        logger.error(f"Error getting economic data: {e}")
        return []

def get_news_data():
    """Get financial news"""
    if not newsapi:
        return []
    
    try:
        news = newsapi.get_top_headlines(
            category='business',
            language='en',
            country='us',
            page_size=10
        )
        
        return [
            {
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'published_at': article['publishedAt'],
                'source': article['source']['name']
            }
            for article in news.get('articles', [])
        ]
    except Exception as e:
        logger.error(f"Error getting news: {e}")
        return []

def analyze_market_sentiment(news_data):
    """Analyze market sentiment using OpenAI"""
    if not openai or not news_data:
        return "Market sentiment analysis unavailable."
    
    try:
        # Create a summary of recent news
        news_summary = "\n".join([
            f"- {article['title']}" for article in news_data[:5]
        ])
        
        prompt = f"""
        Based on the following financial news, provide a brief market sentiment analysis:
        
        {news_summary}
        
        Please provide a 2-3 sentence analysis of the current market sentiment.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        return "Market sentiment analysis unavailable."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
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
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
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
    # Get some sample stock data
    stocks = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
    stock_data = []
    
    for symbol in stocks:
        data = get_stock_data(symbol)
        if data:
            stock_data.append(data)
    
    # Get economic data
    economic_data = get_economic_data()
    
    # Get news
    news_data = get_news_data()
    
    # Analyze sentiment
    sentiment = analyze_market_sentiment(news_data)
    
    return render_template('dashboard.html', 
                         stocks=stock_data,
                         economic_data=economic_data,
                         news=news_data,
                         sentiment=sentiment)

@app.route('/stock/<symbol>')
@login_required
def stock_detail(symbol):
    stock_data = get_stock_data(symbol)
    if not stock_data:
        flash('Stock data not available')
        return redirect(url_for('dashboard'))
    
    return render_template('stock_detail.html', stock=stock_data)

@app.route('/api/stock/<symbol>')
def api_stock_data(symbol):
    data = get_stock_data(symbol)
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Stock data not available'}), 404

@app.route('/api/economic')
def api_economic_data():
    data = get_economic_data()
    return jsonify(data)

@app.route('/api/news')
def api_news():
    data = get_news_data()
    return jsonify(data)

@app.route('/api/sentiment')
def api_sentiment():
    news_data = get_news_data()
    sentiment = analyze_market_sentiment(news_data)
    return jsonify({'sentiment': sentiment})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 