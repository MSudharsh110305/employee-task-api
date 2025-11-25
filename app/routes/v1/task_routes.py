"""
Task routes for API v1.
Wraps existing task routes with v1 prefix.
"""
from flask import Blueprint

# Import existing task routes
from app.routes.task_routes import (
    get_tasks,
    get_task,
    create_task,
    update_task,
    delete_task
)

# Create v1 task blueprint
bp = Blueprint('v1_tasks', __name__, url_prefix='/api/v1/tasks')

# Register routes
bp.add_url_rule('', view_func=get_tasks, methods=['GET'])
bp.add_url_rule('', view_func=create_task, methods=['POST'])
bp.add_url_rule('/<int:task_id>', view_func=get_task, methods=['GET'])
bp.add_url_rule('/<int:task_id>', view_func=update_task, methods=['PUT'])
bp.add_url_rule('/<int:task_id>', view_func=delete_task, methods=['DELETE'])
