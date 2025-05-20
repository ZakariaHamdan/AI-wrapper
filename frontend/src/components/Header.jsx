// Header.jsx with improved dark mode styling
import React from 'react';

function Header({ activeTab, setActiveTab, darkMode, setDarkMode, apiStatus }) {
  return (
    <header className="bg-gray-800 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-semibold text-blue-400">SQL Database Assistant</h1>
          </div>
          
          <nav className="flex space-x-2">
            <button
              onClick={() => setActiveTab('chat')}
              className={`px-4 py-2 rounded-md transition-colors duration-200 ${
                activeTab === 'chat'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-700'
              }`}
            >
              Chat
            </button>
            
            <button
              onClick={() => setActiveTab('upload')}
              className={`px-4 py-2 rounded-md transition-colors duration-200 ${
                activeTab === 'upload'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-700'
              }`}
            >
              Upload File
            </button>
          </nav>
          
          <div className="flex items-center space-x-4">
            {/* API Status indicator */}
            <div className="flex items-center bg-gray-700 px-3 py-1 rounded-full">
              <div className={`w-2 h-2 rounded-full mr-2 ${apiStatus ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-sm">{apiStatus ? 'Connected' : 'Offline'}</span>
            </div>
            
            {/* Theme toggle */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-full bg-gray-700 text-gray-300 hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500"
              title={darkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
            >
              {darkMode ? (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
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