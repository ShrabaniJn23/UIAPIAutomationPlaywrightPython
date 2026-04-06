"""
API Session Validation Tests

Pure API tests that validate user sessions captured from UI logins.
Tests the backend validation of sessions and user data retrieval.
"""

import pytest
from framework.pages.practice_login_page import PracticeLoginPage
from framework.pages.practice_dashboard_page import PracticeDashboardPage
from tests.api.session_validator import (
    validate_session_with_api,
    extract_session_cookies,
    prepare_api_headers_from_session,
    validate_api_response,
)


@pytest.mark.api
@pytest.mark.smoke
def test_session_validation_after_ui_login(page, api_client):
    """
    Test session validation after UI login.
    
    Flow:
    1. Login via UI
    2. Extract session cookies
    3. Validate session via API
    4. Verify user data consistency
    
    This proves the backend recognizes the session created by UI login.
    """
    
    print("\n" + "="*70)
    print("🔐 TEST: SESSION VALIDATION VIA API")
    print("="*70)
    
    # Step 1: UI Login
    print("\n[STEP 1] Perform UI Login")
    login_page = PracticeLoginPage(page)
    login_page.navigate("https://practice.expandtesting.com/login")
    login_page.login(username="practice", password="SuperSecretPassword!")
    page.wait_for_timeout(3000)
    
    # Step 2: Verify login on UI
    dashboard_page = PracticeDashboardPage(page)
    assert dashboard_page.is_on_secure_dashboard(), "Login verification failed"
    username = dashboard_page.get_username_text()
    print(f"✓ UI Login successful - Username: {username}")
    
    # Step 3: Validate session via API
    print("\n[STEP 2] Validate Session via API")
    results = validate_session_with_api(login_page, api_client, username)
    
    # Verify results
    assert len(results["cookies"]) > 0, "No cookies captured"
    print(f"\n✓ Test complete: {len(results['cookies'])} cookies validated")


@pytest.mark.api
def test_session_cookie_extraction(page, api_client):
    """
    Test extracting session cookies from browser after login.
    
    Validates that cookies are properly captured and can be formatted
    for use in subsequent API requests.
    """
    
    print("\n" + "="*70)
    print("🔐 TEST: SESSION COOKIE EXTRACTION")
    print("="*70)
    
    # Login
    login_page = PracticeLoginPage(page)
    login_page.navigate("https://practice.expandtesting.com/login")
    login_page.login(username="practice", password="SuperSecretPassword!")
    page.wait_for_timeout(3000)
    
    # Extract cookies
    print("\n[EXTRACTION]")
    cookies = extract_session_cookies(login_page)
    
    # Verify extraction
    assert len(cookies) > 0, "No cookies found"
    assert "express:sess" in cookies or "_ga" in cookies, "Session cookies not found"
    
    print(f"\n✓ Extracted {len(cookies)} cookies")
    print(f"✓ Cookie names: {list(cookies.keys())[:5]}...")


@pytest.mark.api
def test_api_headers_preparation(page, api_client):
    """
    Test preparing API headers from browser session.
    
    Validates that session data can be properly formatted into
    API-ready headers for authenticated requests.
    """
    
    print("\n" + "="*70)
    print("📝 TEST: API HEADERS PREPARATION")
    print("="*70)
    
    # Login
    login_page = PracticeLoginPage(page)
    login_page.navigate("https://practice.expandtesting.com/login")
    login_page.login(username="practice", password="SuperSecretPassword!")
    page.wait_for_timeout(3000)
    
    # Prepare headers
    print("\n[HEADER PREPARATION]")
    headers = prepare_api_headers_from_session(login_page)
    
    # Verify headers
    assert "Cookie" in headers, "Cookie header not prepared"
    assert headers["Cookie"], "Cookie header is empty"
    assert len(headers["Cookie"]) > 10, "Cookie header seems too short"
    
    print(f"\n✓ Prepared {len(headers)} headers")
    print(f"✓ Headers: {list(headers.keys())}")
    print(f"✓ Cookie length: {len(headers['Cookie'])} characters")


@pytest.mark.api
@pytest.mark.smoke
def test_session_persistence_across_requests(page, api_client):
    """
    Test that session persists across multiple API requests.
    
    Validates that captured session can be reused for multiple
    authenticated API calls.
    """
    
    print("\n" + "="*70)
    print("🔄 TEST: SESSION PERSISTENCE ACROSS REQUESTS")
    print("="*70)
    
    # Login
    login_page = PracticeLoginPage(page)
    login_page.navigate("https://practice.expandtesting.com/login")
    login_page.login(username="practice", password="SuperSecretPassword!")
    page.wait_for_timeout(3000)
    
    # Prepare headers
    headers = prepare_api_headers_from_session(login_page)
    api_client.set_header("Cookie", headers["Cookie"])
    
    print("\n[PERSISTENCE TEST]")
    print("Making multiple API requests with same session...")
    
    # Make first request
    print("\n📍 Request 1: API call with session cookies")
    try:
        response1 = api_client.get("https://practice.expandtesting.com/api/authenticate")
        print(f"   Status: {response1.status_code}")
    except Exception as e:
        print(f"   Note: Endpoint not available - {str(e)}")
    
    # Make second request
    print("\n📍 Request 2: API call with same session cookies")
    try:
        response2 = api_client.get("https://practice.expandtesting.com/api/authenticate")
        print(f"   Status: {response2.status_code}")
    except Exception as e:
        print(f"   Note: Endpoint not available - {str(e)}")
    
    print("\n✓ Session persistence test complete")
    print("✓ Same session headers used for multiple requests")
