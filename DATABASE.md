# Database Documentation

## 📊 Database Overview

**Type**: SQLite (Single file database)  
**Location**: `c:\Users\dmercure\Projets\DashboardNvidia\backend\nvidia_dashboard.db`  
**Created**: Automatically on first server start  
**ORM**: SQLAlchemy

## 🗄️ Database Tables

### 1. **economic_indicators**
Stores global economic data from FRED and World Bank APIs.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| date | Date | Data date |
| global_gdp_growth | Float | Global GDP growth % |
| us_gdp_growth | Float | US GDP growth % |
| federal_funds_rate | Float | Federal interest rate % |
| inflation_rate | Float | CPI inflation rate % |
| created_at | DateTime | Record creation time |
| updated_at | DateTime | Last update time |

**Used by**: `/api/metrics/economic-indicators` endpoint

---

### 2. **stock_data**
NVIDIA stock market data from Yahoo Finance (yfinance library).

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| date | Date | Trading date |
| open_price | Float | Opening price |
| close_price | Float | Closing price |
| high_price | Float | Daily high |
| low_price | Float | Daily low |
| volume | Integer | Trading volume |
| market_cap | Float | Market cap in billions |
| created_at | DateTime | Record creation time |
| updated_at | DateTime | Last update time |

**Used by**: `/api/metrics/stock-data` and dashboard summary

---

### 3. **nvidia_financials**
Quarterly financial data for NVIDIA (manual entry or API).

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| quarter | String | Q1, Q2, Q3, Q4 |
| year | Integer | Fiscal year |
| fiscal_period | String | e.g., "2024-Q1" (unique) |
| data_center_revenue | Float | Data center revenue ($M) |
| gaming_revenue | Float | Gaming revenue ($M) |
| professional_visualization_revenue | Float | Pro viz revenue ($M) |
| automotive_revenue | Float | Auto revenue ($M) |
| total_revenue | Float | Total revenue ($M) |
| gross_margin | Float | Gross margin % |
| operating_income | Float | Operating income ($M) |
| net_income | Float | Net income ($M) |
| earnings_per_share | Float | EPS |

**Note**: Currently empty - needs manual population or scraper

---

### 4. **sector_metrics**
AI/GPU market demand and competitor data.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| date | Date | Data date |
| ai_market_demand_index | Float | Custom AI demand index (0-100) |
| gpu_market_size | Float | GPU market size ($B) |
| amd_market_share | Float | AMD market share % |
| intel_market_share | Float | Intel market share % |
| nvidia_market_share | Float | NVIDIA market share % |

**Note**: Currently using placeholder data

---

### 5. **geopolitical_indices**
Geopolitical risk tracking.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| date | Date | Data date |
| overall_risk_score | Float | Overall risk (0-100) |
| us_china_tension_score | Float | US-China tensions (0-100) |
| supply_chain_risk_score | Float | Supply chain risk (0-100) |
| regulatory_risk_score | Float | Regulatory risk (0-100) |
| events_summary | Text | Brief event description |

**Note**: Currently using placeholder data

---

### 6. **update_logs**
Audit trail of all data updates.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| timestamp | DateTime | Update time |
| update_type | String | 'automatic' or 'manual' |
| status | String | 'success', 'partial', 'failed' |
| sources_updated | Text | JSON string of updated sources |
| errors | Text | JSON string of errors (if any) |
| duration_seconds | Float | Update duration |

**Used by**: `/api/status` endpoint

---

## 🔧 How It Works

### Automatic Creation
When you run `python main.py`, this happens:

1. **main.py** calls `init_db()` on startup
2. **database/database.py** creates SQLite connection
3. **database/models.py** defines table schemas
4. SQLAlchemy creates all tables if they don't exist

### Data Flow

```
API Services → Data Aggregator → Database → API Routes → Frontend
    ↓              ↓                ↓            ↓           ↓
  FRED          Combines         SQLite      Query DB    Display
World Bank      & Saves          Tables      Return       Charts
 yfinance                                    JSON
```

### Example SQL Operations

**Inserting Data** (from `data_aggregator.py`):
```python
indicator = EconomicIndicator(
    date=date,
    global_gdp_growth=2.8,
    federal_funds_rate=5.5
)
db.add(indicator)
db.commit()
```

**Querying Data** (from `routes.py`):
```python
latest = db.query(EconomicIndicator).order_by(
    desc(EconomicIndicator.date)
).first()
```

---

## 🔍 Viewing the Database

### Method 1: SQLite Browser
1. Download [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Open `nvidia_dashboard.db`
3. View all tables and data

### Method 2: Python Script
```python
import sqlite3
conn = sqlite3.connect('nvidia_dashboard.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM economic_indicators LIMIT 5")
for row in cursor.fetchall():
    print(row)
```

### Method 3: API Endpoints
- View via Swagger: http://localhost:8000/docs
- Direct query: http://localhost:8000/api/dashboard/summary

---

## 📝 Current Status

✅ **Tables Created**: All 6 tables exist  
✅ **Economic Data**: Being populated from FRED/World Bank  
✅ **Stock Data**: Being populated from yfinance  
⚠️ **NVIDIA Financials**: Empty (needs manual entry)  
⚠️ **Sector Metrics**: Placeholder data  
⚠️ **Geopolitical Index**: Placeholder data  

---

## 🚀 Next Steps for Full Data

To populate all tables with real data:

1. **Trigger first update** (if not done):
   ```powershell
   Invoke-WebRequest -Uri http://localhost:8000/api/update -Method POST
   ```

2. **Add NVIDIA quarterly data** manually or via scraper

3. **Implement sector metrics** collection from industry reports

4. **Add geopolitical tracking** from news APIs
