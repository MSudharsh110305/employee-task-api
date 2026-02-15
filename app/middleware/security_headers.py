"""
Security headers configuration using Flask-Talisman.
"""
import os
from flask_talisman import Talisman


def init_security_headers(app):
    """
    Initialize security headers with Flask-Talisman.

    Args:
        app: Flask application instance
    """
    # Only enforce HTTPS in production
    force_https = app.config.get('ENVIRONMENT', 'development') == 'production'

    # Content Security Policy
    csp = {
        'default-src': "'self'",
        'script-src': ["'self'", "'unsafe-inline'"],  # Allow inline scripts for development
        'style-src': ["'self'", "'unsafe-inline'"],   # Allow inline styles
        'img-src': ["'self'", 'data:', 'https:'],
        'font-src': ["'self'", 'data:'],
        'connect-src': "'self'",
        'frame-ancestors': "'none'",
        'base-uri': "'self'",
        'form-action': "'self'"
    }

    # Initialize Talisman with security headers
    # Using minimal configuration for maximum compatibility across Talisman versions
    Talisman(
        app,
        force_https=force_https,
        strict_transport_security=force_https,
        strict_transport_security_max_age=31536000,  # 1 year
        content_security_policy=csp,
        referrer_policy='strict-origin-when-cross-origin',
        session_cookie_secure=force_https,
        session_cookie_http_only=True,
        force_file_save=False
    )
