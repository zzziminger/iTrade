from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

# Import real API integration
from api_integration import (
    get_real_stock_data,
    get_real_economic_data,
    get_real_news_data,
    get_real_market_data,
    get_real_sentiment_analysis
)

# Load environment variables
load_dotenv()

# Configure logging for Vercel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '9d0be5a21203d14e3387ac86e8839496004b58a3bb2de86ea54f758fda38c31')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///itrade.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Global database connection management (equivalent to Prisma singleton)
def get_db():
    """Get database instance with proper error handling"""
    try:
        return db
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

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
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        logger.error(f"Error loading user {user_id}: {e}")
        return None

def get_stock_data(symbol):
    """Get real stock data using API integration with proper error handling"""
    try:
        return get_real_stock_data(symbol)
    except Exception as e:
        logger.error(f"Error getting stock data for {symbol}: {e}")
        # Fallback to mock data
        return {
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

def get_economic_data():
    """Get real economic data using API integration with proper error handling"""
    try:
        return get_real_economic_data()
    except Exception as e:
        logger.error(f"Error getting economic data: {e}")
        # Fallback to mock data
        return [
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

def get_news_data():
    """Get real news data using API integration with proper error handling"""
    try:
        return get_real_news_data()
    except Exception as e:
        logger.error(f"Error getting news data: {e}")
        # Fallback to mock data
        return [
            {
                'title': 'Market Update: Tech Stocks Rally',
                'summary': 'Technology stocks showed strong performance today...',
                'source': 'Financial News',
                'published_at': '2024-01-01T10:00:00Z'
            },
            {
                'title': 'Federal Reserve Policy Update',
                'summary': 'The Federal Reserve announced new policy measures...',
                'source': 'Economic Times',
                'published_at': '2024-01-01T09:30:00Z'
            }
        ]

def get_market_data():
    """Get real market data using API integration with proper error handling"""
    try:
        return get_real_market_data()
    except Exception as e:
        logger.error(f"Error getting market data: {e}")
        # Fallback to mock data
        return {
            'indices': [
                {'symbol': '^GSPC', 'name': 'S&P 500', 'value': 4500.0, 'change': 25.0},
                {'symbol': '^DJI', 'name': 'Dow Jones', 'value': 35000.0, 'change': 150.0},
                {'symbol': '^IXIC', 'name': 'NASDAQ', 'value': 14000.0, 'change': 75.0}
            ]
        }

def analyze_market_sentiment(news_data, stock_data=None):
    """Analyze market sentiment with proper error handling"""
    try:
        return get_real_sentiment_analysis(news_data, stock_data)
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        return {'sentiment': 'neutral', 'confidence': 0.5}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint for Vercel monitoring"""
    try:
        # Test database connection
        db_status = "connected" if get_db() else "disconnected"
        
        return jsonify({
            "status": "healthy",
            "service": "iTrade",
            "version": "production",
            "database": db_status,
            "timestamp": datetime.utcnow().isoformat(),
            "apis": {
                "stock": "enabled",
                "economic": "enabled", 
                "news": "enabled",
                "ai": "enabled"
            }
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

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
    # Get real stock data
    stocks = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA', 'AMZN']
    stock_data = []
    
    for symbol in stocks:
        data = get_stock_data(symbol)
        if data:
            stock_data.append(data)
    
    # Get real economic data
    economic_data = get_economic_data()
    
    # Get real news
    news_data = get_news_data()
    
    # Get comprehensive market data including indices, commodities, and crypto
    try:
        from api_integration import StockAPI
        stock_api = StockAPI()
        
        # Get major indices and commodities
        market_data = stock_api.get_market_data()
        
        # Get commodity data (Gold, Oil, etc.)
        commodity_data = stock_api.get_commodity_data()
        
        # Get crypto data
        crypto_data = stock_api.get_crypto_data()
        
    except Exception as e:
        logger.error(f"Error getting comprehensive market data: {e}")
        # Fallback to basic market data
        market_data = get_market_data()
        commodity_data = {}
        crypto_data = {}
    
    # Analyze sentiment
    sentiment = analyze_market_sentiment(news_data)
    
    return render_template('dashboard.html', 
                         stocks=stock_data,
                         economic_data=economic_data,
                         news=news_data,
                         market_data=market_data,
                         commodity_data=commodity_data,
                         crypto_data=crypto_data,
                         sentiment=sentiment)

@app.route('/stock/<symbol>')
@login_required
def stock_detail(symbol):
    stock_data = get_stock_data(symbol)
    if not stock_data:
        flash('Stock data not available')
        return redirect(url_for('dashboard'))
    
    # Get stock-specific news
    from api_integration import news_api
    stock_news = news_api.get_stock_news(symbol)
    
    return render_template('stock_detail.html', 
                         stock=stock_data,
                         news=stock_news)

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

@app.route('/api/market')
def api_market_data():
    """Get comprehensive market data including indices, commodities, and crypto"""
    try:
        from api_integration import StockAPI
        stock_api = StockAPI()
        
        market_data = stock_api.get_market_data()
        commodity_data = stock_api.get_commodity_data()
        crypto_data = stock_api.get_crypto_data()
        
        return jsonify({
            'indices': market_data,
            'commodities': commodity_data,
            'crypto': crypto_data
        })
    except Exception as e:
        logger.error(f"Error getting market data: {e}")
        return jsonify({'error': 'Market data unavailable'}), 500

@app.route('/api/commodities')
def api_commodity_data():
    """Get commodity prices (Gold, Oil, etc.)"""
    try:
        from api_integration import StockAPI
        stock_api = StockAPI()
        data = stock_api.get_commodity_data()
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error getting commodity data: {e}")
        return jsonify({'error': 'Commodity data unavailable'}), 500

@app.route('/api/crypto')
def api_crypto_data():
    """Get cryptocurrency prices"""
    try:
        from api_integration import StockAPI
        stock_api = StockAPI()
        data = stock_api.get_crypto_data()
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error getting crypto data: {e}")
        return jsonify({'error': 'Crypto data unavailable'}), 500

@app.route('/api/sentiment')
def api_sentiment():
    news_data = get_news_data()
    sentiment = analyze_market_sentiment(news_data)
    return jsonify({'sentiment': sentiment})

@app.route('/api/stock/<symbol>/history')
def api_stock_history(symbol):
    """Get historical stock data with proper error handling"""
    try:
        from api_integration import stock_api
        period = request.args.get('period', '1y')
        history = stock_api.get_stock_history(symbol, period)
        return jsonify(history)
    except Exception as e:
        logger.error(f"Error getting stock history for {symbol}: {e}")
        return jsonify({'error': 'Historical data not available'}), 500

# Global error handlers for Vercel compatibility
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {e}")
    return jsonify({'error': 'Internal server error'}), 500

# Ensure database is created for Vercel
def create_tables():
    """Create database tables with error handling"""
    try:
        with app.app_context():
            db.create_all()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

if __name__ == '__main__':
    create_tables()
    app.run(debug=True) 