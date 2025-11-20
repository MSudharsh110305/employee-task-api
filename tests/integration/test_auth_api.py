"""
Integration tests for authentication API.
"""
import json
import pytest
from tests.factories import UserFactory, AdminUserFactory


class TestAuthRegistration:
    """Integration tests for user registration."""

    def test_register_success(self, client, init_database):
        """Test successful user registration."""
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepassword123',
            'first_name': 'New',
            'last_name': 'User'
        }

        response = client.post(
            '/api/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'access_token' in data['data']
        assert 'refresh_token' in data['data']
        assert data['data']['user']['username'] == 'newuser'

    def test_register_duplicate_email(self, client, init_database):
        """Test registration with duplicate email fails."""
        UserFactory(email='existing@example.com')

        user_data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'password123'
        }

        response = client.post(
            '/api/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'email' in str(data).lower()

    def test_register_missing_fields(self, client, init_database):
        """Test registration with missing required fields."""
        user_data = {'username': 'incomplete'}

        response = client.post(
            '/api/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )

        assert response.status_code == 400


class TestAuthLogin:
    """Integration tests for user login."""

    def test_login_success(self, client, init_database):
        """Test successful login."""
        user = UserFactory(username='testuser', password='password123')

        login_data = {
            'username': 'testuser',
            'password': 'password123'
        }

        response = client.post(
            '/api/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'access_token' in data['data']
        assert 'refresh_token' in data['data']

    def test_login_invalid_password(self, client, init_database):
        """Test login with invalid password."""
        UserFactory(username='testuser', password='correctpassword')

        login_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

        response = client.post(
            '/api/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )

        assert response.status_code == 401

    def test_login_inactive_user(self, client, init_database):
        """Test login with inactive user account."""
        user = UserFactory(username='inactive', password='password123')
        user.is_active = False
        from app import db
        db.session.commit()

        login_data = {
            'username': 'inactive',
            'password': 'password123'
        }

        response = client.post(
            '/api/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )

        assert response.status_code == 403


class TestProtectedEndpoints:
    """Integration tests for JWT-protected endpoints."""

    def test_access_without_token(self, client, init_database):
        """Test accessing protected endpoint without token."""
        response = client.get('/api/employees')

        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'authorization' in str(data).lower() or 'token' in str(data).lower()

    def test_access_with_valid_token(self, client, init_database):
        """Test accessing protected endpoint with valid token."""
        user = AdminUserFactory(username='admin', password='password123')

        # Login to get token
        login_response = client.post(
            '/api/auth/login',
            data=json.dumps({'username': 'admin', 'password': 'password123'}),
            content_type='application/json'
        )
        token = json.loads(login_response.data)['data']['access_token']

        # Access protected endpoint
        response = client.get(
            '/api/employees',
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200
