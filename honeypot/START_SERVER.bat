@echo off
REM Start Agentic Honeypot Server - Production Ready
REM This script starts the FastAPI server on port 8000

echo.
echo =====================================================
echo   AGENTIC HONEYPOT - SCAM DETECTION SYSTEM
echo   Starting Production Server...
echo =====================================================
echo.

cd /d D:\Buildathon\honeypot

echo 📦 Checking Python environment...
call venv\Scripts\activate.bat

echo.
echo 🚀 Starting FastAPI server...
echo    Server: http://localhost:8000
echo    Docs:   http://localhost:8000/docs
echo    ReDoc:  http://localhost:8000/redoc
echo.
echo Press CTRL+C to stop the server
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
