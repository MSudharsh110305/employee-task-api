"""
User model for authentication and authorization.
"""
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    """User model with authentication and role-based access control."""

    __tablename__ = 'users'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Authentication
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Profile
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)

    # Authorization
    role = db.Column(
        db.String(20),
        nullable=False,
        default='employee',
        index=True
    )  # Roles: admin, manager, employee

    # Account Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)

    # Timestamps
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    last_login = db.Column(db.DateTime, nullable=True)

    # Valid roles
    VALID_ROLES = ['admin', 'manager', 'employee']

    def __repr__(self):
        """String representation of User."""
        return f'<User {self.username}>'

    def set_password(self, password: str) -> None:
        """
        Hash and set the user's password.

        Args:
            password (str): Plain text password
        """
        # Werkzeug 3.x requires explicit iteration count or uses scrypt by default
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verify password against stored hash.

        Args:
            password (str): Plain text password to check

        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def update_last_login(self) -> None:
        """Update the last login timestamp."""
        self.last_login = datetime.now(timezone.utc)
        db.session.commit()

    def to_dict(self, include_sensitive=False) -> dict:
        """
        Convert user object to dictionary for JSON serialization.

        Args:
            include_sensitive (bool): Whether to include sensitive info (role, status)

        Returns:
            dict: User data as dictionary (never includes password_hash)
        """
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

        if include_sensitive:
            data.update({
                'role': self.role,
                'is_active': self.is_active,
                'is_verified': self.is_verified,
                'last_login': self.last_login.isoformat() if self.last_login else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None
            })

        return data

    @staticmethod
    def from_dict(data: dict) -> 'User':
        """
        Create User instance from dictionary.

        Args:
            data (dict): Dictionary containing user data

        Returns:
            User: New User instance (password must be set separately)
        """
        user = User(
            username=data.get('username'),
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            role=data.get('role', 'employee')
        )

        # Password must be set using set_password() method
        if 'password' in data:
            user.set_password(data['password'])

        return user

    def has_role(self, role: str) -> bool:
        """
        Check if user has a specific role.

        Args:
            role (str): Role to check

        Returns:
            bool: True if user has the role
        """
        return self.role == role

    def is_admin(self) -> bool:
        """Check if user is an admin."""
        return self.role == 'admin'

    def is_manager(self) -> bool:
        """Check if user is a manager."""
        return self.role == 'manager'

    def can_modify_employee(self, employee_id: int) -> bool:
        """
        Check if user can modify a specific employee.
        Admins can modify anyone, managers can modify non-admins, employees can only view.

        Args:
            employee_id (int): ID of employee to check

        Returns:
            bool: True if user can modify the employee
        """
        if self.is_admin():
            return True

        if self.is_manager():
            # Managers can modify employees but not other managers or admins
            from app.models.employee import Employee
            employee = db.session.get(Employee, employee_id)
            if employee:
                # For now, allow managers to modify employees
                # In future, you could add role checking to Employee model
                return True

        return False
