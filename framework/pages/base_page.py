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
        self.page.goto(url, wait_until="domcontentloaded")
    
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
    
    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        Take screenshot and save with timestamp
        
        Args:
            name: Name of the screenshot
            
        Returns:
            Path to the saved screenshot
        """
        import os
        from datetime import datetime
        
        os.makedirs(settings.SCREENSHOTS_PATH, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(settings.SCREENSHOTS_PATH, filename)
        
        self.page.screenshot(path=filepath)
        print(f"\n📸 Screenshot saved: {filepath}")
        return filepath
    
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
    
    def get_cookies(self) -> dict:
        """
        Get all cookies from current context
        
        Returns:
            Dictionary of cookies {name: value}
        """
        cookies = self.page.context.cookies()
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        print(f"\n🔐 Captured {len(cookie_dict)} cookies:")
        for name, value in cookie_dict.items():
            print(f"   {name}: {value[:50]}..." if len(value) > 50 else f"   {name}: {value}")
        return cookie_dict
    
    def get_cookie(self, name: str) -> str:
        """
        Get specific cookie by name
        
        Args:
            name: Cookie name
            
        Returns:
            Cookie value or None if not found
        """
        cookies = self.page.context.cookies()
        for cookie in cookies:
            if cookie['name'] == name:
                print(f"\n🔐 Found cookie '{name}': {cookie['value'][:50]}...")
                return cookie['value']
        print(f"\n⚠️  Cookie '{name}' not found")
        return None
    
    def get_all_cookies_as_header(self) -> str:
        """
        Get all cookies formatted as Cookie header value
        
        Returns:
            Cookie header string (e.g., "name1=value1; name2=value2")
        """
        cookies = self.page.context.cookies()
        cookie_header = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        print(f"\n🔐 Cookie header: {cookie_header[:100]}...")
        return cookie_header
    
    def get_session_storage(self) -> dict:
        """
        Get all session storage data
        
        Returns:
            Dictionary of session storage items
        """
        session_data = self.page.evaluate("() => JSON.stringify(window.sessionStorage)")
        import json
        data = json.loads(session_data) if session_data else {}
        print(f"\n💾 Session storage: {data}")
        return data
    
    def get_local_storage(self) -> dict:
        """
        Get all local storage data
        
        Returns:
            Dictionary of local storage items
        """
        local_data = self.page.evaluate("() => JSON.stringify(window.localStorage)")
        import json
        data = json.loads(local_data) if local_data else {}
        print(f"\n💾 Local storage: {data}")
        return data
