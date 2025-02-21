"""Configuration settings for the application"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    # API Settings
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    JANUS_MODEL_ID = os.getenv('JANUS_MODEL_ID', 'deepseek-ai/Janus-Pro-7B')
    
    # Server Settings
    PORT = int(os.getenv('PORT', 9999))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # Retry Settings
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', 5))

    # Add deployment configurations
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Add different configs per environment
    if ENVIRONMENT == 'production':
        HOST = '0.0.0.0'
        PORT = 80
    else:
        HOST = '127.0.0.1'
        PORT = 9999 