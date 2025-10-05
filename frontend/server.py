#!/usr/bin/env python3
"""
Bridgette Frontend Development Server
====================================

This is a specialized HTTP server for frontend development that includes
cache-busting headers to ensure file updates are immediately visible.

Problem Solved:
- Browser caching can prevent CSS/JS updates from being visible during development
- Standard Python HTTP server doesn't include cache-busting headers
- Manual cache clearing is tedious and error-prone

Solution:
- Custom HTTP request handler that adds no-cache headers to all responses
- Ensures files are always fetched fresh from the server
- Maintains development workflow efficiency

Usage:
    python server.py
    
This server should only be used for development, not production deployment.
"""

import http.server
import socketserver
import os

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler that adds cache-busting headers
    
    This handler ensures that browsers always fetch the latest version
    of files, preventing caching issues during development.
    """
    def end_headers(self):
        # Add cache-busting headers to prevent browser caching
        # These headers tell the browser to always fetch fresh content
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')  # HTTP/1.0 compatibility
        self.send_header('Expires', '0')  # Expire immediately
        super().end_headers()

if __name__ == "__main__":
    PORT = 8080  # Standard development port for frontend
    
    # Change to the frontend directory to serve files from the correct location
    # This ensures relative paths in HTML work correctly
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Start the server with cache-busting enabled
    with socketserver.TCPServer(("", PORT), NoCacheHTTPRequestHandler) as httpd:
        print(f"Frontend server running at http://localhost:{PORT}")
        print("Cache-busting enabled - files will always reload")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()
