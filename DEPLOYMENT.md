# Bridgette - Production Deployment Guide

## 🚀 **Production-Ready Backend Setup**

Your Bridgette backend is now configured to work on **any platform** (Render, Railway, Heroku, DigitalOcean, etc.) with these key fixes:

### ✅ **What's Fixed:**

1. **Dynamic PORT handling** - Uses `os.environ.get("PORT", 5000)`
2. **Production WSGI server** - Gunicorn included in requirements.txt
3. **CORS enabled** - Works with any frontend domain
4. **Environment detection** - Automatically switches between dev/production
5. **Platform-specific configs** - Ready for multiple deployment platforms

---

## 📋 **Deployment Options**

### **Option 1: Render (Recommended)**
```bash
# Use these settings in Render dashboard:
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && gunicorn --bind 0.0.0.0:$PORT app:app
```

### **Option 2: Railway**
```bash
# Railway will auto-detect from railway.toml
# Or use: gunicorn --bind 0.0.0.0:$PORT app:app
```

### **Option 3: Heroku**
```bash
# Uses Procfile automatically
# Command: gunicorn --bind 0.0.0.0:$PORT app:app
```

### **Option 4: DigitalOcean App Platform**
```bash
# Use these settings:
Build Command: pip install -r backend/requirements.txt
Run Command: cd backend && gunicorn --bind 0.0.0.0:$PORT app:app
```

---

## 🔧 **Environment Variables**

Set these in your platform's dashboard:

| Variable | Value | Description |
|----------|-------|-------------|
| `FLASK_DEBUG` | `false` | Disable debug mode in production |
| `FLASK_HOST` | `0.0.0.0` | Bind to all interfaces |
| `PORT` | *(auto-set)* | Platform assigns this automatically |

---

## 🧪 **Testing Your Deployment**

### **1. Health Check**
Visit: `https://your-app-url.com/api/health`
Should return: `{"status": "healthy", "message": "Bridgette backend is running"}`

### **2. File Upload Test**
- Upload a CSV or Excel file
- Should process and return first 3 lines
- Check browser console for any CORS errors

### **3. Check Logs**
- Look for: `Starting Bridgette Backend Server...`
- Look for: `Environment: Production`
- Look for: `Backend will be available at: http://0.0.0.0:PORT`

---

## 🐛 **Common Issues & Solutions**

### **Issue: "Backend not starting"**
**Solution:** Check that your start command uses `gunicorn`:
```bash
gunicorn --bind 0.0.0.0:$PORT app:app
```

### **Issue: "Port already in use"**
**Solution:** Make sure you're using `$PORT` environment variable, not hardcoded port 5000

### **Issue: "CORS errors"**
**Solution:** CORS is enabled, but check that your frontend URL matches your backend URL

### **Issue: "Missing dependencies"**
**Solution:** Ensure `requirements.txt` includes all packages, especially `gunicorn`

---

## 📁 **File Structure**
```
bridgette/
├── backend/
│   ├── app.py              # Main Flask app (production-ready)
│   ├── requirements.txt    # All dependencies including gunicorn
│   └── env.production      # Production environment template
├── frontend/               # Static files
├── Procfile               # Heroku deployment
├── railway.toml           # Railway deployment
├── render.yaml            # Render deployment
└── start_production.sh    # Production startup script
```

---

## 🎯 **Quick Deploy Commands**

### **For Render:**
```bash
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && gunicorn --bind 0.0.0.0:$PORT app:app
```

### **For Railway:**
```bash
Start Command: gunicorn --bind 0.0.0.0:$PORT app:app
```

### **For Heroku:**
```bash
# Uses Procfile automatically
# No additional configuration needed
```

---

## ✅ **Verification Checklist**

- [ ] Backend starts without errors
- [ ] Health endpoint responds: `/api/health`
- [ ] File upload works: `/api/process-files`
- [ ] No CORS errors in browser console
- [ ] Environment shows "Production" in logs
- [ ] Uses dynamic PORT (not hardcoded 5000)

---

## 🆘 **Need Help?**

If you're still having issues:

1. **Check deployment logs** - Look for error messages
2. **Verify start command** - Must use gunicorn with $PORT
3. **Test health endpoint** - Should return JSON response
4. **Check environment variables** - FLASK_DEBUG=false, PORT set by platform

Your backend is now **production-ready** and will work on any platform! 🎉
