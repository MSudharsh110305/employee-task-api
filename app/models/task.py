"""
Task model representing tasks assigned to employees.
"""
from datetime import datetime, date, timezone
from app import db


class Task(db.Model):
    """Task model with assignment and tracking information."""
    
    __tablename__ = 'tasks'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Task Information
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Status and Priority
    status = db.Column(
        db.String(20), 
        nullable=False, 
        default='pending',
        index=True
    )
    priority = db.Column(
        db.String(20), 
        nullable=False, 
        default='medium',
        index=True
    )
    
    # Assignment
    employee_id = db.Column(
        db.Integer, 
        db.ForeignKey('employees.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    
    # Deadlines
    deadline = db.Column(db.Date, nullable=True)
    
    # Timestamps

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Valid choices for status and priority
    VALID_STATUSES = ['pending', 'in_progress', 'completed', 'cancelled']
    VALID_PRIORITIES = ['low', 'medium', 'high', 'urgent']
    
    def __repr__(self):
        """String representation of Task."""
        return f'<Task {self.title}>'
    
    def to_dict(self, include_employee=False):
        """
        Convert task object to dictionary for JSON serialization.
        
        Args:
            include_employee (bool): Whether to include assigned employee details
            
        Returns:
            dict: Task data as dictionary
        """
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'employee_id': self.employee_id,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_employee and self.assigned_employee:
            data['employee'] = {
                'id': self.assigned_employee.id,
                'name': f"{self.assigned_employee.first_name} {self.assigned_employee.last_name}",
                'email': self.assigned_employee.email
            }
        
        return data
    
    @staticmethod
    def from_dict(data):
        """
        Create Task instance from dictionary.
        Handles both date objects (from Marshmallow) and date strings.
        
        Args:
            data (dict): Dictionary containing task data
            
        Returns:
            Task: New Task instance
        """
        task = Task(
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'medium'),
            employee_id=data.get('employee_id')
        )
        
        # Handle deadline if provided
        deadline_value = data.get('deadline')
        if deadline_value:
            # Check if it's already a date object (from Marshmallow)
            if isinstance(deadline_value, date):
                task.deadline = deadline_value
            # Otherwise try to parse string
            elif isinstance(deadline_value, str):
                try:
                    task.deadline = datetime.strptime(deadline_value, '%Y-%m-%d').date()
                except ValueError:
                    pass  # Invalid date format, leave as None
        
        return task
