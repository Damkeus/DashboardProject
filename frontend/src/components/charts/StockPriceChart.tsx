/**
 * Stock price chart component using Recharts
 */
import { useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { useDashboardStore } from '../../store/dashboardStore';
import LoadingSkeleton from '../LoadingSkeleton';
import { format } from 'date-fns';

export default function StockPriceChart() {
    const { stockData, loading } = useDashboardStore();

    const chartData = useMemo(() => {
        return stockData.map(item => ({
            date: format(new Date(item.date), 'MMM d'),
            price: item.close_price,
            high: item.high_price,
            low: item.low_price,
        }));
    }, [stockData]);

    if (loading && stockData.length === 0) {
        return <LoadingSkeleton />;
    }

    return (
        <div className="glass-card p-6">
            <h2 className="text-xl font-bold text-white mb-4">NVDA Stock Price</h2>

            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis
                        dataKey="date"
                        stroke="#E0E0E0"
                        tick={{ fill: '#E0E0E0', fontSize: 12 }}
                    />
                    <YAxis
                        stroke="#E0E0E0"
                        tick={{ fill: '#E0E0E0', fontSize: 12 }}
                        domain={['auto', 'auto']}
                    />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#1A1A1A',
                            border: '1px solid #333',
                            borderRadius: '8px',
                            color: '#E0E0E0'
                        }}
                        formatter={(value: number) => ['$' + value.toFixed(2), 'Price']}
                    />
                    <Legend
                        wrapperStyle={{ color: '#E0E0E0' }}
                    />
                    <Line
                        type="monotone"
                        dataKey="price"
                        stroke="#76B900"
                        strokeWidth={2}
                        dot={false}
                        name="Close Price"
                    />
                    <Line
                        type="monotone"
                        dataKey="high"
                        stroke="#a0e000"
                        strokeWidth={1}
                        strokeDasharray="5 5"
                        dot={false}
                        name="High"
                    />
                    <Line
                        type="monotone"
                        dataKey="low"
                        stroke="#5a8700"
                        strokeWidth={1}
                        strokeDasharray="5 5"
                        dot={false}
                        name="Low"
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
