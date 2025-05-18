import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ChatPanel from './components/ChatPanel';
import SqlEditor from './components/SqlEditor';
import DatabaseSchema from './components/DatabaseSchema';
import * as api from './services/api';

function App() {
  // State
  const [darkMode, setDarkMode] = useState(false);
  const [activeTab, setActiveTab] = useState('chat');
  const [apiStatus, setApiStatus] = useState(false);
  const [schema, setSchema] = useState(null);
  
  // Check API status and load schema on mount
  useEffect(() => {
    const initApp = async () => {
      try {
        await api.checkApiStatus();
        setApiStatus(true);
        
        const dbSchema = await api.getDatabaseSchema();
        setSchema(dbSchema);
      } catch (error) {
        console.error('API connection error:', error);
      }
    };
    
    initApp();
  }, []);
  
  return (
    <div className={`min-h-screen ${darkMode ? 'dark bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'}`}>
      <Header 
        activeTab={activeTab} 
        setActiveTab={setActiveTab}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        apiStatus={apiStatus}
      />
      
      <main className="container mx-auto p-4">
        {activeTab === 'chat' && <ChatPanel />}
        {activeTab === 'sql' && <SqlEditor />}
        {activeTab === 'schema' && <DatabaseSchema schema={schema} />}
      </main>
    </div>
  );
}

export default App;