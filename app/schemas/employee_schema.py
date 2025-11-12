from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.employee import Employee


class EmployeeSchema(Schema):
    """Schema for Employee validation and serialization."""
    
    id = fields.Int(dump_only=True)
    
    first_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100, error="First name must be between 2 and 100 characters")
    )
    
    last_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100, error="Last name must be between 2 and 100 characters")
    )
    
    email = fields.Email(
        required=True,
        error_messages={'invalid': 'Invalid email format'}
    )
    
    phone = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=20, error="Phone number must not exceed 20 characters")
    )
    
    department = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=100, error="Department name must not exceed 100 characters")
    )
    
    position = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=100, error="Position must not exceed 100 characters")
    )
    
    hire_date = fields.Date(
        required=False,
        allow_none=True,
        format='%Y-%m-%d'
    )
    
    created_at = fields.DateTime(dump_only=True, format='iso')
    updated_at = fields.DateTime(dump_only=True, format='iso')
    
    # Include tasks when requested
    tasks = fields.List(fields.Dict(), dump_only=True)
    
    @validates('email')
    def validate_email_unique(self, value):

        pass


class EmployeeUpdateSchema(Schema):
    """Schema for updating employee (all fields optional)."""
    
    first_name = fields.Str(
        required=False,
        validate=validate.Length(min=2, max=100)
    )
    
    last_name = fields.Str(
        required=False,
        validate=validate.Length(min=2, max=100)
    )
    
    email = fields.Email(required=False)
    
    phone = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=20)
    )
    
    department = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=100)
    )
    
    position = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=100)
    )
    
    hire_date = fields.Date(
        required=False,
        allow_none=True,
        format='%Y-%m-%d'
    )


# Schema instances
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
employee_update_schema = EmployeeUpdateSchema()
