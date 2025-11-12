"""
Employee API routes for CRUD operations.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.employee_service import EmployeeService
from app.schemas.employee_schema import (
    employee_schema,
    employees_schema,
    employee_update_schema
)

# Create blueprint
bp = Blueprint('employees', __name__, url_prefix='/api/employees')


@bp.route('', methods=['GET'])
def get_employees():
    """
    Get all employees with pagination and filtering.
    
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 10)
        department (str): Filter by department
        position (str): Filter by position
    
    Returns:
        JSON response with employees list and pagination info
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        department = request.args.get('department', None, type=str)
        position = request.args.get('position', None, type=str)
        
        # Validate pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
        
        # Get employees from service
        employees, pagination_info = EmployeeService.get_all_employees(
            page=page,
            per_page=per_page,
            department=department,
            position=position
        )
        
        # Serialize employees manually to avoid tasks serialization issue
        result = []
        for employee in employees:
            emp_dict = employee_schema.dump(employee)
            # Get tasks as list instead of using the dynamic relationship
            emp_dict['tasks'] = [task.to_dict() for task in employee.tasks.all()]
            result.append(emp_dict)
        
        return jsonify({
            'status': 'success',
            'data': result,
            'pagination': pagination_info
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving employees: {str(e)}'
        }), 500


@bp.route('/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """
    Get a single employee by ID.
    
    Args:
        employee_id (int): Employee ID
    
    Returns:
        JSON response with employee data
    """
    try:
        employee = EmployeeService.get_employee_by_id(employee_id)
        
        if not employee:
            return jsonify({
                'status': 'error',
                'message': f'Employee with ID {employee_id} not found'
            }), 404
        
        # Serialize employee with tasks
        result = employee_schema.dump(employee)
        result['tasks'] = [task.to_dict() for task in employee.tasks.all()]
        
        return jsonify({
            'status': 'success',
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving employee: {str(e)}'
        }), 500


@bp.route('', methods=['POST'])
def create_employee():
    """
    Create a new employee.
    
    Request Body:
        JSON object with employee data
    
    Returns:
        JSON response with created employee data
    """
    try:
        # Validate request data
        data = employee_schema.load(request.json)
        
        # Create employee
        employee, error = EmployeeService.create_employee(data)
        
        if error:
            return jsonify({
                'status': 'error',
                'message': error
            }), 400
        
        # Serialize response
        result = employee_schema.dump(employee)
        result['tasks'] = []  # New employee has no tasks
        
        return jsonify({
            'status': 'success',
            'message': 'Employee created successfully',
            'data': result
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'status': 'error',
            'message': 'Validation failed',
            'errors': e.messages
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error creating employee: {str(e)}'
        }), 500


@bp.route('/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """
    Update an existing employee.
    
    Args:
        employee_id (int): Employee ID
    
    Request Body:
        JSON object with updated employee data
    
    Returns:
        JSON response with updated employee data
    """
    try:
        # Validate request data
        data = employee_update_schema.load(request.json)
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided for update'
            }), 400
        
        # Update employee
        employee, error = EmployeeService.update_employee(employee_id, data)
        
        if error:
            status_code = 404 if 'not found' in error.lower() else 400
            return jsonify({
                'status': 'error',
                'message': error
            }), status_code
        
        # Serialize response
        result = employee_schema.dump(employee)
        result['tasks'] = [task.to_dict() for task in employee.tasks.all()]
        
        return jsonify({
            'status': 'success',
            'message': 'Employee updated successfully',
            'data': result
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
            'message': f'Error updating employee: {str(e)}'
        }), 500


@bp.route('/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """
    Delete an employee.
    
    Args:
        employee_id (int): Employee ID
    
    Returns:
        JSON response confirming deletion
    """
    try:
        success, error = EmployeeService.delete_employee(employee_id)
        
        if not success:
            status_code = 404 if 'not found' in error.lower() else 500
            return jsonify({
                'status': 'error',
                'message': error
            }), status_code
        
        return jsonify({
            'status': 'success',
            'message': f'Employee with ID {employee_id} deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error deleting employee: {str(e)}'
        }), 500


@bp.route('/<int:employee_id>/tasks', methods=['GET'])
def get_employee_tasks(employee_id):
    """
    Get all tasks assigned to a specific employee.
    
    Args:
        employee_id (int): Employee ID
    
    Returns:
        JSON response with list of tasks
    """
    try:
        tasks, error = EmployeeService.get_employee_tasks(employee_id)
        
        if error:
            return jsonify({
                'status': 'error',
                'message': error
            }), 404
        
        # Serialize tasks
        result = [task.to_dict() for task in tasks]
        
        return jsonify({
            'status': 'success',
            'data': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving employee tasks: {str(e)}'
        }), 500
