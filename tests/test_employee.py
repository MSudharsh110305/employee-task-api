"""
Test cases for Employee API endpoints.
"""
import json


def test_root_endpoint(client):
    """Test root endpoint returns API information."""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'Employee-Task Management API' in data['message']


def test_create_employee(client, init_database):
    """Test creating a new employee."""
    employee_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@test.com',
        'department': 'Engineering',
        'position': 'Backend Developer'
    }
    response = client.post('/api/employees', 
                          data=json.dumps(employee_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['email'] == 'john.doe@test.com'


def test_create_employee_duplicate_email(client, sample_employee):
    """Test creating employee with duplicate email fails."""
    employee_data = {
        'first_name': 'Another',
        'last_name': 'User',
        'email': sample_employee.email
    }
    response = client.post('/api/employees',
                          data=json.dumps(employee_data),
                          content_type='application/json')
    assert response.status_code == 400


def test_create_employee_missing_fields(client, init_database):
    """Test creating employee with missing required fields fails."""
    employee_data = {
        'first_name': 'John'
        # Missing last_name and email
    }
    response = client.post('/api/employees',
                          data=json.dumps(employee_data),
                          content_type='application/json')
    assert response.status_code == 400


def test_get_all_employees(client, sample_employee):
    """Test retrieving all employees."""
    response = client.get('/api/employees')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert len(data['data']) >= 1


def test_get_employee_by_id(client, sample_employee):
    """Test retrieving a single employee by ID."""
    response = client.get(f'/api/employees/{sample_employee.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['email'] == sample_employee.email


def test_get_employee_not_found(client, init_database):
    """Test retrieving non-existent employee returns 404."""
    response = client.get('/api/employees/99999')
    assert response.status_code == 404


def test_update_employee(client, sample_employee):
    """Test updating an employee."""
    update_data = {
        'position': 'Senior Software Engineer'
    }
    response = client.put(f'/api/employees/{sample_employee.id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['position'] == 'Senior Software Engineer'


def test_delete_employee(client, sample_employee):
    """Test deleting an employee."""
    response = client.delete(f'/api/employees/{sample_employee.id}')
    assert response.status_code == 200
    
    # Verify deletion
    response = client.get(f'/api/employees/{sample_employee.id}')
    assert response.status_code == 404


def test_filter_employees_by_department(client, sample_employee):
    """Test filtering employees by department."""
    response = client.get(f'/api/employees?department={sample_employee.department}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['data']) >= 1


def test_pagination(client, init_database):
    """Test employee pagination."""
    response = client.get('/api/employees?page=1&per_page=5')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'pagination' in data
    assert data['pagination']['page'] == 1
