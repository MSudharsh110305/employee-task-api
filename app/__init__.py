"""
Application factory for creating Flask app instances.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from flask_compress import Compress
from app.config import config

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
compress = Compress()


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
    compress.init_app(app)

    # Configure CORS with specific origins
    allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000,http://localhost:5000')
    CORS(
        app,
        resources={r"/api/*": {
            "origins": allowed_origins.split(','),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization", "X-Request-ID"],
            "supports_credentials": True,
            "max_age": 3600
        }}
    )

    # Initialize JWT authentication
    from app.auth import init_jwt
    init_jwt(app)

    # Initialize rate limiting
    from app.middleware.rate_limiting import init_rate_limiting
    init_rate_limiting(app)

    # Initialize security headers (only in production)
    if config_name == 'production':
        from app.middleware.security_headers import init_security_headers
        init_security_headers(app)

    # Initialize request ID middleware
    from app.middleware.request_id import init_request_id
    init_request_id(app)

    # Setup structured logging
    from app.utils.logger import setup_logging
    setup_logging(app)

    # Initialize Sentry error tracking
    from app.utils.monitoring import init_sentry
    init_sentry(app)
    
    # Import models (must be after db initialization)
    # This ensures Flask-Migrate can detect models for migrations
    from app.models import Employee, Task, User

    # Note: Database tables are now managed via Flask-Migrate
    # To create tables, run: flask db upgrade
    # DO NOT use db.create_all() in production!
    
    # Register blueprints
    from app.routes import employee_routes, task_routes, auth_routes
    from app.routes.v1 import auth_routes as v1_auth
    from app.routes.v1 import employee_routes as v1_employees
    from app.routes.v1 import task_routes as v1_tasks

    # Register v1 routes (primary)
    app.register_blueprint(v1_auth.bp)
    app.register_blueprint(v1_employees.bp)
    app.register_blueprint(v1_tasks.bp)

    # Register legacy routes (for backward compatibility)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(employee_routes.bp)
    app.register_blueprint(task_routes.bp)

    # Initialize Swagger API documentation
    from app.utils.swagger_config import init_swagger
    init_swagger(app)

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
            'version': '2.0.0',
            'documentation': '/api/docs/',
            'api_versions': {
                'v1': {
                    'status': 'current',
                    'endpoints': {
                        'auth': '/api/v1/auth',
                        'employees': '/api/v1/employees',
                        'tasks': '/api/v1/tasks'
                    }
                },
                'legacy': {
                    'status': 'deprecated',
                    'endpoints': {
                        'auth': '/api/auth',
                        'employees': '/api/employees',
                        'tasks': '/api/tasks'
                    },
                    'deprecation_notice': 'Legacy endpoints will be removed in v3.0. Please migrate to /api/v1/*'
                }
            }
        }, 200
    
    # Health check endpoints
    from app.utils.health_check import health_check_simple, health_check_detailed

    @app.route('/health')
    def health():
        """
        Simple health check endpoint for basic monitoring.
        ---
        tags:
          - Health
        responses:
          200:
            description: Service is healthy
        """
        response, status_code = health_check_simple()
        return response, status_code

    @app.route('/health/detailed')
    def health_detailed():
        """
        Detailed health check with system metrics.
        ---
        tags:
          - Health
        responses:
          200:
            description: Service is healthy with details
          503:
            description: Service is degraded
        """
        response, status_code = health_check_detailed()
        return response, status_code
    
    return app
