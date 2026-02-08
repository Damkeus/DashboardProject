/**
 * Loading skeleton component for charts and data
 */

export default function LoadingSkeleton() {
    return (
        <div className="glass-card p-6 space-y-4">
            {/* Title skeleton */}
            <div className="h-6 w-1/3 skeleton rounded"></div>

            {/* Chart skeleton */}
            <div className="space-y-3">
                <div className="h-48 skeleton rounded"></div>
                <div className="flex space-x-2">
                    <div className="h-4 w-20 skeleton rounded"></div>
                    <div className="h-4 w-20 skeleton rounded"></div>
                    <div className="h-4 w-20 skeleton rounded"></div>
                </div>
            </div>
        </div>
    );
}

export function KPISkeletonGrid() {
    return (
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
            {[...Array(5)].map((_, i) => (
                <div key={i} className="glass-card p-6 space-y-3">
                    <div className="h-4 w-3/4 skeleton rounded"></div>
                    <div className="h-8 w-1/2 skeleton rounded"></div>
                    <div className="h-3 w-1/3 skeleton rounded"></div>
                </div>
            ))}
        </div>
    );
}
