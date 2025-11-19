"""
Unit tests for database models.
"""
import pytest
from datetime import date, datetime
from app.models import User, Employee, Task


class TestUserModel:
    """Unit tests for User model."""

    def test_user_password_hashing(self, init_database):
        """Test password hashing works correctly."""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')

        assert user.password_hash is not None
        assert user.password_hash != 'password123'
        assert user.check_password('password123') is True
        assert user.check_password('wrongpassword') is False

    def test_user_to_dict(self, init_database):
        """Test user to_dict serialization."""
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role='admin'
        )
        user.set_password('password123')

        data = user.to_dict(include_sensitive=True)

        assert data['username'] == 'testuser'
        assert data['email'] == 'test@example.com'
        assert data['role'] == 'admin'
        assert 'password_hash' not in data  # Should never include password

    def test_user_roles(self, init_database):
        """Test user role checking methods."""
        admin = User(username='admin', email='admin@test.com', role='admin')
        manager = User(username='manager', email='manager@test.com', role='manager')
        employee = User(username='employee', email='employee@test.com', role='employee')

        assert admin.is_admin() is True
        assert admin.is_manager() is False

        assert manager.is_admin() is False
        assert manager.is_manager() is True

        assert employee.is_admin() is False
        assert employee.is_manager() is False


class TestEmployeeModel:
    """Unit tests for Employee model."""

    def test_employee_to_dict(self, init_database):
        """Test employee to_dict serialization."""
        employee = Employee(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            department='Engineering',
            position='Developer'
        )

        data = employee.to_dict()

        assert data['first_name'] == 'John'
        assert data['last_name'] == 'Doe'
        assert data['email'] == 'john@example.com'
        assert data['department'] == 'Engineering'

    def test_employee_from_dict(self, init_database):
        """Test employee creation from dict."""
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'hire_date': '2024-01-15'
        }

        employee = Employee.from_dict(data)

        assert employee.first_name == 'Jane'
        assert employee.last_name == 'Smith'
        assert employee.hire_date == date(2024, 1, 15)


class TestTaskModel:
    """Unit tests for Task model."""

    def test_task_valid_statuses(self):
        """Test valid task statuses."""
        assert 'pending' in Task.VALID_STATUSES
        assert 'in_progress' in Task.VALID_STATUSES
        assert 'completed' in Task.VALID_STATUSES
        assert 'cancelled' in Task.VALID_STATUSES

    def test_task_to_dict(self, init_database):
        """Test task to_dict serialization."""
        task = Task(
            title='Test Task',
            description='Test description',
            status='pending',
            priority='high'
        )

        data = task.to_dict()

        assert data['title'] == 'Test Task'
        assert data['status'] == 'pending'
        assert data['priority'] == 'high'
