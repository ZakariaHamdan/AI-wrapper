// api.js - FIXED with longer timeout for file uploads
import axios from 'axios';

// Single backend API instance
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 1200000, // 10 seconds for regular requests
  headers: {
    'Content-Type': 'application/json'
  }
});

// Special instance for file uploads with longer timeout
const fileApi = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 60000, // 60 seconds for file uploads
  headers: {
    'Content-Type': 'application/json'
  }
});

// DB Query API functions
export const checkDbApiStatus = async () => {
  try {
    const response = await api.get('/');
    return response.data;
  } catch (error) {
    throw new Error('Database API unavailable');
  }
};

export const sendDbChatMessage = async (message, sessionId = null) => {
  const response = await api.post('/db/chat', { 
    message, 
    session_id: sessionId 
  });
  return response.data;
};

export const clearDbChat = async (sessionId) => {
  const response = await api.post('/db/clear', { 
    session_id: sessionId 
  });
  return response.data;
};

// File Analysis API functions with longer timeout
export const checkFileApiStatus = async () => {
  try {
    const response = await api.get('/');
    return response.data;
  } catch (error) {
    throw new Error('File Analysis API unavailable');
  }
};

export const uploadAndAnalyzeFile = async (formData, sessionId = null) => {
  if (sessionId) {
    formData.append('session_id', sessionId);
  }
  
  // Use fileApi with longer timeout for uploads
  const response = await fileApi.post('/files/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    timeout: 120000, // 2 minutes for large files
    onUploadProgress: (progressEvent) => {
      // Optional: Add progress tracking later
      const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
      console.log(`Upload progress: ${percentCompleted}%`);
    }
  });
  
  return response.data;
};

export const sendFileAnalysisMessage = async (message, sessionId) => {
  const response = await api.post('/files/chat', { 
    message, 
    session_id: sessionId 
  });
  return response.data;
};

export const clearFileAnalysisChat = async (sessionId) => {
  const response = await api.post('/files/clear', { 
    session_id: sessionId 
  });
  return response.data;
};