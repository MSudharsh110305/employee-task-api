"""
Request ID middleware for distributed tracing.
"""
import uuid
from flask import g, request


def init_request_id(app):
    """
    Initialize request ID middleware.

    Adds a unique request ID to each request for tracing across services.

    Args:
        app: Flask application instance
    """

    @app.before_request
    def generate_request_id():
        """Generate or extract request ID."""
        # Check if request ID is provided in headers
        request_id = request.headers.get('X-Request-ID')

        # Generate new ID if not provided
        if not request_id:
            request_id = str(uuid.uuid4())

        # Store in Flask's g object for use throughout request
        g.request_id = request_id

    @app.after_request
    def add_request_id_header(response):
        """Add request ID to response headers."""
        response.headers['X-Request-ID'] = g.request_id
        return response
