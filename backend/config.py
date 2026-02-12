"""
Configuration management for Weather Dashboard
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # OpenWeatherMap API configuration
    OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
    OPENWEATHERMAP_BASE_URL = 'https://api.openweathermap.org/data/2.5'
    
    # Cache configuration
    CACHE_DEFAULT_TTL = int(os.getenv('CACHE_DEFAULT_TTL', '900'))  # 15 minutes
    
    # Rate limiting
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', '100'))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '3600'))  # 1 hour
    
    # API timeouts
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '10'))
    
    # Test mode configuration
    TEST_MODE = os.getenv('TEST_MODE', 'False').lower() == 'true'
    
    @staticmethod
    def validate_config():
        """Validate required configuration"""
        if not Config.OPENWEATHERMAP_API_KEY:
            raise ValueError("OPENWEATHERMAP_API_KEY environment variable is required")
        
        return True