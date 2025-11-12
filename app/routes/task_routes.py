"""
Task API routes for CRUD operations.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.task_service import TaskService
from app.schemas.task_schema import (
    task_schema,
    tasks_schema,
    task_update_schema
)

# Create blueprint
bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


@bp.route('', methods=['GET'])
def get_tasks():
    """
    Get all tasks with pagination and filtering.
    
    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 10)
        status (str): Filter by status
        priority (str): Filter by priority
        employee_id (int): Filter by assigned employee
    
    Returns:
        JSON response with tasks list and pagination info
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', None, type=str)
        priority = request.args.get('priority', None, type=str)
        employee_id = request.args.get('employee_id', None, type=int)
        
        # Validate pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
        
        # Get tasks from service
        tasks, pagination_info = TaskService.get_all_tasks(
            page=page,
            per_page=per_page,
            status=status,
            priority=priority,
            employee_id=employee_id
        )
        
        # Serialize tasks with employee info
        result = []
        for task in tasks:
            task_dict = task_schema.dump(task)
            if task.assigned_employee:
                task_dict['employee'] = {
                    'id': task.assigned_employee.id,
                    'name': f"{task.assigned_employee.first_name} {task.assigned_employee.last_name}",
                    'email': task.assigned_employee.email
                }
            result.append(task_dict)
        
        return jsonify({
            'status': 'success',
            'data': result,
            'pagination': pagination_info
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving tasks: {str(e)}'
        }), 500


@bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Get a single task by ID.
    
    Args:
        task_id (int): Task ID
    
    Returns:
        JSON response with task data
    """
    try:
        task = TaskService.get_task_by_id(task_id)
        
        if not task:
            return jsonify({
                'status': 'error',
                'message': f'Task with ID {task_id} not found'
            }), 404
        
        # Serialize task with employee info
        result = task_schema.dump(task)
        if task.assigned_employee:
            result['employee'] = {
                'id': task.assigned_employee.id,
                'name': f"{task.assigned_employee.first_name} {task.assigned_employee.last_name}",
                'email': task.assigned_employee.email
            }
        
        return jsonify({
            'status': 'success',
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving task: {str(e)}'
        }), 500


@bp.route('', methods=['POST'])
def create_task():
    """
    Create a new task.
    
    Request Body:
        JSON object with task data
    
    Returns:
        JSON response with created task data
    """
    try:
        # Validate request data
        data = task_schema.load(request.json)
        
        # Create task
        task, error = TaskService.create_task(data)
        
        if error:
            return jsonify({
                'status': 'error',
                'message': error
            }), 400
        
        # Serialize response
        result = task_schema.dump(task)
        
        return jsonify({
            'status': 'success',
            'message': 'Task created successfully',
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
            'message': f'Error creating task: {str(e)}'
        }), 500


@bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update an existing task.
    
    Args:
        task_id (int): Task ID
    
    Request Body:
        JSON object with updated task data
    
    Returns:
        JSON response with updated task data
    """
    try:
        # Validate request data
        data = task_update_schema.load(request.json)
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No data provided for update'
            }), 400
        
        # Update task
        task, error = TaskService.update_task(task_id, data)
        
        if error:
            status_code = 404 if 'not found' in error.lower() else 400
            return jsonify({
                'status': 'error',
                'message': error
            }), status_code
        
        # Serialize response
        result = task_schema.dump(task)
        
        return jsonify({
            'status': 'success',
            'message': 'Task updated successfully',
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
            'message': f'Error updating task: {str(e)}'
        }), 500


@bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete a task.
    
    Args:
        task_id (int): Task ID
    
    Returns:
        JSON response confirming deletion
    """
    try:
        success, error = TaskService.delete_task(task_id)
        
        if not success:
            status_code = 404 if 'not found' in error.lower() else 500
            return jsonify({
                'status': 'error',
                'message': error
            }), status_code
        
        return jsonify({
            'status': 'success',
            'message': f'Task with ID {task_id} deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error deleting task: {str(e)}'
        }), 500
