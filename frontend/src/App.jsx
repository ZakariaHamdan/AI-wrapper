// App.jsx
import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ChatPanel from './components/ChatPanel';
import Notification from './components/Notification';
import * as api from './services/api';

function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [activeTab, setActiveTab] = useState('chat');
  const [apiStatus, setApiStatus] = useState({
    dbApi: false
  });
  const [notification, setNotification] = useState(null);

  // Check API status on mount
  useEffect(() => {
    const initApp = async () => {
      try {
        await api.checkDbApiStatus();
        setApiStatus(prev => ({ ...prev, dbApi: true }));
      } catch (error) {
        console.error('Database API connection error:', error);
      }
    };

    initApp();
  }, []);

  // Show notification function
  const showNotification = (notificationData) => {
    setNotification(notificationData);
  };

  // Close notification function
  const closeNotification = () => {
    setNotification(null);
  };

  // Listen for database change events (optional - for any app-level handling)
  useEffect(() => {
    const handleDatabaseChange = (event) => {
      const { database, result } = event.detail;
      console.log(`App: Database changed to: ${database}`);
      // Additional app-level handling if needed
    };

    window.addEventListener('databaseChanged', handleDatabaseChange);

    return () => {
      window.removeEventListener('databaseChanged', handleDatabaseChange);
    };
  }, []);

  return (
      <div className={`min-h-screen transition-colors duration-200 ${darkMode ? 'dark bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'}`}>
        <Header
            activeTab={activeTab}
            setActiveTab={setActiveTab}
            darkMode={darkMode}
            setDarkMode={setDarkMode}
            apiStatus={apiStatus}
            showNotification={showNotification}
        />

        <main className="container mx-auto p-4">
          <ChatPanel />
        </main>

        {/* Notification component */}
        <Notification
            notification={notification}
            onClose={closeNotification}
        />
      </div>
  );
}

export default App;