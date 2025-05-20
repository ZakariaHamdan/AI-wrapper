// api.js - Updated to support both services
import axios from 'axios';

// Create axios instances for each service
const dbQueryApi = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

const fileAnalysisApi = axios.create({
  baseURL: 'http://localhost:8001',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// DB Query API functions
export const checkDbApiStatus = async () => {
  try {
    const response = await dbQueryApi.get('/');
    return response.data;
  } catch (error) {
    throw new Error('Database API unavailable');
  }
};

export const getDatabaseContext = async () => {
  const response = await dbQueryApi.get('/context');
  return response.data;
};

export const sendDbChatMessage = async (message, sessionId = null) => {
  const response = await dbQueryApi.post('/chat', { 
    message, 
    session_id: sessionId 
  });
  return response.data;
};

export const clearDbChat = async (sessionId) => {
  const response = await dbQueryApi.post('/clear', { 
    session_id: sessionId 
  });
  return response.data;
};

// File Analysis API functions
export const checkFileApiStatus = async () => {
  try {
    const response = await fileAnalysisApi.get('/');
    return response.data;
  } catch (error) {
    throw new Error('File Analysis API unavailable');
  }
};

export const uploadAndAnalyzeFile = async (formData, sessionId = null) => {
  if (sessionId) {
    formData.append('session_id', sessionId);
  }
  
  const response = await fileAnalysisApi.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  return response.data;
};

export const sendFileAnalysisMessage = async (message, sessionId) => {
  const response = await fileAnalysisApi.post('/chat', { 
    message, 
    session_id: sessionId 
  });
  return response.data;
};

export const clearFileAnalysisChat = async (sessionId) => {
  const response = await fileAnalysisApi.post('/clear', { 
    session_id: sessionId 
  });
  return response.data;
};