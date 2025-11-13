"""
Manual API Testing Script with Debug Output
Tests all endpoints with comprehensive error reporting.
"""
import requests
import json
from datetime import datetime, timedelta


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class APITester:
    """API Testing class with comprehensive error reporting"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.test_count = 0
        self.passed_count = 0
        self.failed_count = 0
        self.created_employee_ids = []
        self.created_task_ids = []
    
    def log_info(self, message):
        """Print info message"""
        print(f"{Colors.BLUE}ℹ️  {message}{Colors.RESET}")
    
    def log_success(self, message):
        """Print success message"""
        print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")
    
    def log_error(self, message):
        """Print error message"""
        print(f"{Colors.RED}❌ {message}{Colors.RESET}")
    
    def log_warning(self, message):
        """Print warning message"""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")
    
    def log_section(self, title):
        """Print section header"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}{Colors.RESET}\n")
    
    def make_request(self, method, endpoint, data=None, params=None):
        """
        Make HTTP request with error handling
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint
            data (dict): Request body data
            params (dict): Query parameters
            
        Returns:
            tuple: (response object, success boolean, error message)
        """
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        try:
            self.log_info(f"Request: {method} {url}")
            if data:
                print(f"  Body: {json.dumps(data, indent=2)}")
            if params:
                print(f"  Params: {params}")
            
            if method == "GET":
                response = requests.get(url, params=params, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return None, False, f"Invalid HTTP method: {method}"
            
            print(f"  Status: {response.status_code}")
            
            # Try to parse JSON response
            try:
                response_data = response.json()
                print(f"  Response: {json.dumps(response_data, indent=2)}")
            except json.JSONDecodeError:
                print(f"  Response: {response.text}")
                response_data = {"error": "Invalid JSON response"}
            
            # Check if request was successful
            if 200 <= response.status_code < 300:
                return response, True, None
            else:
                error_msg = response_data.get('message', 'Unknown error')
                return response, False, error_msg
                
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection Error: Cannot connect to {url}. Is the server running?"
            self.log_error(error_msg)
            return None, False, error_msg
        except requests.exceptions.Timeout as e:
            error_msg = f"Timeout Error: Request took too long"
            self.log_error(error_msg)
            return None, False, error_msg
        except Exception as e:
            error_msg = f"Unexpected Error: {str(e)}"
            self.log_error(error_msg)
            return None, False, error_msg
    
    def run_test(self, test_name, method, endpoint, data=None, params=None, 
                 expected_status=200, should_fail=False):
        """
        Run a single test
        
        Args:
            test_name (str): Name of the test
            method (str): HTTP method
            endpoint (str): API endpoint
            data (dict): Request body
            params (dict): Query parameters
            expected_status (int): Expected status code
            should_fail (bool): Whether this test is expected to fail
            
        Returns:
            response object if successful, None otherwise
        """
        self.test_count += 1
        print(f"\n{Colors.BOLD}Test #{self.test_count}: {test_name}{Colors.RESET}")
        print("-" * 70)
        
        response, success, error = self.make_request(method, endpoint, data, params)
        
        if response is None:
            self.failed_count += 1
            self.log_error(f"Test Failed: {error}")
            return None
        
        # Check status code
        if response.status_code == expected_status:
            self.passed_count += 1
            self.log_success(f"Test Passed: Status {response.status_code} (Expected {expected_status})")
            return response
        else:
            self.failed_count += 1
            self.log_error(f"Test Failed: Status {response.status_code} (Expected {expected_status})")
            if error:
                self.log_error(f"Error Message: {error}")
            return None
    
    def print_summary(self):
        """Print test summary"""
        self.log_section("TEST SUMMARY")
        print(f"Total Tests: {self.test_count}")
        print(f"{Colors.GREEN}Passed: {self.passed_count}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {self.failed_count}{Colors.RESET}")
        
        if self.failed_count == 0:
            self.log_success("🎉 ALL TESTS PASSED!")
        else:
            self.log_error(f"❌ {self.failed_count} test(s) failed")
        print()


def main():
    """Main test execution"""
    tester = APITester()
    
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║          Employee-Task Management API - Test Suite               ║")
    print("║                  ProU Technologies Assessment                     ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    # Test 0: Check if server is running
    tester.log_section("PHASE 0: SERVER HEALTH CHECK")
    response = tester.run_test(
        "Health Check - Root Endpoint",
        "GET", "/",
        expected_status=200
    )
    
    if response is None:
        tester.log_error("Server is not running! Please start the server with: python run.py")
        return
    
    # Phase 1: Employee CRUD Operations
    tester.log_section("PHASE 1: EMPLOYEE CRUD OPERATIONS")
    
    # Test 1: Create Employee 1
    employee1_data = {
        "first_name": "Alice",
        "last_name": "Williams",
        "email": "alice.williams@company.com",
        "department": "Engineering",
        "position": "Senior Software Engineer",
        "phone": "+919876543210",
        "hire_date": "2024-01-15"
    }
    response = tester.run_test(
        "Create Employee 1 (Alice)",
        "POST", "/api/employees",
        data=employee1_data,
        expected_status=201
    )
    if response:
        emp1_id = response.json()['data']['id']
        tester.created_employee_ids.append(emp1_id)
        tester.log_info(f"Created Employee ID: {emp1_id}")
    
    # Test 2: Create Employee 2
    employee2_data = {
        "first_name": "Michael",
        "last_name": "Chen",
        "email": "michael.chen@company.com",
        "department": "Product Management",
        "position": "Product Manager",
        "phone": "+919876543211",
        "hire_date": "2024-03-20"
    }
    response = tester.run_test(
        "Create Employee 2 (Michael)",
        "POST", "/api/employees",
        data=employee2_data,
        expected_status=201
    )
    if response:
        emp2_id = response.json()['data']['id']
        tester.created_employee_ids.append(emp2_id)
        tester.log_info(f"Created Employee ID: {emp2_id}")
    
    # Test 3: Create Employee 3
    employee3_data = {
        "first_name": "Sarah",
        "last_name": "Martinez",
        "email": "sarah.martinez@company.com",
        "department": "Engineering",
        "position": "DevOps Engineer",
        "hire_date": "2024-06-10"
    }
    response = tester.run_test(
        "Create Employee 3 (Sarah)",
        "POST", "/api/employees",
        data=employee3_data,
        expected_status=201
    )
    if response:
        emp3_id = response.json()['data']['id']
        tester.created_employee_ids.append(emp3_id)
        tester.log_info(f"Created Employee ID: {emp3_id}")
    
    # Test 4: Duplicate Email (Should Fail)
    tester.run_test(
        "Create Duplicate Email (Should Fail)",
        "POST", "/api/employees",
        data=employee1_data,
        expected_status=400
    )
    
    # Test 5: Get All Employees
    tester.run_test(
        "Get All Employees",
        "GET", "/api/employees",
        expected_status=200
    )
    
    # Test 6: Get Single Employee
    if tester.created_employee_ids:
        tester.run_test(
            f"Get Employee by ID ({tester.created_employee_ids[0]})",
            "GET", f"/api/employees/{tester.created_employee_ids[0]}",
            expected_status=200
        )
    
    # Test 7: Get Non-existent Employee
    tester.run_test(
        "Get Non-existent Employee (Should Fail)",
        "GET", "/api/employees/99999",
        expected_status=404
    )
    
    # Test 8: Update Employee
    if tester.created_employee_ids:
        update_data = {
            "position": "Lead Software Engineer",
            "department": "Engineering - Backend Team"
        }
        tester.run_test(
            f"Update Employee ({tester.created_employee_ids[0]})",
            "PUT", f"/api/employees/{tester.created_employee_ids[0]}",
            data=update_data,
            expected_status=200
        )
    
    # Test 9: Filter by Department
    tester.run_test(
        "Filter Employees by Department (Engineering)",
        "GET", "/api/employees",
        params={"department": "Engineering"},
        expected_status=200
    )
    
    # Test 10: Pagination
    tester.run_test(
        "Get Employees with Pagination (page=1, per_page=2)",
        "GET", "/api/employees",
        params={"page": 1, "per_page": 2},
        expected_status=200
    )
    
    # Phase 2: Task CRUD Operations
    tester.log_section("PHASE 2: TASK CRUD OPERATIONS")
    
    # Test 11: Create Task 1
    if tester.created_employee_ids:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        task1_data = {
            "title": "Implement User Authentication",
            "description": "Add JWT-based authentication to the API",
            "status": "in_progress",
            "priority": "high",
            "employee_id": tester.created_employee_ids[0],
            "deadline": tomorrow
        }
        response = tester.run_test(
            "Create Task 1 (Assigned to Alice)",
            "POST", "/api/tasks",
            data=task1_data,
            expected_status=201
        )
        if response:
            task1_id = response.json()['data']['id']
            tester.created_task_ids.append(task1_id)
            tester.log_info(f"Created Task ID: {task1_id}")
    
    # Test 12: Create Task 2
    if len(tester.created_employee_ids) >= 2:
        next_week = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        task2_data = {
            "title": "Product Roadmap Planning",
            "description": "Create Q1 2026 product roadmap",
            "status": "pending",
            "priority": "medium",
            "employee_id": tester.created_employee_ids[1],
            "deadline": next_week
        }
        response = tester.run_test(
            "Create Task 2 (Assigned to Michael)",
            "POST", "/api/tasks",
            data=task2_data,
            expected_status=201
        )
        if response:
            task2_id = response.json()['data']['id']
            tester.created_task_ids.append(task2_id)
            tester.log_info(f"Created Task ID: {task2_id}")
    
    # Test 13: Create Unassigned Task
    task3_data = {
        "title": "Code Review for PR #123",
        "description": "Review pull request from team member",
        "status": "pending",
        "priority": "low"
    }
    response = tester.run_test(
        "Create Task 3 (Unassigned)",
        "POST", "/api/tasks",
        data=task3_data,
        expected_status=201
    )
    if response:
        task3_id = response.json()['data']['id']
        tester.created_task_ids.append(task3_id)
        tester.log_info(f"Created Task ID: {task3_id}")
    
    # Test 14: Create Task with Invalid Employee
    invalid_task_data = {
        "title": "Invalid Task",
        "description": "This should fail",
        "employee_id": 99999
    }
    tester.run_test(
        "Create Task with Invalid Employee (Should Fail)",
        "POST", "/api/tasks",
        data=invalid_task_data,
        expected_status=400
    )
    
    # Test 15: Get All Tasks
    tester.run_test(
        "Get All Tasks",
        "GET", "/api/tasks",
        expected_status=200
    )
    
    # Test 16: Get Single Task
    if tester.created_task_ids:
        tester.run_test(
            f"Get Task by ID ({tester.created_task_ids[0]})",
            "GET", f"/api/tasks/{tester.created_task_ids[0]}",
            expected_status=200
        )
    
    # Test 17: Update Task
    if tester.created_task_ids:
        update_task_data = {
            "status": "completed",
            "priority": "urgent"
        }
        tester.run_test(
            f"Update Task ({tester.created_task_ids[0]})",
            "PUT", f"/api/tasks/{tester.created_task_ids[0]}",
            data=update_task_data,
            expected_status=200
        )
    
    # Test 18: Filter Tasks by Status
    tester.run_test(
        "Filter Tasks by Status (pending)",
        "GET", "/api/tasks",
        params={"status": "pending"},
        expected_status=200
    )
    
    # Test 19: Filter Tasks by Priority
    tester.run_test(
        "Filter Tasks by Priority (high)",
        "GET", "/api/tasks",
        params={"priority": "high"},
        expected_status=200
    )
    
    # Phase 3: Relationship Operations
    tester.log_section("PHASE 3: RELATIONSHIP OPERATIONS")
    
    # Test 20: Get Employee's Tasks
    if tester.created_employee_ids:
        tester.run_test(
            f"Get Tasks for Employee ({tester.created_employee_ids[0]})",
            "GET", f"/api/employees/{tester.created_employee_ids[0]}/tasks",
            expected_status=200
        )
    
    # Phase 4: Delete Operations
    tester.log_section("PHASE 4: DELETE OPERATIONS")
    
    # Test 21: Delete Task
    if tester.created_task_ids and len(tester.created_task_ids) >= 3:
        tester.run_test(
            f"Delete Task ({tester.created_task_ids[2]})",
            "DELETE", f"/api/tasks/{tester.created_task_ids[2]}",
            expected_status=200
        )
    
    # Test 22: Delete Non-existent Task
    tester.run_test(
        "Delete Non-existent Task (Should Fail)",
        "DELETE", "/api/tasks/99999",
        expected_status=404
    )
    
    # Test 23: Delete Employee
    if tester.created_employee_ids and len(tester.created_employee_ids) >= 3:
        tester.run_test(
            f"Delete Employee ({tester.created_employee_ids[2]})",
            "DELETE", f"/api/employees/{tester.created_employee_ids[2]}",
            expected_status=200
        )
    
    # Phase 5: Validation Tests
    tester.log_section("PHASE 5: VALIDATION TESTS")
    
    # Test 24: Create Employee with Missing Fields
    invalid_employee = {
        "first_name": "Test"
        # Missing required fields
    }
    tester.run_test(
        "Create Employee with Missing Fields (Should Fail)",
        "POST", "/api/employees",
        data=invalid_employee,
        expected_status=400
    )
    
    # Test 25: Create Task with Invalid Status
    invalid_task = {
        "title": "Test Task",
        "status": "invalid_status"
    }
    tester.run_test(
        "Create Task with Invalid Status (Should Fail)",
        "POST", "/api/tasks",
        data=invalid_task,
        expected_status=400
    )
    
    # Print final summary
    tester.print_summary()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Tests interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ Fatal Error: {str(e)}{Colors.RESET}")
        import traceback
        traceback.print_exc()
