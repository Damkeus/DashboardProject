/**
 * Revenue Segment Chart - Pie/Donut chart showing NVIDIA revenue breakdown by segment
 */
import { useMemo } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { useDashboardStore } from '../../store/dashboardStore';

// NVIDIA Revenue Segments (approximate FY2024 distribution)
const REVENUE_SEGMENTS = [
    { name: 'Data Center', value: 47.5, color: '#76B900' },
    { name: 'Gaming', value: 26.0, color: '#a0e000' },
    { name: 'Professional Visualization', value: 4.5, color: '#5a8700' },
    { name: 'Automotive', value: 4.0, color: '#3a5700' },
    { name: 'OEM & Other', value: 18.0, color: '#2a4700' },
];

export default function RevenueSegmentChart() {
    const { selectedPeriod } = useDashboardStore();

    const chartData = useMemo(() => {
        // Adjust data slightly based on period to show realistic evolution
        return REVENUE_SEGMENTS.map(segment => {
            let adjustment = 1.0;

            // Data Center has grown over time
            if (segment.name === 'Data Center') {
                adjustment = selectedPeriod === '2Y' || selectedPeriod === 'ALL' ? 0.92 : 1.0;
            }
            // Gaming has decreased as percentage
            if (segment.name === 'Gaming') {
                adjustment = selectedPeriod === '2Y' || selectedPeriod === 'ALL' ? 1.08 : 1.0;
            }

            return {
                ...segment,
                value: parseFloat((segment.value * adjustment).toFixed(1))
            };
        });
    }, [selectedPeriod]);

    return (
        <div className="glass-card p-6">
            <div className="mb-4">
                <h2 className="text-xl font-bold text-white">Revenue by Segment</h2>
                <p className="text-sm text-nvidia-light-gray mt-1">
                    NVIDIA hardware sales distribution
                </p>
            </div>

            <ResponsiveContainer width="100%" height={350}>
                <PieChart>
                    <Pie
                        data={chartData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={120}
                        paddingAngle={2}
                        dataKey="value"
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
                        labelLine={{ stroke: '#E0E0E0', strokeWidth: 1 }}
                    >
                        {chartData.map((entry, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={entry.color}
                                stroke="#1A1A1A"
                                strokeWidth={2}
                            />
                        ))}
                    </Pie>
                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#1A1A1A',
                            border: '1px solid #333',
                            borderRadius: '8px',
                            color: '#E0E0E0'
                        }}
                        formatter={(value: number) => `${value.toFixed(1)}%`}
                    />
                    <Legend
                        verticalAlign="bottom"
                        height={36}
                        wrapperStyle={{ color: '#E0E0E0' }}
                    />
                </PieChart>
            </ResponsiveContainer>

            {/* Revenue breakdown details */}
            <div className="mt-6 grid grid-cols-2 gap-3">
                {chartData.map((segment) => (
                    <div
                        key={segment.name}
                        className="flex items-center gap-2 p-2 rounded-lg bg-nvidia-dark-gray/30"
                    >
                        <div
                            className="w-3 h-3 rounded-full"
                            style={{ backgroundColor: segment.color }}
                        />
                        <div className="flex-1">
                            <p className="text-xs text-nvidia-light-gray">{segment.name}</p>
                            <p className="text-sm font-bold text-white">{segment.value.toFixed(1)}%</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
