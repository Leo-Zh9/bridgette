# Bridgette - Intelligent Financial Data Processing Platform

<div align="center">
  <img src="frontend/images/BridgetteLogo.png" alt="Bridgette Logo" width="120" height="120">
  <h3>Bridgette - Your Trusted Financial Platform for Modern Banking Solutions</h3>
  <p><em>Intelligent schema mapping and data processing for financial institutions</em></p>
</div>

---

## 🌟 Overview

**Bridgette** is a comprehensive financial data processing platform designed to bridge the gap between traditional banking and modern digital solutions. It provides secure, efficient, and user-friendly banking services with AI-powered schema matching capabilities.

### 🎯 Key Features

- **🤖 AI-Powered Schema Matching**: Uses OpenAI API for intelligent mapping between different bank data formats
- **📊 Multi-Format Support**: Handles CSV, Excel (.xlsx, .xls) files with up to 50MB per file
- **🔄 Real-Time Processing**: Live file upload with immediate feedback and progress tracking
- **📱 Responsive Design**: Beautiful, modern UI that works on desktop, tablet, and mobile
- **🛡️ Secure Processing**: Local file processing with no data transmission to third parties
- **⚡ Fallback Mechanisms**: Reliable operation even when AI services are unavailable
- **📈 Excel Generation**: Creates unified Excel files from processed data
- **🎨 Modern UI/UX**: Smooth animations, drag-and-drop uploads, and intuitive navigation

---

## 🏗️ Architecture

### Backend (Python Flask)
- **API Server**: RESTful endpoints for file processing and data management
- **Schema Analysis**: Intelligent mapping between different bank data formats
- **OpenAI Integration**: AI-powered schema matching and data processing
- **File Management**: Organized storage with bank-specific directories
- **Excel Generation**: Creates unified output files with customer data consolidation

### Frontend (Vanilla HTML/CSS/JavaScript)
- **Responsive Design**: Mobile-first approach with modern CSS Grid and Flexbox
- **Interactive UI**: Drag-and-drop file uploads with real-time feedback
- **API Communication**: Seamless backend integration with error handling
- **Progressive Enhancement**: Works without JavaScript for basic functionality
- **Cache Management**: Intelligent caching with version control for updates

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** with pip
- **Node.js 18+** (for development tools)
- **OpenAI API Key** (for AI features)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

### 1. Clone and Setup
   ```bash
# Clone the repository
git clone https://github.com/your-username/bridgette.git
   cd bridgette

   # Install Python dependencies
   cd backend
   pip install -r requirements.txt
   cd ..
   
# Install Node.js dependencies (optional, for development)
   npm install
   ```

### 2. Environment Configuration
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
```

### 3. Start the Application

#### Option A: Automated Start (Recommended)
   ```bash
# Windows
start_servers.bat

# Linux/Mac
./start_servers.sh
```

#### Option B: Manual Start
```bash
# Terminal 1: Backend Server
cd backend
python app.py

# Terminal 2: Frontend Server
cd frontend
python -m http.server 8080
```

### 4. Access the Application
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5001
- **Health Check**: http://localhost:5001/api/health

---

## 📋 Usage Guide

### 1. Upload Schema Files
- **Bank Schema Files**: Upload schema files that define the mapping between different bank formats
- **Drag & Drop**: Simply drag files onto the upload areas
- **Multiple Files**: Upload multiple schema files for comprehensive mapping

### 2. Upload Data Files
- **Regular Data Files**: Upload your actual financial data files
- **Format Support**: CSV, Excel (.xlsx, .xls) files
- **File Size**: Up to 50MB per file
- **Unlimited Count**: Upload as many files as needed

### 3. Process and Merge
- **AI Processing**: The system uses OpenAI API to intelligently match schemas
- **Fallback Mode**: If AI is unavailable, uses rule-based matching
- **Real-Time Feedback**: Progress indicators and status updates
- **Error Handling**: Clear error messages and recovery suggestions

### 4. Download Results
- **Excel Output**: Download unified Excel file with processed data
- **Customer Consolidation**: Data is merged and organized by customer
- **Automatic Cleanup**: Files are automatically cleaned up after download

---

## 🔧 API Endpoints

### Core Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check and server status |
| `POST` | `/api/process-files` | Upload and process files |
| `POST` | `/api/trigger-main-processing` | Start AI-powered processing |
| `POST` | `/api/download-files` | Get download link for processed files |
| `GET` | `/api/download-excel/<filename>` | Download specific Excel file |

### File Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/uploaded-files` | List all uploaded files |
| `GET` | `/api/uploaded-files/<filename>` | Get specific file info |
| `DELETE` | `/api/uploaded-files/<filename>` | Delete uploaded file |
| `POST` | `/api/cleanup-json-files` | Clean up temporary files |

### Query Parameters
- `?schema=true` - Process as schema files
- `?box=1` or `?box=2` - Specify upload box (bank1 or bank2)

---

## 🛠️ Development

