from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///itrade.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Environment variables
FRED_API_KEY = os.getenv('FRED_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

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
    """Get stock data using simple API calls"""
    try:
        # Mock data for demonstration
        mock_data = {
            'symbol': symbol,
            'current_price': 150.0,
            'previous_price': 148.0,
            'change': 2.0,
            'change_percent': 1.35,
            'info': {
                'market_cap': 2500000000000,
                'pe_ratio': 25.5,
                'volume': 50000000,
                'avg_volume': 45000000
            }
        }
        return mock_data
    except Exception as e:
        return None

def get_economic_data():
    """Get economic data using simple API calls"""
    try:
        # Mock economic data
        mock_data = [
            {
                'name': 'CPI',
                'latest_value': 3.2,
                'latest_date': '2024-01-01',
                'trend': 'increasing'
            },
            {
                'name': 'Interest Rate',
                'latest_value': 5.5,
                'latest_date': '2024-01-01',
                'trend': 'stable'
            },
            {
                'name': 'Unemployment',
                'latest_value': 3.7,
                'latest_date': '2024-01-01',
                'trend': 'decreasing'
            }
        ]
        return mock_data
    except Exception as e:
        return []

def get_news_data():
    """Get financial news using simple API calls"""
    try:
        # Mock news data
        mock_news = [
            {
                'title': 'Market Update: Tech Stocks Rally',
                'description': 'Technology stocks showed strong performance today with major gains across the sector.',
                'url': '#',
                'published_at': '2024-01-01T10:00:00Z',
                'source': 'Financial News'
            },
            {
                'title': 'Federal Reserve Policy Review',
                'description': 'Latest insights on monetary policy decisions and their impact on markets.',
                'url': '#',
                'published_at': '2024-01-01T09:00:00Z',
                'source': 'Economic Times'
            },
            {
                'title': 'Earnings Season Kicks Off',
                'description': 'Major companies report strong quarterly results, boosting market confidence.',
                'url': '#',
                'published_at': '2024-01-01T08:00:00Z',
                'source': 'Market Watch'
            }
        ]
        return mock_news
    except Exception as e:
        return []

def analyze_market_sentiment(news_data):
    """Simple market sentiment analysis"""
    if not news_data:
        return "Market sentiment analysis unavailable."
    
    # Simple sentiment analysis
    positive_keywords = ['rally', 'gain', 'positive', 'growth', 'up', 'strong']
    negative_keywords = ['fall', 'drop', 'negative', 'decline', 'down', 'weak']
    
    positive_count = 0
    negative_count = 0
    
    for article in news_data:
        text = (article.get('title', '') + ' ' + article.get('description', '')).lower()
        for keyword in positive_keywords:
            if keyword in text:
                positive_count += 1
        for keyword in negative_keywords:
            if keyword in text:
                negative_count += 1
    
    if positive_count > negative_count:
        return "Market sentiment appears positive based on recent news with strong earnings and tech rally."
    elif negative_count > positive_count:
        return "Market sentiment appears cautious based on recent news and economic indicators."
    else:
        return "Market sentiment appears neutral based on recent news and mixed economic signals."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "iTrade",
        "version": "production"
    })

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
    # Get sample stock data
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

@app.route('/watchlist')
@login_required
def watchlist():
    return render_template('watchlist.html')

@app.route('/news')
@login_required
def news():
    news_data = get_news_data()
    return render_template('news.html', news=news_data)

@app.route('/economic')
@login_required
def economic():
    economic_data = get_economic_data()
    return render_template('economic.html', economic_data=economic_data)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

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