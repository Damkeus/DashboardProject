/**
 * Economic indicators chart (GDP & Interest Rates)
 */
import { useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { useDashboardStore } from '../../store/dashboardStore';
import LoadingSkeleton from '../LoadingSkeleton';
import { format } from 'date-fns';

export default function EconomicIndicatorsChart() {
    const { economicIndicators, loading } = useDashboardStore();

    const chartData = useMemo(() => {
        return economicIndicators
            .filter(item => item.global_gdp_growth !== null || item.federal_funds_rate !== null)
            .map(item => ({
                date: format(new Date(item.date), 'MMM yy'),
                gdp: item.global_gdp_growth,
                rate: item.federal_funds_rate,
                inflation: item.inflation_rate,
            }));
    }, [economicIndicators]);

    if (loading && economicIndicators.length === 0) {
        return <LoadingSkeleton />;
    }

    return (
        <div className="glass-card p-6">
            <h2 className="text-xl font-bold text-white mb-4">Economic Indicators</h2>

            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis
                        dataKey="date"
                        stroke="#E0E0E0"
                        tick={{ fill: '#E0E0E0', fontSize: 12 }}
                    />
                    <YAxis
                        yAxisId="left"
                        stroke="#E0E0E0"
                        tick={{ fill: '#E0E0E0', fontSize: 12 }}
                        label={{ value: 'GDP Growth (%)', angle: -90, position: 'insideLeft', fill: '#76B900' }}
                    />
                    <YAxis
                        yAxisId="right"
                        orientation="right"
                        stroke="#E0E0E0"
                        tick={{ fill: '#E0E0E0', fontSize: 12 }}
                        label={{ value: 'Interest Rate (%)', angle: 90, position: 'insideRight', fill: '#0066cc' }}
                    />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#1A1A1A',
                            border: '1px solid #333',
                            borderRadius: '8px',
                            color: '#E0E0E0'
                        }}
                        formatter={(value: number) => [value?.toFixed(2) + '%', '']}
                    />
                    <Legend wrapperStyle={{ color: '#E0E0E0' }} />
                    <Line
                        yAxisId="left"
                        type="monotone"
                        dataKey="gdp"
                        stroke="#76B900"
                        strokeWidth={2}
                        dot={{ fill: '#76B900', r: 3 }}
                        name="Global GDP Growth"
                    />
                    <Line
                        yAxisId="right"
                        type="monotone"
                        dataKey="rate"
                        stroke="#0066cc"
                        strokeWidth={2}
                        dot={{ fill: '#0066cc', r: 3 }}
                        name="Federal Funds Rate"
                    />
                    <Line
                        yAxisId="left"
                        type="monotone"
                        dataKey="inflation"
                        stroke="#ff6b6b"
                        strokeWidth={1.5}
                        strokeDasharray="5 5"
                        dot={false}
                        name="Inflation Rate"
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
