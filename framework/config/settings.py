import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Browser Configuration
    BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))
    
    # Test Configuration
    BASE_URL = os.getenv("BASE_URL", "https://example.com")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))  # milliseconds
    
    # Test Data
    SCREENSHOTS_PATH = os.getenv("SCREENSHOTS_PATH", "reports/screenshots")
    VIDEO_PATH = os.getenv("VIDEO_PATH", "reports/videos")
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
