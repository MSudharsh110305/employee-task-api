"""
Test cases for Task API endpoints.
"""
import json


def test_create_task(client, sample_employee):
    """Test creating a new task."""
    task_data = {
        'title': 'Test Task',
        'description': 'Test description',
        'status': 'pending',
        'priority': 'high',
        'employee_id': sample_employee.id
    }
    response = client.post('/api/tasks',
                          data=json.dumps(task_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['title'] == 'Test Task'


def test_create_task_invalid_employee(client, init_database):
    """Test creating task with invalid employee ID fails."""
    task_data = {
        'title': 'Test Task',
        'employee_id': 99999
    }
    response = client.post('/api/tasks',
                          data=json.dumps(task_data),
                          content_type='application/json')
    assert response.status_code == 400


def test_create_task_invalid_status(client, init_database):
    """Test creating task with invalid status fails."""
    task_data = {
        'title': 'Test Task',
        'status': 'invalid_status'
    }
    response = client.post('/api/tasks',
                          data=json.dumps(task_data),
                          content_type='application/json')
    assert response.status_code == 400


def test_get_all_tasks(client, sample_task):
    """Test retrieving all tasks."""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert len(data['data']) >= 1


def test_get_task_by_id(client, sample_task):
    """Test retrieving a single task by ID."""
    response = client.get(f'/api/tasks/{sample_task.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['title'] == sample_task.title


def test_update_task(client, sample_task):
    """Test updating a task."""
    update_data = {
        'status': 'completed',
        'priority': 'urgent'
    }
    response = client.put(f'/api/tasks/{sample_task.id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['status'] == 'completed'
    assert data['data']['priority'] == 'urgent'


def test_delete_task(client, sample_task):
    """Test deleting a task."""
    response = client.delete(f'/api/tasks/{sample_task.id}')
    assert response.status_code == 200
    
    # Verify deletion
    response = client.get(f'/api/tasks/{sample_task.id}')
    assert response.status_code == 404


def test_filter_tasks_by_status(client, sample_task):
    """Test filtering tasks by status."""
    response = client.get(f'/api/tasks?status={sample_task.status}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) >= 1


def test_filter_tasks_by_priority(client, sample_task):
    """Test filtering tasks by priority."""
    response = client.get(f'/api/tasks?priority={sample_task.priority}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) >= 1


def test_get_employee_tasks(client, sample_employee, sample_task):
    """Test retrieving all tasks for a specific employee."""
    response = client.get(f'/api/employees/{sample_employee.id}/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) >= 1
    assert data['data'][0]['employee_id'] == sample_employee.id
