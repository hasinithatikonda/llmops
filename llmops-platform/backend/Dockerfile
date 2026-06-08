FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create chroma directory
RUN mkdir -p /app/chroma_db

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)" && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000
