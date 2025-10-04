#!/bin/bash
# Production startup script for Bridgette backend

echo "Starting Bridgette Backend in Production Mode..."

# Set production environment variables
export FLASK_DEBUG=false
export FLASK_HOST=0.0.0.0

# Check if PORT is set (required for most platforms)
if [ -z "$PORT" ]; then
    echo "Warning: PORT environment variable not set, using default 5000"
    export PORT=5000
fi

echo "Starting server on port $PORT..."

# Start with gunicorn for production
cd backend
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app
