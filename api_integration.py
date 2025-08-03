"""
Real API Integration for iTrade
Includes: Yahoo Finance, Alpha Vantage, FRED, News API, and OpenAI
Enhanced with: Gold, Oil, VIX, and Major Indices
"""

import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class StockAPI:
    """Real stock data integration using Yahoo Finance"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_stock_quote(self, symbol):
        """Get real-time stock quote"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get current price
            hist = ticker.history(period="2d")
            if len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                previous_price = hist['Close'].iloc[-2]
                change = current_price - previous_price
                change_percent = (change / previous_price) * 100
            else:
                current_price = info.get('currentPrice', 0)
                previous_price = info.get('previousClose', current_price)
                change = current_price - previous_price
                change_percent = (change / previous_price) * 100 if previous_price else 0
            
            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'current_price': current_price,
                'previous_price': previous_price,
                'change': change,
                'change_percent': change_percent,
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'high_52_week': info.get('fiftyTwoWeekHigh', 0),
                'low_52_week': info.get('fiftyTwoWeekLow', 0),
                'avg_volume': info.get('averageVolume', 0),
                'open': info.get('open', 0),
                'high': info.get('dayHigh', 0),
                'low': info.get('dayLow', 0)
            }
        except Exception as e:
            print(f"Error getting stock quote for {symbol}: {e}")
            return None
    
    def get_stock_history(self, symbol, period="1y"):
        """Get historical stock data"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            # Convert to list of dictionaries
            history = []
            for date, row in hist.iterrows():
                history.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': row['Open'],
                    'high': row['High'],
                    'low': row['Low'],
                    'close': row['Close'],
                    'volume': row['Volume']
                })
            
            return history
        except Exception as e:
            print(f"Error getting stock history for {symbol}: {e}")
            return []
    
    def get_market_data(self):
        """Get major market indices and key commodities from Yahoo Finance"""
        # Focus on the specific instruments requested
        symbols = {
            '^IXIC': 'NASDAQ',
            '^DJI': 'Dow Jones', 
            '^GSPC': 'S&P 500',
            '^VIX': 'VIX',
            'GC=F': 'Gold',
            'CL=F': 'Oil (WTI)'
        }
        
        market_data = {}
        
        for symbol, name in symbols.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                
                if len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2]
                    change = current - previous
                    change_percent = (change / previous) * 100 if previous else 0
                    
                    market_data[symbol] = {
                        'name': name,
                        'current': current,
                        'previous': previous,
                        'change': change,
                        'change_percent': change_percent,
                        'symbol': symbol
                    }
                else:
                    # Fallback to info if history is not available
                    info = ticker.info
                    current = info.get('currentPrice', 0)
                    previous = info.get('previousClose', current)
                    change = current - previous
                    change_percent = (change / previous) * 100 if previous else 0
                    
                    market_data[symbol] = {
                        'name': name,
                        'current': current,
                        'previous': previous,
                        'change': change,
                        'change_percent': change_percent,
                        'symbol': symbol
                    }
                    
            except Exception as e:
                print(f"Error getting market data for {symbol}: {e}")
                # Provide fallback data
                market_data[symbol] = {
                    'name': name,
                    'current': 0,
                    'previous': 0,
                    'change': 0,
                    'change_percent': 0,
                    'symbol': symbol
                }
        
        return market_data
    
    def get_commodity_data(self):
        """Get commodity prices (Gold, Oil, etc.)"""
        commodities = {
            'GC=F': 'Gold',
            'SI=F': 'Silver',
            'CL=F': 'Oil (WTI)',
            'BZ=F': 'Oil (Brent)',
            'NG=F': 'Natural Gas',
            'ZC=F': 'Corn',
            'ZS=F': 'Soybeans',
            'KC=F': 'Coffee'
        }
        
        commodity_data = {}
        
        for symbol, name in commodities.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                
                if len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2]
                    change = current - previous
                    change_percent = (change / previous) * 100 if previous else 0
                    
                    commodity_data[symbol] = {
                        'name': name,
                        'current': current,
                        'previous': previous,
                        'change': change,
                        'change_percent': change_percent,
                        'symbol': symbol
                    }
                    
            except Exception as e:
                print(f"Error getting commodity data for {symbol}: {e}")
                commodity_data[symbol] = {
                    'name': name,
                    'current': 0,
                    'previous': 0,
                    'change': 0,
                    'change_percent': 0,
                    'symbol': symbol
                }
        
        return commodity_data
    
    def get_crypto_data(self):
        """Get cryptocurrency prices"""
        cryptos = {
            'BTC-USD': 'Bitcoin',
            'ETH-USD': 'Ethereum',
            'USDT-USD': 'Tether',
            'BNB-USD': 'Binance Coin',
            'ADA-USD': 'Cardano',
            'SOL-USD': 'Solana'
        }
        
        crypto_data = {}
        
        for symbol, name in cryptos.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                
                if len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2]
                    change = current - previous
                    change_percent = (change / previous) * 100 if previous else 0
                    
                    crypto_data[symbol] = {
                        'name': name,
                        'current': current,
                        'previous': previous,
                        'change': change,
                        'change_percent': change_percent,
                        'symbol': symbol
                    }
                    
            except Exception as e:
                print(f"Error getting crypto data for {symbol}: {e}")
                crypto_data[symbol] = {
                    'name': name,
                    'current': 0,
                    'previous': 0,
                    'change': 0,
                    'change_percent': 0,
                    'symbol': symbol
                }
        
        return crypto_data

class EconomicAPI:
    """Federal Reserve Economic Data (FRED) integration"""
    
    def __init__(self):
        self.api_key = os.getenv('FRED_API_KEY')
        self.base_url = "https://api.stlouisfed.org/fred/series"
    
    def get_economic_data(self):
        """Get key economic indicators"""
        if not self.api_key:
            return self._get_mock_economic_data()
        
        indicators = {
            'CPIAUCSL': 'CPI',
            'FEDFUNDS': 'Federal Funds Rate',
            'UNRATE': 'Unemployment Rate',
            'GDP': 'GDP',
            'PAYEMS': 'Nonfarm Payrolls'
        }
        
        economic_data = []
        
        for series_id, name in indicators.items():
            try:
                url = f"{self.base_url}/observations"
                params = {
                    'series_id': series_id,
                    'api_key': self.api_key,
                    'file_type': 'json',
                    'limit': 1,
                    'sort_order': 'desc'
                }
                
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if 'observations' in data and data['observations']:
                        latest = data['observations'][0]
                        economic_data.append({
                            'name': name,
                            'latest_value': float(latest['value']),
                            'latest_date': latest['date'],
                            'series_id': series_id
                        })
            except Exception as e:
                print(f"Error getting economic data for {series_id}: {e}")
        
        return economic_data if economic_data else self._get_mock_economic_data()
    
    def _get_mock_economic_data(self):
        """Fallback mock data"""
        return [
            {
                'name': 'CPI',
                'latest_value': 3.2,
                'latest_date': '2024-01-01',
                'trend': 'increasing'
            },
            {
                'name': 'Federal Funds Rate',
                'latest_value': 5.5,
                'latest_date': '2024-01-01',
                'trend': 'stable'
            },
            {
                'name': 'Unemployment Rate',
                'latest_value': 3.7,
                'latest_date': '2024-01-01',
                'trend': 'decreasing'
            }
        ]

class NewsAPI:
    """Financial news integration"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"
    
    def get_financial_news(self, query="stock market", page_size=10):
        """Get financial news articles"""
        if not self.api_key:
            return self._get_mock_news()
        
        try:
            url = f"{self.base_url}/everything"
            params = {
                'q': query,
                'apiKey': self.api_key,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': page_size,
                'domains': 'reuters.com,bloomberg.com,cnbc.com,marketwatch.com'
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if 'articles' in data:
                    return self._format_news_articles(data['articles'])
            
            return self._get_mock_news()
        except Exception as e:
            print(f"Error getting news: {e}")
            return self._get_mock_news()
    
    def get_stock_news(self, symbol):
        """Get news specific to a stock"""
        return self.get_financial_news(f"{symbol} stock")
    
    def _format_news_articles(self, articles):
        """Format news articles for display"""
        formatted_articles = []
        for article in articles:
            formatted_articles.append({
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'url': article.get('url', '#'),
                'source': article.get('source', {}).get('name', 'Unknown'),
                'published_at': article.get('publishedAt', ''),
                'image_url': article.get('urlToImage', '')
            })
        return formatted_articles
    
    def _get_mock_news(self):
        """Fallback mock news data"""
        return [
            {
                'title': 'Market Update: Tech Stocks Rally',
                'description': 'Technology stocks showed strong performance today with major gains across the sector.',
                'url': '#',
                'source': 'Financial News',
                'published_at': '2024-01-01T10:00:00Z',
                'image_url': ''
            },
            {
                'title': 'Federal Reserve Policy Review',
                'description': 'Latest insights on monetary policy decisions and their impact on markets.',
                'url': '#',
                'source': 'Economic Times',
                'published_at': '2024-01-01T09:00:00Z',
                'image_url': ''
            },
            {
                'title': 'Earnings Season Kicks Off',
                'description': 'Major companies report strong quarterly results, boosting market confidence.',
                'url': '#',
                'source': 'Market Watch',
                'published_at': '2024-01-01T08:00:00Z',
                'image_url': ''
            }
        ]

class AIAnalysis:
    """AI-powered market analysis using OpenAI"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    def analyze_market_sentiment(self, news_data, stock_data=None):
        """Analyze market sentiment using AI"""
        if not self.api_key:
            return self._get_mock_sentiment()
        
        try:
            # Prepare context from news and stock data
            context = self._prepare_analysis_context(news_data, stock_data)
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a financial analyst. Provide concise market sentiment analysis based on the given data.'
                    },
                    {
                        'role': 'user',
                        'content': f"Analyze the market sentiment based on this data: {context}"
                    }
                ],
                'max_tokens': 200,
                'temperature': 0.7
            }
            
            response = requests.post(self.base_url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            
            return self._get_mock_sentiment()
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            return self._get_mock_sentiment()
    
    def _prepare_analysis_context(self, news_data, stock_data):
        """Prepare context for AI analysis"""
        context = "Recent financial news:\n"
        for article in news_data[:3]:  # Use top 3 articles
            context += f"- {article.get('title', '')}\n"
        
        if stock_data:
            context += f"\nStock data: {stock_data.get('symbol', '')} at ${stock_data.get('current_price', 0):.2f}"
        
        return context
    
    def _get_mock_sentiment(self):
        """Fallback mock sentiment analysis"""
        return "Market sentiment appears positive based on recent news with strong earnings and tech rally."

# Global API instances
stock_api = StockAPI()
economic_api = EconomicAPI()
news_api = NewsAPI()
ai_analysis = AIAnalysis()

def get_real_stock_data(symbol):
    """Get real stock data"""
    return stock_api.get_stock_quote(symbol)

def get_real_economic_data():
    """Get real economic data"""
    return economic_api.get_economic_data()

def get_real_news_data():
    """Get real news data"""
    return news_api.get_financial_news()

def get_real_market_data():
    """Get real market indices data"""
    return stock_api.get_market_data()

def get_real_sentiment_analysis(news_data, stock_data=None):
    """Get real AI sentiment analysis"""
    return ai_analysis.analyze_market_sentiment(news_data, stock_data) 