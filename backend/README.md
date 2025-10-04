# Bridgette Backend

Python Flask backend for processing uploaded files and extracting first lines.

## Setup Instructions

### 1. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Backend Server
```bash
python app.py
```

The backend will start on `http://localhost:5000`

## API Endpoints

### POST /api/process-files
Processes uploaded files and returns the first line of each file.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: files (multiple files allowed)

**Response:**
```json
{
    "success": true,
    "result": "filename1.csv: col1 col2 col3 filename2.xlsx: data1 data2 data3",
    "file_count": 2
}
```

### GET /api/health
Health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "message": "Bridgette backend is running"
}
```

## Supported File Types

- CSV (.csv)
- Excel (.xlsx, .xls)
- JSON (.json)

## File Size Limit

Maximum file size: 10MB per file

## Features

- Reads first line/row from CSV files
- Reads first row from Excel files
- Reads first object/entry from JSON files
- Combines all first lines with spaces
- Handles file validation and error reporting
- Temporary file cleanup

