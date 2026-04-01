"""API Tests"""
import pytest
from framework.api.api_client import APIClient


@pytest.mark.api
@pytest.mark.smoke
class TestPublicAPI:
    """Test cases for public API (JSONPlaceholder)"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for API tests"""
        self.client = APIClient(base_url="https://jsonplaceholder.typicode.com")
        yield
        self.client.close()
    
    def test_get_posts(self):
        """Test GET all posts"""
        response = self.client.get("/posts")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0
    
    def test_get_single_post(self):
        """Test GET single post"""
        response = self.client.get("/posts/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "title" in data
        assert "body" in data
    
    def test_create_post(self):
        """Test POST to create new post"""
        payload = {
            "title": "Test Post",
            "body": "This is a test post",
            "userId": 1
        }
        
        response = self.client.post("/posts", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Post"
        assert data["body"] == "This is a test post"
    
    def test_update_post(self):
        """Test PUT to update post"""
        payload = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated body",
            "userId": 1
        }
        
        response = self.client.put("/posts/1", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
    
    def test_partial_update_post(self):
        """Test PATCH to partially update post"""
        payload = {
            "title": "Patched Title"
        }
        
        response = self.client.patch("/posts/1", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Patched Title"
    
    def test_delete_post(self):
        """Test DELETE post"""
        response = self.client.delete("/posts/1")
        
        assert response.status_code == 200
    
    def test_get_post_with_params(self):
        """Test GET with query parameters"""
        params = {"userId": 1}
        
        response = self.client.get("/posts", params=params)
        
        assert response.status_code == 200
        data = response.json()
        assert all(post["userId"] == 1 for post in data)
    
    def test_get_users(self):
        """Test GET users"""
        response = self.client.get("/users")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert "name" in data[0]
        assert "email" in data[0]
    
    def test_get_comments(self):
        """Test GET comments"""
        response = self.client.get("/comments/1")
        
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "name" in data


@pytest.mark.api
@pytest.mark.regression
class TestAPIErrorHandling:
    """Test error handling in API responses"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for API tests"""
        self.client = APIClient(base_url="https://jsonplaceholder.typicode.com")
        yield
        self.client.close()
    
    def test_get_nonexistent_post(self):
        """Test GET request to nonexistent resource"""
        response = self.client.get("/posts/999999")
        
        assert response.status_code == 404  # JSONPlaceholder returns 404 for nonexistent
    
    def test_invalid_endpoint(self):
        """Test GET to invalid endpoint"""
        response = self.client.get("/invalid-endpoint")
        
        assert response.status_code == 404
    
    def test_post_with_invalid_content_type(self):
        """Test POST with incorrect data"""
        response = self.client.post(
            "/posts",
            data="invalid",
            headers={"Content-Type": "text/plain"}
        )
        
        # API should still process it
        assert response.status_code in [201, 400, 415]
