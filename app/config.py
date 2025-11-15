"""
Application configuration classes for different environments.
"""
import os
from datetime import timedelta


class Config:
    """Base configuration with common settings."""
    
    # Get the base directory (project root)
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-fallback')

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # Database - Use absolute path for SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # JSON settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Upload limits
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    
    # Pagination defaults
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100


class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    TESTING = False

    # Production database (PostgreSQL from Render/Railway)
    # Fix postgres:// to postgresql:// for SQLAlchemy 1.4+
    @staticmethod
    def get_database_uri():
        """Get database URI with postgres:// -> postgresql:// fix."""
        uri = os.getenv('DATABASE_URL')
        if uri and uri.startswith('postgres://'):
            uri = uri.replace('postgres://', 'postgresql://', 1)
        return uri

    SQLALCHEMY_DATABASE_URI = get_database_uri.__func__()

    # Force HTTPS in production
    PREFERRED_URL_SCHEME = 'https'


class TestingConfig(Config):
    """Testing environment configuration."""
    
    TESTING = True
    DEBUG = True
    
    # Use in-memory SQLite for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
