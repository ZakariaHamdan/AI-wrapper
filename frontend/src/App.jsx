// App.jsx
import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ChatPanel from './components/ChatPanel';
import FileAnalysisPanel from './components/FileAnalysisPanel';
import * as api from './services/api';

function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [activeTab, setActiveTab] = useState('chat');
  const [apiStatus, setApiStatus] = useState({
    dbApi: false,
    fileApi: false
  });
  
  // Check API status on mount
  useEffect(() => {
    const initApp = async () => {
      try {
        await api.checkDbApiStatus();
        setApiStatus(prev => ({ ...prev, dbApi: true }));
      } catch (error) {
        console.error('Database API connection error:', error);
      }
      
      try {
        await api.checkFileApiStatus();
        setApiStatus(prev => ({ ...prev, fileApi: true }));
      } catch (error) {
        console.error('File Analysis API connection error:', error);
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
        {activeTab === 'fileAnalysis' && <FileAnalysisPanel />}
      </main>
    </div>
  );
}

export default App;