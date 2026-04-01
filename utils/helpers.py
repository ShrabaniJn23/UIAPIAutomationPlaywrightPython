"""Utility helpers for test automation"""
import time
from datetime import datetime


class TestDataHelper:
    """Helper class for test data generation"""
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def get_unique_email(prefix: str = "test") -> str:
        """Generate unique email"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}_{timestamp}@test.com"
    
    @staticmethod
    def get_unique_username(prefix: str = "user") -> str:
        """Generate unique username"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}_{timestamp}"


class WaitHelper:
    """Helper class for wait operations"""
    
    @staticmethod
    def wait(seconds: int) -> None:
        """Wait for specified seconds"""
        time.sleep(seconds)
    
    @staticmethod
    def wait_until(condition_func, timeout: int = 10, poll_interval: int = 1) -> bool:
        """Wait until condition is true"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if condition_func():
                    return True
            except:
                pass
            time.sleep(poll_interval)
        return False


class ResponseValidator:
    """Helper class for validating API responses"""
    
    @staticmethod
    def validate_status_code(response, expected_code: int) -> bool:
        """Validate response status code"""
        return response.status_code == expected_code
    
    @staticmethod
    def validate_response_contains_key(response, key: str, nested_key: str = None) -> bool:
        """Validate response contains key"""
        try:
            data = response.json()
            if nested_key:
                return key in data and nested_key in data[key]
            return key in data
        except:
            return False
    
    @staticmethod
    def validate_response_is_list(response) -> bool:
        """Validate response is a list"""
        try:
            return isinstance(response.json(), list)
        except:
            return False
    
    @staticmethod
    def validate_response_is_dict(response) -> bool:
        """Validate response is a dictionary"""
        try:
            return isinstance(response.json(), dict)
        except:
            return False
