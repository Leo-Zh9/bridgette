# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .
COPY frontend/ ./frontend/

# Create a simple static file server for frontend
RUN pip install --no-cache-dir http-server

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_DEBUG=false
ENV FLASK_HOST=0.0.0.0
ENV PORT=5000

# Run the application
CMD ["python", "wsgi.py"]