### Project Structure
```
bridgette/
├── 📁 backend/                    # Backend API server
│   ├── 📄 app.py                 # Main Flask application
│   ├── 📄 main.py                # Core processing logic
│   ├── 📄 config.py              # Configuration management
│   ├── 📄 requirements.txt       # Python dependencies
│   ├── 📄 wsgi.py                # WSGI configuration
│   └── 📁 uploaded_files/        # File storage
│       ├── 📁 bank1/             # Bank 1 files
│       └── 📁 bank2/             # Bank 2 files
├── 📁 frontend/                  # Frontend application
│   ├── 📄 index.html             # Main HTML file
│   ├── 📄 script.js              # JavaScript functionality
│   ├── 📄 styles.css             # CSS styles
│   ├── 📄 server.py              # Development server
│   └── 📁 images/                # Assets
├── 📁 schema_analysis/           # Schema analysis results
├── 📄 .env                       # Environment variables
├── 📄 docker-compose.yml         # Docker configuration
├── 📄 Dockerfile                 # Docker image
└── 📄 README.md                  # This file
```

### Development Commands
```bash
# Start development servers
npm run dev

# Run backend only
cd backend && python app.py

# Run frontend only
cd frontend && python server.py

# Run with cache-busting
cd frontend && python server.py

# Install dependencies
pip install -r backend/requirements.txt
npm install
```

### Code Quality
- **Comprehensive Comments**: All code is thoroughly documented
- **Error Handling**: Graceful error handling with user feedback
- **Type Safety**: Python type hints where applicable
- **Security**: Input validation and sanitization
- **Performance**: Optimized for large file processing

---

## 🚀 Deployment

### Vercel Deployment (Recommended)
```bash
# 1. Connect GitHub repository to Vercel
# 2. Set environment variables in Vercel dashboard:
#    - OPENAI_API_KEY=your_key_here
#    - FLASK_DEBUG=false
# 3. Deploy automatically
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t bridgette .
docker run -p 5000:5000 bridgette
```

### Traditional Hosting
   ```bash
# 1. Upload files to your hosting provider
# 2. Install Python dependencies
   pip install -r backend/requirements.txt

# 3. Configure WSGI using backend/wsgi.py
# 4. Set environment variables
export FLASK_DEBUG=false
export PORT=5000
```

### Environment Variables
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | - | Yes |
| `FLASK_DEBUG` | Enable debug mode | `false` | No |
| `FLASK_HOST` | Host to bind to | `0.0.0.0` | No |
| `PORT` | Port to run on | `5001` | No |

---

## 🔒 Security & Privacy

### Data Protection
- **Local Processing**: All data processing happens locally
- **No Data Storage**: Files are processed and immediately cleaned up
- **Secure API Keys**: Environment variable management
- **Input Validation**: Comprehensive file type and size validation
- **Error Handling**: Secure error messages without data exposure

### Privacy Features
- **No Third-Party Tracking**: No analytics or tracking scripts
- **Local File Handling**: Files never leave your server
- **Automatic Cleanup**: Temporary files are automatically removed
- **Secure Headers**: CORS and security headers configured

---

## 🐛 Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.11+

# Install dependencies
pip install -r backend/requirements.txt

# Check environment variables
echo $OPENAI_API_KEY
```

#### Frontend Not Loading
```bash
# Clear browser cache
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)

# Use cache-busting server
cd frontend && python server.py
```

#### File Upload Issues
- **File Size**: Ensure files are under 50MB
- **File Format**: Only CSV, Excel (.xlsx, .xls) supported
- **Browser Compatibility**: Use modern browsers (Chrome, Firefox, Safari, Edge)

#### AI Processing Errors
- **API Key**: Verify OpenAI API key is set correctly
- **Network**: Check internet connection for API calls
- **Fallback**: System will use rule-based matching if AI fails

### Debug Mode
```bash
# Enable debug mode
export FLASK_DEBUG=True

# Check logs
tail -f backend/logs/app.log
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Follow the existing code style
4. **Add tests**: Ensure your changes work correctly
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**: Describe your changes clearly

### Development Guidelines
- **Code Comments**: Add comprehensive comments for new code
- **Error Handling**: Include proper error handling and user feedback
- **Testing**: Test your changes thoroughly
- **Documentation**: Update documentation for new features

---

## 📄 License

This project is licensed under the **ISC License** - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support & Contact

### Getting Help
- **GitHub Issues**: [Create an issue](https://github.com/your-username/bridgette/issues)
- **Documentation**: Check this README and inline code comments
- **Email**: info@bridgette.com
- **Phone**: (647) 390 4658

### Business Inquiries
- **Address**: 145 Columbia St W, Waterloo, ON N2L 3J5
- **Email**: info@bridgette.com
- **Website**: [bridgette.com](https://bridgette.com)

---

## 🙏 Acknowledgments

- **OpenAI**: For providing intelligent schema matching capabilities
- **Flask Community**: For the excellent web framework
- **Pandas Team**: For powerful data processing capabilities
- **Font Awesome**: For beautiful icons
- **Contributors**: All developers who have contributed to this project

---

<div align="center">
  <p><strong>Bridgette</strong> - Bridging the gap between traditional banking and modern digital solutions</p>
  <p>Made with ❤️ for the financial community</p>
</div>