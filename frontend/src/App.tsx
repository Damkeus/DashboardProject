/**
 * Main App component - NVIDIA Economic Dashboard
 */
import { useEffect } from 'react';
import { motion } from 'framer-motion';
import Header from './components/Header';
import KPICard from './components/KPICard';
import Toast from './components/Toast';
import DateRangeSelector from './components/DateRangeSelector';
import StockPriceChart from './components/charts/StockPriceChart';
import EconomicIndicatorsChart from './components/charts/EconomicIndicatorsChart';
import GeographicMap from './components/charts/GeographicMap';
import RevenueSegmentChart from './components/charts/RevenueSegmentChart';
import { KPISkeletonGrid } from './components/LoadingSkeleton';
import { useDashboardStore } from './store/dashboardStore';
import './index.css';

function App() {
  const { summary, loading, fetchAllData } = useDashboardStore();

  // Fetch data on mount
  useEffect(() => {
    fetchAllData();
  }, [fetchAllData]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-nvidia-black via-nvidia-black to-nvidia-dark-gray p-6 custom-scrollbar overflow-x-hidden">
      {/* Animated background particles */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-72 h-72 bg-nvidia-green/5 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-nvidia-green/3 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header */}
        <Header />

        {/* Toast Notifications */}
        <Toast />

        {/* KPI Cards */}
        {loading && !summary ? (
          <KPISkeletonGrid />
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-8"
          >
            {summary?.kpis.map((kpi, index) => (
              <KPICard key={kpi.name} metric={kpi} index={index} />
            ))}
          </motion.div>
        )}

        {/* Date Range Selector */}
        <div className="mb-6">
          <DateRangeSelector />
        </div>

        {/* Charts Grid */}
        <div className="space-y-6">
          {/* Row 1: Stock Price + Economic Indicators */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <StockPriceChart />
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <EconomicIndicatorsChart />
            </motion.div>
          </div>

          {/* Row 2: Geographic Map + Revenue Segments */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              <GeographicMap />
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              <RevenueSegmentChart />
            </motion.div>
          </div>
        </div>

        {/* Footer */}
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="text-center text-sm text-nvidia-light-gray/40 mt-12 pb-4"
        >
          <div className="backdrop-blur-sm bg-nvidia-dark-gray/30 rounded-xl py-4 px-6 border border-nvidia-green/10">
            <p>
              Data sources: <span className="text-nvidia-green/70">FRED</span> · <span className="text-nvidia-green/70">World Bank</span> · <span className="text-nvidia-green/70">Yahoo Finance</span>
            </p>
            <p className="mt-2">
              <span className="text-nvidia-green font-semibold">NVIDIA</span> Economic Dashboard © 2026
            </p>
          </div>
        </motion.footer>
      </div>
    </div>
  );
}

export default App;

