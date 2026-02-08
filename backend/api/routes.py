"""FastAPI routes for NVIDIA Dashboard API."""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta, date
from typing import List, Optional
import logging

from database.database import get_db
from database.models import (
    EconomicIndicator,
    StockData,
    UpdateLog,
    NvidiaFinancial
)
from api.schemas import (
    DashboardSummary,
    KPIMetric,
    EconomicIndicatorSchema,
    StockDataSchema,
    UpdateRequest,
    UpdateResponse,
    StatusResponse,
    MetricHistoryRequest,
    MetricHistoryResponse,
    TimeSeriesDataPoint
)
from services.data_aggregator import data_aggregator
from services.stock_service import stock_service

logger = logging.getLogger(__name__)

router = APIRouter()

# Debounce tracking for manual updates
last_manual_update = None
UPDATE_COOLDOWN_SECONDS = 30


def calculate_trend(current: Optional[float], previous: Optional[float]) -> dict:
    """Calculate trend percentage and direction."""
    if current is None or previous is None:
        return {'trend': None, 'trend_direction': 'neutral'}
    
    if previous == 0:
        return {'trend': None, 'trend_direction': 'neutral'}
    
    trend_pct = ((current - previous) / previous) * 100
    direction = 'up' if trend_pct > 0 else 'down' if trend_pct < 0 else 'neutral'
    
    return {
        'trend': round(trend_pct, 2),
        'trend_direction': direction
    }


@router.get("/dashboard/summary", response_model=DashboardSummary)
async def get_dashboard_summary(db: Session = Depends(get_db)):
    """
    Get complete dashboard summary with all KPIs.
    
    Returns:
        Dashboard summary including all key metrics and trend indicators
    """
    try:
        # Get latest values for each metric separately (they come at different frequencies)
        
        # Helper to get latest non-null value
        def get_latest_value(field):
            result = db.query(EconomicIndicator).filter(
                field != None
            ).order_by(desc(EconomicIndicator.date)).first()
            return result
        
        # Get latest non-null GDP
        latest_gdp_record = get_latest_value(EconomicIndicator.global_gdp_growth)
        prev_gdp_record = db.query(EconomicIndicator).filter(
            EconomicIndicator.global_gdp_growth != None,
            EconomicIndicator.date < (latest_gdp_record.date if latest_gdp_record else datetime.now().date())
        ).order_by(desc(EconomicIndicator.date)).first() if latest_gdp_record else None
        
        # Get latest non-null Federal Funds Rate
        latest_fed_record = get_latest_value(EconomicIndicator.federal_funds_rate)
        prev_fed_record = db.query(EconomicIndicator).filter(
            EconomicIndicator.federal_funds_rate != None,
            EconomicIndicator.date < (latest_fed_record.date if latest_fed_record else datetime.now().date())
        ).order_by(desc(EconomicIndicator.date)).first() if latest_fed_record else None
        
        # Get latest non-null Inflation
        latest_inf_record = get_latest_value(EconomicIndicator.inflation_rate)
        prev_inf_record = db.query(EconomicIndicator).filter(
            EconomicIndicator.inflation_rate != None,
            EconomicIndicator.date < (latest_inf_record.date if latest_inf_record else datetime.now().date())
        ).order_by(desc(EconomicIndicator.date)).first() if latest_inf_record else None
        
        # Get latest stock data
        latest_stock = db.query(StockData).order_by(
            desc(StockData.date)
        ).first()
        
        previous_stock = db.query(StockData).order_by(
                **gdp_trend
            ))
        
        # 2. US Federal Interest Rate
        if latest_fed_record:
            rate_trend = calculate_trend(
                latest_fed_record.federal_funds_rate,
                prev_fed_record.federal_funds_rate if prev_fed_record else None
            )
            kpis.append(KPIMetric(
                name="Federal Funds Rate",
                value=latest_fed_record.federal_funds_rate,
                unit="%",
                **rate_trend
            ))
        
        # 3. Inflation Rate
        if latest_inf_record:
            inflation_trend = calculate_trend(
                latest_inf_record.inflation_rate,
                prev_inf_record.inflation_rate if prev_inf_record else None
            )
            kpis.append(KPIMetric(
                name="Inflation Rate",
                value=latest_inf_record.inflation_rate,
                unit="%",
                **inflation_trend
            ))
        
        # 4. NVIDIA Stock Price
        if latest_stock:
            price_trend = calculate_trend(
                latest_stock.close_price,
                previous_stock.close_price if previous_stock else None
            )
            kpis.append(KPIMetric(
                name="NVDA Stock Price",
                value=latest_stock.close_price,
                unit="$",
                **price_trend
            ))
            
            # 5. Market Cap
            market_cap_trend = calculate_trend(
                latest_stock.market_cap,
                previous_stock.market_cap if previous_stock else None
            )
            kpis.append(KPIMetric(
                name="Market Cap",
                value=latest_stock.market_cap,
                unit="$B",
                **market_cap_trend
            ))
        
        # Get last update timestamp
        last_update_log = db.query(UpdateLog).order_by(
            desc(UpdateLog.timestamp)
        ).first()
        
        last_updated = last_update_log.timestamp if last_update_log else datetime.utcnow()
        
        return DashboardSummary(
            last_updated=last_updated,
            kpis=kpis,
            latest_stock_price=latest_stock.close_price if latest_stock else None,
            market_cap=latest_stock.market_cap if latest_stock else None
        )
        
    except Exception as e:
        logger.error(f"Failed to generate dashboard summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/metrics/economic-indicators", response_model=List[EconomicIndicatorSchema])
