// Notification.jsx
import React, { useEffect } from 'react';

const Notification = ({ notification, onClose }) => {
    useEffect(() => {
        if (notification && notification.duration) {
            const timer = setTimeout(() => {
                onClose();
            }, notification.duration);

            return () => clearTimeout(timer);
        }
    }, [notification, onClose]);

    if (!notification) return null;

    const bgColor = notification.type === 'success' ? 'bg-green-600' : 'bg-red-600';
    const icon = notification.type === 'success' ? '✓' : '✕';

    return (
        <div className="fixed top-4 right-4 z-50 animate-in slide-in-from-top duration-300">
            <div className={`${bgColor} text-white p-4 rounded-lg shadow-lg max-w-md`}>
                <div className="flex items-start space-x-3">
                    <div className={`flex-shrink-0 w-6 h-6 rounded-full ${notification.type === 'success' ? 'bg-green-500' : 'bg-red-500'} flex items-center justify-center text-sm font-bold`}>
                        {icon}
                    </div>
                    <div className="flex-1">
                        <h4 className="font-semibold">{notification.title}</h4>
                        <p className="text-sm mt-1 opacity-90">{notification.message}</p>
                    </div>
                    <button
                        onClick={onClose}
                        className="flex-shrink-0 text-white hover:text-gray-200 font-bold text-lg leading-none"
                    >
                        ×
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Notification;