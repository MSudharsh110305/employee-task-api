"""
Test data factories using Factory Boy.
"""
import factory
from factory.faker import Faker
from datetime import date, timedelta
from werkzeug.security import generate_password_hash
import random
from app import db
from app.models import Employee, Task, User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating User test data."""

    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'flush'

    username = Faker('user_name')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    role = 'employee'
    is_active = True
    is_verified = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override create to set password before commit."""
        password = kwargs.pop('password', 'testpassword123')
        obj = model_class(*args, **kwargs)
        obj.set_password(password)
        db.session.add(obj)
        db.session.commit()
        return obj


class AdminUserFactory(UserFactory):
    """Factory for creating Admin users."""
    role = 'admin'
    is_verified = True


class ManagerUserFactory(UserFactory):
    """Factory for creating Manager users."""
    role = 'manager'
    is_verified = True


class EmployeeFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Employee test data."""

    class Meta:
        model = Employee
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    phone = Faker('phone_number')
    department = factory.Faker('random_element', elements=[
        'Engineering', 'Sales', 'HR', 'Marketing', 'Finance', 'Operations'
    ])
    position = factory.Faker('random_element', elements=[
        'Software Engineer', 'Senior Engineer', 'Manager',
        'Director', 'Analyst', 'Specialist'
    ])
    hire_date = factory.LazyFunction(
        lambda: date.today() - timedelta(days=random.randint(30, 1000))
    )


class TaskFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Task test data."""

    class Meta:
        model = Task
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    title = Faker('sentence', nb_words=6)
    description = Faker('paragraph', nb_sentences=3)
    status = factory.Faker('random_element', elements=Task.VALID_STATUSES)
    priority = factory.Faker('random_element', elements=Task.VALID_PRIORITIES)
    employee_id = None  # Can be set explicitly or use SubFactory
    deadline = factory.LazyFunction(
        lambda: date.today() + timedelta(days=random.randint(7, 90))
    )


class TaskWithEmployeeFactory(TaskFactory):
    """Factory for creating Task with associated Employee."""

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create task with employee."""
        # Remove employee from kwargs if present (SubFactory adds it)
        kwargs.pop('employee', None)

        # Create employee first if employee_id not provided
        if 'employee_id' not in kwargs or kwargs['employee_id'] is None:
            employee = EmployeeFactory()
            kwargs['employee_id'] = employee.id

        # Create task using parent class
        task = model_class(*args, **kwargs)
        db.session.add(task)
        db.session.commit()
        return task
