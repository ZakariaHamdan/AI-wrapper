# 🤖 Talon - AI Database & File Assistant

<div align="center">

![Talon AI Logo](https://via.placeholder.com/200x200?text=Talon+AI)

**A powerful conversational AI assistant powered by Google's Gemini API**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.1.0-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![Gemini](https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tailwind](https://img.shields.io/badge/Tailwind-3.4.17-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

</div>

## 📋 Overview

Talon is a sophisticated full-stack application that provides an intuitive interface to interact with Google's Gemini AI models. It combines a FastAPI backend with a modern React frontend to deliver a powerful AI assistant with advanced data intelligence capabilities:

- **🗃️ Database Query Service** - Query SQL databases using natural language with automatic SQL generation and professional table display
- **📊 File Analysis Service** - Upload and analyze Excel/CSV files with AI-powered insights and pattern recognition
- **📄 PDF Export** - Generate professional reports with one-click PDF export functionality
- **🎨 Modern UI** - Dark mode support, responsive design, and intuitive chat interface

## ✨ Features

### 🗃️ Database Query Assistant
- **Natural Language Processing** - Convert plain English to precise SQL queries
- **Intelligent Query Execution** - Automatic SQL generation and execution
- **Professional Table Display** - Structured data visualization with clean formatting
- **PDF Report Generation** - Export query results with original questions and metadata
- **Session Management** - Persistent chat history and context awareness
- **Error Handling** - Smart error detection with alternative query suggestions

### 📊 File Analysis Assistant
- **Smart File Upload** - Drag-and-drop support for Excel (.xlsx, .xls) and CSV files
- **AI-Powered Insights** - Advanced pattern recognition and statistical analysis
- **Interactive Q&A** - Continuous conversation about uploaded data
- **Data Quality Assessment** - Automatic validation and recommendations
- **Visual Summaries** - Rich HTML formatting with key metrics highlighted

### 🎨 Modern Interface
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Dark Mode Support** - Comfortable viewing in any environment
- **Real-time Processing** - Instant query execution and response generation
- **Professional Styling** - Clean, modern UI built with Tailwind CSS
- **Export Options** - One-click PDF generation with professional formatting

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** with pip
- **Node.js 16+** and npm
- **SQL Server** (for database queries)
- **Google Gemini API Key** ([Get one here](https://ai.google.dev/))

### ⚡ Run the Application

We provide convenient batch scripts to start the application:

```bash
# Start both backend and frontend (Recommended)
run-all.bat

# Start only the backend
run-backend.bat

# Start only the frontend  
run-frontend.bat
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 🔧 Manual Setup

<details>
<summary>Click to expand manual setup instructions</summary>

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Configure environment (copy .env.example to .env and edit)
copy .env.example .env

# Start the backend
python -m app.main
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

</details>

## 🏗️ Project Structure

```
Wrapper AI/
├── 📁 backend/                 # FastAPI backend service
│   ├── 📁 app/                 # Main application package
│   │   ├── 📁 api/             # API routes and endpoints
│   │   │   └── 📁 routes/      # Database and file analysis routes
│   │   ├── 📁 core/            # Core functionality
│   │   │   ├── config.py       # Application configuration
│   │   │   ├── gemini_client.py # Gemini AI integration
│   │   │   └── logging.py      # Logging configuration
│   │   ├── 📁 models/          # Pydantic data models
│   │   ├── 📁 services/        # Business logic services
│   │   │   ├── ai_service.py   # AI processing service
│   │   │   ├── db_service.py   # Database operations
│   │   │   └── file_service.py # File processing
│   │   └── 📁 utils/           # Utility functions
│   ├── 📁 context/             # Database schema context files
│   ├── 📁 uploads/             # Uploaded files directory
│   ├── 📄 .env                 # Environment variables
│   ├── 📄 .env.example         # Environment template
│   ├── 📄 requirements.txt     # Python dependencies
│   └── 📄 README.md            # Backend documentation
├── 📁 frontend/                # React frontend application
│   ├── 📁 public/              # Static assets
│   ├── 📁 src/                 # Source code
│   │   ├── 📁 components/      # React components
│   │   │   ├── ChatPanel.jsx   # Main chat interface
│   │   │   ├── MessageItem.jsx # Message display with PDF export
│   │   │   ├── Header.jsx      # Application header
│   │   │   └── FileAnalysisPanel.jsx # File upload interface
│   │   └── 📁 services/        # API integration
│   ├── 📄 package.json         # Node.js dependencies
│   └── 📄 README.md            # Frontend documentation
├── 📄 run-all.bat              # Script to run both services
├── 📄 run-backend.bat          # Script to run backend only
├── 📄 run-frontend.bat         # Script to run frontend only
├── 📄 .gitignore               # Git ignore rules
└── 📄 README.md                # This file
```

## 🔧 Configuration

Create a `.env` file in the backend directory with the following variables:

```env
# API settings
API_HOST=0.0.0.0
API_PORT=8000
BASE_URL=http://localhost:8000

# Gemini AI settings
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash-001

# Database settings (SQL Server)
DB_CONNECTION_STRING="Driver={ODBC Driver 17 for SQL Server};Server=yourserver;Database=yourdb;Trusted_Connection=yes;"

# Logging settings
LOG_LEVEL=INFO
```

### 🗄️ Database Schema Setup

Place your database schema files in the `backend/context/` directory:
- **`.cs` files** - Entity Framework models
- **`.sql` files** - Database schemas  
- **`.json` files** - Schema definitions
- **`.py` files** - SQLAlchemy models

Talon will automatically load and use these for intelligent query generation.

## 📡 API Endpoints

### Database Query Endpoints

- `GET /db/status` - Check database connection status
- `POST /db/chat` - Send natural language queries and get AI-generated SQL with structured results
- `POST /db/clear` - Clear a database chat session

### File Analysis Endpoints

- `POST /files/upload` - Upload and analyze Excel/CSV files with AI insights
- `POST /files/chat` - Interactive Q&A about uploaded file data
- `POST /files/clear` - Clear a file analysis session

### Enhanced Response Format

The API now returns structured data perfect for table display and PDF export:

```json
{
  "response": "AI analysis in HTML format",
  "session_id": "uuid-session-id",
  "has_sql": true,
  "sql_query": "SELECT * FROM Employees...",
  "sql_table": {
    "headers": ["EmployeeId", "Name", "Department"],
    "rows": [[1, "John Doe", "Engineering"]],
    "row_count": 1
  },
  "user_question": "Show me all employees"
}
```

## 💡 Usage Examples

### 🗃️ Database Queries

**Natural Language Query:**
```json
POST /db/chat
{
  "message": "Show me the top 10 employees with most overtime hours",
  "session_id": null
}
```

**Response includes:**
- AI-generated analysis in HTML
- Executable SQL query
- Structured table data ready for display
- Professional PDF export capability

### 📊 File Analysis

**Upload Excel file for analysis:**
```bash
POST /files/upload
Form-data:
  - file: employee_data.xlsx
  - session_id: (optional)
```

**Follow-up questions:**
```json
POST /files/chat
{
  "message": "What trends do you see in the overtime data?",
  "session_id": "existing-session-id"
}
```

### 📄 PDF Export

Users can export any query result as a professional PDF containing:
- **Original Question** - The user's natural language query
- **Formatted Data Table** - Clean, professional table layout
- **Metadata** - Timestamp, row count, and session information
- **Automatic Naming** - Files named based on the question content

## 🧠 How It Works

1. **🎯 User Interaction**:
   - Users ask questions in natural language through the React frontend
   - Talon's chat interface provides real-time feedback and professional styling

2. **🤖 AI Processing**:
   - Gemini AI analyzes the question and database schema context
   - Generates precise SQL queries or provides file analysis insights
   - Returns both human-readable responses and structured data

3. **📊 Data Presentation**:
   - Frontend receives structured table data for optimal display
   - Users can interact with results, ask follow-up questions
   - One-click PDF export generates professional reports

4. **💾 Session Management**:
   - Conversations maintain context across multiple interactions
   - Each service (database/file) manages independent sessions
   - Users can clear sessions or start fresh conversations anytime

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Google Gemini AI** - Advanced multimodal AI model for natural language processing
- **Pydantic** - Data validation and serialization
- **PyODBC** - Database connectivity for SQL Server
- **Python 3.9+** - Core backend language

### Frontend  
- **React 19.1.0** - Latest React with modern features
- **Tailwind CSS 3.4.17** - Utility-first CSS framework
- **Axios** - HTTP client for API communication
- **jsPDF + AutoTable** - Client-side PDF generation
- **Modern JavaScript** - ES6+ with latest browser features

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Backend won't start** | Check Python version (3.9+) and `pip install -r requirements.txt` |
| **Frontend build fails** | Verify Node.js 16+ and run `npm install` in frontend directory |
| **Database connection errors** | Verify `DB_CONNECTION_STRING` in `.env` file |
| **Gemini API errors** | Check `GEMINI_API_KEY` and API quota limits |
| **PDF export not working** | Clear browser cache, ensure jsPDF libraries loaded |

### 🔍 Quick Diagnostics

```bash
# Check if services are running
curl http://localhost:8000/          # Backend health
curl http://localhost:3000/          # Frontend health

# View detailed logs
tail -f backend/api.log              # Backend logs
```

## 📚 Documentation

- **[Backend API Documentation](./backend/README.md)** - FastAPI, Gemini AI integration, database services
- **[Frontend Documentation](./frontend/README.md)** - React components, PDF export, UI features  
- **[Interactive API Docs](http://localhost:8000/docs)** - Swagger UI when backend is running

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- **[Google Gemini](https://ai.google.dev/)** - Advanced AI capabilities for natural language processing
- **[FastAPI](https://fastapi.tiangolo.com/)** - Fast, modern web framework for building APIs
- **[React](https://reactjs.org/)** - Powerful JavaScript library for building user interfaces  
- **[Tailwind CSS](https://tailwindcss.com/)** - Beautiful utility-first CSS framework
- **[jsPDF Community](https://github.com/parallax/jsPDF)** - Client-side PDF generation capabilities

---

<div align="center">

**🚀 Ready to transform your data interactions with AI?**

Made with ❤️ by the Talon Team

</div>