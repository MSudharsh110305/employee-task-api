"""
Task service containing business logic for task operations.
"""
from sqlalchemy.exc import IntegrityError
from app import db
from app.models.task import Task
from app.models.employee import Employee


class TaskService:
    """Service class for task-related business logic."""
    
    @staticmethod
    def get_all_tasks(page=1, per_page=10, status=None, priority=None, employee_id=None):
        """
        Retrieve all tasks with pagination and filtering.
        
        Args:
            page (int): Page number
            per_page (int): Items per page
            status (str): Filter by status
            priority (str): Filter by priority
            employee_id (int): Filter by assigned employee
            
        Returns:
            tuple: (list of tasks, pagination info)
        """
        query = Task.query
        
        # Apply filters
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        if employee_id:
            query = query.filter(Task.employee_id == employee_id)
        
        # Order by creation date (newest first)
        query = query.order_by(Task.created_at.desc())
        
        # Paginate
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        pagination_info = {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
        
        return pagination.items, pagination_info
    
    @staticmethod
    def get_task_by_id(task_id):
        """
        Retrieve a single task by ID.
        
        Args:
            task_id (int): Task ID
            
        Returns:
            Task or None: Task object if found
        """
        from app import db
        return db.session.get(Task, task_id)
    
    @staticmethod
    def create_task(data):
        """
        Create a new task.
        
        Args:
            data (dict): Task data (already validated by Marshmallow)
            
        Returns:
            tuple: (Task object or None, error message or None)
        """
        try:
            # Validate employee_id if provided
            employee_id = data.get('employee_id')
            if employee_id:
                employee = db.session.get(Employee, employee_id)

                if not employee:
                    return None, f'Employee with ID {employee_id} not found'
            
            # Create new task directly (data is already validated by Marshmallow)
            task = Task(
                title=data.get('title'),
                description=data.get('description'),
                status=data.get('status', 'pending'),
                priority=data.get('priority', 'medium'),
                employee_id=data.get('employee_id'),
                deadline=data.get('deadline')  # Already a date object from Marshmallow
            )
            
            db.session.add(task)
            db.session.commit()
            
            return task, None
            
        except Exception as e:
            db.session.rollback()
            return None, f'Error creating task: {str(e)}'
    
    @staticmethod
    def update_task(task_id, data):
        """
        Update an existing task.
        
        Args:
            task_id (int): Task ID
            data (dict): Updated task data
            
        Returns:
            tuple: (Task object or None, error message or None)
        """
        try:
            task = db.session.get(Task, task_id)

            if not task:
                return None, 'Task not found'
            
            # Validate employee_id if being updated
            if 'employee_id' in data and data['employee_id']:
                employee = Employee.query.get(data['employee_id'])
                if not employee:
                    return None, f'Employee with ID {data["employee_id"]} not found'
            
            # Update fields
            for key, value in data.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            
            db.session.commit()
            return task, None
            
        except Exception as e:
            db.session.rollback()
            return None, f'Error updating task: {str(e)}'
    
    @staticmethod
    def delete_task(task_id):
        """
        Delete a task.
        
        Args:
            task_id (int): Task ID
            
        Returns:
            tuple: (success boolean, error message or None)
        """
        try:
            task = db.session.get(Task, task_id)

            if not task:
                return False, 'Task not found'
            
            db.session.delete(task)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f'Error deleting task: {str(e)}'
