# Talon - AI Database & File Assistant Frontend

[![React](https://img.shields.io/badge/React-19.1.0-61DAFB?style=flat-square&logo=react&logoColor=white)](https://reactjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4.17-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Axios](https://img.shields.io/badge/Axios-1.9.0-5A29E4?style=flat-square&logo=axios&logoColor=white)](https://axios-http.com/)
[![jsPDF](https://img.shields.io/badge/jsPDF-3.0.1-FF6B6B?style=flat-square)](https://github.com/parallax/jsPDF)

> **Talon** is a sophisticated React-based frontend for an AI-powered database query and file analysis assistant. Built with modern web technologies, it provides an intuitive interface for natural language database interactions and intelligent file processing.

## 🚀 Features

- **🤖 AI-Powered Chat Interface** - Natural language database queries powered by Gemini AI
- **📊 Intelligent Table Display** - Structured data visualization with professional formatting
- **📄 PDF Export** - One-click export of query results to professionally formatted PDFs
- **📁 File Analysis** - Upload and analyze Excel/CSV files with AI insights
- **🌙 Dark Mode Support** - Modern dark/light theme with system preference detection
- **📱 Responsive Design** - Mobile-first design that works on all devices
- **⚡ Real-time Processing** - Instant query execution and result display
- **🔄 Session Management** - Persistent chat sessions with conversation history

## 🛠️ Tech Stack

**Core Technologies:**
- **React 19.1.0** - Modern frontend framework with latest features
- **Tailwind CSS 3.4.17** - Utility-first CSS framework for rapid styling
- **Axios 1.9.0** - Promise-based HTTP client for API communication

**PDF Generation:**
- **jsPDF 3.0.1** - Client-side PDF generation
- **jsPDF-AutoTable 5.0.2** - Professional table formatting in PDFs

**Development Tools:**
- **React Scripts 5.0.1** - Build toolchain and development server
- **PostCSS & Autoprefixer** - CSS processing and vendor prefixing

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (version 16.0 or higher)
- **npm** (version 8.0 or higher) or **yarn**
- **Backend API** - The Talon backend service running on `http://localhost:8000`

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   # Ensure your backend API is running on http://localhost:8000
   # No additional environment variables needed for frontend
   ```

4. **Start the development server**
   ```bash
   npm start
   ```

5. **Open your browser**
   ```
   Navigate to http://localhost:3000
   ```

## 💡 Usage

### Database Queries
1. **Natural Language Queries**: Type questions like "Show me top 10 employees with most overtime"
2. **Direct SQL**: Execute SQL queries directly by starting with `SELECT`
3. **View Results**: Results display in formatted tables with export options
4. **Export PDFs**: Click the "📄 Export PDF" button to generate professional reports

### File Analysis
1. **Upload Files**: Drag and drop Excel or CSV files
2. **AI Analysis**: Receive intelligent insights about your data
3. **Pattern Recognition**: Discover trends and anomalies in your datasets

### Interface Features
- **Tab Navigation**: Switch between "DB Query" and "File Analysis"
- **Theme Toggle**: Switch between dark and light modes
- **Session Management**: Clear chat history or start fresh sessions
- **API Status**: Monitor backend connectivity in real-time

## 📁 Project Structure

```
frontend/
├── public/
│   ├── index.html              # Main HTML template
│   ├── manifest.json           # PWA manifest
│   └── favicon.ico             # Application icon
├── src/
│   ├── components/             # React components
│   │   ├── ChatPanel.jsx       # Main chat interface
│   │   ├── MessageItem.jsx     # Individual message display
│   │   ├── Header.jsx          # Application header
│   │   ├── FileAnalysisPanel.jsx # File upload and analysis
│   │   ├── SqlEditor.jsx       # Direct SQL query interface
│   │   └── DatabaseSchema.jsx  # Schema visualization
│   ├── services/               # API integration
│   │   └── api.js              # HTTP client and API methods
│   ├── App.jsx                 # Root application component
│   ├── index.js                # Application entry point
│   └── index.css               # Global styles and Tailwind imports
├── package.json                # Dependencies and scripts
├── tailwind.config.js          # Tailwind CSS configuration
├── postcss.config.js           # PostCSS configuration
└── README.md                   # This file
```

## ⚙️ Configuration

### API Endpoints
The frontend connects to these backend endpoints:
- `GET /` - API status check
- `POST /db/chat` - Database chat messages
- `POST /db/clear` - Clear database sessions
- `POST /files/upload` - File upload and analysis
- `POST /files/chat` - File analysis chat
- `POST /files/clear` - Clear file sessions

### Environment Variables
No environment variables required for frontend. Backend URL is configured in `src/services/api.js`:
```javascript
baseURL: 'http://localhost:8000'
```

### Tailwind Configuration
Custom Tailwind configuration in `tailwind.config.js` includes:
- Dark mode support
- Custom color palette
- Responsive breakpoints
- Typography plugin integration

## 🔧 Development

### Available Scripts

- **`npm start`** - Start development server
- **`npm build`** - Build for production
- **`npm test`** - Run test suite
- **`npm eject`** - Eject from Create React App (⚠️ irreversible)

### Code Style
- **ES6+ JavaScript** with modern React patterns
- **Functional Components** with hooks
- **Tailwind CSS** for styling
- **Responsive Design** principles

### Browser Support
- **Chrome** (latest)
- **Firefox** (latest)
- **Safari** (latest)
- **Edge** (latest)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines
- Follow existing code style and patterns
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **"Cannot connect to backend"** | Ensure backend API is running on `http://localhost:8000` |
| **"PDF export not working"** | Check browser console for errors, ensure jsPDF libraries are loaded |
| **"Tables not displaying properly"** | Verify backend is sending `sql_table` structured data |
| **"Dark mode not working"** | Clear browser cache and reload the application |

## 📖 API Integration

The frontend integrates with the Talon backend API:

```javascript
// Example API call
import * as api from './services/api';

const response = await api.sendDbChatMessage(
  "Show me employee data",
  sessionId
);
```

Response format includes:
- `response` - AI-generated response text
- `sql_table` - Structured table data for display
- `user_question` - Original user question
- `session_id` - Chat session identifier

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs via the project issue tracker
- **Backend**: Ensure the Talon backend service is running and accessible

## 🙏 Acknowledgments

- **React Team** for the amazing framework
- **Tailwind CSS** for the utility-first approach
- **jsPDF Community** for client-side PDF generation
- **Google Gemini** for AI capabilities integration

---

**Built with ❤️ for intelligent database interactions**