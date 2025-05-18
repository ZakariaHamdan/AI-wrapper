import React, { useState, useRef, useEffect } from 'react';
import MessageItem from './MessageItem';
import * as api from '../services/api';

function ChatPanel() {
  const [messages, setMessages] = useState([
    { sender: 'assistant', content: 'Hello! I\'m your SQL Database Assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);
  
  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const handleSend = async () => {
    if (!input.trim()) return;
    
    // Add user message
    setMessages(prev => [...prev, { sender: 'user', content: input }]);
    setLoading(true);
    
    try {
      // Call API
      const response = await api.sendChatMessage(input, sessionId);
      
      // Save session ID if first message
      if (!sessionId && response.session_id) {
        setSessionId(response.session_id);
      }
      
      // Add assistant response
      setMessages(prev => [...prev, { 
        sender: 'assistant', 
        content: response.response,
        sqlQuery: response.sql_query,
        sqlResult: response.sql_result,
        sqlError: response.sql_error
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
      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
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
      
      {/* Input area */}
      <div className="border-t p-4 dark:border-gray-700">
        <div className="flex space-x-2">
          <textarea
            className="flex-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none dark:bg-gray-800 dark:border-gray-700"
            placeholder="Ask a question about your database..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            rows={1}
          />
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
            onClick={handleSend}
            disabled={loading || !input.trim()}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatPanel;