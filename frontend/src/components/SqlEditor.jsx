import React, { useState } from 'react';
import * as api from '../services/api';

function SqlEditor() {
  const [query, setQuery] = useState('SELECT * FROM Users LIMIT 10;');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const executeQuery = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    setResult(null);
    setError(null);
    
    try {
      const response = await api.executeSqlQuery(query);
      setResult(response.sql_result);
      
      if (response.sql_error) {
        setError(response.sql_error);
      }
    } catch (error) {
      console.error('Error executing query:', error);
      setError('Failed to execute query. Check your syntax or connection.');
    } finally {
      setLoading(false);
    }
  };
  
  const formatSqlResults = (results) => {
    if (!results) return <p className="text-gray-500">No results to display.</p>;
    
    try {
      // Split results into lines
      const lines = results.trim().split('\n');
      if (lines.length < 2) return <pre>{results}</pre>;
      
      // Extract headers from first line
      const headers = lines[0].trim().split(/\s\s+/).map(h => h.trim());
      
      // Process data rows (skip header)
      const rows = [];
      for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim();
        
        // Skip empty lines or row count information
        if (!line || line.includes('rows returned') || line.startsWith('--')) {
          continue;
        }
        
        // Split by multiple spaces
        const cells = line.split(/\s\s+/);
        if (cells.length > 0) {
          rows.push(cells);
        }
      }
      
      return (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead>
              <tr>
                {headers.map((header, index) => (
                  <th 
                    key={index}
                    className="px-6 py-3 bg-gray-50 dark:bg-gray-800 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
                  >
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
              {rows.map((row, rowIndex) => (
                <tr key={rowIndex} className={rowIndex % 2 === 0 ? '' : 'bg-gray-50 dark:bg-gray-800'}>
                  {row.map((cell, cellIndex) => (
                    <td 
                      key={cellIndex}
                      className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-200"
                    >
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    } catch (error) {
      console.error('Error formatting SQL results:', error);
      return <pre className="whitespace-pre-wrap">{results}</pre>;
    }
  };
  
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-medium mb-2">SQL Editor</h2>
        <div className="bg-gray-50 dark:bg-gray-800 rounded-md overflow-hidden">
          <textarea
            className="w-full p-4 font-mono text-sm focus:outline-none bg-gray-50 dark:bg-gray-800 dark:text-gray-200"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={5}
            placeholder="Enter your SQL query here..."
          />
        </div>
        <div className="mt-2 flex justify-end">
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
            onClick={executeQuery}
            disabled={loading}
          >
            {loading ? 'Executing...' : 'Execute Query'}
          </button>
        </div>
      </div>
      
      {error && (
        <div className="bg-red-50 dark:bg-red-900 p-4 rounded-md">
          <h3 className="text-md font-medium text-red-800 dark:text-red-300 mb-2">Error</h3>
          <pre className="text-sm text-red-700 dark:text-red-300 whitespace-pre-wrap font-mono">{error}</pre>
        </div>
      )}
      
      {result && (
        <div>
          <h3 className="text-md font-medium mb-2">Results</h3>
          {formatSqlResults(result)}
        </div>
      )}
    </div>
  );
}

export default SqlEditor;