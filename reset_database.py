"""
Database Reset Script
Deletes all data from the database or recreates tables from scratch.
"""
import os
import sys
from app import create_app, db
from app.models import Employee, Task


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def clear_all_data():
    """Delete all data from tables but keep table structure"""
    try:
        print(f"\n{Colors.YELLOW}⚠️  Clearing all data from database...{Colors.RESET}")
        
        # Delete all tasks first (due to foreign key constraint)
        task_count = Task.query.count()
        Task.query.delete()
        print(f"{Colors.BLUE}  Deleted {task_count} tasks{Colors.RESET}")
        
        # Delete all employees
        employee_count = Employee.query.count()
        Employee.query.delete()
        print(f"{Colors.BLUE}  Deleted {employee_count} employees{Colors.RESET}")
        
        # Commit changes
        db.session.commit()
        
        print(f"{Colors.GREEN}✅ All data cleared successfully!{Colors.RESET}\n")
        return True
        
    except Exception as e:
        db.session.rollback()
        print(f"{Colors.RED}❌ Error clearing data: {str(e)}{Colors.RESET}\n")
        return False


def recreate_tables():
    """Drop all tables and recreate them (complete reset)"""
    try:
        print(f"\n{Colors.YELLOW}⚠️  Dropping all tables...{Colors.RESET}")
        db.drop_all()
        print(f"{Colors.BLUE}  All tables dropped{Colors.RESET}")
        
        print(f"{Colors.YELLOW}⚠️  Creating fresh tables...{Colors.RESET}")
        db.create_all()
        print(f"{Colors.BLUE}  All tables created{Colors.RESET}")
        
        print(f"{Colors.GREEN}✅ Database recreated successfully!{Colors.RESET}\n")
        return True
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error recreating database: {str(e)}{Colors.RESET}\n")
        return False


def show_database_info():
    """Show current database information"""
    try:
        employee_count = Employee.query.count()
        task_count = Task.query.count()
        
        print(f"\n{Colors.CYAN}{'='*60}")
        print(f"  Current Database Status")
        print(f"{'='*60}{Colors.RESET}")
        print(f"  Employees: {employee_count}")
        print(f"  Tasks: {task_count}")
        print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error reading database: {str(e)}{Colors.RESET}\n")


def main():
    """Main function"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║              Database Reset Utility                               ║")
    print("║         Employee-Task Management API                              ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    # Create app context
    app = create_app()
    
    with app.app_context():
        # Show current status
        print(f"{Colors.BOLD}Current Database Status:{Colors.RESET}")
        show_database_info()
        
        # Ask user what to do
        print(f"{Colors.BOLD}Choose an option:{Colors.RESET}")
        print(f"  1. Clear all data (keep tables)")
        print(f"  2. Recreate tables (complete reset)")
        print(f"  3. Show info only (no changes)")
        print(f"  4. Exit")
        
        choice = input(f"\n{Colors.YELLOW}Enter your choice (1-4): {Colors.RESET}").strip()
        
        if choice == '1':
            # Confirm
            confirm = input(f"{Colors.RED}⚠️  This will delete ALL data. Continue? (yes/no): {Colors.RESET}").strip().lower()
            if confirm == 'yes':
                if clear_all_data():
                    show_database_info()
            else:
                print(f"{Colors.YELLOW}Operation cancelled.{Colors.RESET}\n")
                
        elif choice == '2':
            # Confirm
            confirm = input(f"{Colors.RED}⚠️  This will DROP and RECREATE all tables. Continue? (yes/no): {Colors.RESET}").strip().lower()
            if confirm == 'yes':
                if recreate_tables():
                    show_database_info()
            else:
                print(f"{Colors.YELLOW}Operation cancelled.{Colors.RESET}\n")
                
        elif choice == '3':
            print(f"{Colors.GREEN}No changes made.{Colors.RESET}\n")
            
        elif choice == '4':
            print(f"{Colors.CYAN}Goodbye!{Colors.RESET}\n")
            
        else:
            print(f"{Colors.RED}Invalid choice.{Colors.RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Operation cancelled by user{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Fatal Error: {str(e)}{Colors.RESET}\n")
        import traceback
        traceback.print_exc()
