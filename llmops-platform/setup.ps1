# LLMOps Monitoring Platform - Setup Script (PowerShell)
# This script helps you set up the project quickly on Windows

Write-Host "🚀 LLMOps Monitoring Platform Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ .env file created" -ForegroundColor Green
    Write-Host "⚠️  Please edit .env and add your GROQ_API_KEY" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Check for Docker
try {
    docker --version | Out-Null
    Write-Host "✅ Docker found" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "   Visit: https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Yellow
    exit 1
}

# Check for Docker Compose
try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose found" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose is not installed." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Ask user if they want to start services
$response = Read-Host "🤔 Do you want to start all services now? (y/n)"

if ($response -eq "y" -or $response -eq "Y") {
    Write-Host ""
    Write-Host "🐳 Starting services with Docker Compose..." -ForegroundColor Cyan
    Write-Host "This may take a few minutes on first run..." -ForegroundColor Yellow
    Write-Host ""
    
    docker-compose up --build -d
    
    Write-Host ""
    Write-Host "✨ Services started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Application URLs:" -ForegroundColor Cyan
    Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
    Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
    Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "📝 Next steps:" -ForegroundColor Cyan
    Write-Host "   1. Open http://localhost:3000 in your browser" -ForegroundColor White
    Write-Host "   2. Register a new account" -ForegroundColor White
    Write-Host "   3. Start using the platform!" -ForegroundColor White
    Write-Host ""
    Write-Host "🛑 To stop services: docker-compose down" -ForegroundColor Yellow
    Write-Host "📋 To view logs: docker-compose logs -f" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "⏭️  Skipping service start" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To start services later, run:" -ForegroundColor Cyan
    Write-Host "   docker-compose up --build -d" -ForegroundColor White
}

Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   Quick Start: QUICKSTART.md" -ForegroundColor White
Write-Host "   Full Docs:   README.md" -ForegroundColor White
Write-Host "   Features:    FEATURES.md" -ForegroundColor White
Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
