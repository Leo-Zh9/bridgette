"""
WSGI configuration for production deployment
"""
import os
from app import app

# This is the WSGI application that will be used by production servers
application = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
