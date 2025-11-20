"""
Integration tests for employee API endpoints.
"""
import json
import pytest
from tests.factories import UserFactory, AdminUserFactory, ManagerUserFactory, EmployeeFactory


class TestEmployeeListEndpoint:
    """Integration tests for GET /api/employees."""

    def test_get_employees_without_auth(self, client, init_database):
        """Test accessing employees without authentication fails."""
        response = client.get('/api/employees')

        assert response.status_code == 401

    def test_get_employees_with_auth(self, client, init_database):
        """Test getting employees list with authentication."""
        user = UserFactory(username='testuser', password='password123')
        EmployeeFactory.create_batch(5)

        # Login to get token
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'testuser', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Get employees
        response = client.get(
            '/api/employees',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['data']) == 5

    def test_get_employees_pagination(self, client, init_database):
        """Test employee pagination works correctly."""
        user = UserFactory(username='testuser', password='password123')
        EmployeeFactory.create_batch(15)

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'testuser', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Get first page
        response = client.get(
            '/api/employees?page=1&per_page=10',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['data']) == 10


class TestEmployeeCreateEndpoint:
    """Integration tests for POST /api/employees."""

    def test_create_employee_as_employee_fails(self, client, init_database):
        """Test regular employee cannot create employees."""
        user = UserFactory(username='employee', password='password123', role='employee')

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'employee', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Try to create employee
        employee_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'department': 'Engineering'
        }

        response = client.post(
            '/api/employees',
            data=json.dumps(employee_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 403

    def test_create_employee_as_manager_success(self, client, init_database):
        """Test manager can create employees."""
        manager = ManagerUserFactory(username='manager', password='password123')

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'manager', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Create employee
        employee_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'department': 'Marketing',
            'position': 'Marketing Manager'
        }

        response = client.post(
            '/api/employees',
            data=json.dumps(employee_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['email'] == 'jane@example.com'

    def test_create_employee_invalid_data(self, client, init_database):
        """Test creating employee with invalid data fails."""
        manager = ManagerUserFactory(username='manager', password='password123')

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'manager', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Missing required fields
        employee_data = {'first_name': 'John'}

        response = client.post(
            '/api/employees',
            data=json.dumps(employee_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 400


class TestEmployeeDetailEndpoint:
    """Integration tests for GET /api/employees/<id>."""

    def test_get_employee_detail(self, client, init_database):
        """Test getting single employee details."""
        user = UserFactory(username='testuser', password='password123')
        employee = EmployeeFactory(first_name='John', last_name='Doe')

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'testuser', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Get employee detail
        response = client.get(
            f'/api/employees/{employee.id}',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['first_name'] == 'John'
        assert data['data']['last_name'] == 'Doe'

    def test_get_nonexistent_employee(self, client, init_database):
        """Test getting non-existent employee returns 404."""
        user = UserFactory(username='testuser', password='password123')

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'testuser', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Try to get non-existent employee
        response = client.get(
            '/api/employees/99999',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 404


class TestEmployeeDeleteEndpoint:
    """Integration tests for DELETE /api/employees/<id>."""

    def test_delete_employee_as_non_admin_fails(self, client, init_database):
        """Test non-admin cannot delete employees."""
        manager = ManagerUserFactory(username='manager', password='password123')
        employee = EmployeeFactory()

        # Login as manager
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'manager', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Try to delete
        response = client.delete(
            f'/api/employees/{employee.id}',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 403

    def test_delete_employee_as_admin_success(self, client, init_database):
        """Test admin can delete employees."""
        admin = AdminUserFactory(username='admin', password='password123')
        employee = EmployeeFactory()

        # Login as admin
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'admin', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Delete employee
        response = client.delete(
            f'/api/employees/{employee.id}',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
