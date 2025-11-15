"""
Authentication schema for request validation and response serialization.
"""
from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.user import User


class RegisterSchema(Schema):
    """Schema for user registration."""

    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80, error="Username must be between 3 and 80 characters")
    )

    email = fields.Email(
        required=True,
        error_messages={'invalid': 'Invalid email format'}
    )

    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, error="Password must be at least 8 characters")
    )

    first_name = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=100)
    )

    last_name = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=100)
    )

    role = fields.Str(
        required=False,
        validate=validate.OneOf(
            User.VALID_ROLES,
            error="Role must be one of: admin, manager, employee"
        ),
        load_default='employee'
    )

    @validates('username')
    def validate_username_unique(self, value):
        """Check if username already exists."""
        if User.query.filter_by(username=value).first():
            raise ValidationError('Username already exists')

    @validates('email')
    def validate_email_unique(self, value):
        """Check if email already exists."""
        if User.query.filter_by(email=value).first():
            raise ValidationError('Email already exists')


class LoginSchema(Schema):
    """Schema for user login."""

    username = fields.Str(required=True)
    password = fields.Str(required=True)


class UserResponseSchema(Schema):
    """Schema for user response data."""

    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Email()
    first_name = fields.Str()
    last_name = fields.Str()
    role = fields.Str()
    is_active = fields.Boolean()
    is_verified = fields.Boolean()
    created_at = fields.DateTime(dump_only=True, format='iso')
    last_login = fields.DateTime(dump_only=True, format='iso')


# Schema instances
register_schema = RegisterSchema()
login_schema = LoginSchema()
user_response_schema = UserResponseSchema()
