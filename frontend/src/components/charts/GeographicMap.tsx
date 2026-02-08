/**
 * Interactive Leaflet map showing NVIDIA revenue by region
 * Dark mode with sales markers sized by revenue
 */
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import { motion } from 'framer-motion';
import 'leaflet/dist/leaflet.css';
import { useEffect } from 'react';

interface RegionSale {
    name: string;
    lat: number;
    lng: number;
    hardware: number;  // Revenue in billions
    software: number;
    services: number;
    total: number;
    growth: number;
}

// Set dark mode tiles
function DarkModeLayer() {
    const map = useMap();

    useEffect(() => {
        map.invalidateSize();
    }, [map]);

    return null;
}

export default function GeographicMap() {
    const salesData: RegionSale[] = [
        {
            name: 'North America',
            lat: 40.0,
            lng: -100.0,
            hardware: 32.5,
            software: 8.2,
            services: 4.5,
            total: 45.2,
            growth: 18.5
        },
        {
            name: 'Silicon Valley',
            lat: 37.3861,
            lng: -122.0839,
            hardware: 15.2,
            software: 4.8,
            services: 2.5,
            total: 22.5,
            growth: 25.3
        },
        {
            name: 'Europe',
            lat: 50.0,
            lng: 10.0,
            hardware: 8.5,
            software: 2.8,
            services: 1.5,
            total: 12.8,
            growth: 22.1
        },
        {
            name: 'China',
            lat: 35.0,
            lng: 105.0,
            hardware: 22.3,
            software: 3.2,
            services: 2.1,
            total: 27.6,
            growth: 42.5
        },
        {
            name: 'Japan',
            lat: 36.2048,
            lng: 138.2529,
            hardware: 4.2,
            software: 1.5,
            services: 0.8,
            total: 6.5,
            growth: 15.8
        },
        {
            name: 'Taiwan',
            lat: 23.6978,
            lng: 120.9605,
            hardware: 3.8,
            software: 0.6,
            services: 0.4,
            total: 4.8,
            growth: 38.2
        },
        {
            name: 'India',
            lat: 20.5937,
            lng: 78.9629,
            hardware: 2.1,
            software: 0.8,
            services: 0.5,
            total: 3.4,
            growth: 52.3
        }
    ];

    const maxRevenue = Math.max(...salesData.map(s => s.total));

    const getMarkerSize = (revenue: number) => {
        // Scale marker between 15 and 60 pixels based on revenue
        return Math.max(15, (revenue / maxRevenue) * 60);
    };

    const getMarkerColor = (growth: number) => {
        if (growth > 40) return '#76B900';  // High growth - bright green
        if (growth > 25) return '#a0e000';  // Medium-high - light green
        if (growth > 15) return '#5a8700';  // Medium - dark green
        return '#4a7000';  // Lower growth - darker
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="glass-card p-6"
        >
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-white">Global Revenue Distribution</h2>
                <div className="flex items-center space-x-4 text-xs">
                    <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 rounded-full bg-nvidia-green"></div>
                        <span className="text-nvidia-light-gray/70">High Growth (&gt;40%)</span>
                    </div>
                    <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#5a8700' }}></div>
                        <span className="text-nvidia-light-gray/70">Moderate Growth</span>
                    </div>
                </div>
            </div>

            <div className="rounded-xl overflow-hidden border-2 border-nvidia-green/20" style={{ height: '500px' }}>
                <MapContainer
                    center={[20, 0]}
                    zoom={2}
                    style={{ height: '100%', width: '100%', background: '#0a0a0a' }}
                    zoomControl={true}
                >
                    {/* Dark mode tile layer */}
                    <TileLayer
                        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                    />

                    <DarkModeLayer />

                    {/* Sales markers */}
                    {salesData.map((sale, index) => (
                        <CircleMarker
                            key={sale.name}
                            center={[sale.lat, sale.lng]}
                            radius={getMarkerSize(sale.total)}
                            pathOptions={{
                                fillColor: getMarkerColor(sale.growth),
                                fillOpacity: 0.7,
                                color: getMarkerColor(sale.growth),
                                weight: 2,
                                opacity: 1
                            }}
                        >
                            <Popup>
                                <div className="p-3 bg-nvidia-black text-white min-w-[220px]">
                                    <h3 className="font-bold text-nvidia-green text-lg mb-3 pb-2 border-b border-nvidia-green/30">{sale.name}</h3>

                                    <div className="space-y-2 text-sm">
                                        <div className="flex justify-between items-center pb-2 mb-2 border-b border-nvidia-gray/50">
                                            <span className="font-semibold text-nvidia-light-gray/80">Total Revenue:</span>
                                            <span className="text-nvidia-green font-bold text-base">${sale.total.toFixed(1)}B</span>
                                        </div>

                                        <div className="space-y-1.5 bg-nvidia-gray/20 rounded-lg p-2">
                                            <div className="flex justify-between">
                                                <span className="text-nvidia-light-gray/70 flex items-center gap-1">
                                                    <span className="text-xs">🔧</span> Hardware:
                                                </span>
                                                <span className="font-medium">${sale.hardware.toFixed(1)}B</span>
                                            </div>
                                            <div className="flex justify-between">
                                                <span className="text-nvidia-light-gray/70 flex items-center gap-1">
                                                    <span className="text-xs">💻</span> Software:
                                                </span>
                                                <span className="font-medium">${sale.software.toFixed(1)}B</span>
                                            </div>
                                            <div className="flex justify-between">
                                                <span className="text-nvidia-light-gray/70 flex items-center gap-1">
                                                    <span className="text-xs">🛠️</span> Services:
                                                </span>
                                                <span className="font-medium">${sale.services.toFixed(1)}B</span>
                                            </div>
                                        </div>

                                        <div className="pt-2 mt-2 border-t border-nvidia-gray/50 flex justify-between items-center bg-nvidia-green/10 rounded-lg px-2 py-1.5">
                                            <span className="text-nvidia-light-gray/80 font-medium">Growth:</span>
                                            <span className="text-nvidia-green font-bold text-base">+{sale.growth.toFixed(1)}%</span>
                                        </div>
                                    </div>
                                </div>
                            </Popup>
                        </CircleMarker>
                    ))}
                </MapContainer>
            </div>

            {/* Legend */}
            <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
                <div className="backdrop-blur-sm bg-nvidia-black/30 rounded-lg p-3 border border-nvidia-green/20">
                    <div className="text-nvidia-light-gray/60 text-xs mb-1">Total Global Revenue</div>
                    <div className="text-2xl font-bold text-nvidia-green">
                        ${salesData.reduce((sum, s) => sum + s.total, 0).toFixed(1)}B
                    </div>
                </div>
                <div className="backdrop-blur-sm bg-nvidia-black/30 rounded-lg p-3 border border-nvidia-green/20">
                    <div className="text-nvidia-light-gray/60 text-xs mb-1">Average Growth</div>
                    <div className="text-2xl font-bold text-nvidia-green">
                        +{(salesData.reduce((sum, s) => sum + s.growth, 0) / salesData.length).toFixed(1)}%
                    </div>
                </div>
                <div className="backdrop-blur-sm bg-nvidia-black/30 rounded-lg p-3 border border-nvidia-green/20">
                    <div className="text-nvidia-light-gray/60 text-xs mb-1">Active Markets</div>
                    <div className="text-2xl font-bold text-nvidia-green">
                        {salesData.length}
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
