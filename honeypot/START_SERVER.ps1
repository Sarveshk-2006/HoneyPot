# Start Agentic Honeypot Server - PowerShell Version
# This script starts the FastAPI server and shows the URLs

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     AGENTIC HONEYPOT - SCAM DETECTION SYSTEM              ║" -ForegroundColor Cyan
Write-Host "║     Starting Production Server...                         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Change to project directory
Set-Location -Path "D:\Buildathon\honeypot"

Write-Host "📦 Activating Python environment..." -ForegroundColor Yellow
. .\venv\Scripts\Activate.ps1

Write-Host "✅ Environment activated" -ForegroundColor Green
Write-Host ""

Write-Host "🚀 Starting FastAPI server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📍 API Endpoints:" -ForegroundColor Green
Write-Host "   🔵 Main API:      http://localhost:8000" -ForegroundColor Cyan
Write-Host "   📖 Swagger Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "   📚 ReDoc:         http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 In another terminal, you can run:" -ForegroundColor Yellow
Write-Host "   • Test API:     python test_api.py" -ForegroundColor Gray
Write-Host "   • Monitor:      python monitor.py" -ForegroundColor Gray
Write-Host "   • Tests:        pytest tests/test_honeypot.py -v" -ForegroundColor Gray
Write-Host ""
Write-Host "⏹️  Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level info

Write-Host ""
Write-Host "✅ Server stopped." -ForegroundColor Green
