@echo off
echo.
echo ===============================================
echo Starting LLMOps Backend with MongoDB
echo ===============================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment and run MongoDB-enabled backend
echo Starting backend on http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

venv\Scripts\python.exe app/main_mongo.py

pause
