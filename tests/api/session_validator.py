"""
Session Validation Helper Functions

Reusable utilities for validating user sessions via API.
Can be imported and used by both API tests and hybrid UI+API tests.
"""


def validate_session_with_api(page_object, api_client, username: str = None) -> dict:
    """
    Validate an active session by extracting cookies and calling API.
    
    This function:
    1. Extracts cookies from the Playwright page context
    2. Prepares them as a Cookie header for API requests
    3. Calls the backend API to validate the session
    4. Returns validation results
    
    Args:
        page_object: BasePage object with active session
        api_client: APIClient instance for making requests
        username: Expected username to verify (optional)
    
    Returns:
        dict with keys:
        - cookies: dict of all cookies
        - cookie_header: formatted cookie header string
        - local_storage: browser local storage data
        - session_storage: browser session storage data
        - api_validated: bool indicating if API validation succeeded
        - api_response: raw API response
    
    Example:
        >>> from tests.api.session_validator import validate_session_with_api
        >>> result = validate_session_with_api(login_page, api_client, "practice")
        >>> if result['api_validated']:
        ...     print(f"Session validated for {username}")
    """
    
    print("\n[SESSION CAPTURE & VALIDATION]")
    print("-" * 70)
    
    # Step 1: Extract cookies
    print("\n📍 Step 1: Extract cookies from browser")
    cookies = page_object.get_cookies()
    print(f"✓ Captured {len(cookies)} cookies")
    
    # Step 2: Get cookie header
    print("\n📍 Step 2: Extract session header")
    cookie_header = page_object.get_all_cookies_as_header()
    print(f"✓ Cookie header extracted ({len(cookie_header)} characters)")
    
    # Step 3: Extract storage
    print("\n📍 Step 3: Extract browser storage")
    local_storage = {}
    session_storage = {}
    try:
        local_storage = page_object.get_local_storage()
        session_storage = page_object.get_session_storage()
        print(f"✓ Storage extracted")
    except Exception as e:
        print(f"ℹ️  Storage not available: {str(e)}")
    
    # Step 4: Validate via API
    print("\n📍 Step 4: Validate session via API")
    print("   Endpoint: https://practice.expandtesting.com/api/authenticate")
    
    # Configure API client with cookies
    api_client.set_header("Cookie", cookie_header)
    print(f"✓ API client configured with cookies")
    
    # Make validation request
    api_validated = False
    api_response = None
    
    try:
        response = api_client.get("https://practice.expandtesting.com/api/authenticate")
        api_response = response
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"   Response: {response_data}")
            api_validated = True
            
            # Verify username if provided
            if username and "user" in response_data:
                api_username = response_data.get("user", {}).get("username", "")
                if api_username.lower() == username.lower():
                    print(f"✓ Username '{username}' validated via API")
                else:
                    print(f"⚠️  Username mismatch: API='{api_username}', Expected='{username}'")
        else:
            print(f"⚠️  API returned status {response.status_code}")
            print(f"   Response: {response.text[:200] if hasattr(response, 'text') else str(response)}")
    
    except Exception as e:
        print(f"⚠️  API validation request failed: {str(e)}")
        print(f"   (This may be expected - endpoint may not exist)")
    
    # Return results
    results = {
        "cookies": cookies,
        "cookie_header": cookie_header,
        "local_storage": local_storage,
        "session_storage": session_storage,
        "api_validated": api_validated,
        "api_response": api_response,
    }
    
    print("\n" + "="*70)
    print(f"✅ Session validation complete")
    print(f"   Cookies: {len(cookies)}")
    print(f"   API Response: {api_response.status_code if api_response else 'None'}")
    print("="*70)
    
    return results


def extract_session_cookies(page_object) -> dict:
    """
    Extract cookies from current page context.
    
    Args:
        page_object: BasePage object with active session
    
    Returns:
        dict of cookies {name: value}
    """
    cookies = page_object.get_cookies()
    print(f"✓ Extracted {len(cookies)} cookies from browser")
    return cookies


def prepare_api_headers_from_session(page_object) -> dict:
    """
    Prepare API headers using session data from browser.
    
    Args:
        page_object: BasePage object with active session
    
    Returns:
        dict of headers ready for API requests
    """
    cookie_header = page_object.get_all_cookies_as_header()
    headers = {
        "Cookie": cookie_header,
        "User-Agent": "Playwright Test Automation",
    }
    print(f"✓ Prepared headers for API requests")
    return headers


def validate_api_response(response, expected_status=200) -> bool:
    """
    Validate an API response status.
    
    Args:
        response: API response object
        expected_status: Expected HTTP status code
    
    Returns:
        bool indicating if response matches expected status
    """
    if response.status_code == expected_status:
        print(f"✓ API response valid: {response.status_code}")
        return True
    else:
        print(f"✗ API response invalid: {response.status_code} (expected {expected_status})")
        return False
