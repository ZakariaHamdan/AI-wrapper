from fastapi import FastAPI, Request 
from fastapi.middleware.cors import CORSMiddleware 
import time 
 
from app.core.config import get_settings 
from app.core.logging import configure_logging 
from app.api.endpoints import register_routes 
from app.services.file_service import load_context_files 
 
# Configure logging 
logger = configure_logging(logger_name="gemini-ai-service", log_file="api.log") 
 
# Initialize settings 
settings = get_settings() 
 
# Create FastAPI app 
app = FastAPI( 
    title="Gemini AI Assistant API", 
    description="AI-powered assistant using Gemini to help with database queries and file analysis", 
    version="1.0.0" 
) 
 
# Add CORS middleware 
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
) 
 
@app.middleware("http") 
async def log_requests(request: Request, call_next): 
    """Log request information""" 
    start_time = time.time() 
    response = await call_next(request) 
    process_time = time.time() - start_time 
    path = request.url.path 
    if not path.startswith("/static") and not path.endswith("favicon.ico"): 
        logger.info(f"{request.method} {path} - Status: {response.status_code} - {process_time:.2f}s") 
    return response 
 
@app.on_event("startup") 
async def startup_event(): 
    """Load context files and initialize services on startup""" 
    file_context, file_count, _ = load_context_files() 
    app.state.db_context = file_context 
    logger.info(f"Server started - Loaded {file_count} database context files") 
 
# Register API routes 
register_routes(app) 
 
@app.get("/") 
async def root(): 
    """Root endpoint with API information""" 
    return { 
        "status": "Gemini AI Assistant API is running", 
        "version": "1.0.0", 
        "endpoints": { 
            "database": "/db/chat", 
            "file_analysis": "/files/upload" 
        } 
    } 
 
if __name__ == "__main__": 
    import uvicorn 
    uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True) 
