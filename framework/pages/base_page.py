"""Base page object model for all page classes"""
from playwright.sync_api import Page
from framework.config.settings import settings
import time


class BasePage:
    """
    Base class for all page objects.
    Provides common methods for page interactions.
    """
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = settings.TIMEOUT
    
    def navigate(self, url: str) -> None:
        """Navigate to a URL"""
        self.page.goto(url, wait_until="networkidle")
    
    def click(self, selector: str, timeout: int = None) -> None:
        """Click an element"""
        self.page.click(selector, timeout=timeout or self.timeout)
    
    def type_text(self, selector: str, text: str, delay: int = 0) -> None:
        """Type text into an input field"""
        self.page.fill(selector, "")
        self.page.type(selector, text, delay=delay)
    
    def fill(self, selector: str, text: str) -> None:
        """Fill an input field with text"""
        self.page.fill(selector, text)
    
    def get_text(self, selector: str) -> str:
        """Get text content of an element"""
        return self.page.text_content(selector)
    
    def is_visible(self, selector: str, timeout: int = None) -> bool:
        """Check if element is visible"""
        try:
            self.page.is_visible(selector, timeout=timeout or self.timeout)
            return True
        except:
            return False
    
    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled"""
        return self.page.is_enabled(selector)
    
    def wait_for_selector(self, selector: str, state: str = "visible", timeout: int = None) -> None:
        """Wait for element to appear"""
        self.page.wait_for_selector(selector, state=state, timeout=timeout or self.timeout)
    
    def wait_for_url(self, url_pattern: str, timeout: int = None) -> None:
        """Wait for URL to match pattern"""
        self.page.wait_for_url(url_pattern, timeout=timeout or self.timeout)
    
    def get_url(self) -> str:
        """Get current page URL"""
        return self.page.url
    
    def get_title(self) -> str:
        """Get page title"""
        return self.page.title()
    
    def wait_for_load_state(self, state: str = "networkidle", timeout: int = None) -> None:
        """Wait for page load state"""
        self.page.wait_for_load_state(state, timeout=timeout or self.timeout)
    
    def select_option(self, selector: str, value: str) -> None:
        """Select option from dropdown"""
        self.page.select_option(selector, value)
    
    def get_attribute(self, selector: str, attribute: str) -> str:
        """Get element attribute"""
        return self.page.get_attribute(selector, attribute)
    
    def take_screenshot(self, name: str) -> None:
        """Take screenshot"""
        self.page.screenshot(path=f"{settings.SCREENSHOTS_PATH}/{name}.png")
    
    def accept_alert(self) -> None:
        """Accept browser alert"""
        self.page.once("dialog", lambda dialog: dialog.accept())
    
    def dismiss_alert(self) -> None:
        """Dismiss browser alert"""
        self.page.once("dialog", lambda dialog: dialog.dismiss())
    
    def scroll_to_element(self, selector: str) -> None:
        """Scroll to element"""
        self.page.locator(selector).scroll_into_view_if_needed()
    
    def double_click(self, selector: str) -> None:
        """Double click an element"""
        self.page.dblclick(selector)
    
    def right_click(self, selector: str) -> None:
        """Right click an element"""
        self.page.click(selector, button="right")
