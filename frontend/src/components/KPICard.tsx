/**
 * KPI Card component with trend indicator
 */
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import type { KPIMetric } from '../types';

interface KPICardProps {
    metric: KPIMetric;
    index: number;
}

export default function KPICard({ metric, index }: KPICardProps) {
    const { name, value, unit, trend, trend_direction } = metric;

    // Format value based on unit
    const formatValue = (val: number | null): string => {
        if (val === null) return 'N/A';

        if (unit === '$' || unit === '$B') {
            return val.toFixed(2);
        }
        return val.toFixed(2);
    };

    // Get trend icon and color
    const getTrendIcon = () => {
        switch (trend_direction) {
            case 'up':
                return <TrendingUp size={18} className="trend-up" />;
            case 'down':
                return <TrendingDown size={18} className="trend-down" />;
            default:
                return <Minus size={18} className="trend-neutral" />;
        }
    };

    const getTrendClass = () => {
        switch (trend_direction) {
            case 'up':
                return 'trend-up';
            case 'down':
                return 'trend-down';
            default:
                return 'trend-neutral';
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1, duration: 0.3 }}
            className="glass-card-hover p-6"
        >
            {/* Metric Name */}
            <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-medium text-nvidia-light-gray opacity-80 uppercase tracking-wide">
                    {name}
                </h3>
                {getTrendIcon()}
            </div>

            {/* Value */}
            <div className="flex items-baseline space-x-2 mb-2">
                <span className="text-sm text-nvidia-light-gray">{unit}</span>
                <motion.span
                    key={value}
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="text-3xl font-bold text-white"
                >
                    {formatValue(value)}
                </motion.span>
            </div>

            {/* Trend */}
            {trend !== null && (
                <div className="flex items-center space-x-1">
                    <span className={`text-sm font-semibold ${getTrendClass()}`}>
                        {trend > 0 ? '+' : ''}{trend.toFixed(2)}%
                    </span>
                    <span className="text-xs text-nvidia-light-gray opacity-60">
                        vs previous
                    </span>
                </div>
            )}
        </motion.div>
    );
}
