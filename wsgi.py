"""
WSGI entry point for production deployment.
Used by Gunicorn, uWSGI, or other WSGI servers.

Usage:
    gunicorn wsgi:app
"""
import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app for production
app = create_app('production')

if __name__ == '__main__':
    app.run()
