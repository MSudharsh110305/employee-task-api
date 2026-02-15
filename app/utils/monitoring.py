"""
Error tracking and monitoring configuration.
"""
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def init_sentry(app):
    """
    Initialize Sentry error tracking.

    Args:
        app: Flask application instance
    """
    sentry_dsn = os.getenv('SENTRY_DSN')

    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[FlaskIntegration()],
            environment=app.config.get('ENVIRONMENT', 'development'),
            traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
            send_default_pii=False,  # Don't send personally identifiable information
            before_send=before_send_filter,
        )
        app.logger.info('Sentry error tracking initialized')
    else:
        app.logger.info('Sentry DSN not configured, error tracking disabled')


def before_send_filter(event, hint):
    """
    Filter events before sending to Sentry.

    Args:
        event: Sentry event dictionary
        hint: Additional context

    Returns:
        Modified event or None to skip
    """
    # Don't send 404 errors to Sentry
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if 'NotFound' in str(exc_type):
            return None

    return event
