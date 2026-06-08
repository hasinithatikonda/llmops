#!/bin/bash

# LLMOps Monitoring Platform - Setup Script
# This script helps you set up the project quickly

set -e

echo "🚀 LLMOps Monitoring Platform Setup"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "⚠️  Please edit .env and add your GROQ_API_KEY"
    echo ""
else
    echo "✅ .env file already exists"
fi

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker found"

# Check for Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker Compose found"
echo ""

# Ask user if they want to start services
read -p "🤔 Do you want to start all services now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🐳 Starting services with Docker Compose..."
    echo "This may take a few minutes on first run..."
    echo ""
    
    docker-compose up --build -d
    
    echo ""
    echo "✨ Services started successfully!"
    echo ""
    echo "📊 Application URLs:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend:  http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Open http://localhost:3000 in your browser"
    echo "   2. Register a new account"
    echo "   3. Start using the platform!"
    echo ""
    echo "🛑 To stop services: docker-compose down"
    echo "📋 To view logs: docker-compose logs -f"
else
    echo ""
    echo "⏭️  Skipping service start"
    echo ""
    echo "To start services later, run:"
    echo "   docker-compose up --build -d"
fi

echo ""
echo "📚 Documentation:"
echo "   Quick Start: QUICKSTART.md"
echo "   Full Docs:   README.md"
echo "   Features:    FEATURES.md"
echo ""
echo "✅ Setup complete!"
