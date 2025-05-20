// API service for communicating with the backend
import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:8000', // Default API URL
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Check API status
export const checkApiStatus = async () => {
  try {
    const response = await api.get('/');
    return response.data;
  } catch (error) {
    throw new Error('API unavailable');
  }
};

// Get database schema
export const getDatabaseSchema = async () => {
  const response = await api.get('/schema');
  return response.data;
};

// Get context files
export const getDatabaseContext = async () => {
  const response = await api.get('/context');
  return response.data;
};

// Send chat message
export const sendChatMessage = async (message, sessionId = null) => {
  const response = await api.post('/chat', { 
    message, 
    session_id: sessionId 
  });
  return response.data;
};

// Execute SQL query
export const executeSqlQuery = async (query, sessionId = null) => {
  const response = await api.post('/sql', { 
    query, 
    session_id: sessionId 
  });
  return response.data;
};

// Clear chat session
export const clearChat = async (sessionId) => {
  const response = await api.post('/clear', { 
    session_id: sessionId 
  });
  return response.data;
};

export const uploadFile = async (formData, sessionId = null) => {
  // Add session ID if provided
  if (sessionId) {
    formData.append('session_id', sessionId);
  }
  
  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  return response.data;
};

export default api;