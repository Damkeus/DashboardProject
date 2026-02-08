"""Pydantic schemas for API request/response validation."""
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List, Dict


class EconomicIndicatorSchema(BaseModel):
    """Schema for economic indicator response."""
    date: date
    global_gdp_growth: Optional[float] = None
    us_gdp_growth: Optional[float] = None
    federal_funds_rate: Optional[float] = None
    inflation_rate: Optional[float] = None
    
    class Config:
        from_attributes = True


class StockDataSchema(BaseModel):
    """Schema for stock data response."""
    date: date
    open_price: Optional[float] = None
    close_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    volume: Optional[int] = None
    market_cap: Optional[float] = None
    
    class Config:
        from_attributes = True


class KPIMetric(BaseModel):
    """Single KPI metric for dashboard."""
    name: str
    value: Optional[float]
    unit: str  # '%', '$B', etc.
    trend: Optional[float] = None  # Percentage change
    trend_direction: Optional[str] = None  # 'up', 'down', 'neutral'


class DashboardSummary(BaseModel):
    """Complete dashboard summary response."""
    last_updated: datetime
    kpis: List[KPIMetric]
    latest_stock_price: Optional[float]
    market_cap: Optional[float]
    
    class Config:
        from_attributes = True


class UpdateRequest(BaseModel):
    """Request to trigger manual update."""
    force: bool = Field(default=False, description="Force update even if recently updated")


class UpdateResponse(BaseModel):
    """Response from update operation."""
    status: str  # 'success', 'partial', 'failed'
    message: str
    duration: Optional[float] = None
    timestamp: datetime
    details: Optional[Dict] = None


class StatusResponse(BaseModel):
    """System status response."""
    last_update: Optional[datetime]
    scheduler_running: bool
    database_status: str
    next_scheduled_update: Optional[str] = None


class MetricHistoryRequest(BaseModel):
    """Request for historical metric data."""
    metric_name: str
    period: str = Field(default="1Y", description="1M, 3M, 6M, 1Y, 2Y, ALL")


class TimeSeriesDataPoint(BaseModel):
    """Single time series data point."""
    date: date
    value: Optional[float]


class MetricHistoryResponse(BaseModel):
    """Historical metric data response."""
    metric_name: str
    data: List[TimeSeriesDataPoint]
    period: str
