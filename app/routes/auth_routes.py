"""
Authentication API routes for login, register, and token management.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from marshmallow import ValidationError
from app import db
from app.models.user import User
from app.schemas.auth_schema import (
    register_schema,
    login_schema,
    user_response_schema
)
from app.middleware.rate_limiting import limiter

# Create blueprint
bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/register', methods=['POST'])
@limiter.limit("5 per hour")  # Prevent registration spam
def register():
    """
    Register a new user account.

    Request Body:
        JSON object with user registration data

    Returns:
        JSON response with created user data and access token
    """
    try:
        # Validate request data
        data = register_schema.load(request.json)

        # Create new user
        user = User.from_dict(data)
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        # Serialize user data
        user_data = user_response_schema.dump(user)

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
        return jsonify({
            'status': 'error',
            'message': f'Error registering user: {str(e)}'
        }), 500


@bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Prevent brute force attacks
def login():
    """
    Authenticate user and return access tokens.

    Request Body:
        JSON object with username and password

    Returns:
        JSON response with user data and access tokens
    """
    try:
        # Validate request data
        data = login_schema.load(request.json)

        # Find user by username
        user = User.query.filter_by(username=data['username']).first()

        if not user or not user.check_password(data['password']):
            return jsonify({
                'status': 'error',
                'message': 'Invalid username or password'
            }), 401

        # Check if account is active
        if not user.is_active:
            return jsonify({
                'status': 'error',
                'message': 'Account is inactive'
            }), 403

        # Update last login
        user.update_last_login()

        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        # Serialize user data
        user_data = user_response_schema.dump(user)

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
        return jsonify({
            'status': 'error',
            'message': f'Error during login: {str(e)}'
        }), 500


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token.

    Headers:
        Authorization: Bearer <refresh_token>

    Returns:
        JSON response with new access token
    """
    try:
        # Get current user from refresh token
        current_user_id = get_jwt_identity()

        # Generate new access token
        access_token = create_access_token(identity=current_user_id)

        return jsonify({
            'status': 'success',
            'message': 'Token refreshed successfully',
            'data': {
                'access_token': access_token
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error refreshing token: {str(e)}'
        }), 500


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user information.

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        JSON response with current user data
    """
    try:
        # Get current user from access token
        current_user_id = get_jwt_identity()
        user = db.session.get(User, current_user_id)

        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404

        # Serialize user data
        user_data = user_response_schema.dump(user)

        return jsonify({
            'status': 'success',
            'data': user_data
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving user: {str(e)}'
        }), 500


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout current user (placeholder - requires token blacklist for full implementation).

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        JSON response confirming logout
    """
    # Note: Full logout implementation requires token blacklist (Redis)
    # For now, client should discard tokens
    return jsonify({
        'status': 'success',
        'message': 'Logout successful. Please discard your tokens.'
    }), 200
