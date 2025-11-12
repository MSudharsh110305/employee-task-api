"""
Development server entry point.
Run this file to start the Flask development server.

Usage:
    python run.py
"""
import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Get host and port from environment or use defaults
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"\n{'='*60}")
    print(f"🚀 Employee-Task Management API")
    print(f"{'='*60}")
    print(f"📍 Running on: http://{host}:{port}")
    print(f"🔧 Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"🐛 Debug Mode: {debug}")
    print(f"{'='*60}\n")
    print("Available endpoints:")
    print("  - GET    /api/employees")
    print("  - POST   /api/employees")
    print("  - GET    /api/employees/<id>")
    print("  - PUT    /api/employees/<id>")
    print("  - DELETE /api/employees/<id>")
    print("  - GET    /api/employees/<id>/tasks")
    print("  - GET    /api/tasks")
    print("  - POST   /api/tasks")
    print("  - GET    /api/tasks/<id>")
    print("  - PUT    /api/tasks/<id>")
    print("  - DELETE /api/tasks/<id>")
    print(f"{'='*60}\n")
    
    app.run(host=host, port=port, debug=debug)
