"""SQLAlchemy ORM models for NVIDIA Dashboard."""
from sqlalchemy import Column, Integer, Float, String, Date, DateTime, Text, func
from database.database import Base
from datetime import datetime


class EconomicIndicator(Base):
    """Global economic indicators affecting NVIDIA."""
    __tablename__ = "economic_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False, index=True)
    
    # GDP metrics
    global_gdp_growth = Column(Float)  # Percentage
    us_gdp_growth = Column(Float)      # Percentage
    
    # Interest rates and inflation
    federal_funds_rate = Column(Float)  # Percentage
    inflation_rate = Column(Float)      # CPI year-over-year %
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<EconomicIndicator(date={self.date}, gdp={self.global_gdp_growth}%)>"


class NvidiaFinancial(Base):
    """NVIDIA quarterly financial performance."""
    __tablename__ = "nvidia_financials"
    
    id = Column(Integer, primary_key=True, index=True)
    quarter = Column(String(2), nullable=False)  # Q1, Q2, Q3, Q4
    year = Column(Integer, nullable=False)
    fiscal_period = Column(String(10), unique=True, index=True)  # e.g., "2024-Q1"
    
    # Revenue breakdown (in millions USD)
    data_center_revenue = Column(Float)
    gaming_revenue = Column(Float)
    professional_visualization_revenue = Column(Float)
    automotive_revenue = Column(Float)
    total_revenue = Column(Float)
    
    # Profitability
    gross_margin = Column(Float)  # Percentage
    operating_income = Column(Float)
    net_income = Column(Float)
    earnings_per_share = Column(Float)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<NvidiaFinancial({self.fiscal_period}, revenue=${self.total_revenue}M)>"


class SectorMetric(Base):
    """AI/GPU sector market metrics."""
    __tablename__ = "sector_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False, index=True)
    
    # Market demand indicators
    ai_market_demand_index = Column(Float)  # Custom index (0-100)
    gpu_market_size = Column(Float)         # In billions USD
    
    # Competitor data
    amd_market_share = Column(Float)        # Percentage
    intel_market_share = Column(Float)      # Percentage
    nvidia_market_share = Column(Float)     # Percentage
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<SectorMetric(date={self.date}, ai_index={self.ai_market_demand_index})>"


class GeopoliticalIndex(Base):
    """Geopolitical risk factors affecting NVIDIA."""
    __tablename__ = "geopolitical_indices"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False, index=True)
    
    # Risk scores (0-100, higher = more risk)
    overall_risk_score = Column(Float)
    us_china_tension_score = Column(Float)
    supply_chain_risk_score = Column(Float)
    regulatory_risk_score = Column(Float)
    
    # Event summary
    events_summary = Column(Text)  # Brief description of key events
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<GeopoliticalIndex(date={self.date}, risk={self.overall_risk_score})>"


class StockData(Base):
    """NVIDIA stock market data."""
    __tablename__ = "stock_data"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False, index=True)
    
    # Price data
    open_price = Column(Float)
    close_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    
    # Volume and market cap
    volume = Column(Integer)
    market_cap = Column(Float)  # In billions USD
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<StockData(date={self.date}, close=${self.close_price})>"


class UpdateLog(Base):
    """Log of automated and manual data updates."""
    __tablename__ = "update_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_type = Column(String(20))  # 'automatic' or 'manual'
    status = Column(String(20))       # 'success', 'partial', 'failed'
    
    # Detailed results
    sources_updated = Column(Text)     # JSON string of updated sources
    errors = Column(Text)              # JSON string of errors if any
    duration_seconds = Column(Float)   # How long the update took
    
    def __repr__(self):
        return f"<UpdateLog({self.timestamp}, {self.status})>"
