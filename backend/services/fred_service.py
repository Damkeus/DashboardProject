"""FRED (Federal Reserve Economic Data) API integration service."""
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from config import settings

logger = logging.getLogger(__name__)

BASE_URL = "https://api.stlouisfed.org/fred"


class FREDService:
    """Service for fetching economic data from FRED API."""
    
    def __init__(self):
        self.api_key = settings.fred_api_key
        self.base_url = BASE_URL
        
    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """Make HTTP request to FRED API with error handling."""
        params['api_key'] = self.api_key
        params['file_type'] = 'json'
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(
                url, 
                params=params,
                timeout=settings.request_timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"FRED API request failed: {e}")
            return None
    
    def get_federal_funds_rate(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """
        Get Federal Funds Effective Rate.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of observations with date and value
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        params = {
            'series_id': 'FEDFUNDS',
            'observation_start': start_date,
            'observation_end': end_date
        }
        
        data = self._make_request('series/observations', params)
        
        if data and 'observations' in data:
            logger.info(f"Fetched {len(data['observations'])} federal funds rate observations")
            return data['observations']
        return []
    
    def get_gdp_growth(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """
        Get Real GDP Growth Rate (quarterly).
        
        Series: A191RL1Q225SBEA - Real Gross Domestic Product, Percent Change from Previous Period
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")  # 2 years
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        params = {
            'series_id': 'A191RL1Q225SBEA',
            'observation_start': start_date,
            'observation_end': end_date
        }
        
        data = self._make_request('series/observations', params)
        
        if data and 'observations' in data:
            logger.info(f"Fetched {len(data['observations'])} GDP growth observations")
            return data['observations']
        return []
    
    def get_inflation_rate(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """
        Get Consumer Price Index (CPI) for inflation tracking.
        
        Series: CPIAUCSL - Consumer Price Index for All Urban Consumers: All Items
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=1095)).strftime("%Y-%m-%d")  # 3 years
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        params = {
            'series_id': 'CPIAUCSL',
            'observation_start': start_date,
            'observation_end': end_date
        }
        
        data = self._make_request('series/observations', params)
        
        if data and 'observations' in data:
            # Calculate year-over-year percentage change
            observations = data['observations']
            logger.info(f"Fetched {len(observations)} CPI observations")
            return observations
        return []
    
    def calculate_cpi_yoy_change(self, observations: List[Dict]) -> List[Dict]:
        """Calculate year-over-year CPI change from raw observations."""
        if len(observations) < 12:
            return []
        
        result = []
        for i in range(12, len(observations)):
            current = observations[i]
            year_ago = observations[i - 12]
            
            try:
                current_value = float(current['value'])
                year_ago_value = float(year_ago['value'])
                yoy_change = ((current_value - year_ago_value) / year_ago_value) * 100
                
                result.append({
                    'date': current['date'],
                    'value': round(yoy_change, 2)
                })
            except (ValueError, KeyError):
                continue
        
        return result


# Singleton instance
fred_service = FREDService()
