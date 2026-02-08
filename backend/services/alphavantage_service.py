"""Alpha Vantage API service for real-time stock data.

This service fetches NVIDIA stock data from Alpha Vantage API,
avoiding SSL certificate issues that occur with yfinance.

API Documentation: https://www.alphavantage.co/documentation/
"""
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
import time
import urllib3

# Disable SSL warnings for Windows firewall environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


class AlphaVantageService:
    """Service for fetching stock data from Alpha Vantage API."""
    
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self, api_key: str = "demo", ticker: str = "NVDA"):
        """
        Initialize Alpha Vantage service.
        
        Args:
            api_key: Alpha Vantage API key (get free key at https://www.alphavantage.co/support/#api-key)
            ticker: Stock ticker symbol (default: NVDA for NVIDIA)
        """
        self.api_key = api_key
        self.ticker = ticker
        self._last_request_time = 0
        self._rate_limit_delay = 12  # Alpha Vantage free tier: 5 requests/minute
        
    def _make_request(self, params: Dict) -> Dict:
        """
        Make rate-limited request to Alpha Vantage API.
        
        Args:
            params: Query parameters for the API
            
        Returns:
            JSON response from API
        """
        # Rate limiting: wait if needed
        elapsed = time.time() - self._last_request_time
        if elapsed < self._rate_limit_delay:
            wait_time = self._rate_limit_delay - elapsed
            logger.info(f"Rate limiting: waiting {wait_time:.1f}s")
            time.sleep(wait_time)
        
        params['apikey'] = self.api_key
        
        try:
            # Disable SSL verification to bypass Windows firewall/certificate issues
            response = requests.get(
                self.BASE_URL, 
                params=params, 
                timeout=10,
                verify=False  # Bypass SSL certificate validation
            )
            response.raise_for_status()
            self._last_request_time = time.time()
            
            data = response.json()
            
            # Check for API errors
            if "Error Message" in data:
                raise ValueError(f"API Error: {data['Error Message']}")
            if "Note" in data:
                logger.warning(f"API Note: {data['Note']}")
                
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
    
    def get_daily_data(self, outputsize: str = "compact") -> List[Dict]:
        """
        Get daily time series data.
        
        Args:
            outputsize: 'compact' (100 days) or 'full' (20+ years)
            
        Returns:
            List of daily stock data points
        """
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': self.ticker,
            'outputsize': outputsize
        }
        
        try:
            logger.info(f"Fetching daily data for {self.ticker} from Alpha Vantage")
            data = self._make_request(params)
            
            if "Time Series (Daily)" not in data:
                logger.warning(f"No time series data in response: {list(data.keys())}")
                return []
            
            time_series = data["Time Series (Daily)"]
            
            # Convert to our format
            result = []
            for date_str, values in time_series.items():
                result.append({
                    'date': date_str,
                    'open': round(float(values['1. open']), 2),
                    'high': round(float(values['2. high']), 2),
                    'low': round(float(values['3. low']), 2),
                    'close': round(float(values['4. close']), 2),
                    'volume': int(values['5. volume'])
                })
            
            # Sort by date (oldest first)
            result.sort(key=lambda x: x['date'])
            
            logger.info(f"✅ Fetched {len(result)} days of real data from Alpha Vantage")
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch data from Alpha Vantage: {e}")
            return []
    
    def get_historical_data(self, period: str = "1y") -> List[Dict]:
        """
        Get historical data for a specific period.
        
        Args:
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, etc.)
            
        Returns:
            List of daily stock data
        """
        # Determine output size based on period
        period_days = {
            '1d': 1, '5d': 5, '1mo': 30, '3mo': 90,
            '6mo': 180, '1y': 365, '2y': 730, '5y': 1825,
            '10y': 3650, 'ALL': 7300
        }
        
        days_needed = period_days.get(period, 365)
        
        # Alpha Vantage: compact=100 days, full=20+ years
        outputsize = 'full' if days_needed > 100 else 'compact'
        
        all_data = self.get_daily_data(outputsize=outputsize)
        
        if not all_data:
            return []
        
        # Filter to requested period
        if days_needed < len(all_data):
            return all_data[-days_needed:]
        
        return all_data
    
    def get_current_price(self) -> Optional[float]:
        """Get the most recent closing price."""
        try:
            data = self.get_daily_data(outputsize='compact')
            if data:
                latest = data[-1]
                price = latest['close']
                logger.info(f"Current {self.ticker} price: ${price}")
                return price
            return None
        except Exception as e:
            logger.error(f"Failed to get current price: {e}")
            return None
    
    def get_global_quote(self) -> Optional[Dict]:
        """
        Get real-time quote (faster than daily time series).
        
        Returns:
            Dict with current price, change, volume, etc.
        """
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': self.ticker
        }
        
        try:
            data = self._make_request(params)
            
            if "Global Quote" not in data:
                return None
            
            quote = data["Global Quote"]
            
            return {
                'price': round(float(quote.get('05. price', 0)), 2),
                'change': round(float(quote.get('09. change', 0)), 2),
                'change_percent': quote.get('10. change percent', '0%'),
                'volume': int(quote.get('06. volume', 0)),
                'latest_trading_day': quote.get('07. latest trading day', ''),
            }
            
        except Exception as e:
            logger.error(f"Failed to get global quote: {e}")
            return None


# Example usage
if __name__ == "__main__":
    # For testing - use demo key or replace with your own
    service = AlphaVantageService(api_key="demo", ticker="NVDA")
    
    # Get current price
    price = service.get_current_price()
    print(f"Current NVDA price: ${price}")
    
    # Get recent data
    data = service.get_historical_data(period="1mo")
    print(f"Got {len(data)} data points")
    if data:
        print(f"Latest: {data[-1]}")
