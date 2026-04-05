"""Practice Expand Testing - Login Page"""
from framework.pages.base_page import BasePage


class PracticeLoginPage(BasePage):
    """Page object for practice.expandtesting.com login page"""
    
    # Selectors for practice.expandtesting.com
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    
    def navigate_to_login(self) -> None:
        """Navigate to practice login page"""
        self.navigate("https://practice.expandtesting.com/login")
    
    def enter_username(self, username: str) -> None:
        """Enter username in the username field"""
        self.fill(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str) -> None:
        """Enter password in the password field"""
        self.fill(self.PASSWORD_INPUT, password)
    
    def click_login_button(self) -> None:
        """Click the login button"""
        self.click(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str) -> None:
        """Complete login flow"""
        self.navigate_to_login()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def is_on_login_page(self) -> bool:
        """Verify we are on login page"""
        return self.is_visible(self.USERNAME_INPUT) and self.is_visible(self.PASSWORD_INPUT)
