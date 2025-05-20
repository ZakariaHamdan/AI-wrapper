// FileAnalysisPanel.jsx
import React, { useState, useRef, useEffect } from 'react';
import MessageItem from './MessageItem';
import * as api from '../services/api';

function FileAnalysisPanel() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([
    { sender: 'assistant', content: 'Hello! I\'m your File Analysis Assistant. Upload an Excel or CSV file to get started.' }
  ]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  
  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setError(null);
  };
  
  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file to upload");
      return;
    }
    
    // Check file extension
    const fileExt = file.name.split('.').pop().toLowerCase();
    if (!['xlsx', 'xls', 'csv'].includes(fileExt)) {
      setError("Only Excel (.xlsx, .xls) and CSV files are supported");
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const result = await api.uploadAndAnalyzeFile(formData);
      
      // Save session ID
      setSessionId(result.session_id);
      
      // Add file info and AI response as messages
      setMessages(prev => [
        ...prev,
        { 
          sender: 'user', 
          content: `Uploaded file: ${file.name} (${result.file_info.rows} rows × ${result.file_info.columns} columns)`
        },
        {
          sender: 'assistant',
          content: result.response,
          fileInfo: result.file_info
        }
      ]);
      
      // Reset file after successful upload
      setFile(null);
    } catch (err) {
      console.error('Error uploading file:', err);
      setError(err.response?.data?.detail || "Failed to upload file");
    } finally {
      setLoading(false);
    }
  };
  
  const handleSend = async () => {
    if (!input.trim() || !sessionId) return;
    
    // Add user message
    setMessages(prev => [...prev, { sender: 'user', content: input }]);
    setLoading(true);
    
    try {
      // Call File Analysis API
      const response = await api.sendFileAnalysisMessage(input, sessionId);
      
      // Add assistant response
      setMessages(prev => [...prev, { 
        sender: 'assistant', 
        content: response.response
      }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        sender: 'assistant', 
        content: 'Sorry, there was an error processing your request. Please try again.' 
      }]);
    } finally {
      setLoading(false);
      setInput('');
    }
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };
  
  return (
    <div className="flex flex-col h-[calc(100vh-5rem)]">
      {/* File upload area */}
      {!sessionId && (
        <div className="p-6 bg-gray-800 rounded-lg shadow-lg mb-6">
          <h2 className="text-xl font-semibold mb-4 text-blue-400">Upload Data File</h2>
          <p className="text-gray-300 mb-6">
            Upload an Excel (.xlsx, .xls) or CSV file to analyze with the AI assistant.
          </p>
          
          {/* Upload area with drag & drop styling */}
          <div className="mb-6">
            <label 
              htmlFor="file-upload" 
              className="flex flex-col items-center justify-center w-full h-32 px-4 transition bg-gray-700 border-2 border-gray-600 border-dashed rounded-lg cursor-pointer hover:bg-gray-600"
            >
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <svg className="w-10 h-10 mb-3 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                </svg>
                <p className="mb-2 text-sm text-gray-300">
                  <span className="font-semibold">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-gray-400">Excel or CSV files only</p>
                {file && <p className="mt-2 text-sm text-blue-300">Selected: {file.name}</p>}
              </div>
              <input 
                id="file-upload" 
                type="file" 
                onChange={handleFileChange} 
                className="hidden" 
                accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" 
              />
            </label>
          </div>
          
          <div className="flex justify-center">
            <button
              onClick={handleUpload}
              disabled={!file || loading}
              className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
            >
              {loading ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Uploading...
                </span>
              ) : 'Upload File'}
            </button>
          </div>
          
          {error && (
            <div className="mt-4 p-3 bg-red-900/50 border border-red-700 text-red-300 rounded-md">
              <div className="flex items-center">
                <svg className="w-5 h-5 mr-2 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                {error}
              </div>
            </div>
          )}
        </div>
      )}
      
      {/* Messages container */}
      <div className={`flex-1 overflow-y-auto p-4 space-y-4 ${!sessionId ? 'hidden' : ''}`}>
        {messages.map((message, index) => (
          <MessageItem key={index} message={message} />
        ))}
        
        {loading && (
          <div className="flex justify-center p-2">
            <div className="animate-pulse flex space-x-4">
              <div className="h-4 w-4 bg-blue-400 rounded-full"></div>
              <div className="h-4 w-4 bg-blue-400 rounded-full"></div>
              <div className="h-4 w-4 bg-blue-400 rounded-full"></div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input area - only show if session exists */}
      {sessionId && (
        <div className="border-t p-4 dark:border-gray-700">
          <div className="flex space-x-2">
            <textarea
              className="flex-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none dark:bg-gray-800 dark:border-gray-700"
              placeholder="Ask questions about your data..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              rows={1}
            />
            <button
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
              onClick={handleSend}
              disabled={loading || !input.trim() || !sessionId}
            >
              Send
            </button>
          </div>
          
          <div className="flex justify-between mt-2">
            <button
              className="text-sm text-gray-400 hover:text-gray-300"
              onClick={() => {
                if (window.confirm("Are you sure you want to start a new analysis? This will clear your current session.")) {
                  setSessionId(null);
                  setMessages([{ sender: 'assistant', content: 'Hello! I\'m your File Analysis Assistant. Upload an Excel or CSV file to get started.' }]);
                }
              }}
            >
              New Analysis
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default FileAnalysisPanel;