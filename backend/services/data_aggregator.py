"""Data aggregator service to orchestrate all data collection and database updates."""
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Dict, List
import time

from database.models import (
    EconomicIndicator,
    NvidiaFinancial,
    SectorMetric,
    GeopoliticalIndex,
    StockData,
    UpdateLog
)
from services.fred_service import fred_service
from services.world_bank_service import world_bank_service
from services.stock_service import stock_service

logger = logging.getLogger(__name__)


class DataAggregator:
    """Orchestrates data collection from all sources and database updates."""
    
    def __init__(self):
        self.sources = {
            'fred': fred_service,
            'world_bank': world_bank_service,
            'stock': stock_service
        }
    
    def update_economic_indicators(self, db: Session) -> Dict[str, str]:
        """Update economic indicators from FRED and World Bank."""
        try:
            # Fetch FRED data
            fed_rates = fred_service.get_federal_funds_rate()
            gdp_data = fred_service.get_gdp_growth()
            cpi_data = fred_service.get_inflation_rate()
            inflation_data = fred_service.calculate_cpi_yoy_change(cpi_data)
            
            # Fetch World Bank data
            global_gdp = world_bank_service.get_global_gdp_growth()
            us_gdp = world_bank_service.get_us_gdp_growth()
            
            # Process and store FRED data (monthly/quarterly)
            updates_count = 0
            
            # Create a mapping of dates to combine data
            data_by_date = {}
            
            # Process federal funds rate
            for obs in fed_rates[-12:]:  # Last 12 months
                try:
                    date = datetime.strptime(obs['date'], '%Y-%m-%d').date()
                    value = float(obs['value'])
                    
                    if date not in data_by_date:
                        data_by_date[date] = {}
                    data_by_date[date]['federal_funds_rate'] = value
                except (ValueError, KeyError):
                    continue
            
            # Process inflation data
            for obs in inflation_data[-12:]:
                try:
                    date = datetime.strptime(obs['date'], '%Y-%m-%d').date()
                    value = float(obs['value'])
                    
                    if date not in data_by_date:
                        data_by_date[date] = {}
                    data_by_date[date]['inflation_rate'] = value
                except (ValueError, KeyError):
                    continue
            
            # Process GDP data (quarterly, use first day of quarter)
            for obs in gdp_data[-8:]:  # Last 8 quarters
                try:
                    date = datetime.strptime(obs['date'], '%Y-%m-%d').date()
                    value = float(obs['value'])
                    
                    if date not in data_by_date:
                        data_by_date[date] = {}
                    data_by_date[date]['us_gdp_growth'] = value
                except (ValueError, KeyError):
                    continue
            
            # Add global GDP (annual data) with forward fill
            # First, find the most recent GDP value from the fetched data
            latest_gdp_value = None
            if global_gdp:
                # Sort by year descending to get latest
                sorted_gdp = sorted(global_gdp, key=lambda x: x['year'], reverse=True)
                if sorted_gdp:
                    latest_gdp_value = float(sorted_gdp[0]['value'])
            
            # Add specific annual records
            for item in global_gdp[-5:]:  # Last 5 years
                try:
                    date = datetime(item['year'], 12, 31).date()
                    value = float(item['value'])
                    
                    if date not in data_by_date:
                        data_by_date[date] = {}
                    data_by_date[date]['global_gdp_growth'] = value
                except (ValueError, KeyError):
                    continue
            
            # Forward fill GDP to all other dates (so monthly charts show the line)
            if latest_gdp_value is not None:
                for date in data_by_date:
                    if 'global_gdp_growth' not in data_by_date[date]:
                        data_by_date[date]['global_gdp_growth'] = latest_gdp_value
            
            # Insert or update database records
            for date, values in data_by_date.items():
                existing = db.query(EconomicIndicator).filter(
                    EconomicIndicator.date == date
                ).first()
                
                if existing:
                    # Update existing record
                    for key, value in values.items():
                        setattr(existing, key, value)
                    existing.updated_at = datetime.utcnow()
                else:
                    # Create new record
                    indicator = EconomicIndicator(
                        date=date,
                        **values
                    )
                    db.add(indicator)
                
                updates_count += 1
            
            db.commit()
            logger.info(f"Updated {updates_count} economic indicator records")
            return {'status': 'success', 'count': updates_count}
            
        except Exception as e:
            logger.error(f"Failed to update economic indicators: {e}")
            db.rollback()
            return {'status': 'error', 'message': str(e)}
    
    def update_stock_data(self, db: Session) -> Dict[str, str]:
        """Update NVIDIA stock market data."""
        try:
            # Fetch last 90 days of stock data from Alpha Vantage
            stock_data = stock_service.get_historical_data(period="3mo")
            
            if not stock_data:
                logger.error("❌ Stock API failed - no data to update")
                return {'status': 'error', 'message': 'No stock data available from Alpha Vantage'}
            
            updates_count = 0
            shares_outstanding = 24.6  # billions (NVIDIA shares outstanding)
            
            for item in stock_data:
                try:
                    date = datetime.strptime(item['date'], '%Y-%m-%d').date()
                    
                    # Calculate market cap for THIS specific day using the closing price
                    market_cap = round(item['close'] * shares_outstanding, 2)
                    
                    existing = db.query(StockData).filter(
                        StockData.date == date
                    ).first()
                    
                    if existing:
                        # Update existing
                        existing.open_price = item['open']
                        existing.close_price = item['close']
                        existing.high_price = item['high']
                        existing.low_price = item['low']
                        existing.volume = item['volume']
                        existing.market_cap = market_cap
                        existing.updated_at = datetime.utcnow()
                    else:
                        # Create new
                        stock_record = StockData(
                            date=date,
                            open_price=item['open'],
                            close_price=item['close'],
                            high_price=item['high'],
                            low_price=item['low'],
                            volume=item['volume'],
                            market_cap=market_cap
                        )
                        db.add(stock_record)
                    
                    updates_count += 1
                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping invalid stock data: {e}")
                    continue
            
            db.commit()
            logger.info(f"Updated {updates_count} stock data records")
            return {'status': 'success', 'count': updates_count}
            
        except Exception as e:
            logger.error(f"Failed to update stock data: {e}")
            db.rollback()
            return {'status': 'error', 'message': str(e)}
    

    
    def update_all_data(self, db: Session, update_type: str = 'automatic') -> Dict:
        """
        Execute full data update from all sources.
        
        Args:
            db: Database session
            update_type: 'automatic' or 'manual'
            
        Returns:
            Summary of update results
        """
        start_time = time.time()
        results = {
            'economic_indicators': None,
            'stock_data': None,
            'errors': []
        }
        
        logger.info(f"Starting {update_type} data update")
        
        # Update economic indicators
        try:
            results['economic_indicators'] = self.update_economic_indicators(db)
        except Exception as e:
            results['errors'].append(f"Economic indicators: {str(e)}")
            logger.error(f"Economic indicators update failed: {e}")
        
        # Update stock data
        try:
            results['stock_data'] = self.update_stock_data(db)
        except Exception as e:
            results['errors'].append(f"Stock data: {str(e)}")
            logger.error(f"Stock data update failed: {e}")
        
        # Determine overall status
        if results['errors']:
            status = 'partial' if any(r and r.get('status') == 'success' for r in results.values() if isinstance(r, dict)) else 'failed'
        else:
            status = 'success'
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log the update
        update_log = UpdateLog(
            timestamp=datetime.utcnow(),
            update_type=update_type,
            status=status,
            sources_updated=str(results),
            errors=str(results['errors']) if results['errors'] else None,
            duration_seconds=round(duration, 2)
        )
        db.add(update_log)
        db.commit()
        
        logger.info(f"Update completed with status: {status} in {duration:.2f}s")
        
        return {
            'status': status,
            'duration': duration,
            'results': results,
            'timestamp': datetime.utcnow().isoformat()
        }


# Singleton instance
data_aggregator = DataAggregator()
