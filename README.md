# Playwright UI & API Test Automation Framework

A comprehensive Python test automation framework built with Playwright for UI testing and requests for API testing.

##Using Restful Booker

Step-by-step:
Create booking via API
Capture bookingId
Open UI
Search/filter booking
Validate all booking details
(Optional) Cleanup via API


##Sceanrio 2 Steps:
Go to: https://practice.expandtesting.com/login
Enter:
Username: practice
Password: SuperSecretPassword!
Click Login
Verify:
URL contains /secure
Success message is visible
Username is displayed on page
    API Validation (Backend)

Now here’s the smart part 👇

After login:

Capture session cookie / token
Call API to validate user

## Features

- ✅ **UI Testing** with Playwright (Chromium, Firefox, WebKit)
- ✅ **API Testing** with requests library
- ✅ **Page Object Model (POM)** pattern for UI tests
- ✅ **Pytest** fixtures and markers
- ✅ **Configurable settings** via `.env` file
- ✅ **HTML Reports** with pytest-html
- ✅ **Utility helpers** for common operations
- ✅ **Multiple test tags** (smoke, regression, ui, api)

## Project Structure

```
PlaywrightUIAPIAutomation/
├── framework/
│   ├── config/
│   │   └── settings.py          # Configuration management
│   ├── pages/
│   │   ├── base_page.py         # Base page object class
│   │   ├── login_page.py        # Login page object
│   │   └── home_page.py         # Home page object
│   ├── api/
│   │   └── api_client.py        # API client class
│   ├── fixtures/
│   │   └── fixtures.py          # Pytest fixtures
│   └── __init__.py
├── tests/
│   ├── ui/
│   │   └── test_login.py        # UI test examples
│   └── api/
│       └── test_api.py          # API test examples
├── utils/
│   └── helpers.py               # Utility helpers
├── reports/                     # Test reports (generated)
├── .env                         # Environment variables
├── conftest.py                  # Root pytest configuration
├── pytest.ini                   # Pytest settings
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd PlaywrightUIAPIAutomation
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

## Configuration

### .env File

The `.env` file contains configuration settings. Customize as needed:

```env
# Browser Configuration
BROWSER_TYPE=chromium          # Options: chromium, firefox, webkit
HEADLESS=true                  # Run in headless mode
SLOW_MO=0                       # Slow down actions (ms)

# Test Configuration
BASE_URL=https://example.com   # Application base URL
API_BASE_URL=https://api.example.com  # API base URL
TIMEOUT=30000                  # Timeout in milliseconds

# Test Data
SCREENSHOTS_PATH=reports/screenshots
VIDEO_PATH=reports/videos

# Environment
ENVIRONMENT=dev                # dev, staging, prod
DEBUG=false                    # Enable debug mode
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/ui/test_login.py
pytest tests/api/test_api.py
```

### Run Tests by Marker
```bash
# Run only UI tests
pytest -m ui

# Run only API tests
pytest -m api

# Run only smoke tests
pytest -m smoke

# Run only regression tests
pytest -m regression
```

### Run with Options
```bash
# Run with verbose output
pytest -v

# Run with specific browser
BROWSER_TYPE=firefox pytest

# Run with HTML report
pytest --html=reports/pytest_report.html --self-contained-html

# Run in headless mode
HEADLESS=true pytest

# Run without headless mode (show browser)
HEADLESS=false pytest

# Run with screenshots on failure
pytest --screenshot=only-on-failure

# Run specific number of tests in parallel
pytest -n 4
```

## Page Object Model (POM)

All page objects inherit from `BasePage` which provides common methods:

### BasePage Methods
- `navigate(url)` - Navigate to URL
- `click(selector)` - Click element
- `fill(selector, text)` - Fill input field
- `get_text(selector)` - Get element text
- `is_visible(selector)` - Check if element is visible
- `wait_for_selector(selector)` - Wait for element
- `take_screenshot(name)` - Take screenshot
- `scroll_to_element(selector)` - Scroll to element

### Example Page Object

```python
from framework.pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    
    def login(self, username: str, password: str):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
```

## API Client Usage

### Basic Usage

```python
from framework.api.api_client import APIClient

# Create client
client = APIClient(base_url="https://api.example.com")

# Set headers
client.set_header("Authorization", "Bearer token123")

# Make requests
response = client.get("/users")
response = client.post("/users", json={"name": "John"})
response = client.put("/users/1", json={"name": "Jane"})
response = client.delete("/users/1")

# Close client
client.close()
```

### With Context Manager

```python
with APIClient(base_url="https://api.example.com") as client:
    response = client.get("/users")
    # Client closes automatically
```

## Fixtures

### Browser Fixture
```python
def test_example(page):
    page.goto("https://example.com")
    assert "Example" in page.title()
```

### API Client Fixture
```python
def test_api_example(api_client):
    response = api_client.get("/users")
    assert response.status_code == 200
```

## Writing Tests

### UI Test Example

```python
import pytest
from framework.pages.login_page import LoginPage

@pytest.mark.ui
@pytest.mark.smoke
def test_login(page):
    login_page = LoginPage(page)
    login_page.navigate("https://example.com")
    login_page.login("user@example.com", "password123")
    assert "dashboard" in page.url
```

### API Test Example

```python
import pytest

@pytest.mark.api
def test_get_users(api_client):
    response = api_client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## Utilities

### Test Data Helper
```python
from utils.helpers import TestDataHelper

unique_email = TestDataHelper.get_unique_email("user")
unique_username = TestDataHelper.get_unique_username("test")
timestamp = TestDataHelper.get_timestamp()
```

### Wait Helper
```python
from utils.helpers import WaitHelper

WaitHelper.wait(2)  # Wait 2 seconds
WaitHelper.wait_until(lambda: condition_is_true, timeout=10)
```

### Response Validator
```python
from utils.helpers import ResponseValidator

ResponseValidator.validate_status_code(response, 200)
ResponseValidator.validate_response_is_list(response)
ResponseValidator.validate_response_contains_key(response, "id")
```

## Test Reports

HTML reports are generated in the `reports/` directory:

```bash
# Reports will be saved as
reports/pytest_report.html
```

## Best Practices

1. **Use Page Object Model** - Keep selectors and page logic in page objects
2. **Use Fixtures** - Share browser/API client across tests
3. **Use Markers** - Tag tests for selective execution
4. **Meaningful Names** - Use descriptive test names
5. **Assertions** - Use clear and specific assertions
6. **Error Handling** - Handle API response errors appropriately
7. **Test Data** - Use helpers for generating test data
8. **Wait Strategies** - Use explicit waits instead of hardcoded sleeps
9. **Screenshots** - Take screenshots on test failures
10. **Isolation** - Tests should be independent

## Troubleshooting

### Browser not found
```bash
playwright install
```

### Import errors
```bash
pip install -r requirements.txt
```

### Playwright timeout issues
Increase `TIMEOUT` in `.env`:
```env
TIMEOUT=60000
```

### Tests running in headless mode
Set `HEADLESS=false` in `.env` to see browser:
```env
HEADLESS=false
```

## Contributing

1. Create page objects for new pages
2. Write tests using existing page objects
3. Follow naming conventions
4. Use appropriate test markers
5. Keep tests focused and independent

## License

MIT

## Contact

For issues or questions, please raise an issue in the repository.
