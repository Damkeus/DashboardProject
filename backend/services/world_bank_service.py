"""World Bank API integration service for global GDP and economic indicators."""
import requests
from typing import Dict, List, Optional
from datetime import datetime
import logging
from config import settings

logger = logging.getLogger(__name__)

BASE_URL = "https://api.worldbank.org/v2"


class WorldBankService:
    """Service for fetching global economic data from World Bank API."""
    
    def __init__(self):
        self.base_url = BASE_URL
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[List]:
        """Make HTTP request to World Bank API."""
        if params is None:
            params = {}
        
        params['format'] = 'json'
        params['per_page'] = 100
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(
                url,
                params=params,
                timeout=settings.request_timeout
            )
            response.raise_for_status()
            data = response.json()
            
            # World Bank API returns [metadata, data]
            if isinstance(data, list) and len(data) > 1:
                return data[1]
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"World Bank API request failed: {e}")
            return None
    
    def get_global_gdp_growth(self, start_year: int = None, end_year: int = None) -> List[Dict]:
        """
        Get global GDP growth rate.
        
        Indicator: NY.GDP.MKTP.KD.ZG - GDP growth (annual %)
        Country: WLD (World)
        
        Args:
            start_year: Start year (default: 5 years ago)
            end_year: End year (default: current year)
            
        Returns:
            List of {year, value} dictionaries
        """
        if not start_year:
            start_year = datetime.now().year - 5
        if not end_year:
            end_year = datetime.now().year
        
        endpoint = f"country/WLD/indicator/NY.GDP.MKTP.KD.ZG"
        params = {
            'date': f"{start_year}:{end_year}"
        }
        
        data = self._make_request(endpoint, params)
        
        if data:
            # Transform to simpler format
            result = []
            for item in data:
                if item.get('value') is not None:
                    result.append({
                        'year': int(item['date']),
                        'value': round(item['value'], 2),
                        'country': item.get('country', {}).get('value', 'World')
                    })
            
            logger.info(f"Fetched {len(result)} global GDP growth data points")
            return sorted(result, key=lambda x: x['year'])
        return []
    
    def get_regional_gdp_data(self, region_codes: List[str] = None) -> Dict[str, List[Dict]]:
        """
        Get GDP data for multiple regions.
        
        Default regions:
        - NAC: North America
        - EAS: East Asia & Pacific
        - ECS: Europe & Central Asia
        - LCN: Latin America & Caribbean
        - MEA: Middle East & North Africa
        - SAS: South Asia
        - SSF: Sub-Saharan Africa
        """
        if not region_codes:
            region_codes = ['NAC', 'EAS', 'ECS', 'LCN', 'MEA', 'SAS', 'SSF']
        
        result = {}
        current_year = datetime.now().year
        
        for region in region_codes:
            endpoint = f"country/{region}/indicator/NY.GDP.MKTP.KD.ZG"
            params = {
                'date': f"{current_year-5}:{current_year}"
            }
            
            data = self._make_request(endpoint, params)
            
            if data:
                region_data = []
                for item in data:
                    if item.get('value') is not None:
                        region_data.append({
                            'year': int(item['date']),
                            'value': round(item['value'], 2)
                        })
                result[region] = sorted(region_data, key=lambda x: x['year'])
                logger.info(f"Fetched GDP data for region {region}")
        
        return result
    
    def get_us_gdp_growth(self, start_year: int = None, end_year: int = None) -> List[Dict]:
        """
        Get United States GDP growth specifically.
        
        Country code: USA
        """
        if not start_year:
            start_year = datetime.now().year - 5
        if not end_year:
            end_year = datetime.now().year
        
        endpoint = f"country/USA/indicator/NY.GDP.MKTP.KD.ZG"
        params = {
            'date': f"{start_year}:{end_year}"
        }
        
        data = self._make_request(endpoint, params)
        
        if data:
            result = []
            for item in data:
                if item.get('value') is not None:
                    result.append({
                        'year': int(item['date']),
                        'value': round(item['value'], 2)
                    })
            
            logger.info(f"Fetched {len(result)} US GDP growth data points")
            return sorted(result, key=lambda x: x['year'])
        return []


# Singleton instance
world_bank_service = WorldBankService()
