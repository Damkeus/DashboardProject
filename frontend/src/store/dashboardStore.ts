/**
 * Zustand store for dashboard state management
 */
import { create } from 'zustand';
import type {
    DashboardSummary,
    EconomicIndicator,
    StockData,
    Period,
    StatusResponse
} from '../types';
import { dashboardAPI } from '../utils/api';

interface DashboardState {
    // Data
    summary: DashboardSummary | null;
    economicIndicators: EconomicIndicator[];
    stockData: StockData[];
    status: StatusResponse | null;

    // UI State
    loading: boolean;
    error: string | null;
    selectedPeriod: Period;
    lastFetch: Date | null;
    isUpdating: boolean;
    updateMessage: string | null;

    // Actions
    fetchSummary: () => Promise<void>;
    fetchEconomicIndicators: (period: Period) => Promise<void>;
    fetchStockData: (period: Period) => Promise<void>;
    fetchStatus: () => Promise<void>;
    fetchAllData: () => Promise<void>;
    triggerManualUpdate: () => Promise<void>;
    setPeriod: (period: Period) => void;
    exportData: () => Promise<void>;
    clearError: () => void;
}

export const useDashboardStore = create<DashboardState>((set, get) => ({
    // Initial state
    summary: null,
    economicIndicators: [],
    stockData: [],
    status: null,
    loading: false,
    error: null,
    selectedPeriod: '1Y',
    lastFetch: null,
    isUpdating: false,
    updateMessage: null,

    // Fetch dashboard summary
    fetchSummary: async () => {
        set({ loading: true, error: null });
        try {
            const summary = await dashboardAPI.getSummary();
            set({ summary, loading: false, lastFetch: new Date() });
        } catch (error) {
            set({
                error: error instanceof Error ? error.message : 'Failed to fetch dashboard summary',
                loading: false
            });
        }
    },

    // Fetch economic indicators
    fetchEconomicIndicators: async (period: Period) => {
        set({ loading: true, error: null });
        try {
            const indicators = await dashboardAPI.getEconomicIndicators(period);
            set({ economicIndicators: indicators, loading: false });
        } catch (error) {
            set({
                error: error instanceof Error ? error.message : 'Failed to fetch economic indicators',
                loading: false
            });
        }
    },

    // Fetch stock data
    fetchStockData: async (period: Period) => {
        set({ loading: true, error: null });
        try {
            const stockData = await dashboardAPI.getStockData(period);
            set({ stockData, loading: false });
        } catch (error) {
            set({
                error: error instanceof Error ? error.message : 'Failed to fetch stock data',
                loading: false
            });
        }
    },

    // Fetch system status
    fetchStatus: async () => {
        try {
            const status = await dashboardAPI.getStatus();
            set({ status });
        } catch (error) {
            console.error('Failed to fetch status:', error);
        }
    },

    // Fetch all data
    fetchAllData: async () => {
        const period = get().selectedPeriod;
        set({ loading: true, error: null });

        try {
            await Promise.all([
                get().fetchSummary(),
                get().fetchEconomicIndicators(period),
                get().fetchStockData(period),
                get().fetchStatus(),
            ]);

            set({ loading: false, lastFetch: new Date() });
        } catch (error) {
            set({
                error: error instanceof Error ? error.message : 'Failed to fetch data',
                loading: false
            });
        }
    },

    // Trigger manual update
    triggerManualUpdate: async () => {
        set({ isUpdating: true, updateMessage: null, error: null });

        try {
            const result = await dashboardAPI.triggerUpdate(false);

            set({
                updateMessage: result.message,
                isUpdating: false
            });

            // Refresh data after update
            setTimeout(() => {
                get().fetchAllData();
            }, 1000);

            // Clear message after 5 seconds
            setTimeout(() => {
                set({ updateMessage: null });
            }, 5000);

        } catch (error) {
            set({
                error: error instanceof Error ? error.message : 'Update failed',
                isUpdating: false
            });
        }
    },

    // Set selected period
    setPeriod: (period: Period) => {
        set({ selectedPeriod: period });
        // Refetch data with new period
        get().fetchEconomicIndicators(period);
        get().fetchStockData(period);
    },

    // Export data to CSV
    exportData: async () => {
        try {
            const blob = await dashboardAPI.exportCSV();

            // Create download link
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `nvidia_dashboard_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);

            set({ updateMessage: 'Data exported successfully!' });
            setTimeout(() => set({ updateMessage: null }), 3000);
        } catch (error) {
            set({
                error: error instanceof Error ? error.message : 'Export failed'
            });
        }
    },

    // Clear error
    clearError: () => set({ error: null }),
}));