async def get_economic_indicators(
    period: str = "1Y",
    db: Session = Depends(get_db)
):
    """Get historical economic indicators."""
    try:
        # Calculate start date based on period
        period_map = {
            '1M': 30,
            '3M': 90,
            '6M': 180,
            '1Y': 365,
            '2Y': 730,
            'ALL': 3650
        }
        
        days = period_map.get(period.upper(), 365)
        start_date = datetime.now().date() - timedelta(days=days)
        
        indicators = db.query(EconomicIndicator).filter(
            EconomicIndicator.date >= start_date
        ).order_by(EconomicIndicator.date).all()
        
        return indicators
        
    except Exception as e:
        logger.error(f"Failed to fetch economic indicators: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/stock-data", response_model=List[StockDataSchema])
async def get_stock_data(
    period: str = "1Y",
    db: Session = Depends(get_db)
):
    """Get historical NVIDIA stock data."""
    try:
        period_map = {
            '1M': 30,
            '3M': 90,
            '6M': 180,
            '1Y': 365,
            '2Y': 730,
            'ALL': 3650
        }
        
        days = period_map.get(period.upper(), 365)
        start_date = datetime.now().date() - timedelta(days=days)
        
        stock_data = db.query(StockData).filter(
            StockData.date >= start_date
        ).order_by(StockData.date).all()
        
        return stock_data
        
    except Exception as e:
        logger.error(f"Failed to fetch stock data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update", response_model=UpdateResponse)
async def trigger_manual_update(
    request: UpdateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Trigger manual data update.
    
    Includes 30-second cooldown to prevent spam.
    """
    global last_manual_update
    
    # Check cooldown
    if last_manual_update and not request.force:
        elapsed = (datetime.utcnow() - last_manual_update).total_seconds()
        if elapsed < UPDATE_COOLDOWN_SECONDS:
            raise HTTPException(
                status_code=429,
                detail=f"Please wait {int(UPDATE_COOLDOWN_SECONDS - elapsed)} seconds before updating again"
            )
    
    try:
        # Update timestamp
        last_manual_update = datetime.utcnow()
        
        # Run update
        result = data_aggregator.update_all_data(db, update_type='manual')
        
        return UpdateResponse(
            status=result['status'],
            message=f"Update completed with status: {result['status']}",
            duration=result['duration'],
            timestamp=datetime.fromisoformat(result['timestamp']),
            details=result['results']
        )
        
    except Exception as e:
        logger.error(f"Manual update failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=StatusResponse)
async def get_status(db: Session = Depends(get_db)):
    """Get system status and health check."""
    try:
        # Get last update
        last_update_log = db.query(UpdateLog).order_by(
            desc(UpdateLog.timestamp)
        ).first()
        
        # Check scheduler status (would need access to scheduler instance)
        # For now, always return True
        scheduler_running = True
        
        return StatusResponse(
            last_update=last_update_log.timestamp if last_update_log else None,
            scheduler_running=scheduler_running,
            database_status="connected",
            next_scheduled_update="9:00 AM daily"
        )
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return StatusResponse(
            last_update=None,
            scheduler_running=False,
            database_status="error",
            next_scheduled_update=None
        )


@router.get("/export/csv")
async def export_to_csv(db: Session = Depends(get_db)):
    """Export dashboard data to CSV format."""
    from fastapi.responses import StreamingResponse
    import io
    import csv
    
    try:
        # Get all data
        economic_data = db.query(EconomicIndicator).order_by(EconomicIndicator.date).all()
        stock_data = db.query(StockData).order_by(StockData.date).all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write economic indicators
        writer.writerow(['ECONOMIC INDICATORS'])
        writer.writerow(['Date', 'Global GDP Growth', 'US GDP Growth', 'Federal Funds Rate', 'Inflation Rate'])
        for item in economic_data:
            writer.writerow([
                item.date,
                item.global_gdp_growth,
                item.us_gdp_growth,
                item.federal_funds_rate,
                item.inflation_rate
            ])
        
        writer.writerow([])  # Empty row
        
        # Write stock data
        writer.writerow(['STOCK DATA'])
        writer.writerow(['Date', 'Open', 'Close', 'High', 'Low', 'Volume', 'Market Cap'])
        for item in stock_data:
            writer.writerow([
                item.date,
                item.open_price,
                item.close_price,
                item.high_price,
                item.low_price,
                item.volume,
                item.market_cap
            ])
        
        output.seek(0)
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=nvidia_dashboard_{datetime.now().strftime('%Y%m%d')}.csv"
            }
        )
        
    except Exception as e:
        logger.error(f"CSV export failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
