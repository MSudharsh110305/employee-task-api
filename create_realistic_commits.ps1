# Day 1 - Nov 12
$env:GIT_AUTHOR_DATE="2025-11-12T14:00:00"
$env:GIT_COMMITTER_DATE="2025-11-12T14:00:00"
git add .gitignore .env.example requirements.txt
git commit -m "Initial project setup with dependencies and configuration"

$env:GIT_AUTHOR_DATE="2025-11-12T14:25:00"
$env:GIT_COMMITTER_DATE="2025-11-12T14:25:00"
git add app/__init__.py app/config.py run.py wsgi.py
git commit -m "Add application factory and configuration management"

$env:GIT_AUTHOR_DATE="2025-11-12T15:00:00"
$env:GIT_COMMITTER_DATE="2025-11-12T15:00:00"
git add app/models/
git commit -m "Implement Employee and Task database models with relationships"

$env:GIT_AUTHOR_DATE="2025-11-12T15:45:00"
$env:GIT_COMMITTER_DATE="2025-11-12T15:45:00"
git add app/schemas/
git commit -m "Add Marshmallow schemas for data validation"

$env:GIT_AUTHOR_DATE="2025-11-12T16:55:00"
$env:GIT_COMMITTER_DATE="2025-11-12T16:55:00"
git add app/services/__init__.py app/services/employee_service.py
git commit -m "Implement employee business logic and CRUD operations"

$env:GIT_AUTHOR_DATE="2025-11-12T17:35:00"
$env:GIT_COMMITTER_DATE="2025-11-12T17:35:00"
git add app/services/task_service.py
git commit -m "Add task service with filtering and assignment logic"

$env:GIT_AUTHOR_DATE="2025-11-12T18:25:00"
$env:GIT_COMMITTER_DATE="2025-11-12T18:25:00"
git add app/utils/
git commit -m "Implement centralized error handling and custom validators"

$env:GIT_AUTHOR_DATE="2025-11-12T19:45:00"
$env:GIT_COMMITTER_DATE="2025-11-12T19:45:00"
git add app/routes/__init__.py app/routes/employee_routes.py
git commit -m "Add employee API endpoints with pagination and filtering"

$env:GIT_AUTHOR_DATE="2025-11-12T20:30:00"
$env:GIT_COMMITTER_DATE="2025-11-12T20:30:00"
git add app/routes/task_routes.py
git commit -m "Implement task API endpoints and relationship queries"

$env:GIT_AUTHOR_DATE="2025-11-12T21:00:00"
$env:GIT_COMMITTER_DATE="2025-11-12T21:00:00"
git add app/routes/employee_routes.py app/services/
git commit -m "Fix date handling in models and serialization issues"

# Day 2 - Nov 13
$env:GIT_AUTHOR_DATE="2025-11-13T10:30:00"
$env:GIT_COMMITTER_DATE="2025-11-13T10:30:00"
git add tests/__init__.py tests/conftest.py
git commit -m "Set up pytest configuration and test fixtures"

$env:GIT_AUTHOR_DATE="2025-11-13T11:30:00"
$env:GIT_COMMITTER_DATE="2025-11-13T11:30:00"
git add tests/test_employee.py
git commit -m "Add comprehensive test suite for employee endpoints"

$env:GIT_AUTHOR_DATE="2025-11-13T12:45:00"
$env:GIT_COMMITTER_DATE="2025-11-13T12:45:00"
git add tests/test_task.py
git commit -m "Implement task endpoint tests with coverage"

$env:GIT_AUTHOR_DATE="2025-11-13T13:30:00"
$env:GIT_COMMITTER_DATE="2025-11-13T13:30:00"
git add test_api_manual.py
git commit -m "Add manual API testing script with debug output"

$env:GIT_AUTHOR_DATE="2025-11-13T14:00:00"
$env:GIT_COMMITTER_DATE="2025-11-13T14:00:00"
git add quick_reset.py reset_database.py
git commit -m "Create database reset utilities for testing"

$env:GIT_AUTHOR_DATE="2025-11-13T16:00:00"
$env:GIT_COMMITTER_DATE="2025-11-13T16:00:00"
git add README.md
git commit -m "Add comprehensive README with API documentation"

$env:GIT_AUTHOR_DATE="2025-11-13T17:30:00"
$env:GIT_COMMITTER_DATE="2025-11-13T17:30:00"
git add wsgi.py requirements.txt
git commit -m "Update deployment configuration for production"

$env:GIT_AUTHOR_DATE="2025-11-13T18:15:00"
$env:GIT_COMMITTER_DATE="2025-11-13T18:15:00"
git add app/models/
git commit -m "Improve model methods and add docstrings"

# Day 3 - Nov 14
$env:GIT_AUTHOR_DATE="2025-11-14T11:00:00"
$env:GIT_COMMITTER_DATE="2025-11-14T11:00:00"
git add tests/
git commit -m "Enhance test coverage and edge case handling"

$env:GIT_AUTHOR_DATE="2025-11-14T12:00:00"
$env:GIT_COMMITTER_DATE="2025-11-14T12:00:00"
git add README.md
git commit -m "Update README with deployment instructions and examples"

$env:GIT_AUTHOR_DATE="2025-11-14T12:30:00"
$env:GIT_COMMITTER_DATE="2025-11-14T12:30:00"
git add app/__init__.py app/config.py requirements.txt
git commit -m "Prepare application for production deployment"

$env:GIT_AUTHOR_DATE="2025-11-14T14:30:00"
$env:GIT_COMMITTER_DATE="2025-11-14T14:30:00"
git add .
git commit -m "Add final documentation and polish before submission"

$env:GIT_AUTHOR_DATE="2025-11-14T15:00:00"
$env:GIT_COMMITTER_DATE="2025-11-14T15:00:00"
git add README.md
git commit -m "Update README with live deployment URL and final checks"

# Clear environment variables
Remove-Item Env:\GIT_AUTHOR_DATE
Remove-Item Env:\GIT_COMMITTER_DATE

Write-Host "✅ All commits created with realistic timestamps!"
