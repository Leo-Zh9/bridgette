# Bridgette Setup Instructions

## 🔐 Environment Configuration

### 1. Create your `.env` file
Copy `env.example` to `.env` and add your actual API key:

```bash
cp env.example .env
```

Then edit `.env` and replace `your_openai_api_key_here` with your actual OpenAI API key.

### 2. Install Dependencies
```bash
cd backend
pip install python-dotenv
```

### 3. Verify Configuration
The application will automatically load your API key from the `.env` file when you run it.

## 🚀 Running the Application

### Option 1: Manual Start
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend  
cd frontend
python -m http.server 8080
```

### Option 2: Batch File (Windows)
```bash
start_servers.bat
```

## 🔒 Security Features

- ✅ API keys are stored in `.env` file (not committed to git)
- ✅ `.env` file is ignored by git (see `.gitignore`)
- ✅ Configuration is validated on startup
- ✅ Example configuration provided (`env.example`)

## 📁 File Structure
```
bridgette-new/
├── .env                    # Your API keys (NOT committed to git)
├── .gitignore             # Git ignore rules
├── env.example            # Example environment file
├── SETUP.md              # This file
├── backend/
│   ├── config.py         # Configuration management
│   ├── main.py           # Main processing logic
│   └── app.py            # Flask backend
└── frontend/
    ├── index.html        # Frontend interface
    ├── script.js         # Frontend logic
    └── styles.css        # Styling
```

## 🚨 Important Security Notes

1. **Never commit your `.env` file to git**
2. **Never share your API keys publicly**
3. **Use different API keys for development and production**
4. **Rotate your API keys regularly**
