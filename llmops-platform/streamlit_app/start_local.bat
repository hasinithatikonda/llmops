@echo off
echo ================================
echo Starting Streamlit Frontend
echo ================================
echo.
echo Make sure backend is running on http://localhost:8000
echo.
echo Frontend will be available at: http://localhost:8501
echo.
echo Press Ctrl+C to stop
echo ================================
echo.

streamlit run app.py
