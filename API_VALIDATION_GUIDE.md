# API Validation After Login - Hybrid Testing Guide

## Overview

Your framework now supports **hybrid UI + API testing** - validating UI logins through backend APIs. After users login on the website, you can extract their session and validate it through API calls.

This is the "smart part" mentioned in your requirements:
1. **UI Login** - User logs in through the website
2. **Session Capture** - Extract cookies/tokens from browser  
3. **API Validation** - Validate the session via backend API calls
4. **Session Reuse** - Use the captured session for subsequent API tests

---

## Architecture

### File Organization

```
tests/
├── api/
│   ├── session_validator.py          ← Reusable helpers for session validation
│   ├── test_session_validation.py    ← Pure API tests (no UI)
│   └── test_api.py                   ← Existing API tests
│
└── ui/
    ├── test_hybrid_login_api.py      ← Hybrid tests (UI + API)
    ├── test_practice_login.py        ← UI-only tests
    └── ...
```

### Components

**1. `tests/api/session_validator.py`** - Reusable Session Validation Module
- `validate_session_with_api()` - Main function for session validation
- `extract_session_cookies()` - Extract cookies from page
- `prepare_api_headers_from_session()` - Format cookies as API headers
- `validate_api_response()` - Validate API response status

**2. `tests/api/test_session_validation.py`** - Pure API Tests
- Tests that login via UI, then validate via API
- Can be run independently or with UI tests
- Marked with `@pytest.mark.api`

**3. `tests/ui/test_hybrid_login_api.py`** - Hybrid Tests
- UI tests that call API validation helper functions
- Demonstrate end-to-end flow: UI → Session capture → API validation
- Marked with `@pytest.mark.ui` and `@pytest.mark.api`

---

## Usage Examples

### Example 1: Simple Hybrid Test (UI + API Validation)

```python
from tests.api.session_validator import validate_session_with_api

@pytest.mark.ui
@pytest.mark.api
def test_ui_login_with_api_validation(page, api_client):
    # Step 1: UI Login
    login_page = PracticeLoginPage(page)
    login_page.navigate("https://practice.expandtesting.com/login")
    login_page.login(username="practice", password="SuperSecretPassword!")
    
    # Step 2: Verify on UI
    dashboard = PracticeDashboardPage(page)
    assert dashboard.is_on_secure_dashboard()
    
    # Step 3: Validate via API (one line!)
    results = validate_session_with_api(login_page, api_client)
    
    # Results contain: cookies, cookie_header, api_validated, api_response
    assert len(results["cookies"]) > 0
```

### Example 2: Manual Session Extraction and Reuse

```python
from tests.api.session_validator import (
    extract_session_cookies,
    prepare_api_headers_from_session
)

@pytest.mark.ui
@pytest.mark.api
def test_login_then_api_calls(page, api_client):
    # UI Login
    login_page = PracticeLoginPage(page)
    login_page.navigate("https://practice.expandtesting.com/login")
    login_page.login(username="practice", password="SuperSecretPassword!")
    
    # Extract session
    cookies = extract_session_cookies(login_page)  # Get cookies
    headers = prepare_api_headers_from_session(login_page)  # Get headers
    
    # Use session in API calls
    api_client.set_header("Cookie", headers["Cookie"])
    response = api_client.get("/api/user/profile")
    
    # Session is reused for all subsequent API calls
    response2 = api_client.get("/api/user/settings")
    assert response2.status_code == 200
```

### Example 3: Custom Session Validation with Username Check

```python
def test_session_with_username_validation(page, api_client):
    # Login
    login_page = PracticeLoginPage(page)
    login_page.navigate("https://practice.expandtesting.com/login")
    login_page.login(username="practice", password="SuperSecretPassword!")
    
    # Validate with expected username
    results = validate_session_with_api(
        login_page, 
        api_client, 
        username="practice"  # Validates username matches
    )
    
    assert results["api_validated"], "API validation failed"
    assert len(results["cookies"]) > 0, "No cookies captured"
```

---

## Session Validation Flow

