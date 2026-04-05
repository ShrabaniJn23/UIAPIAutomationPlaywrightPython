"""Home page object"""
from framework.pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for home page"""
    
    # Selectors
    WELCOME_MESSAGE = ".welcome-message"
    USER_PROFILE_BUTTON = "[data-testid='user-profile']"
    LOGOUT_BUTTON = "button:has-text('Logout')"
    NAVIGATION_MENU = ".navbar"
    SEARCH_INPUT = "[data-testid='search']"
    
    def get_welcome_message(self) -> str:
        """Get welcome message"""
        return self.get_text(self.WELCOME_MESSAGE)
    
    def click_user_profile(self) -> None:
        """Click user profile button"""
        self.click(self.USER_PROFILE_BUTTON)
    
    def logout(self) -> None:
        """Logout from application"""
        self.click(self.LOGOUT_BUTTON)
    
    def search(self, query: str) -> None:
        """Search for something"""
        self.fill(self.SEARCH_INPUT, query)
        self.page.press(self.SEARCH_INPUT, "Enter")
    
    def is_home_page(self) -> bool:
        """Verify if we are on home page"""
        return self.is_visible(self.WELCOME_MESSAGE)
