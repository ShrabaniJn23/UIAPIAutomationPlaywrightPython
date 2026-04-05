import pytest

@pytest.fixture(scope="function")
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
"""Pytest fixtures for browser and API client"""
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from framework.config.settings import settings
from framework.api.api_client import APIClient
import os


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
def context(browser: Browser) -> BrowserContext:
    """Create browser context for each test"""
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    """Create page for each test"""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def api_client() -> APIClient:
    """Create API client for each test"""
    client = APIClient()
    yield client
    client.close()


@pytest.fixture(autouse=True)
def setup_teardown():
    """Setup and teardown for each test"""
    # Create directories if they don't exist
    os.makedirs(settings.SCREENSHOTS_PATH, exist_ok=True)
    os.makedirs(settings.VIDEO_PATH, exist_ok=True)
    
    yield
    
    # Cleanup after test
    pass
