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
    force_https = app.config.get('ENV', 'development') == 'production'

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
    Talisman(
        app,
        force_https=force_https,
        strict_transport_security=force_https,
        strict_transport_security_max_age=31536000,  # 1 year
        strict_transport_security_include_subdomains=True,
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src'],
        referrer_policy='strict-origin-when-cross-origin',
        content_type_options=True,
        frame_options='DENY',
        session_cookie_secure=force_https,
        session_cookie_http_only=True,
        session_cookie_samesite='Lax',
        force_file_save=False
    )
