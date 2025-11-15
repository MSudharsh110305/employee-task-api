"""
Authentication and authorization decorators.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User
from app import db


def admin_required():
    """
    Decorator to require admin role for endpoint access.

    Usage:
        @app.route('/admin/endpoint')
        @jwt_required()
        @admin_required()
        def admin_only():
            pass
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = db.session.get(User, user_id)

            if not user or not user.is_admin():
                return jsonify({
                    'status': 'error',
                    'message': 'Admin access required'
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper


def manager_required():
    """
    Decorator to require manager or admin role for endpoint access.

    Usage:
        @app.route('/manager/endpoint')
        @jwt_required()
        @manager_required()
        def manager_only():
            pass
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = db.session.get(User, user_id)

            if not user or (not user.is_admin() and not user.is_manager()):
                return jsonify({
                    'status': 'error',
                    'message': 'Manager or admin access required'
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper


def active_user_required():
    """
    Decorator to require active user account.

    Usage:
        @app.route('/endpoint')
        @jwt_required()
        @active_user_required()
        def protected():
            pass
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = db.session.get(User, user_id)

            if not user or not user.is_active:
                return jsonify({
                    'status': 'error',
                    'message': 'Account is inactive'
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper
