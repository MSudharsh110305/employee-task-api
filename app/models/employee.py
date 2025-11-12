"""
Employee model representing employees in the system.
"""
from datetime import datetime, date, timezone
from app import db


class Employee(db.Model):
    """Employee model with personal and professional information."""
    
    __tablename__ = 'employees'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Personal Information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    
    # Professional Information
    department = db.Column(db.String(100), nullable=True, index=True)
    position = db.Column(db.String(100), nullable=True)
    hire_date = db.Column(db.Date, nullable=True)
    
    # Timestamps

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    tasks = db.relationship('Task', backref='assigned_employee', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        """String representation of Employee."""
        return f'<Employee {self.first_name} {self.last_name}>'
    
    def to_dict(self, include_tasks=False):
        """
        Convert employee object to dictionary for JSON serialization.
        
        Args:
            include_tasks (bool): Whether to include associated tasks
            
        Returns:
            dict: Employee data as dictionary
        """
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'department': self.department,
            'position': self.position,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_tasks:
            data['tasks'] = [task.to_dict() for task in self.tasks]
        
        return data
    
    @staticmethod
    def from_dict(data):
        """
        Create Employee instance from dictionary.
        Handles both date objects (from Marshmallow) and date strings.
        
        Args:
            data (dict): Dictionary containing employee data
            
        Returns:
            Employee: New Employee instance
        """
        employee = Employee(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            department=data.get('department'),
            position=data.get('position')
        )
        
        # Handle hire_date if provided
        hire_date_value = data.get('hire_date')
        if hire_date_value:
            # Check if it's already a date object (from Marshmallow)
            if isinstance(hire_date_value, date):
                employee.hire_date = hire_date_value
            # Otherwise try to parse string
            elif isinstance(hire_date_value, str):
                try:
                    employee.hire_date = datetime.strptime(hire_date_value, '%Y-%m-%d').date()
                except ValueError:
                    pass  # Invalid date format, leave as None
        
        return employee