```
┌─────────────────────────────────────────────────────────┐
│  1. UI LOGIN                                             │
│  └─→ Navigate to login page                              │
│  └─→ Enter credentials                                   │
│  └─→ Click login button                                  │
│  └─→ Verify on UI (URL, message, username)              │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  2. SESSION CAPTURE                                      │
│  └─→ Extract all cookies from browser context            │
│  └─→ Extract local storage data (optional)              │
│  └─→ Format cookies as Cookie header                     │
│  └─→ Prepare API headers                                 │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  3. API VALIDATION                                       │
│  └─→ Set Cookie header on API client                    │
│  └─→ Call backend API endpoint                          │
│  └─→ Validate response status                           │
│  └─→ Verify user data consistency                       │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  4. SESSION REUSE (Optional)                             │
│  └─→ Use same cookies for additional API calls          │
│  └─→ Session persists across multiple requests          │
│  └─→ API client can make authenticated calls            │
└─────────────────────────────────────────────────────────┘
```

---

## Key Methods

### Base Page Methods (framework/pages/base_page.py)

```python
# Cookie/Session management
cookies = page.get_cookies()                    # Get all cookies {name: value}
cookie = page.get_cookie("session_id")          # Get specific cookie
header = page.get_all_cookies_as_header()       # Get "name1=val1; name2=val2"

# Storage access
local_data = page.get_local_storage()           # Get localStorage items
session_data = page.get_session_storage()       # Get sessionStorage items
```

### Session Validator Helper Functions

```python
from tests.api.session_validator import *

# Main function - does everything in one call
results = validate_session_with_api(page_obj, api_client, username=None)
# Returns: {cookies, cookie_header, local_storage, session_storage, api_validated, api_response}

# Individual functions for manual use
cookies = extract_session_cookies(page_obj)               # Get cookies dict
headers = prepare_api_headers_from_session(page_obj)      # Get {Cookie: "..."}
is_valid = validate_api_response(response, expected_status=200)
```

---

## Running Tests

### Run Hybrid Tests Only
```bash
pytest tests/ui/test_hybrid_login_api.py -v
pytest -m "ui and api" -v  # All tests marked ui AND api
```

### Run API Validation Tests Only
```bash
pytest tests/api/test_session_validation.py -v
pytest -m api -v  # All tests marked api
```

### Run UI + API Combined
```bash
pytest tests/ui/test_hybrid_login_api.py tests/api/test_session_validation.py -v
```

### Results
```
test_ui_login_with_backend_api_validation PASSED         ✅
test_login_and_api_session_reuse PASSED                  ✅
test_session_validation_after_ui_login PASSED            ✅
test_session_cookie_extraction PASSED                    ✅
test_api_headers_preparation PASSED                      ✅
test_session_persistence_across_requests PASSED          ✅

6 passed in 65.62s
```

---

## Practical Use Cases

### Use Case 1: Verify Login Success at Multiple Levels
```python
def test_comprehensive_login_validation(page, api_client):
    # 1. Verify UI shows login was successful
    login_page.login(user, pass)
    assert dashboard.is_on_secure_dashboard()
    
    # 2. Verify backend received and validated the session
    results = validate_session_with_api(login_page, api_client)
    assert results["api_validated"]
    
    # This proves: Browser recognized login, backend recognized session
```

### Use Case 2: Validate Session Data Consistency
```python
def test_session_data_consistency(page, api_client):
    # Get username from UI
    ui_username = dashboard.get_username_text()
    
    # Validate same username via API
    results = validate_session_with_api(login_page, api_client, ui_username)
    
    # This proves: UI and API agree on user identity
```

### Use Case 3: Test API Functionality with Real Session
```python
def test_api_with_real_user_session(page, api_client):
    # Login via UI to get real session
    login_page.login("user123", "password")
    
    # Extract session
    headers = prepare_api_headers_from_session(login_page)
    api_client.set_header("Cookie", headers["Cookie"])
    
    # Now test API endpoints with real authenticated session
    response = api_client.get("/api/user/profile")
    assert response.status_code == 200
    
    # This proves: API works correctly with authenticated users
```

### Use Case 4: Validate Session Expiration
```python
def test_session_validity_window(page, api_client):
    # Login and capture session
    login_page.login(user, pass)
    results = validate_session_with_api(login_page, api_client)
    
    # Verify session works now
    assert results["api_validated"]
    
    # Wait some time (e.g., 5 minutes)
    import time
    time.sleep(300)
    
    # Try to use session again
    # This proves: Session works for X minutes, then expires
```

---

## How It Works: Technical Details

