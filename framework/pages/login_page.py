"""Login page object"""
from framework.pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for login page"""
    
    # Selectors
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error-message"
    REMEMBER_ME_CHECKBOX = "#rememberMe"
    FORGOT_PASSWORD_LINK = "a[href*='forgot']"
    
    def enter_username(self, username: str) -> None:
        """Enter username"""
        self.fill(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str) -> None:
        """Enter password"""
        self.fill(self.PASSWORD_INPUT, password)
    
    def click_login(self) -> None:
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
    
    def get_error_message(self) -> str:
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_visible(self) -> bool:
        """Check if error message is visible"""
        return self.is_visible(self.ERROR_MESSAGE)
    
    def check_remember_me(self) -> None:
        """Check remember me checkbox"""
        self.click(self.REMEMBER_ME_CHECKBOX)
    
    def click_forgot_password(self) -> None:
        """Click forgot password link"""
        self.click(self.FORGOT_PASSWORD_LINK)
    
    def login(self, username: str, password: str, remember_me: bool = False) -> None:
        """Complete login flow"""
        self.enter_username(username)
        self.enter_password(password)
        if remember_me:
            self.check_remember_me()
        self.click_login()
    
    def is_login_page(self) -> bool:
        """Verify if we are on login page"""
        return self.is_visible(self.USERNAME_INPUT)
