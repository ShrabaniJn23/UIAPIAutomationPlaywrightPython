# Practice Expand Testing Login Test Script

This test script automates the login scenario for practice.expandtesting.com with complete verification.

## Quick Start

### Run the Simple Test (Recommended)
```bash
python -m pytest tests/ui/test_practice_login_simple.py -v -s
```

### Run All Practice Login Tests
```bash
python -m pytest tests/ui/test_practice_login.py -v -s
```

### Run Only the Main Test
```bash
python -m pytest tests/ui/test_practice_login.py::TestPracticeLoginFlow::test_successful_login_with_all_verifications -v -s
```

## Test Scenario

### Steps Executed:
1. ✅ Navigate to: https://practice.expandtesting.com/login
2. ✅ Enter Username: `practice`
3. ✅ Enter Password: `SuperSecretPassword!`
4. ✅ Click Login Button

### Verifications:
1. ✅ **URL Verification** - URL contains `/secure`
2. ✅ **Success Message** - "You logged into a secure area!" is displayed
3. ✅ **Username Display** - Username "practice" is visible on the page

## Files Created

### Page Objects
- [framework/pages/practice_login_page.py](framework/pages/practice_login_page.py) - Login page object
- [framework/pages/practice_dashboard_page.py](framework/pages/practice_dashboard_page.py) - Dashboard page object

### Test Files
- [tests/ui/test_practice_login.py](tests/ui/test_practice_login.py) - Comprehensive test suite with 10 test cases
- [tests/ui/test_practice_login_simple.py](tests/ui/test_practice_login_simple.py) - Simple test with detailed output

## Test Classes

### TestPracticeLoginFlow (Main Tests)
- `test_successful_login_with_all_verifications()` - Complete test with all verifications ⭐
- `test_login_and_verify_url_redirect()` - Verify URL redirect to /secure
- `test_login_and_verify_success_message()` - Verify success message visibility
- `test_login_and_verify_username_display()` - Verify username display
- `test_login_complete_flow_with_all_details()` - Detailed logging test

### TestPracticeLoginEdgeCases (Edge Cases)
- `test_login_with_empty_username()` - Empty username validation
- `test_login_with_empty_password()` - Empty password validation
- `test_login_with_wrong_credentials()` - Invalid credentials handling
- `test_page_title_verification()` - Page title check
- `test_logout_functionality()` - Logout functionality

## Configuration

The tests use the `.env` file for configuration:

```env
BASE_URL=https://practice.expandtesting.com
BROWSER_TYPE=chromium
HEADLESS=true
TIMEOUT=30000
```

To run with visible browser:
```bash
$env:HEADLESS='false'; python -m pytest tests/ui/test_practice_login.py -v
```

## Test Reports

HTML reports are generated automatically in:
```
reports/pytest_report.html
```

## Sample Output

```
============================================================
PLAYWRIGHT LOGIN TEST - PRACTICE EXPAND TESTING
============================================================

[STEP 1] Navigating to login page...
✓ Login page loaded successfully

[STEP 2] Entering credentials...
   - Username: practice
   - Password: SuperSecretPassword!
✓ Login button clicked

[STEP 3] Waiting for secure dashboard to load...
✓ Dashboard loaded

[VERIFICATION 1] Checking URL...
   Current URL: https://practice.expandtesting.com/secure
✓ URL contains '/secure' - PASSED

[VERIFICATION 2] Checking success message...
   Message: You logged into a secure area!
✓ Success message visible - PASSED

[VERIFICATION 3] Checking username display...
   Username: practice
✓ Username displayed - PASSED

============================================================
ALL TESTS PASSED!
============================================================
```

## Troubleshooting

### Test Times Out
- Increase TIMEOUT in .env
- Ensure internet connection is stable
- Check if the website is accessible

### Selectors Not Found
- The page object has robust selectors that look for:
  - Alert messages containing success indicators
  - Page content containing username "practice"
  - URL patterns containing "/secure"

### Browser Not Launching
```bash
playwright install
```

## Integration with CI/CD

Run tests in your CI/CD pipeline:

```bash
# Install dependencies
pip install -r requirements.txt
playwright install

# Run tests
pytest tests/ui/test_practice_login.py -v --tb=short

# Generate report
pytest tests/ui/test_practice_login.py --html=reports/pytest_report.html --self-contained-html
```

## Framework Features Used

- ✅ Playwright for browser automation
- ✅ Pytest for test framework
- ✅ Page Object Model (POM) pattern
- ✅ Fixtures for browser management
- ✅ Configuration management via .env
- ✅ HTML reporting
- ✅ Test markers (smoke, regression)
- ✅ Detailed logging and output

## Next Steps

1. Customize the credentials if needed
2. Add more test scenarios
3. Run in your CI/CD pipeline
4. Integrate with test management tools
5. Add API tests for backend validation
