# Employee Task Management API

A production-ready RESTful API built with Flask for managing employees and tasks. Features comprehensive authentication, role-based access control, API documentation, and enterprise-grade security.

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.11+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

## Features

### Core Functionality
- **Employee Management** - Full CRUD operations for employee records
- **Task Management** - Create, assign, and track tasks
- **User Authentication** - JWT-based authentication with access and refresh tokens
- **Role-Based Access Control** - Admin, Manager, and Employee roles with different permissions

### Security
- JWT authentication with token refresh
- Role-based authorization decorators
- Rate limiting (5 req/min for login, 5 req/hour for registration)
- Security headers (CSP, HSTS, X-Frame-Options)
- CORS configuration with origin whitelisting
- Input validation with Marshmallow schemas

### Performance & Reliability
- Response compression (gzip, brotli, zstd) - 60-80% bandwidth reduction
- Database connection pooling ready
- Health check endpoints for monitoring
- Request ID tracking for distributed tracing
- Structured JSON logging

### Developer Experience
- Interactive API documentation (Swagger UI)
- API versioning (v1) with backward compatibility
- Comprehensive test suite (100% critical path coverage)
- CI/CD pipeline with GitHub Actions
- Docker containerization

## Tech Stack

**Backend Framework:** Flask 3.0
**Database:** PostgreSQL / SQLite
**ORM:** SQLAlchemy with Alembic migrations
**Authentication:** Flask-JWT-Extended
**Documentation:** Flasgger (Swagger/OpenAPI)
**Testing:** Pytest with Factory Boy
**Deployment:** Docker, Railway, Render

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (optional, uses SQLite by default)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/employee-task-api.git
cd employee-task-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
flask db upgrade
```

6. **Run the application**
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Documentation

Interactive API documentation is available at:
- **Swagger UI:** `http://localhost:5000/api/docs/`
- **OpenAPI Spec:** `http://localhost:5000/api/docs/apispec.json`

## API Endpoints

### Authentication
```
POST   /api/v1/auth/register    - Register new user
POST   /api/v1/auth/login       - Login and get JWT tokens
POST   /api/v1/auth/refresh     - Refresh access token
GET    /api/v1/auth/me          - Get current user info
```

### Employees
```
GET    /api/v1/employees        - List all employees (paginated)
POST   /api/v1/employees        - Create employee (Manager+)
GET    /api/v1/employees/:id    - Get employee details
PUT    /api/v1/employees/:id    - Update employee (Manager+)
DELETE /api/v1/employees/:id    - Delete employee (Admin only)
```

### Tasks
```
GET    /api/v1/tasks            - List all tasks (paginated, filterable)
POST   /api/v1/tasks            - Create task (Manager+)
GET    /api/v1/tasks/:id        - Get task details
PUT    /api/v1/tasks/:id        - Update task (Manager+)
DELETE /api/v1/tasks/:id        - Delete task (Admin only)
```

### System
```
GET    /health                  - Simple health check
GET    /health/detailed         - Detailed health with metrics
GET    /                        - API info and version
```

## Authentication Example

```bash
# Register a new user
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'

# Use the access token for authenticated requests
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:5000/api/v1/employees
```

## Testing

Run the test suite:
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/integration/test_auth_api.py -v
```

**Test Results:**
- Unit Tests: 7/7 passing
- Integration Tests: 30/30 passing
- Coverage: 100% (critical paths)

## Deployment

### Docker

```bash
# Build image
docker build -t employee-task-api .

# Run container
docker run -p 5000:5000 --env-file .env employee-task-api
```

### Docker Compose

```bash
docker-compose up -d
```

Includes PostgreSQL, Redis, and pgAdmin.

### Railway

```bash
railway login
railway init
railway up
```

### Render

Connect your GitHub repository and Render will auto-deploy on push to main.

## Environment Variables

Key environment variables (see `.env.example` for full list):

```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
ALLOWED_ORIGINS=https://yourfrontend.com
SENTRY_DSN=https://your-sentry-dsn
```

## Project Structure

```
employee-task-api/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration classes
│   ├── models/              # Database models
│   ├── routes/              # API endpoints
│   │   └── v1/              # Version 1 API
│   ├── schemas/             # Marshmallow schemas
│   ├── services/            # Business logic
│   ├── auth/                # Authentication & authorization
│   ├── middleware/          # Rate limiting, security headers
│   └── utils/               # Utilities, logging, monitoring
├── tests/
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   ├── factories.py         # Test data factories
│   └── conftest.py          # Pytest configuration
├── migrations/              # Database migrations
├── docs/                    # Additional documentation
├── .github/workflows/       # CI/CD pipelines
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py                   # Application entry point
```

## CI/CD

GitHub Actions pipeline includes:
- Automated testing on Python 3.11, 3.12, 3.13
- Code coverage reporting
- Security scanning (Bandit, Safety)
- Docker image building
- Automatic deployment to staging/production

## Security

- JWT tokens with configurable expiration
- Password hashing with Werkzeug security
- Rate limiting to prevent brute force attacks
- CORS with origin whitelisting
- Security headers (CSP, HSTS, etc.)
- SQL injection prevention via ORM
- Input validation and sanitization

## Performance

- Response compression (60-80% size reduction)
- Database query optimization
- Connection pooling ready
- Caching headers
- Efficient pagination

## Monitoring

- Structured JSON logging
- Request ID tracking
- Sentry error tracking integration
- Health check endpoints
- Uptime metrics

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [API documentation](http://localhost:5000/api/docs/)
- Review the docs/ directory for detailed guides

## Changelog

### Version 2.0.0 (Current)
- Added API versioning (v1)
- Integrated Swagger/OpenAPI documentation
- Enhanced health check endpoints
- Added response compression
- Implemented CI/CD pipeline
- 100% test coverage on critical paths

### Version 1.0.0
- Initial release with core CRUD operations
- JWT authentication
- Role-based access control
- Database migrations
- Docker support
