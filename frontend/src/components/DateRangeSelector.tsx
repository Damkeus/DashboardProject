/**
 * Date range selector component
 */
import type { Period, DateRangeOption } from '../types';
import { useDashboardStore } from '../store/dashboardStore';

const DATE_RANGES: DateRangeOption[] = [
    { label: '1M', value: '1M' },
    { label: '3M', value: '3M' },
    { label: '6M', value: '6M' },
    { label: '1Y', value: '1Y' },
    { label: '2Y', value: '2Y' },
    { label: 'ALL', value: 'ALL' },
];

export default function DateRangeSelector() {
    const { selectedPeriod, setPeriod } = useDashboardStore();

    return (
        <div className="flex space-x-2 mb-4">
            {DATE_RANGES.map((range) => (
                <button
                    key={range.value}
                    onClick={() => setPeriod(range.value)}
                    className={`px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200 ${selectedPeriod === range.value
                            ? 'bg-nvidia-green text-white shadow-glow-green'
                            : 'bg-nvidia-gray text-nvidia-light-gray hover:bg-nvidia-green hover:bg-opacity-20'
                        }`}
                >
                    {range.label}
                </button>
            ))}
        </div>
    );
}
