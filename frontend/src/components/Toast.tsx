/**
 * Toast notification component
 */
import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, XCircle, AlertCircle, X } from 'lucide-react';
import { useDashboardStore } from '../store/dashboardStore';

export default function Toast() {
    const { error, updateMessage, clearError } = useDashboardStore();

    useEffect(() => {
        if (error) {
            const timer = setTimeout(() => {
                clearError();
            }, 5000);
            return () => clearTimeout(timer);
        }
    }, [error, clearError]);

    const message = error || updateMessage;
    const type = error ? 'error' : updateMessage ? 'success' : null;

    const getIcon = () => {
        switch (type) {
            case 'success':
                return <CheckCircle size={20} className="text-nvidia-green" />;
            case 'error':
                return <XCircle size={20} className="text-red-500" />;
            default:
                return <AlertCircle size={20} className="text-blue-500" />;
        }
    };

    const getBgClass = () => {
        switch (type) {
            case 'success':
                return 'border-nvidia-green';
            case 'error':
                return 'border-red-500';
            default:
                return 'border-blue-500';
        }
    };

    return (
        <AnimatePresence>
            {message && (
                <motion.div
                    initial={{ opacity: 0, x: 100, y: 0 }}
                    animate={{ opacity: 1, x: 0, y: 0 }}
                    exit={{ opacity: 0, x: 100 }}
                    className={`fixed top-4 right-4 z-50 glass-card border-l-4 ${getBgClass()} p-4 max-w-sm shadow-xl`}
                >
                    <div className="flex items-start space-x-3">
                        {getIcon()}
                        <p className="text-sm text-white flex-1">{message}</p>
                        <button
                            onClick={clearError}
                            className="text-nvidia-light-gray hover:text-white transition-colors"
                        >
                            <X size={16} />
                        </button>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}
