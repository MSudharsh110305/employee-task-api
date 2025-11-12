"""
Centralized error handling for the application.
"""
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


def register_error_handlers(app):
    """
    Register error handlers with the Flask app.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({
            'status': 'error',
            'message': 'Bad request',
            'error': str(error)
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({
            'status': 'error',
            'message': 'Resource not found',
            'error': str(error)
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors."""
        return jsonify({
            'status': 'error',
            'message': 'Method not allowed',
            'error': str(error)
        }), 405
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server errors."""
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'error': 'An unexpected error occurred'
        }), 500
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle Marshmallow validation errors."""
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'errors': error.messages
        }), 400
    
    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        """Handle SQLAlchemy database errors."""
        return jsonify({
            'status': 'error',
            'message': 'Database error occurred',
            'error': 'Please try again later'
        }), 500
