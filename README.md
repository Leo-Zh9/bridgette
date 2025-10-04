# Bridgette - Financial Platform

A modern financial platform for dataset mapping and file processing.

## Features

- **File Upload & Processing**: Upload CSV and Excel files to view the first three lines
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Cross-Platform**: Works on desktop and mobile devices
- **Multiple Deployment Options**: Local, Vercel, Docker, and more

## Tech Stack

- **Backend**: Python Flask with CORS support
- **Frontend**: Vanilla HTML, CSS, JavaScript
- **File Processing**: Pandas for CSV/Excel handling
- **Deployment**: Vercel, Docker, or traditional hosting

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Leo-Zh9/bridgette.git
   cd bridgette
   ```

2. **Install dependencies**
   ```bash
   # Install Python dependencies
   cd backend
   pip install -r requirements.txt
   cd ..
   
   # Install Node.js dependencies
   npm install
   ```

3. **Start the application**
   ```bash
   # Option 1: Use the batch files (Windows)
   start_bridgette.bat
   
   # Option 2: Use npm scripts
   npm run start:full
   
   # Option 3: Start manually
   # Terminal 1: Backend
   cd backend && python app.py
   
   # Terminal 2: Frontend
   npm run dev:frontend
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

### Docker Development

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
```

## Deployment

### Vercel Deployment (Recommended)

1. **Connect your GitHub repository to Vercel**
2. **Deploy automatically** - Vercel will detect the configuration from `vercel.json`
3. **Set environment variables** in Vercel dashboard:
   - `FLASK_DEBUG=false`

### Docker Deployment

```bash
# Build the Docker image
docker build -t bridgette .

# Run the container
docker run -p 5000:5000 bridgette
```

### Traditional Hosting

1. **Upload files** to your hosting provider
2. **Install Python dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. **Configure WSGI** using `backend/wsgi.py`
4. **Set environment variables**:
   - `FLASK_DEBUG=false`
   - `PORT=5000`

## API Endpoints

- `POST /api/process-files` - Process uploaded files
- `GET /api/health` - Health check

## File Support

- **CSV files** (.csv)
- **Excel files** (.xlsx, .xls)
- **Maximum file size**: 50MB per file
- **Unlimited file count**: Upload any number of files

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_DEBUG` | Enable debug mode | `false` |
| `FLASK_HOST` | Host to bind to | `0.0.0.0` |
| `PORT` | Port to run on | `5000` |

## Project Structure

```
bridgette/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── app_simple.py       # Simplified version (CSV only)
│   ├── wsgi.py             # WSGI configuration for production
│   ├── requirements.txt    # Python dependencies
│   └── env.example         # Environment variables example
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── script.js           # JavaScript functionality
│   └── styles.css          # CSS styles
├── vercel.json             # Vercel deployment configuration
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose for local development
├── package.json            # Node.js dependencies and scripts
└── README.md               # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

This project is licensed under the ISC License.

## Support

For issues and questions:
- Create an issue on GitHub
- Email: info@bridgette.com
