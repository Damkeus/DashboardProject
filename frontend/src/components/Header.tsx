/**
 * Enhanced Header component with NVIDIA logo, title, and controls
 */
import { RefreshCw, Download } from 'lucide-react';
import { motion } from 'framer-motion';
import { useDashboardStore } from '../store/dashboardStore';
import { format } from 'date-fns';
import nvidiaLogo from '../assets/nvidia-logo.png';

export default function Header() {
    const { summary, isUpdating, triggerManualUpdate, exportData } = useDashboardStore();

    const handleRefresh = () => {
        triggerManualUpdate();
    };

    const handleExport = () => {
        exportData();
    };

    const lastUpdated = summary?.last_updated
        ? format(new Date(summary.last_updated), 'MMM d, yyyy HH:mm:ss')
        : 'Never';

    return (
        <motion.header
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="relative mb-6 overflow-hidden"
        >
            {/* Animated background gradient */}
            <div className="absolute inset-0 bg-gradient-to-r from-nvidia-green/5 via-nvidia-green/10 to-nvidia-green/5 animate-pulse-slow"></div>

            {/* Glass card with stronger effect */}
            <div className="relative backdrop-blur-xl bg-nvidia-dark-gray/80 border border-nvidia-green/30 rounded-2xl px-8 py-6 shadow-2xl shadow-nvidia-green/10">
                <div className="flex items-center justify-between">
                    {/* Logo and Title */}
                    <div className="flex items-center space-x-6">
                        {/* NVIDIA Logo */}
                        <motion.div
                            className="flex items-center space-x-3"
                            whileHover={{ scale: 1.02 }}
                            transition={{ type: "spring", stiffness: 400 }}
                        >
                            <div className="relative">
                                <div className="absolute inset-0 bg-nvidia-green/20 blur-xl rounded-full"></div>
                                <img
                                    src={nvidiaLogo}
                                    alt="NVIDIA"
                                    className="h-12 w-auto relative z-10"
                                    style={{ filter: 'drop-shadow(0 0 10px rgba(118, 185, 0, 0.5))' }}
                                />
                            </div>
                            <div className="h-12 w-px bg-gradient-to-b from-transparent via-nvidia-green to-transparent"></div>
                        </motion.div>

                        <div>
                            <motion.h1
                                className="text-3xl font-bold mb-1"
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.2 }}
                            >
                                <span className="text-gradient">Economic Dashboard</span>
                            </motion.h1>
                            <motion.p
                                className="text-sm text-nvidia-light-gray/70 font-medium tracking-wide"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ delay: 0.3 }}
                            >
                                Real-time Market Intelligence
                            </motion.p>
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="flex items-center space-x-6">
                        {/* Last Updated */}
                        <motion.div
                            className="text-right backdrop-blur-sm bg-nvidia-black/30 rounded-lg px-4 py-2 border border-nvidia-gray/30"
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.4 }}
                        >
                            <p className="text-xs text-nvidia-light-gray/60 uppercase tracking-wider mb-1">Last Updated</p>
                            <p className="text-sm font-bold text-nvidia-green">{lastUpdated}</p>
                        </motion.div>

                        {/* Export Button */}
                        <motion.button
                            onClick={handleExport}
                            className="relative group"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <div className="absolute inset-0 bg-nvidia-green/20 rounded-xl blur-md group-hover:bg-nvidia-green/40 transition-all"></div>
                            <div className="relative px-4 py-3 bg-nvidia-gray/80 backdrop-blur-sm rounded-xl border border-nvidia-green/40 hover:border-nvidia-green transition-all">
                                <Download size={20} className="text-nvidia-green" />
                            </div>
                        </motion.button>

                        {/* Refresh Button */}
                        <motion.button
                            onClick={handleRefresh}
                            disabled={isUpdating}
                            className="relative group"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <div className="absolute inset-0 bg-nvidia-green/30 rounded-xl blur-lg group-hover:bg-nvidia-green/50 transition-all"></div>
                            <div className="relative px-4 py-3 bg-nvidia-green/20 backdrop-blur-sm rounded-xl border-2 border-nvidia-green hover:bg-nvidia-green/30 transition-all">
                                <RefreshCw
                                    size={20}
                                    className={`text-nvidia-green ${isUpdating ? 'animate-spin' : ''}`}
                                />
                            </div>
                            {isUpdating && (
                                <motion.span
                                    className="absolute -top-1 -right-1 flex h-4 w-4"
                                    initial={{ scale: 0 }}
                                    animate={{ scale: 1 }}
                                >
                                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-nvidia-green opacity-75"></span>
                                    <span className="relative inline-flex rounded-full h-4 w-4 bg-nvidia-green shadow-glow-green-strong"></span>
                                </motion.span>
                            )}
                        </motion.button>
                    </div>
                </div>
            </div>
        </motion.header>
    );
}
