// FileUpload.jsx with improved styling
import React, { useState } from 'react';
import * as api from '../services/api';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  
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
      
      const result = await api.uploadFile(formData);
      setResponse(result);
    } catch (err) {
      console.error('Error uploading file:', err);
      setError(err.response?.data?.detail || "Failed to upload file");
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="flex flex-col h-[calc(100vh-5rem)]">
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
      
      {response && (
        <div className="flex-1 overflow-y-auto">
          <div className="bg-gray-800 rounded-lg shadow-lg p-6 mb-6">
            <h3 className="text-lg font-medium text-green-400 mb-2 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
              File Uploaded Successfully
            </h3>
            <div className="text-gray-300">
              <p className="mb-2">
                <span className="font-medium text-blue-300">{file.name}</span> has been uploaded and added to your conversation.
              </p>
              <div className="grid grid-cols-2 gap-4 mt-4 bg-gray-700 p-4 rounded-md">
                <div>
                  <span className="text-gray-400 block mb-1 text-sm">Rows</span>
                  <span className="text-lg font-semibold">{response.file_info.rows}</span>
                </div>
                <div>
                  <span className="text-gray-400 block mb-1 text-sm">Columns</span>
                  <span className="text-lg font-semibold">{response.file_info.columns}</span>
                </div>
                <div className="col-span-2">
                  <span className="text-gray-400 block mb-1 text-sm">Column Names</span>
                  <div className="flex flex-wrap gap-2">
                    {response.file_info.column_names.map((col, idx) => (
                      <span key={idx} className="px-2 py-1 bg-blue-900/50 text-blue-300 rounded text-sm">{col}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-gray-800 rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-medium text-blue-400 mb-4">AI Analysis</h3>
            <div className="prose dark:prose-invert max-w-none">
              <div dangerouslySetInnerHTML={{ __html: response.response }} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default FileUpload;