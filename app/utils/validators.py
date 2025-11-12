"""
Custom validators for additional validation logic.
"""
import re
from datetime import datetime, date


def validate_phone_number(phone):
    """
    Validate phone number format.
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not phone:
        return True
    
    # Basic phone validation (adjust regex as needed)
    pattern = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$'
    return bool(re.match(pattern, phone))


def validate_date_not_future(date_value):
    """
    Validate that a date is not in the future.
    
    Args:
        date_value: Date to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not date_value:
        return True
    
    if isinstance(date_value, str):
        date_value = datetime.strptime(date_value, '%Y-%m-%d').date()
    
    return date_value <= date.today()


def validate_deadline_not_past(deadline):
    """
    Validate that a deadline is not in the past.
    
    Args:
        deadline: Deadline to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not deadline:
        return True
    
    if isinstance(deadline, str):
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
    
    return deadline >= date.today()
