"""
Health check utilities for monitoring application status.
"""
import os
from datetime import datetime, timezone
from flask import jsonify
from sqlalchemy import text
from app import db


_start_time = datetime.now(timezone.utc)


def check_database():
    """
    Check database connectivity.

    Returns:
        dict: Database health status
    """
    try:
        # Try a simple query
        result = db.session.execute(text('SELECT 1')).scalar()
        return {
            'status': 'healthy',
            'message': 'Database connection successful'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'message': f'Database connection failed: {str(e)}'
        }


def get_system_info():
    """
    Get system information.

    Returns:
        dict: System information
    """
    uptime = datetime.now(timezone.utc) - _start_time
    return {
        'uptime_seconds': int(uptime.total_seconds()),
        'environment': os.getenv('FLASK_ENV', 'development'),
        'python_version': os.sys.version.split()[0],
        'timestamp': datetime.now(timezone.utc).isoformat()
    }


def health_check_detailed():
    """
    Perform detailed health check.

    Returns:
        tuple: (response_dict, status_code)
    """
    db_health = check_database()
    system_info = get_system_info()

    overall_status = 'healthy' if db_health['status'] == 'healthy' else 'degraded'

    response = {
        'status': overall_status,
        'version': '2.0.0',
        'checks': {
            'database': db_health,
            'system': system_info
        }
    }

    status_code = 200 if overall_status == 'healthy' else 503

    return response, status_code


def health_check_simple():
    """
    Simple health check for basic monitoring.

    Returns:
        tuple: (response_dict, status_code)
    """
    return {'status': 'healthy', 'timestamp': datetime.now(timezone.utc).isoformat()}, 200
