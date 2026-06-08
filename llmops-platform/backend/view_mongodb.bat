@echo off
REM Quick script to view MongoDB data
echo.
echo ================================================
echo   MongoDB Data Viewer - LLMOps Platform
echo ================================================
echo.

venv\Scripts\python.exe view_mongodb_data.py

echo.
echo ================================================
echo   Press any key to exit...
echo ================================================
pause > nul
