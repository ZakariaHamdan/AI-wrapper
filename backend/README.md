# Gemini AI Assistant Service

A FastAPI application that provides AI-powered database querying and file analysis using Google's Gemini API.

## Features

- **Database Query Service**: Query SQL databases using natural language, with automatic SQL query generation
- **File Analysis Service**: Upload and analyze Excel and CSV files with AI-powered insights
- **Unified API**: Clean and consistent API endpoints for both services
- **Session Management**: Maintains chat sessions for continuous conversation
- **File Upload**: Support for Excel and CSV file uploads

## Project Structure

```
gemini_ai_service/
├── app/                        # Main application package
│   ├── __init__.py             # Package marker
│   ├── main.py                 # FastAPI entry point
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration management
│   │   ├── gemini_client.py    # Unified Gemini AI client
│   │   └── logging.py          # Logging configuration
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── db_query.py     # Database query endpoints
│   │   │   └── file_analysis.py # File analysis endpoints
│   │   └── endpoints.py        # Route registration
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── ai_service.py       # AI processing service
│   │   ├── db_service.py       # Database service  
│   │   └── file_service.py     # File processing service
│   ├── models/                 # Schema definitions
│   │   ├── __init__.py
│   │   ├── api.py              # API request/response models
│   │   └── schemas.py          # Internal models
│   └── utils/                  # Utilities
│       ├── __init__.py
│       └── file_processor.py   # File processing utilities
├── context/                    # Context files for database schema
├── .env                        # Environment variables
├── .env.example                # Example environment config
├── requirements.txt            # Dependencies
└── README.md                   # Documentation
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration:
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

4. Create the `context` folder and add your database schema files:
   ```bash
   mkdir -p context
   # Add your .cs, .py, .sql, .json, or .ts files with database schemas
   ```

## Running the Application

```bash
python -m app.main
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000.

## API Endpoints

### Database Query

- `GET /db/status` - Check database connection status
- `POST /db/chat` - Send a database query message
- `POST /db/clear` - Clear a database chat session

### File Analysis

- `POST /files/upload` - Upload and analyze a file
- `POST /files/chat` - Send a file analysis message
- `POST /files/clear` - Clear a file analysis chat session

## Frontend Integration

The API is designed to work with the provided React frontend. The frontend connects to the API endpoints for database querying and file analysis.