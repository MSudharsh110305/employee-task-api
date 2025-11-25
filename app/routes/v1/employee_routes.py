"""
Employee routes for API v1.
Wraps existing employee routes with v1 prefix.
"""
from flask import Blueprint

# Import existing employee routes
from app.routes.employee_routes import (
    get_employees,
    get_employee,
    create_employee,
    update_employee,
    delete_employee
)

# Create v1 employee blueprint
bp = Blueprint('v1_employees', __name__, url_prefix='/api/v1/employees')

# Register routes
bp.add_url_rule('', view_func=get_employees, methods=['GET'])
bp.add_url_rule('', view_func=create_employee, methods=['POST'])
bp.add_url_rule('/<int:employee_id>', view_func=get_employee, methods=['GET'])
bp.add_url_rule('/<int:employee_id>', view_func=update_employee, methods=['PUT'])
bp.add_url_rule('/<int:employee_id>', view_func=delete_employee, methods=['DELETE'])
