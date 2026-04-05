"""UI Tests for Login functionality"""
import pytest
from framework.pages.login_page import LoginPage
from framework.pages.home_page import HomePage
from framework.config.settings import settings


@pytest.mark.ui
@pytest.mark.smoke
class TestLoginPage:
    """Test cases for login page"""
    
    def test_login_page_loads(self, page):
        """Test that login page loads successfully"""
        login_page = LoginPage(page)
        login_page.navigate(settings.BASE_URL)
        assert login_page.is_login_page()
    
    def test_successful_login(self, page):
        """Test successful login"""
        login_page = LoginPage(page)
        login_page.navigate(settings.BASE_URL)
        
        # Replace with actual credentials
        login_page.login("testuser", "password123")
        
        # Wait for navigation to home page
        home_page = HomePage(page)
        home_page.wait_for_url("**/dashboard")
    
    def test_login_with_remember_me(self, page):
        """Test login with remember me option"""
        login_page = LoginPage(page)
        login_page.navigate(settings.BASE_URL)
        
        login_page.login("testuser", "password123", remember_me=True)
        
        # Check if remember me checkbox was selected
        assert login_page.page.is_checked("#rememberMe")
    
    def test_invalid_credentials(self, page):
        """Test login with invalid credentials"""
        login_page = LoginPage(page)
        login_page.navigate(settings.BASE_URL)
        
        login_page.login("invaliduser", "invalidpass")
        
        # Check for error message
        assert login_page.is_error_visible()
    
    def test_empty_username(self, page):
        """Test login with empty username"""
        login_page = LoginPage(page)
        login_page.navigate(settings.BASE_URL)
        
        login_page.enter_password("password123")
        login_page.click_login()
        
        # Verify validation error
        assert login_page.is_error_visible()


@pytest.mark.ui
@pytest.mark.regression
class TestHomePage:
    """Test cases for home page"""
    
    def test_home_page_elements_visible(self, page):
        """Test that home page elements are visible"""
        home_page = HomePage(page)
        home_page.navigate(settings.BASE_URL + "/dashboard")
        
        assert home_page.is_visible(".welcome-message")
        assert home_page.is_visible("[data-testid='user-profile']")
    
    def test_logout_functionality(self, page):
        """Test logout functionality"""
        home_page = HomePage(page)
        home_page.navigate(settings.BASE_URL + "/dashboard")
        
        home_page.logout()
        
        # Should redirect to login page
        home_page.wait_for_url("**/login")
    
    def test_search_functionality(self, page):
        """Test search functionality"""
        home_page = HomePage(page)
        home_page.navigate(settings.BASE_URL + "/dashboard")
        
        search_query = "test search"
        home_page.search(search_query)
        
        # Wait for search results page
        home_page.wait_for_url("**/search")
