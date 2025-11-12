"""
Employee service containing business logic for employee operations.
"""
from sqlalchemy.exc import IntegrityError
from app import db
from app.models.employee import Employee


class EmployeeService:
    """Service class for employee-related business logic."""
    
    @staticmethod
    def get_all_employees(page=1, per_page=10, department=None, position=None):
        """
        Retrieve all employees with pagination and filtering.
        
        Args:
            page (int): Page number
            per_page (int): Items per page
            department (str): Filter by department
            position (str): Filter by position
            
        Returns:
            tuple: (list of employees, pagination info)
        """
        query = Employee.query
        
        # Apply filters
        if department:
            query = query.filter(Employee.department.ilike(f'%{department}%'))
        if position:
            query = query.filter(Employee.position.ilike(f'%{position}%'))
        
        # Order by creation date (newest first)
        query = query.order_by(Employee.created_at.desc())
        
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
    def get_employee_by_id(employee_id):
        """
        Retrieve a single employee by ID.
        
        Args:
            employee_id (int): Employee ID
            
        Returns:
            Employee or None: Employee object if found
        """
        from app import db
        return db.session.get(Employee, employee_id)
    
    @staticmethod
    def create_employee(data):
        """
        Create a new employee.
        
        Args:
            data (dict): Employee data (already validated by Marshmallow)
            
        Returns:
            tuple: (Employee object or None, error message or None)
        """
        try:
            # Check if email already exists
            existing = Employee.query.filter_by(email=data.get('email')).first()
            if existing:
                return None, 'Email already exists'
            
            # Create new employee directly (data is already validated by Marshmallow)
            employee = Employee(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                phone=data.get('phone'),
                department=data.get('department'),
                position=data.get('position'),
                hire_date=data.get('hire_date')  # Already a date object from Marshmallow
            )
            
            db.session.add(employee)
            db.session.commit()
            
            return employee, None
            
        except IntegrityError as e:
            db.session.rollback()
            return None, 'Database integrity error: Email must be unique'
        except Exception as e:
            db.session.rollback()
            return None, f'Error creating employee: {str(e)}'
    
    @staticmethod
    def update_employee(employee_id, data):
        """
        Update an existing employee.
        
        Args:
            employee_id (int): Employee ID
            data (dict): Updated employee data
            
        Returns:
            tuple: (Employee object or None, error message or None)
        """
        try:
            employee = db.session.get(Employee, employee_id)

            if not employee:
                return None, 'Employee not found'
            
            # Check email uniqueness if email is being updated
            if 'email' in data and data['email'] != employee.email:
                existing = Employee.query.filter_by(email=data['email']).first()
                if existing:
                    return None, 'Email already exists'
            
            # Update fields
            for key, value in data.items():
                if hasattr(employee, key):
                    setattr(employee, key, value)
            
            db.session.commit()
            return employee, None
            
        except IntegrityError:
            db.session.rollback()
            return None, 'Database integrity error: Email must be unique'
        except Exception as e:
            db.session.rollback()
            return None, f'Error updating employee: {str(e)}'
    
    @staticmethod
    def delete_employee(employee_id):
        """
        Delete an employee.
        
        Args:
            employee_id (int): Employee ID
            
        Returns:
            tuple: (success boolean, error message or None)
        """
        try:
            employee = db.session.get(Employee, employee_id)

            if not employee:
                return False, 'Employee not found'
            
            db.session.delete(employee)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f'Error deleting employee: {str(e)}'
    
    @staticmethod
    def get_employee_tasks(employee_id):
        """
        Get all tasks assigned to an employee.
        
        Args:
            employee_id (int): Employee ID
            
        Returns:
            tuple: (list of tasks or None, error message or None)
        """
        employee = db.session.get(Employee, employee_id)

        if not employee:
            return None, 'Employee not found'
        
        tasks = employee.tasks.all()
        return tasks, None
