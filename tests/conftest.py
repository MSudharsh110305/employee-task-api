"""
Pytest configuration and fixtures for testing.
"""
import pytest
from app import create_app, db
from app.models import Employee, Task


@pytest.fixture(scope='session')
def app():
    """Create application instance for testing."""
    app = create_app('testing')
    return app


@pytest.fixture(scope='session')
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def init_database(app):
    """Initialize database for each test."""
    with app.app_context():
        # Create tables
        db.create_all()
        
        yield db
        
        # Clean up after test
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_employee(init_database):
    """Create a sample employee for testing."""
    employee = Employee(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        department="Engineering",
        position="Software Engineer"
    )
    db.session.add(employee)
    db.session.commit()
    return employee


@pytest.fixture
def sample_task(init_database, sample_employee):
    """Create a sample task for testing."""
    task = Task(
        title="Test Task",
        description="Test description",
        status="pending",
        priority="medium",
        employee_id=sample_employee.id
    )
    db.session.add(task)
    db.session.commit()
    return task
