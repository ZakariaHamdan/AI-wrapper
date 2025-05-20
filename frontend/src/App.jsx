// App.jsx with dark mode set as default
import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ChatPanel from './components/ChatPanel';
import FileUpload from './components/FileUpload'; // New import
import * as api from './services/api';

function App() {
  // Set dark mode as default
  const [darkMode, setDarkMode] = useState(true);
  const [activeTab, setActiveTab] = useState('chat');
  const [apiStatus, setApiStatus] = useState(false);
  
  // Check API status on mount
  useEffect(() => {
    const initApp = async () => {
      try {
        await api.checkApiStatus();
        setApiStatus(true);
      } catch (error) {
        console.error('API connection error:', error);
      }
    };
    
    initApp();
  }, []);
  
  return (
    <div className={`min-h-screen transition-colors duration-200 ${darkMode ? 'dark bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'}`}>
      <Header 
        activeTab={activeTab} 
        setActiveTab={setActiveTab}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        apiStatus={apiStatus}
      />
      
      <main className="container mx-auto p-4">
        {activeTab === 'chat' && <ChatPanel />}
        {activeTab === 'upload' && <FileUpload />}
      </main>
    </div>
  );
}

export default App;