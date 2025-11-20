"""
Integration tests for task API endpoints.
"""
import json
import pytest
from tests.factories import UserFactory, AdminUserFactory, ManagerUserFactory, EmployeeFactory, TaskFactory, TaskWithEmployeeFactory


class TestTaskListEndpoint:
    """Integration tests for GET /api/tasks."""

    def test_get_tasks_without_auth(self, client, init_database):
        """Test accessing tasks without authentication fails."""
        response = client.get('/api/tasks')

        assert response.status_code == 401

    def test_get_tasks_with_auth(self, client, init_database):
        """Test getting tasks list with authentication."""
        user = UserFactory(username='testuser', password='password123')
        TaskWithEmployeeFactory.create_batch(5)

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'testuser', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Get tasks
        response = client.get(
            '/api/tasks',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['data']) == 5

    def test_get_tasks_filter_by_status(self, client, init_database):
        """Test filtering tasks by status."""
        user = UserFactory(username='testuser', password='password123')
        employee = EmployeeFactory()

        # Create tasks with different statuses
        TaskFactory(employee_id=employee.id, status='pending')
        TaskFactory(employee_id=employee.id, status='pending')
        TaskFactory(employee_id=employee.id, status='completed')

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'testuser', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Get pending tasks only
        response = client.get(
            '/api/tasks?status=pending',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['data']) == 2
        assert all(task['status'] == 'pending' for task in data['data'])


class TestTaskCreateEndpoint:
    """Integration tests for POST /api/tasks."""

    def test_create_task_as_employee_fails(self, client, init_database):
        """Test regular employee cannot create tasks."""
        user = UserFactory(username='employee', password='password123', role='employee')
        employee = EmployeeFactory()

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'employee', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Try to create task
        task_data = {
            'title': 'New Task',
            'description': 'Task description',
            'employee_id': employee.id,
            'priority': 'high'
        }

        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 403

    def test_create_task_as_manager_success(self, client, init_database):
        """Test manager can create tasks."""
        manager = ManagerUserFactory(username='manager', password='password123')
        employee = EmployeeFactory()

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'manager', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Create task
        task_data = {
            'title': 'Complete Project Documentation',
            'description': 'Write comprehensive docs for the project',
            'employee_id': employee.id,
            'priority': 'high',
            'status': 'pending'
        }

        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['title'] == 'Complete Project Documentation'
        assert data['data']['priority'] == 'high'

    def test_create_task_missing_required_fields(self, client, init_database):
        """Test creating task with missing fields fails."""
        manager = ManagerUserFactory(username='manager', password='password123')

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'manager', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Missing title
        task_data = {'description': 'Task without title'}

        response = client.post(
            '/api/tasks',
            data=json.dumps(task_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 400


class TestTaskDetailEndpoint:
    """Integration tests for GET /api/tasks/<id>."""

    def test_get_task_detail(self, client, init_database):
        """Test getting single task details."""
        user = UserFactory(username='testuser', password='password123')
        task = TaskWithEmployeeFactory(title='Important Task')

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'testuser', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Get task detail
        response = client.get(
            f'/api/tasks/{task.id}',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['title'] == 'Important Task'

    def test_get_nonexistent_task(self, client, init_database):
        """Test getting non-existent task returns 404."""
        user = UserFactory(username='testuser', password='password123')

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'testuser', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Try to get non-existent task
        response = client.get(
            '/api/tasks/99999',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 404


class TestTaskUpdateEndpoint:
    """Integration tests for PUT /api/tasks/<id>."""

    def test_update_task_as_manager(self, client, init_database):
        """Test manager can update tasks."""
        manager = ManagerUserFactory(username='manager', password='password123')
        task = TaskWithEmployeeFactory(status='pending')

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'manager', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Update task
        update_data = {'status': 'in_progress'}

        response = client.put(
            f'/api/tasks/{task.id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['status'] == 'in_progress'

    def test_update_task_invalid_status(self, client, init_database):
        """Test updating task with invalid status fails."""
        manager = ManagerUserFactory(username='manager', password='password123')
        task = TaskWithEmployeeFactory()

        # Login
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'manager', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Try invalid status
        update_data = {'status': 'invalid_status'}

        response = client.put(
            f'/api/tasks/{task.id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 400


class TestTaskDeleteEndpoint:
    """Integration tests for DELETE /api/tasks/<id>."""

    def test_delete_task_as_non_admin_fails(self, client, init_database):
        """Test non-admin cannot delete tasks."""
        manager = ManagerUserFactory(username='manager', password='password123')
        task = TaskWithEmployeeFactory()

        # Login as manager
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'manager', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Try to delete
        response = client.delete(
            f'/api/tasks/{task.id}',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 403

    def test_delete_task_as_admin_success(self, client, init_database):
        """Test admin can delete tasks."""
        admin = AdminUserFactory(username='admin', password='password123')
        task = TaskWithEmployeeFactory()

        # Login as admin
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'admin', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Delete task
        response = client.delete(
            f'/api/tasks/{task.id}',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
