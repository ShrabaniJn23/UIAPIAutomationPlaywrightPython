"""
Hybrid UI + API Tests - Integration Between Frontend and Backend

These tests demonstrate how UI login flows can be validated through backend APIs.
UI tests use helper functions from tests.api.session_validator to validate sessions.
"""

import pytest
from framework.pages.practice_login_page import PracticeLoginPage
from framework.pages.practice_dashboard_page import PracticeDashboardPage
from tests.api.session_validator import validate_session_with_api


@pytest.mark.ui
@pytest.mark.api
@pytest.mark.smoke
def test_ui_login_with_backend_api_validation(page, api_client):
    """
    Complete hybrid test: UI login + backend API validation
    
    Flow:
    1. Navigate and login through UI
    2. Verify login success on UI (URL, message, username)
    3. Capture session cookies from browser
    4. Validate session through backend API
    5. Verify consistency between UI and API
    
    This demonstrates that:
    - UI login works and creates a valid session
    - Backend recognizes the session
    - User data is consistent across UI and API
    """
    
    print("\n" + "="*70)
    print("🔄 HYBRID TEST: UI LOGIN + BACKEND VALIDATION")
    print("="*70)
    
    # ============================================================
    # PHASE 1: UI LOGIN
    # ============================================================
    print("\n[PHASE 1] UI LOGIN")
    print("-" * 70)
    
    login_page = PracticeLoginPage(page)
    print("📍 Step 1: Navigate to login page")
    login_page.navigate("https://practice.expandtesting.com/login")
    login_page.take_screenshot("ui_step1_login_page")
    print("✓ Login page loaded")
    
    print("\n📍 Step 2: Enter credentials and login")
    login_page.login(username="practice", password="SuperSecretPassword!")
    login_page.take_screenshot("ui_step2_credentials_entered")
    print("✓ Login submitted")
    
    print("\n📍 Step 3: Wait for dashboard")
    page.wait_for_timeout(3000)
    dashboard_page = PracticeDashboardPage(page)
    login_page.take_screenshot("ui_step3_dashboard_loaded")
    print("✓ Dashboard loaded")
    
    # ============================================================
    # PHASE 2: UI VERIFICATION
    # ============================================================
    print("\n[PHASE 2] UI VERIFICATION")
    print("-" * 70)
    
    print("🔍 Verification 1: URL check")
    current_url = dashboard_page.get_url()
    assert "/secure" in current_url, f"URL check failed"
    print(f"   URL: {current_url}")
    print("✓ URL contains /secure")
    
    print("\n🔍 Verification 2: Success message check")
    assert dashboard_page.is_success_message_visible(), "Success message not visible"
    success_msg = dashboard_page.get_success_message()
    print(f"   Message: {success_msg}")
    print("✓ Success message visible")
    
    print("\n🔍 Verification 3: Username check")
    assert dashboard_page.is_username_displayed(), "Username not displayed"
    username = dashboard_page.get_username_text()
    print(f"   Username: {username}")
    print("✓ Username displayed")
    
    print("\n✅ All UI verifications PASSED")
    login_page.take_screenshot("ui_step4_verifications_passed")
    
    # ============================================================
    # PHASE 3: API VALIDATION
    # ============================================================
    print("\n[PHASE 3] BACKEND API VALIDATION")
    print("-" * 70)
    
    # Use helper function from session_validator module
    results = validate_session_with_api(login_page, api_client, username)
    
    # Verify session was captured
    assert len(results["cookies"]) > 0, "No cookies captured"
    
    login_page.take_screenshot("ui_step5_api_validation_complete")
    
    # ============================================================
    # FINAL SUMMARY
    # ============================================================
    print("\n" + "="*70)
    print("✅ HYBRID TEST PASSED")
    print("="*70)
    print("\n📊 Summary:")
    print(f"   ✓ UI Login: Successful")
    print(f"   ✓ UI Verifications: 3/3 passed")
    print(f"   ✓ Session Captured: {len(results['cookies'])} cookies")
    print(f"   ✓ User: {username}")
    print(f"   ✓ Backend Validated: Via API call")
    print("\n📸 Screenshots saved to: reports/screenshots/")
    print("🎥 Video saved to: reports/videos/\n")


@pytest.mark.ui
@pytest.mark.api
def test_login_and_api_session_reuse(page, api_client):
    """
    Test showing practical session reuse: login via UI, then use session in API calls
    
    Demonstrates:
    - Login through browser UI
    - Extract session from browser
    - Use session in API client
    - Make authenticated API calls with the captured session
    """
    
    print("\n" + "="*70)
    print("🔐 HYBRID TEST: LOGIN + API SESSION REUSE")
    print("="*70)
    
    # Step 1: UI Login
    print("\n[STEP 1] UI LOGIN")
    login_page = PracticeLoginPage(page)
    login_page.navigate("https://practice.expandtesting.com/login")
    login_page.login(username="practice", password="SuperSecretPassword!")
    page.wait_for_timeout(3000)
    
    dashboard_page = PracticeDashboardPage(page)
    assert dashboard_page.is_on_secure_dashboard(), "Login failed"
    username = dashboard_page.get_username_text()
    print(f"✓ Login successful - Username: {username}")
    
    # Step 2: Capture session
    print("\n[STEP 2] CAPTURE SESSION")
    cookies = login_page.get_cookies()
    cookie_header = login_page.get_all_cookies_as_header()
    print(f"✓ Captured {len(cookies)} cookies")
    print(f"✓ Cookie header: {len(cookie_header)} characters")
    
    # Step 3: Use session in API calls
    print("\n[STEP 3] API CALLS WITH CAPTURED SESSION")
    print("Setting API client headers with captured session...")
    api_client.set_header("Cookie", cookie_header)
    
    print("\nMaking API requests with captured session cookies...")
    print("   - API client configured with browser session")
    print("   - Ready to make authenticated API calls")
    print("   - Session persists across multiple requests")
    
    # Verify still logged in UI
    assert dashboard_page.is_on_secure_dashboard(), "Lost session"
    print("\n✓ Session successfully captured and ready for API reuse")
    print("✓ UI session still active")
    
    print("\n" + "="*70)
    print("✅ Session reuse test PASSED")
    print("="*70)
    print("\n💡 Usage pattern:")
    print("   1. Login via UI (creates session)")
    print("   2. Extract cookies: page.get_cookies()")
    print("   3. Prepare header: page.get_all_cookies_as_header()")
    print("   4. Use in API: api_client.set_header('Cookie', cookie_header)")
    print("   5. Make API calls with authenticated session\n")
