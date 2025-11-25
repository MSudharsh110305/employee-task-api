"""
Authentication routes for API v1.
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from app.schemas.auth_schema import RegisterSchema, LoginSchema, UserResponseSchema
from app.models.user import User
from app import db
from app.middleware.rate_limiting import limiter
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)

# Create v1 auth blueprint
bp = Blueprint('v1_auth', __name__, url_prefix='/api/v1/auth')


@bp.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    """
    Register a new user.
    Rate limit: 5 requests per hour to prevent spam.

    Returns:
        JSON response with user data and JWT tokens
    """
    from flask import request, jsonify

    try:
        # Validate request data
        schema = RegisterSchema()
        data = schema.load(request.get_json())

        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'status': 'error',
                'message': 'Username already exists'
            }), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'status': 'error',
                'message': 'Email already registered'
            }), 400

        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role=data.get('role', 'employee')
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        # Generate JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        # Serialize user data
        user_schema = UserResponseSchema()
        user_data = user_schema.dump(user)

        logger.info(f"New user registered: {user.username}")

        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'data': {
                'user': user_data,
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 201

    except ValidationError as e:
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'errors': e.messages
        }), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Registration failed: {str(e)}'
        }), 500


@bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """
    Authenticate user and return JWT tokens.
    Rate limit: 5 requests per minute to prevent brute force attacks.

    Returns:
        JSON response with user data and JWT tokens
    """
    from flask import request, jsonify
    from datetime import datetime, timezone

    try:
        # Validate request data
        schema = LoginSchema()
        data = schema.load(request.get_json())

        # Find user
        user = User.query.filter_by(username=data['username']).first()

        if not user or not user.check_password(data['password']):
            return jsonify({
                'status': 'error',
                'message': 'Invalid username or password'
            }), 401

        # Check if user is active
        if not user.is_active:
            return jsonify({
                'status': 'error',
                'message': 'Account is inactive. Please contact support.'
            }), 403

        # Update last login
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()

        # Generate JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        # Serialize user data
        user_schema = UserResponseSchema()
        user_data = user_schema.dump(user)

        logger.info(f"User logged in: {user.username}")

        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'user': user_data,
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 200

    except ValidationError as e:
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'errors': e.messages
        }), 400
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Login failed: {str(e)}'
        }), 500


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token.

    Returns:
        JSON response with new access token
    """
    from flask import jsonify

    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)

        return jsonify({
            'status': 'success',
            'data': {
                'access_token': new_access_token
            }
        }), 200

    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Token refresh failed: {str(e)}'
        }), 500


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user information.

    Returns:
        JSON response with user data
    """
    from flask import jsonify

    try:
        current_user_id = get_jwt_identity()
        user = db.session.get(User, int(current_user_id))

        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        user_schema = UserResponseSchema()
        user_data = user_schema.dump(user)

        return jsonify({
            'status': 'success',
            'data': user_data
        }), 200

    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to get user data: {str(e)}'
        }), 500
