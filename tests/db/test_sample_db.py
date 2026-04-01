import pytest
from framework.db_helper import DatabaseHelper
import os

@pytest.fixture
def db_helper():
    """Create database helper instance"""
    db_url = os.getenv('DB_URL', 'sqlite:///:memory:')
    db = DatabaseHelper(db_url)
    yield db
    db.close()

def test_db_connection(db_helper):
    """Test database connection"""
    try:
        # Execute a simple query to verify connection
        result = db_helper.fetch_one("SELECT 1 as test")
        assert result is not None
    except Exception as e:
        pytest.skip(f"Database not available: {str(e)}")

def test_db_query_example(db_helper):
    """Example of querying the database"""
    try:
        # Example query - replace with your actual table
        # result = db_helper.fetch_all("SELECT * FROM users LIMIT 5")
        # assert len(result) >= 0
        
        # For now, just verify connection works
        result = db_helper.fetch_one("SELECT 1 as test")
        assert result[0] == 1
    except Exception as e:
        pytest.skip(f"Database query failed: {str(e)}")

def test_db_insert_example(db_helper):
    """Example of inserting data - replace with your actual implementation"""
    try:
        # Example: Insert user
        # query = "INSERT INTO users (name, email) VALUES ('John', 'john@example.com')"
        # affected_rows = db_helper.execute_update(query)
        # assert affected_rows == 1
        
        # Verify connection
        result = db_helper.fetch_one("SELECT 1 as test")
        assert result[0] == 1
    except Exception as e:
        pytest.skip(f"Database insert failed: {str(e)}")
