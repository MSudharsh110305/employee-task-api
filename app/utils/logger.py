"""
Structured logging configuration with JSON format.
"""
import logging
import sys
from pythonjsonlogger import jsonlogger
from flask import g, request, has_request_context


class RequestFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter that includes request context."""

    def add_fields(self, log_record, record, message_dict):
        """Add custom fields to log record."""
        super().add_fields(log_record, record, message_dict)

        # Add request context if available
        if has_request_context():
            log_record['request_id'] = getattr(g, 'request_id', None)
            log_record['method'] = request.method
            log_record['path'] = request.path
            log_record['ip'] = request.remote_addr
            log_record['user_agent'] = request.headers.get('User-Agent', '')

        # Add service metadata
        log_record['service'] = 'employee-task-api'
        log_record['environment'] = record.__dict__.get('environment', 'development')


def setup_logging(app):
    """
    Setup structured JSON logging for the application.

    Args:
        app: Flask application instance
    """
    # Create JSON formatter
    formatter = RequestFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s',
        timestamp=True
    )

    # Configure handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Set log level based on environment
    log_level = logging.DEBUG if app.debug else logging.INFO
    app.logger.setLevel(log_level)

    # Remove default handlers
    app.logger.handlers = []

    # Add our custom handler
    app.logger.addHandler(handler)

    # Log application startup
    app.logger.info(
        'Application started',
        extra={'environment': app.config.get('ENV', 'development')}
    )

    # Request logging
    @app.before_request
    def log_request():
        """Log each request."""
        app.logger.info(
            'Request started',
            extra={
                'environment': app.config.get('ENV', 'development'),
                'query_params': dict(request.args)
            }
        )

    @app.after_request
    def log_response(response):
        """Log each response."""
        app.logger.info(
            'Request completed',
            extra={
                'environment': app.config.get('ENV', 'development'),
                'status_code': response.status_code
            }
        )
        return response

    return app.logger
