"""
Rate limiting configuration and setup.
"""
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=os.getenv('RATELIMIT_STORAGE_URL', 'memory://'),
    strategy="fixed-window",
    headers_enabled=True,
)


def init_rate_limiting(app):
    """
    Initialize rate limiting with the Flask app.

    Args:
        app: Flask application instance
    """
    limiter.init_app(app)

    # Add rate limit exceeded handler
    @app.errorhandler(429)
    def ratelimit_handler(e):
        """Custom handler for rate limit exceeded."""
        return {
            'status': 'error',
            'message': 'Rate limit exceeded. Please try again later.',
            'error': 'too_many_requests'
        }, 429
