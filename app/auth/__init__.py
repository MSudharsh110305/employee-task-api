"""
Authentication module initialization.
"""
from flask_jwt_extended import JWTManager

jwt = JWTManager()


def init_jwt(app):
    """
    Initialize JWT manager with the Flask app.

    Args:
        app: Flask application instance
    """
    jwt.init_app(app)

    # JWT configuration callbacks
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        """Convert user object to identity for JWT."""
        user_id = user.id if hasattr(user, 'id') else user
        return str(user_id)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """Load user from JWT identity."""
        from app.models.user import User
        from app import db

        identity = int(jwt_data["sub"])
        return db.session.get(User, identity)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Handle expired tokens."""
        return {
            'status': 'error',
            'message': 'Token has expired',
            'error': 'token_expired'
        }, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Handle invalid tokens."""
        app.logger.error(f"Invalid token error: {error}")
        return {
            'status': 'error',
            'message': f'Invalid token: {error}',
            'error': 'invalid_token'
        }, 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        """Handle missing tokens."""
        return {
            'status': 'error',
            'message': 'Authorization token required',
            'error': 'authorization_required'
        }, 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Handle revoked tokens."""
        return {
            'status': 'error',
            'message': 'Token has been revoked',
            'error': 'token_revoked'
        }, 401
