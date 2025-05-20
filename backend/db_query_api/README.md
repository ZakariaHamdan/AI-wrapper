# Wrapper AI Backend

This is a dual-service backend system that provides AI-powered database query and file analysis capabilities using Google's Gemini API.

## Services

### 1. Database Query API (Port 8000)
- SQL querying with AI interpretation
- Context-aware database schema understanding
- Direct SQL query execution or AI-generated queries

### 2. File Analysis API (Port 8001)
- Excel and CSV file analysis
- AI-powered insights and data visualization suggestions
- Interactive chat about uploaded data

## Directory Structure

```
backend/
├── core/                   # Shared core functionality
│   ├── config.py           # Configuration loader
│   ├── file_processor.py   # File processing utilities
│   ├── gemini_base.py      # Gemini AI client setup
│   └── __init__.py         # Package initialization
├── db_query_api/           # Database Query service
│   ├── .env                # Environment variables
│   ├── ai_service.py       # Gemini AI integration
│   ├── app.py              # FastAPI application
│   ├── db_service.py       # Database operations
│   ├── file_service.py     # Context file handling
│   ├── models.py           # Data models
│   ├── __init__.py         # Package initialization
│   └── requirements.txt    # Dependencies
├── file_analysis_api/      # File Analysis service
│   ├── .env                # Environment variables
│   ├── ai_service.py       # Gemini AI integration
│   ├── app.py              # FastAPI application
│   ├── models.py           # Data models
│   ├── __init__.py         # Package initialization
│   └── requirements.txt    # Dependencies
└── start_services.py       # Service starter script
```

## Setup

1. Install dependencies for each service:
   ```
   pip install -r db_query_api/requirements.txt
   pip install -r file_analysis_api/requirements.txt
   ```

2. Set up your environment variables:
   - Create/update `.env` files in both service directories
   - Configure your Gemini API key
   - Set database connection string (for DB Query API)

3. Create a `context` folder in the db_query_api directory (optional):
   - Add database schema files (.cs, .py, .sql, .json, .ts)
   - These will be used to provide context to the AI

## Running the Services

Start both services with a single command:
```
python start_services.py
```

This will launch:
- Database Query API on http://localhost:8000
- File Analysis API on http://localhost:8001

## API Endpoints

### Database Query API

- `GET /` - API status
- `GET /config` - Frontend configuration
- `GET /context` - Context file information
- `POST /chat` - Chat with the database assistant
- `POST /clear` - Clear chat session
- `POST /upload` - Upload a file for database schema context

### File Analysis API

- `GET /` - API status
- `GET /config` - Frontend configuration  
- `POST /chat` - Chat about uploaded file
- `POST /clear` - Clear chat session
- `POST /upload` - Upload Excel/CSV file for analysis

## Security Note

⚠️ **IMPORTANT**: In a production environment:
- Replace the placeholder API key with a secure one
- Restrict CORS origins to specific domains
- Implement proper authentication 
- Use HTTPS with valid certificates
- Secure database credentials