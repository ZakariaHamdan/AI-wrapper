// MessageItem.jsx
import React from 'react';
import { jsPDF } from 'jspdf';
import { autoTable } from 'jspdf-autotable';

function MessageItem({ message }) {
  const { sender, content, sqlQuery, sqlResult, sqlTable, sqlError, fileInfo, userQuestion } = message;

  // PDF Export Function - Uses user question instead of SQL query
  const exportToPDF = () => {
    if (!sqlTable || !sqlTable.headers || !sqlTable.rows) {
      alert('No table data available to export');
      return;
    }

    try {
      // Create new PDF document
      const doc = new jsPDF();

      // Add title
      doc.setFontSize(16);
      doc.text('Database Query Results', 14, 15);

      // Add user question instead of SQL query
      if (userQuestion) {
        doc.setFontSize(12);
        doc.text('Question:', 14, 25);

        // Split long question into multiple lines
        const questionLines = doc.splitTextToSize(userQuestion, 180);
        doc.setFontSize(10);
        doc.text(questionLines, 14, 32);

        // Calculate Y position for table based on question length
        const tableStartY = 32 + (questionLines.length * 4) + 15;

        // Add table
        autoTable(doc, {
          head: [sqlTable.headers],
          body: sqlTable.rows,
          startY: tableStartY,
          styles: {
            fontSize: 8,
            cellPadding: 3,
          },
          headStyles: {
            fillColor: [59, 130, 246], // Blue background
            textColor: 255,
            fontStyle: 'bold',
          },
          alternateRowStyles: {
            fillColor: [245, 245, 245], // Light gray for alternate rows
          },
          margin: { top: 10, right: 14, bottom: 10, left: 14 },
        });
      } else {
        // No question, start table higher
        autoTable(doc, {
          head: [sqlTable.headers],
          body: sqlTable.rows,
          startY: 30,
          styles: {
            fontSize: 8,
            cellPadding: 3,
          },
          headStyles: {
            fillColor: [59, 130, 246],
            textColor: 255,
            fontStyle: 'bold',
          },
          alternateRowStyles: {
            fillColor: [245, 245, 245],
          },
          margin: { top: 10, right: 14, bottom: 10, left: 14 },
        });
      }

      // Add footer with timestamp and row count
      const pageCount = doc.internal.getNumberOfPages();
      for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.text(
            `Generated on ${new Date().toLocaleString()} | ${sqlTable.row_count} rows`,
            14,
            doc.internal.pageSize.height - 10
        );
        doc.text(
            `Page ${i} of ${pageCount}`,
            doc.internal.pageSize.width - 30,
            doc.internal.pageSize.height - 10
        );
      }

      // Generate filename with timestamp and question context
      const timestamp = new Date().toISOString().slice(0, 19).replace(/[:]/g, '-');
      const questionContext = userQuestion
          ? userQuestion.slice(0, 30).replace(/[^a-zA-Z0-9\s]/g, '').replace(/\s+/g, '-').toLowerCase()
          : 'database-results';
      const filename = `${questionContext}-${timestamp}.pdf`;

      // Save the PDF
      doc.save(filename);

    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Error generating PDF. Please try again.');
    }
  };

  // Helper function to render structured table data
  const renderTable = (tableData) => {
    if (!tableData || !tableData.headers || !tableData.rows) {
      return <p className="text-gray-500">No table data available.</p>;
    }

    return (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead>
            <tr>
              {tableData.headers.map((header, index) => (
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
            {tableData.rows.map((row, rowIndex) => (
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
          <div className="mt-2 flex justify-between items-center text-xs text-gray-500 dark:text-gray-400">
            <span>{tableData.row_count} rows returned</span>
            {/* Export to PDF Button */}
            <button
                onClick={exportToPDF}
                className="px-3 py-1 bg-blue-600 text-white rounded text-xs hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1"
                title="Export table to PDF"
            >
              📄 Export PDF
            </button>
          </div>
        </div>
    );
  };

  // Helper function to process content for display
  const processContent = (content) => {
    if (sender === 'user') {
      return content; // User messages are always plain text
    }

    if (content.includes('<') && (content.includes('<p>') || content.includes('<b>') || content.includes('<ul>') || content.includes('<li>'))) {
      return <div dangerouslySetInnerHTML={{ __html: content }} />;
    } else {
      let processedContent = content;

      processedContent = processedContent.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      processedContent = processedContent.replace(/\*(.*?)\*/g, '<em>$1</em>');
      processedContent = processedContent.replace(/\n/g, '<br>');
      processedContent = processedContent.replace(/^[•\-\*]\s(.+)$/gm, '<li>$1</li>');
      processedContent = processedContent.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
      processedContent = processedContent.replace(/<\/ul>\s*<ul>/g, '');

      return <div dangerouslySetInnerHTML={{ __html: processedContent }} />;
    }
  };

  return (
      <div
          className={`p-4 rounded-lg max-w-3xl ${
              sender === 'user'
                  ? 'ml-auto bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100'
                  : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
          }`}
      >
        {/* User Question - Show instead of SQL Query */}
        {userQuestion && (
            <div className="mb-3">
              <h4 className="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400 mb-1">Question</h4>
              <div className="bg-blue-50 dark:bg-blue-900/30 p-3 rounded text-sm font-medium">
                {userQuestion}
              </div>
            </div>
        )}

        {/* SQL Query - Optional: Comment out to hide completely */}
        {sqlQuery && (
            <details className="mb-3">
              <summary className="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400 mb-1 cursor-pointer hover:text-gray-700 dark:hover:text-gray-200">
                SQL Query (Click to expand)
              </summary>
              <pre className="bg-gray-200 dark:bg-gray-700 p-2 rounded text-sm overflow-x-auto mt-2">{sqlQuery}</pre>
            </details>
        )}

        {/* SQL Error */}
        {sqlError && (
            <div className="mb-3">
              <h4 className="text-xs uppercase tracking-wide text-red-500 mb-1">Error</h4>
              <pre className="bg-red-100 dark:bg-red-900 p-2 rounded text-sm text-red-700 dark:text-red-300 overflow-x-auto">{sqlError}</pre>
            </div>
        )}

        {/* SQL Results - Use structured table data if available */}
        {(sqlTable || sqlResult) && (
            <div className="mb-3">
              <h4 className="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400 mb-1">Results</h4>
              <div className="bg-white dark:bg-gray-900 p-2 rounded text-sm overflow-x-auto">
                {sqlTable ? renderTable(sqlTable) : <pre>{sqlResult}</pre>}
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
          {processContent(content)}
        </div>
      </div>
  );
}

export default MessageItem;