"""
API v1 route initialization.
"""
from flask import Blueprint

# Import v1 routes
from app.routes.v1 import auth_routes, employee_routes, task_routes

# Create v1 API blueprint
v1_bp = Blueprint('v1', __name__, url_prefix='/api/v1')

def init_v1_routes(app):
    """
    Initialize v1 API routes.

    Args:
        app: Flask application instance
    """
    # Register v1 blueprints
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(employee_routes.bp)
    app.register_blueprint(task_routes.bp)
