import React from 'react';

function DatabaseSchema({ schema }) {
  if (!schema || !schema.tables || !schema.tables.length) {
    return (
      <div className="p-4 bg-yellow-50 dark:bg-yellow-900 rounded-md">
        <p className="text-yellow-700 dark:text-yellow-300">
          No database schema information available. Please check your connection.
        </p>
      </div>
    );
  }
  
  return (
    <div>
      <h2 className="text-lg font-medium mb-4">Database Schema</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {schema.tables.map((table, tableIndex) => (
          <div 
            key={tableIndex}
            className="border rounded-md overflow-hidden dark:border-gray-700"
          >
            <div className="bg-gray-100 dark:bg-gray-800 px-4 py-2 font-medium">
              {table.name}
            </div>
            
            <ul className="divide-y divide-gray-200 dark:divide-gray-700">
              {table.columns && table.columns.map((column, columnIndex) => (
                <li 
                  key={columnIndex}
                  className="px-4 py-2 flex justify-between items-center"
                >
                  <span className="text-sm">{column.name}</span>
                  <span className="text-xs text-gray-500 dark:text-gray-400">{column.type}</span>
                </li>
              ))}
              
              {/* If no columns data is available */}
              {(!table.columns || table.columns.length === 0) && (
                <li className="px-4 py-2 text-sm text-gray-500 dark:text-gray-400">
                  No column information available
                </li>
              )}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DatabaseSchema;