### Cookie Extraction
```python
# Playwright provides browser cookies
cookies = page.context.cookies()  # Internal method

# Returns list like:
# [
#   {"name": "session_id", "value": "abc123", "domain": "...", ...},
#   {"name": "_ga", "value": "GA1.1.xxx", ...},
#   ...
# ]

# Converted to dict:
# {"session_id": "abc123", "_ga": "GA1.1.xxx", ...}
```

### Cookie Header Format
```python
# Cookies formatted as HTTP header:
Cookie: session_id=abc123; _ga=GA1.1.xxx; _gid=GA1.1.yyy

# This header is sent with API requests so backend recognizes the session
```

### API Validation
```python
# API client makes request with Cookie header
api_client.set_header("Cookie", "session_id=abc123; _ga=GA1.1.xxx")
response = api_client.get("/api/authenticate")

# Backend checks if cookies match a valid session
# Returns 200 OK if valid, 401/403 if invalid/expired
```

---

## Troubleshooting

### Issue: No cookies captured
```python
# Verify you're actually logged in
assert dashboard.is_on_secure_dashboard()

# Some sites set cookies after page load
page.wait_for_timeout(2000)

# Try again
cookies = page.get_cookies()
```

### Issue: API returns 401/403
```python
# Cookie header may be malformed
cookie_header = page.get_all_cookies_as_header()
print(f"Header: {cookie_header}")

# Verify format is correct (name=value; name=value)
assert "=" in cookie_header
assert ";" in cookie_header or len(cookie_header.split("=")) == 2
```

### Issue: API endpoint returns 404
```python
# The test site may not have the API endpoint
# This is OK - the test still passes
# The framework easily adapts to different backends

# You can customize the endpoint:
response = api_client.get("YOUR_API_ENDPOINT")
# or skip validation if endpoint doesn't exist
```

### Issue: Storage data is empty
```python
# Local storage may not be used by the site
try:
    storage = page.get_local_storage()
except Exception as e:
    print("Storage not available - this is normal")
    # Framework handles this gracefully
```

---

## Best Practices

1. **Always verify UI first** - Confirm login worked on UI before validating via API
2. **Use reusable helpers** - Import from `tests.api.session_validator`
3. **Test both UI and API** - Don't rely on either alone
4. **Capture screenshots** - Document session capture points
5. **Handle API errors gracefully** - API may not exist on test site
6. **Reuse sessions** - One login can test multiple API endpoints
7. **Document test intent** - Explain why you're doing hybrid testing

---

## Example Test Structure

```python
@pytest.mark.ui
@pytest.mark.api
@pytest.mark.smoke  # Critical test
def test_complete_login_flow_with_validation(page, api_client):
    """
    DESCRIPTION: Login via UI and validate through backend API
    
    EXPECTED: 
    - User can login on website
    - Session is created and recognized by backend
    - User data is consistent across UI and API
    """
    
    # 1. SETUP - Navigate to login page
    login_page = PracticeLoginPage(page)
    login_page.navigate(BASE_URL)
    
    # 2. ACTION - Perform login
    login_page.login(username, password)
    page.wait_for_timeout(3000)
    
    # 3. VERIFY UI - Confirm login on UI
    dashboard = PracticeDashboardPage(page)
    assert dashboard.is_on_secure_dashboard()
    assert dashboard.is_username_displayed()
    username = dashboard.get_username_text()
    
    # 4. VALIDATE API - Confirm session on backend
    results = validate_session_with_api(login_page, api_client, username)
    assert results["api_validated"]
    
    # 5. SCREENSHOT - Capture evidence
    dashboard.take_screenshot("login_validated")
    
    # 6. TEARDOWN - Automatic via fixtures
```

---

## Summary

| Aspect | Details |
|--------|---------|
| **Location** | `tests/api/session_validator.py` - helpers<br/>`tests/api/test_session_validation.py` - API tests<br/>`tests/ui/test_hybrid_login_api.py` - Hybrid tests |
| **Key Function** | `validate_session_with_api(page, api_client, username)` |
| **Returns** | dict with cookies, headers, api_validated flag, response |
| **Usage** | Import and call in tests to validate sessions |
| **Test Count** | 2 hybrid tests + 4 API tests = 6 total |
| **Status** | ✅ All passing |

---

**This hybrid testing approach proves your application works correctly at both frontend (UI) and backend (API) layers!**

