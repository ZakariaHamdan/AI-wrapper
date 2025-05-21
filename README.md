# 🤖 Wrapper AI

<div align="center">

![Wrapper AI Logo](https://via.placeholder.com/200x200?text=Wrapper+AI)

**A powerful conversational AI assistant powered by Google's Gemini API**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![Gemini](https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

## 📋 Overview

Wrapper AI is a full-stack application that provides an intuitive interface to interact with Google's Gemini AI models. It combines a FastAPI backend with a React frontend to deliver a powerful AI assistant with two main capabilities:

- **Database Query Service** - Query SQL databases using natural language, with automatic SQL generation
- **File Analysis Service** - Upload and analyze Excel/CSV files with AI-powered insights

## ✨ Features

### Database Query Assistant
- Natural language to SQL conversion
- Automatic SQL query execution
- Interactive chat interface for database exploration
- Detailed results with rich HTML formatting
- History tracking with session management

### File Analysis Assistant
- Upload and analyze Excel (.xlsx, .xls) and CSV files
- AI-powered data insights and pattern recognition
- Statistical analysis and visualization suggestions
- Interactive Q&A about uploaded data
- Session persistence for continued analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js and npm
- SQL Server (for database queries)

### Run the Application

We provide convenient batch scripts to start the application:

```bash
# Start both backend and frontend
run-all.bat

# Start only the backend
run-backend.bat

# Start only the frontend
run-frontend.bat
```

### Manual Setup

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🏗️ Project Structure

```
wrapper-ai/
├── backend/               # FastAPI backend service
│   ├── app/               # Main application package
│   │   ├── api/           # API routes
│   │   ├── core/          # Core functionality
│   │   ├── models/        # Data models
│   │   ├── services/      # Business logic
│   │   └── utils/         # Utilities
│   ├── context/           # Database schema context files
│   ├── uploads/           # Uploaded files directory
│   ├── .env               # Environment variables
│   └── requirements.txt   # Python dependencies
├── frontend/              # React frontend
├── run-all.bat            # Script to run both services
├── run-backend.bat        # Script to run backend
└── run-frontend.bat       # Script to run frontend
```

## 🔧 Configuration

Create a `.env` file in the backend directory with the following variables:

```
# API settings
API_HOST=0.0.0.0
API_PORT=8000
BASE_URL=http://localhost:8000

# Gemini API settings
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash-001

# Database settings
DB_CONNECTION_STRING="Driver={ODBC Driver 17 for SQL Server};Server=yourserver;Database=yourdb;Trusted_Connection=yes;"

# Logging settings
LOG_LEVEL=INFO
```

## 📡 API Endpoints

### Database Query Endpoints

- `GET /db/status` - Check database connection status
- `POST /db/chat` - Send database queries and get AI-generated SQL
- `POST /db/clear` - Clear a database chat session

### File Analysis Endpoints

- `POST /files/upload` - Upload and analyze Excel/CSV files
- `POST /files/chat` - Query about uploaded file data
- `POST /files/clear` - Clear a file analysis session

## 💡 Usage Examples

### Database Queries

Example request to query the database in natural language:
```json
POST /db/chat
{
  "message": "How many users do we have in the system?",
  "session_id": null
}
```

### File Analysis

Upload an Excel file for analysis:
```
POST /files/upload
Form-data:
  - file: [your-file.xlsx]
  - session_id: (optional, for continuing a session)
```

## 🧠 How It Works

1. **Backend Services**:
   - The FastAPI backend provides separate services for database queries and file analysis
   - Each service integrates with Google's Gemini API for advanced AI capabilities
   - Sessions are maintained for continuous conversation

2. **AI Integration**:
   - The system uses Gemini's instruction-following capabilities to understand natural language
   - For database queries, it generates SQL code and executes it against your database
   - For file analysis, it processes uploaded files and extracts meaningful insights

3. **Frontend Interface**:
   - React frontend provides an intuitive chat interface for both services
   - File upload component with drag-and-drop functionality
   - Real-time response streaming and formatting

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) - Fast web framework for building APIs
- [React](https://reactjs.org/) - JavaScript library for building user interfaces
- [Google Gemini](https://ai.google.dev/) - Google's multimodal AI model
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

---

<div align="center">
  Made with ❤️ by Your Team
</div>