/**
 * API client for NVIDIA Dashboard backend
 */
import axios from 'axios';
import type {
    DashboardSummary,
    EconomicIndicator,
    StockData,
    UpdateResponse,
    StatusResponse,
    Period
} from '../types';

const api = axios.create({
    baseURL: '/api',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor for logging
api.interceptors.request.use(
    (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
    },
    (error) => {
        console.error('Request error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response) {
            // Server responded with error status
            console.error('API Error:', error.response.status, error.response.data);

            if (error.response.status === 429) {
                throw new Error('Too many requests. Please wait before trying again.');
            } else if (error.response.status === 500) {
                throw new Error('Server error. Please try again later.');
            }
        } else if (error.request) {
            // Request made but no response
            console.error('No response from server');
            throw new Error('Unable to connect to server. Please check your connection.');
        }

        return Promise.reject(error);
    }
);

/**
 * API service functions
 */
export const dashboardAPI = {
    /**
     * Get dashboard summary with all KPIs
     */
    getSummary: async (): Promise<DashboardSummary> => {
        const response = await api.get<DashboardSummary>('/dashboard/summary');
        return response.data;
    },

    /**
     * Get historical economic indicators
     */
    getEconomicIndicators: async (period: Period = '1Y'): Promise<EconomicIndicator[]> => {
        const response = await api.get<EconomicIndicator[]>('/metrics/economic-indicators', {
            params: { period }
        });
        return response.data;
    },

    /**
     * Get historical stock data
     */
    getStockData: async (period: Period = '1Y'): Promise<StockData[]> => {
        const response = await api.get<StockData[]>('/metrics/stock-data', {
            params: { period }
        });
        return response.data;
    },

    /**
     * Trigger manual data update
     */
    triggerUpdate: async (force: boolean = false): Promise<UpdateResponse> => {
        const response = await api.post<UpdateResponse>('/update', { force });
        return response.data;
    },

    /**
     * Get system status
     */
    getStatus: async (): Promise<StatusResponse> => {
        const response = await api.get<StatusResponse>('/status');
        return response.data;
    },

    /**
     * Export data to CSV
     */
    exportCSV: async (): Promise<Blob> => {
        const response = await api.get('/export/csv', {
            responseType: 'blob'
        });
        return response.data;
    },
};

export default api;
