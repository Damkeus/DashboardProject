"""Stock market data service with fallback demo data for NVIDIA stock."""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
import random
import math

logger = logging.getLogger(__name__)


class DemoStockDataGenerator:
    """Generate realistic demo stock data for NVIDIA when API is unavailable."""
    
    @staticmethod
    def generate_realistic_price_data(days: int, base_price: float = 189.0) -> List[Dict]:
        """
        Generate realistic NVIDIA stock price data.
        
        Args:
            days: Number of days of historical data to generate
            base_price: Starting price (approx current NVDA price ~$140)
            
        Returns:
            List of daily stock data with realistic price movements
        """
        data = []
        current_date = datetime.now().date()
        current_price = base_price
        
        # Simulate realistic stock volatility and trends
        for i in range(days, 0, -1):
            date = current_date - timedelta(days=i)
            
            # Skip weekends
            if date.weekday() >= 5:
                continue
            
            # Generate realistic daily price movement (-3% to +3%)
            daily_change = random.uniform(-0.03, 0.03)
            
            # Add some trend (NVIDIA has been generally bullish)
            trend = 0.0008  # Slight upward bias
            
            # Calculate OHLC (Open, High, Low, Close)
            open_price = current_price
            close_price = current_price * (1 + daily_change + trend)
            
            # High and low within reasonable range
            intraday_range = abs(close_price - open_price) * 1.5
            high_price = max(open_price, close_price) + random.uniform(0, intraday_range)
            low_price = min(open_price, close_price) - random.uniform(0, intraday_range)
            
            # Volume: realistic range for NVIDIA (millions of shares)
            volume = random.randint(20_000_000, 80_000_000)
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': round(open_price, 2),
                'close': round(close_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'volume': volume
            })
            
            current_price = close_price
        
        return data


class StockService:
    """Service for fetching NVIDIA stock market data using Alpha Vantage API."""
    
    def __init__(self, ticker: str = "NVDA"):
        self.ticker = ticker
        self._demo_generator = DemoStockDataGenerator()
        
        # Try to initialize Alpha Vantage
        try:
            import os
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
            
            if api_key and api_key != 'demo':
                from services.alphavantage_service import AlphaVantageService
                self.alpha_vantage = AlphaVantageService(api_key=api_key, ticker=ticker)
                logger.info(f"✅ Alpha Vantage initialized for {ticker}")
            else:
                logger.warning("No Alpha Vantage API key found, using demo data")
                self.alpha_vantage = None
        except Exception as e:
            logger.warning(f"Could not initialize Alpha Vantage: {e}. Using demo data only.")
            self.alpha_vantage = None
    
    def get_historical_data(self, period: str = "1y") -> List[Dict]:
        """
        Get historical stock data for NVIDIA.
        
        Args:
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            List of daily stock data
        """
        # Try Alpha Vantage first if available
        if self.alpha_vantage:
            try:
                logger.info(f"Fetching REAL stock data from Alpha Vantage for period {period}")
                data = self.alpha_vantage.get_historical_data(period=period)
                
                if data and len(data) > 0:
                    logger.info(f"✅ Successfully fetched {len(data)} REAL data points from Alpha Vantage!")
                    return data
                else:
                    logger.warning("Alpha Vantage returned no data, falling back to demo")
            except Exception as e:
                logger.warning(f"Alpha Vantage failed ({str(e)[:100]}). Falling back to demo data.")
        
        # Fallback to demo data
        logger.info(f"Using demo data for period {period}")
        period_days_map = {
            '1d': 1, '5d': 5, '1mo': 30, '3mo': 90,
            '6mo': 180, '1y': 365, '2y': 730, '5y': 1825,
            '10y': 3650, 'ytd': 365, 'max': 1825
        }
        days = period_days_map.get(period, 365)
        
        demo_data = self._demo_generator.generate_realistic_price_data(days)
        logger.info(f"Generated {len(demo_data)} demo data points")
        return demo_data
    
    def get_historical_data_range(self, start_date: str, end_date: str = None) -> List[Dict]:
        """
        Get historical stock data for a specific date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format (default: today)
            
        Returns:
            List of daily stock data
        """
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Calculate days difference
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        days = (end - start).days
        
        # Try to get from Alpha Vantage
        if self.alpha_vantage and days <= 7300:  # Alpha Vantage limit ~20 years
            try:
                all_data = self.alpha_vantage.get_daily_data(outputsize='full')
                
                # Filter by date range
                filtered = [
                    d for d in all_data
                    if start_date <= d['date'] <= end_date
                ]
                
                if filtered:
                    logger.info(f"Fetched {len(filtered)} data points for date range")
                    return filtered
            except Exception as e:
                logger.warning(f"Alpha Vantage range query failed: {e}")
        
        # Fallback to demo data
        logger.info(f"Generating demo data for range {start_date} to {end_date}")
        return self._demo_generator.generate_realistic_price_data(days)
    
    def get_current_price(self) -> Optional[float]:
        """Get current stock price from Alpha Vantage or latest demo data."""
        # Try Alpha Vantage GLOBAL_QUOTE (faster than daily series)
        if self.alpha_vantage:
            try:
                quote = self.alpha_vantage.get_global_quote()
                if quote and quote.get('price'):
                    price = quote['price']
                    logger.info(f"✅ Current {self.ticker} price from Alpha Vantage: ${price}")
                    return price
            except Exception as e:
                logger.warning(f"Global quote failed, trying daily data: {e}")
                
            # Fallback to daily data
            try:
                price = self.alpha_vantage.get_current_price()
                if price:
                    return price
            except Exception as e:
                logger.warning(f"Alpha Vantage current price failed: {e}")
        
        # Fallback to demo data
        try:
            latest_data = self.get_historical_data(period="1d")
            if latest_data:
                price = latest_data[-1]['close']
                logger.info(f"Current {self.ticker} price (demo): ${price}")
                return price
            return 189.0  # Ultimate fallback
        except Exception as e:
            logger.error(f"Failed to get price: {e}")
            return 189.0
    
    def get_market_cap(self) -> Optional[float]:
        """Get current market capitalization in billions USD."""
        try:
            # Calculate based on current price and shares outstanding
            price = self.get_current_price()
            shares_outstanding = 24.6  # billions (adjusted for stock splits)
            market_cap = (price * shares_outstanding)  # Already in billions
            
            logger.info(f"{self.ticker} market cap: ${market_cap:.2f}B")
            return round(market_cap, 2)
        except Exception as e:
            logger.error(f"Failed to calculate market cap: {e}")
            return 4650.0  # Fallback value (~$4.65T)
    
    def get_company_info(self) -> Dict:
        """Get company information and key metrics."""
        current_price = self.get_current_price()
        market_cap = self.get_market_cap()
        
        return {
            'name': 'NVIDIA Corporation',
            'sector': 'Technology',
            'industry': 'Semiconductors',
            'market_cap': market_cap,
            'current_price': current_price,
            'pe_ratio': 65.5,
            'forward_pe': 45.2,
            'dividend_yield': 0.03,
            '52_week_high': 150.32,
            '52_week_low': 108.13,
            'average_volume': 45_000_000
        }
    
    def get_latest_data_point(self) -> Optional[Dict]:
        """Get the most recent trading day's data."""
        data = self.get_historical_data(period="5d")
        
        if data:
            return data[-1]  # Last item is most recent
        return None


# Singleton instance for NVIDIA
stock_service = StockService("NVDA")
