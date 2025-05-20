// MessageItem.jsx
import React from 'react';

function MessageItem({ message }) {
  const { sender, content, sqlQuery, sqlResult, sqlError, fileInfo } = message;
  
  return (
    <div 
      className={`p-4 rounded-lg max-w-3xl ${
        sender === 'user' 
          ? 'ml-auto bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100' 
          : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
      }`}
    >
      {/* SQL Query */}
      {sqlQuery && (
        <div className="mb-3">
          <h4 className="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400 mb-1">SQL Query</h4>
          <pre className="bg-gray-200 dark:bg-gray-700 p-2 rounded text-sm overflow-x-auto">{sqlQuery}</pre>
        </div>
      )}
      
      {/* SQL Error */}
      {sqlError && (
        <div className="mb-3">
          <h4 className="text-xs uppercase tracking-wide text-red-500 mb-1">Error</h4>
          <pre className="bg-red-100 dark:bg-red-900 p-2 rounded text-sm text-red-700 dark:text-red-300 overflow-x-auto">{sqlError}</pre>
        </div>
      )}
      
      {/* SQL Result */}
      {sqlResult && (
        <div className="mb-3">
          <h4 className="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400 mb-1">Results</h4>
          <div className="bg-white dark:bg-gray-900 p-2 rounded text-sm overflow-x-auto">
            <pre>{sqlResult}</pre>
          </div>
        </div>
      )}
      
      {/* File Info */}
      {fileInfo && (
        <div className="mb-3 p-3 bg-blue-900/30 rounded">
          <h4 className="text-xs uppercase tracking-wide text-blue-400 mb-2">File Information</h4>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div>
              <span className="text-gray-400 block">Filename:</span>
              <span>{fileInfo.filename}</span>
            </div>
            <div>
              <span className="text-gray-400 block">Size:</span>
              <span>{fileInfo.rows} rows × {fileInfo.columns} columns</span>
            </div>
            <div className="col-span-2">
              <span className="text-gray-400 block mb-1">Columns:</span>
              <div className="flex flex-wrap gap-1">
                {fileInfo.column_names.map((col, idx) => (
                  <span key={idx} className="px-2 py-0.5 bg-blue-900/50 text-blue-300 rounded text-xs">{col}</span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* Message Content */}
      <div className="prose dark:prose-invert prose-sm max-w-none">
        {/* Render as HTML if from assistant and contains tags */}
        {sender === 'assistant' && content.includes('<') 
          ? <div dangerouslySetInnerHTML={{ __html: content }} />
          : content
        }
      </div>
    </div>
  );
}

export default MessageItem;