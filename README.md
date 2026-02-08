Tutoriel en français pour les nuls:
1. Télécharger le repo ( dossier
2. Aller dans votre terminal : cd Project, installer python et node (pip install -r requirements.txt=
3. activate env :DashboardNvidia/venv/Scripts/Activate.ps1
4. cd backend puis python main.py
5. cd..
6. Cd frontend npm run dev

7. Entrer: Localhost:5153 dans votre moteur de recherche si le projet ne s'est pas lancé seul





# NVIDIA Economic Dashboard

A professional, real-time economic dashboard for NVIDIA analysis with automatic daily updates, interactive visualizations, and a polished UI reflecting NVIDIA's brand identity.

![NVIDIA Dashboard](https://via.placeholder.com/1200x600/000000/76B900?text=NVIDIA+Economic+Dashboard)

## Features

- **Real-time Data Collection** from FRED, World Bank, and Yahoo Finance
- **Automated Daily Updates** at 9 AM (configurable)
- **Interactive Visualizations** with Recharts
- **5 Key Economic Metrics**:
  - Global GDP Growth
  - US Federal Interest Rates
  - NVDA Stock Price
  - Market Capitalization
  - Inflation Rate
- **Premium UI** with glassmorphism effects and NVIDIA branding
- **Smooth Animations** powered by Framer Motion
- **Data Export** to CSV
- **Responsive Design** for all devices

##  Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database
- **APScheduler** - Automated task scheduling
- **yfinance** - Stock market data
- **Requests** - HTTP client for API calls

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization
- **Framer Motion** - Animations
- **Zustand** - State management
- **Axios** - HTTP client

##  Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env and add your API keys
# FRED_API_KEY=your_key_here
# ALPHA_VANTAGE_API_KEY=your_key_here

# Run the server
python main.py
```

The backend will start on **http://localhost:8000**

API documentation available at: **http://localhost:8000/docs**

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on **http://localhost:5173**

##  Configuration

### Environment Variables (.env)

```env
# API Keys
FRED_API_KEY=your_fred_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key

# Database
DATABASE_URL=sqlite:///./nvidia_dashboard.db

# Scheduler (24-hour format)
UPDATE_SCHEDULE_HOUR=9
UPDATE_SCHEDULE_MINUTE=0
UPDATE_SCHEDULE_TIMEZONE=America/New_York

# Application
ENVIRONMENT=development
DEBUG=True
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Getting API Keys

1. **FRED API**: Register at https://fred.stlouisfed.org/docs/api/api_key.html
2. **Alpha Vantage**: Get free key at https://www.alphavantage.co/support/#api-key

##  Usage

### Automatic Updates
The system automatically fetches new data daily at 9:00 AM (configurable in `.env`).

### Manual Refresh
Click the refresh button in the dashboard header to manually trigger a data update.

### Date Range Selection
Use the period selector (1M, 3M, 6M, 1Y, 2Y, ALL) to adjust the time range for charts.

### Export Data
Click the download button to export all data to CSV format.

## API Endpoints

- `GET /api/dashboard/summary` - Get all KPIs and latest metrics
- `GET /api/metrics/economic-indicators?period=1Y` - Historical economic data
- `GET /api/metrics/stock-data?period=1Y` - Historical stock prices
- `POST /api/update` - Trigger manual data update
- `GET /api/status` - System health check
- `GET /api/export/csv` - Export data to CSV

##  Project Structure

```
DashboardNvidia/
├── backend/
│   ├── api/
│   │   ├── routes.py          # API endpoints
│   │   └── schemas.py         # Pydantic models
│   ├── database/
│   │   ├── database.py        # DB connection
│   │   └── models.py          # SQLAlchemy models
│   ├── services/
│   │   ├── fred_service.py    # FRED API integration
│   │   ├── world_bank_service.py
│   │   ├── stock_service.py   # Stock data (yfinance)
│   │   └── data_aggregator.py # Data orchestration
│   ├── config.py              # Configuration
│   ├── scheduler.py           # APScheduler setup
│   ├── main.py                # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── KPICard.tsx
│   │   │   ├── Toast.tsx
│   │   │   └── charts/
│   │   ├── store/
│   │   │   └── dashboardStore.ts  # Zustand store
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── utils/
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

##  Design System

### Colors
- **Primary**: NVIDIA Green (#76B900)
- **Background**: Black (#000000), Dark Gray (#1A1A1A)
- **Text**: White (#FFFFFF), Light Gray (#E0E0E0)

### Typography
- **Font**: Inter (Google Fonts)

### Components
- Glassmorphism cards with backdrop blur
- Smooth hover effects and transitions
- Custom scrollbars
- Loading skeletons with shimmer effect

### Manual Deployment

1. run frontend:
```bash
cd frontend
npm run dev
```
2. Run backend with production settings:
```bash
cd backend
ENVIRONMENT=production uvicorn main:app --host 0.0.0.0 --port 8000
DashboardNvidia/venv/Scripts/Activate.ps1
cd backend
python main.py
```
3. go on localhost:5173 and enjpy

##  Data Sources

- **FRED** (Federal Reserve Economic Data) - GDP, Interest Rates, Inflation
- **World Bank** - Global GDP Growth
- **Yahoo Finance** (via yfinance/alpha vantage) - NVIDIA Stock Data


##  Ressources

- NVIDIA for brand inspiration
- FRED, World Bank, and Yahoo Finance for data APIs

---
