"""
Quick Test Script for Practice Expand Testing Login

This script demonstrates the complete login flow:
1. Go to: https://practice.expandtesting.com/login
2. Enter username: practice
3. Enter password: SuperSecretPassword!
4. Click Login
5. Verify all requirements:
   - URL contains /secure
   - Success message is visible
   - Username is displayed on page

Run this script with:
    python -m pytest tests/ui/test_practice_login.py::TestPracticeLoginFlow::test_successful_login_with_all_verifications -v -s

Or run all practice login tests:
    python -m pytest tests/ui/test_practice_login.py -v
"""

import pytest
from framework.pages.practice_login_page import PracticeLoginPage
from framework.pages.practice_dashboard_page import PracticeDashboardPage


@pytest.mark.ui
@pytest.mark.smoke
def test_practice_login_complete_scenario(page):
    """
    Complete test scenario for practice.expandtesting.com login
    
    Scenario:
    1. Navigate to login page
    2. Enter credentials (practice / SuperSecretPassword!)
    3. Click login button
    
    Verifications:
    ✓ URL contains /secure
    ✓ Success message is visible
    ✓ Username 'practice' is displayed
    """
    
    print("\n" + "="*60)
    print("PLAYWRIGHT LOGIN TEST - PRACTICE EXPAND TESTING")
    print("="*60)
    
    # Step 1: Navigate to login page
    print("\n[STEP 1] Navigating to login page...")
    login_page = PracticeLoginPage(page)
    login_page.navigate("https://practice.expandtesting.com/login")
    assert login_page.is_on_login_page(), "Failed to load login page"
    print("✓ Login page loaded successfully")
    
    # Step 2: Enter credentials and login
    print("\n[STEP 2] Entering credentials...")
    print("   - Username: practice")
    print("   - Password: SuperSecretPassword!")
    login_page.login(
        username="practice",
        password="SuperSecretPassword!"
    )
    print("✓ Login button clicked")
    
    # Step 3: Wait for dashboard to load
    print("\n[STEP 3] Waiting for secure dashboard to load...")
    page.wait_for_timeout(3000)
    dashboard_page = PracticeDashboardPage(page)
    print("✓ Dashboard loaded")
    
    # Verification 1: Check URL
    print("\n[VERIFICATION 1] Checking URL...")
    current_url = dashboard_page.get_url()
    print(f"   Current URL: {current_url}")
    assert "/secure" in current_url, f"URL does not contain '/secure'"
    print("✓ URL contains '/secure' - PASSED")
    
    # Verification 2: Check success message
    print("\n[VERIFICATION 2] Checking success message...")
    assert dashboard_page.is_success_message_visible(), "Success message not visible"
    success_msg = dashboard_page.get_success_message()
    print(f"   Message: {success_msg}")
    print("✓ Success message visible - PASSED")
    
    # Verification 3: Check username display
    print("\n[VERIFICATION 3] Checking username display...")
    assert dashboard_page.is_username_displayed(), "Username not displayed"
    username = dashboard_page.get_username_text()
    print(f"   Username: {username}")
    print("✓ Username displayed - PASSED")
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED!")
    print("="*60 + "\n")
