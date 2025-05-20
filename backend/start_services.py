import subprocess
import sys
import os

def start_services():
    """Start both the database query and file analysis services."""
    # Start the database query service
    db_query_service = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        cwd=os.path.join(os.path.dirname(__file__), "db_query_api")
    )
    
    # Start the file analysis service
    file_analysis_service = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001", "--reload"],
        cwd=os.path.join(os.path.dirname(__file__), "file_analysis_api")
    )
    
    print("Services started!")
    print("Database Query API running on http://localhost:8000")
    print("File Analysis API running on http://localhost:8001")
    
    try:
        # Keep the script running
        db_query_service.wait()
        file_analysis_service.wait()
    except KeyboardInterrupt:
        print("Stopping services...")
        db_query_service.terminate()
        file_analysis_service.terminate()
        sys.exit(0)

if __name__ == "__main__":
    start_services()