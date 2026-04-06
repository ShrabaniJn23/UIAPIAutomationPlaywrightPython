"""Pytest fixtures for browser, page, and API client with video/screenshot support"""
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from framework.config.settings import settings
from framework.api.api_client import APIClient
import os
import shutil


@pytest.fixture(scope="session")
def browser() -> Browser:
    """Create browser instance for session"""
    p = sync_playwright().start()
    
    if settings.BROWSER_TYPE.lower() == "firefox":
        browser = p.firefox.launch(headless=settings.HEADLESS, slow_mo=settings.SLOW_MO)
    elif settings.BROWSER_TYPE.lower() == "webkit":
        browser = p.webkit.launch(headless=settings.HEADLESS, slow_mo=settings.SLOW_MO)
    else:  # chromium
        browser = p.chromium.launch(headless=settings.HEADLESS, slow_mo=settings.SLOW_MO)
    
    yield browser
    browser.close()
    p.stop()


@pytest.fixture
def context(browser: Browser, request) -> BrowserContext:
    """Create browser context for each test with video recording"""
    # Create video directory if it doesn't exist
    os.makedirs(settings.VIDEO_PATH, exist_ok=True)
    
    # Create video file path based on test name
    video_path = os.path.join(settings.VIDEO_PATH, f"{request.node.name}.webm")
    
    # Create context with video recording
    context = browser.new_context(
        record_video_dir=settings.VIDEO_PATH
    )
    
    yield context
    
    # Save video with proper naming
    context.close()
    # Video is automatically saved with the test name


@pytest.fixture
def page(context: BrowserContext, request) -> Page:
    """Create page for each test"""
    page = context.new_page()
    
    # Add screenshot utility to page object
    page.screenshot_path = lambda name=None: take_screenshot(page, name or request.node.name)
    
    yield page
    page.close()


@pytest.fixture
def api_client() -> APIClient:
    """Create API client for each test"""
    client = APIClient()
    yield client
    client.close()


def take_screenshot(page: Page, name: str) -> str:
    """Take a screenshot and save it with timestamp"""
    os.makedirs(settings.SCREENSHOTS_PATH, exist_ok=True)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(settings.SCREENSHOTS_PATH, filename)
    
    page.screenshot(path=filepath)
    print(f"\n📸 Screenshot saved: {filepath}")
    return filepath


@pytest.fixture(autouse=True)
def setup_teardown(request):
    """Setup and teardown for each test"""
    # Create directories if they don't exist
    os.makedirs(settings.SCREENSHOTS_PATH, exist_ok=True)
    os.makedirs(settings.VIDEO_PATH, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"🧪 Starting Test: {request.node.name}")
    print(f"{'='*60}")
    
    yield
    
    # Teardown
    print(f"\n{'='*60}")
    print(f"✅ Test Completed: {request.node.name}")
    print(f"📸 Screenshots: {settings.SCREENSHOTS_PATH}")
    print(f"🎥 Videos: {settings.VIDEO_PATH}")
    print(f"{'='*60}\n")


@pytest.fixture
def booking_details(api_client):
    """Create a booking via API and return bookingid, firstname, lastname"""
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 123,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-04-01",
            "checkout": "2026-04-05"
        },
        "additionalneeds": "Breakfast"
    }
    api_client.base_url = "https://restful-booker.herokuapp.com"
    response = api_client.post("/booking", json=payload)
    assert response.status_code == 200
    data = response.json()
    result = {
        "bookingid": data["bookingid"],
        "firstname": data["booking"]["firstname"],
        "lastname": data["booking"]["lastname"]
    }
    yield result
    # Optionally, add cleanup code to delete the booking after test
