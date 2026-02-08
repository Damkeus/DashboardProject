/**
 * TypeScript type definitions for NVIDIA Dashboard
 */

export interface KPIMetric {
    name: string;
    value: number | null;
    unit: string;
    trend: number | null;
    trend_direction: 'up' | 'down' | 'neutral';
}

export interface DashboardSummary {
    last_updated: string;
    kpis: KPIMetric[];
    latest_stock_price: number | null;
    market_cap: number | null;
}

export interface EconomicIndicator {
    date: string;
    global_gdp_growth: number | null;
    us_gdp_growth: number | null;
    federal_funds_rate: number | null;
    inflation_rate: number | null;
}

export interface StockData {
    date: string;
    open_price: number | null;
    close_price: number | null;
    high_price: number | null;
    low_price: number | null;
    volume: number | null;
    market_cap: number | null;
}

export interface UpdateResponse {
    status: 'success' | 'partial' | 'failed';
    message: string;
    duration: number | null;
    timestamp: string;
    details?: any;
}

export interface StatusResponse {
    last_update: string | null;
    scheduler_running: boolean;
    database_status: string;
    next_scheduled_update: string | null;
}

export interface TimeSeriesDataPoint {
    date: string;
    value: number | null;
}

export interface ChartDataPoint {
    date: string;
    [key: string]: any;
}

export type Period = '1M' | '3M' | '6M' | '1Y' | '2Y' | 'ALL';

export interface DateRangeOption {
    label: string;
    value: Period;
}
