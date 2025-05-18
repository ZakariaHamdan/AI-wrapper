import React from 'react';

function Header({ activeTab, setActiveTab, darkMode, setDarkMode, apiStatus }) {
  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-semibold">SQL Database Assistant</h1>
          </div>
          
          <nav className="flex space-x-4">
            <button
              onClick={() => setActiveTab('chat')}
              className={`px-3 py-2 rounded-md ${
                activeTab === 'chat'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
              }`}
            >
              Chat
            </button>
            
            <button
              onClick={() => setActiveTab('sql')}
              className={`px-3 py-2 rounded-md ${
                activeTab === 'sql'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
              }`}
            >
              SQL
            </button>
            
            <button
              onClick={() => setActiveTab('schema')}
              className={`px-3 py-2 rounded-md ${
                activeTab === 'schema'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
              }`}
            >
              Schema
            </button>
          </nav>
          
          <div className="flex items-center space-x-4">
            {/* API Status indicator */}
            <div className="flex items-center">
              <div className={`w-2 h-2 rounded-full mr-2 ${apiStatus ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-sm">{apiStatus ? 'Connected' : 'Offline'}</span>
            </div>
            
            {/* Theme toggle */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-1 rounded-full text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              {darkMode ? (
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              ) : (
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;