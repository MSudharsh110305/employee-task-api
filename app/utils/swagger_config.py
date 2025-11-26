"""
Swagger/OpenAPI configuration for API documentation.
"""
from flasgger import Swagger

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/api/docs/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/api/docs/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs/"
}

# API documentation template
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Employee-Task Management API",
        "description": "Production-ready REST API for employee and task management with JWT authentication",
        "contact": {
            "name": "API Support",
            "url": "https://github.com/yourusername/employee-task-api",
        },
        "version": "2.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ],
    "tags": [
        {
            "name": "Authentication",
            "description": "User authentication and authorization endpoints"
        },
        {
            "name": "Employees",
            "description": "Employee management endpoints"
        },
        {
            "name": "Tasks",
            "description": "Task management endpoints"
        }
    ],
    "definitions": {
        "User": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "username": {"type": "string"},
                "email": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "role": {"type": "string", "enum": ["admin", "manager", "employee"]},
                "is_active": {"type": "boolean"},
                "created_at": {"type": "string", "format": "date-time"}
            }
        },
        "Employee": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "email": {"type": "string"},
                "phone": {"type": "string"},
                "department": {"type": "string"},
                "position": {"type": "string"},
                "hire_date": {"type": "string", "format": "date"},
                "created_at": {"type": "string", "format": "date-time"}
            }
        },
        "Task": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "status": {"type": "string", "enum": ["pending", "in_progress", "completed", "cancelled"]},
                "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"]},
                "employee_id": {"type": "integer"},
                "deadline": {"type": "string", "format": "date"},
                "created_at": {"type": "string", "format": "date-time"}
            }
        },
        "Error": {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "message": {"type": "string"},
                "error": {"type": "string"}
            }
        }
    }
}


def init_swagger(app):
    """
    Initialize Swagger API documentation.

    Args:
        app: Flask application instance
    """
    Swagger(app, config=swagger_config, template=swagger_template)
