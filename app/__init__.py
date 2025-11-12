"""
Application factory for creating Flask app instances.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import config

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config_name='development'):
    """
    Application factory pattern for creating Flask app instances.
    
    Args:
        config_name (str): Configuration name (development, production, testing)
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Import models (must be after db initialization)
    from app.models import Employee, Task
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")
    
    # Register blueprints
    from app.routes import employee_routes, task_routes
    app.register_blueprint(employee_routes.bp)
    app.register_blueprint(task_routes.bp)
    
    # Register error handlers
    from app.utils import error_handlers
    error_handlers.register_error_handlers(app)
    
    # Root endpoint
    @app.route('/')
    def index():
        """Root endpoint returning API information."""
        return {
            'status': 'success',
            'message': 'Employee-Task Management API',
            'version': '1.0.0',
            'endpoints': {
                'employees': '/api/employees',
                'tasks': '/api/tasks'
            }
        }, 200
    
    # Health check endpoint
    @app.route('/health')
    def health():
        """Health check endpoint for monitoring."""
        return {'status': 'healthy'}, 200
    
    return app
