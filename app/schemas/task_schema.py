"""
Task schema for request validation and response serialization.
"""
from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.task import Task


class TaskSchema(Schema):
    """Schema for Task validation and serialization."""
    
    id = fields.Int(dump_only=True)
    
    title = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=200, error="Title must be between 3 and 200 characters")
    )
    
    description = fields.Str(
        required=False,
        allow_none=True
    )
    
    status = fields.Str(
        required=False,
        validate=validate.OneOf(
            Task.VALID_STATUSES,
            error="Status must be one of: pending, in_progress, completed, cancelled"
        ),
        load_default='pending'
    )
    
    priority = fields.Str(
        required=False,
        validate=validate.OneOf(
            Task.VALID_PRIORITIES,
            error="Priority must be one of: low, medium, high, urgent"
        ),
        load_default='medium'
    )
    
    employee_id = fields.Int(
        required=False,
        allow_none=True
    )
    
    deadline = fields.Date(
        required=False,
        allow_none=True,
        format='%Y-%m-%d'
    )
    
    created_at = fields.DateTime(dump_only=True, format='iso')
    updated_at = fields.DateTime(dump_only=True, format='iso')
    
    # Include employee details when requested
    employee = fields.Dict(dump_only=True)


class TaskUpdateSchema(Schema):
    """Schema for updating task (all fields optional)."""
    
    title = fields.Str(
        required=False,
        validate=validate.Length(min=3, max=200)
    )
    
    description = fields.Str(
        required=False,
        allow_none=True
    )
    
    status = fields.Str(
        required=False,
        validate=validate.OneOf(Task.VALID_STATUSES)
    )
    
    priority = fields.Str(
        required=False,
        validate=validate.OneOf(Task.VALID_PRIORITIES)
    )
    
    employee_id = fields.Int(
        required=False,
        allow_none=True
    )
    
    deadline = fields.Date(
        required=False,
        allow_none=True,
        format='%Y-%m-%d'
    )


# Schema instances
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
task_update_schema = TaskUpdateSchema()
