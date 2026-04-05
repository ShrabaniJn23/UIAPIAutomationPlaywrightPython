# Quick Start Guide

## Setup Instructions

### Step 1: Install Dependencies
```bash
# Navigate to project directory
cd PlaywrightUIAPIAutomation

# Install all required packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### Step 2: Configure Settings
Edit `.env` file with your application URLs and settings:
```env
BASE_URL=https://your-app.com
API_BASE_URL=https://api.your-app.com
BROWSER_TYPE=chromium
HEADLESS=true
```

### Step 3: Run Tests

#### Run All Tests
```bash
pytest
```

#### Run API Tests Only
```bash
pytest tests/api/ -v
```

#### Run UI Tests Only
```bash
pytest tests/ui/ -v
```

#### Run Specific Test
```bash
pytest tests/api/test_api.py::TestPublicAPI::test_get_posts -v
```

#### Run with Different Browser
```bash
BROWSER_TYPE=firefox pytest tests/ui/
BROWSER_TYPE=webkit pytest tests/ui/
```

#### Run in Non-Headless Mode (Show Browser)
```bash
HEADLESS=false pytest tests/ui/ -v
```

### Step 4: View Test Report
After running tests, open the HTML report:
```
reports/pytest_report.html
```

## Framework Components

### 1. **Page Objects** (`framework/pages/`)
- `base_page.py` - Base class with common methods
- `login_page.py` - Example login page object
- `home_page.py` - Example home page object

### 2. **API Client** (`framework/api/`)
- `api_client.py` - Reusable API client for HTTP requests

### 3. **Fixtures** (`framework/fixtures/`)
- `fixtures.py` - Pytest fixtures for browser, context, page, and API client

### 4. **Configuration** (`framework/config/`)
- `settings.py` - Application settings loaded from .env

### 5. **Tests** (`tests/`)
- `tests/ui/test_login.py` - UI test examples
- `tests/api/test_api.py` - API test examples

### 6. **Utilities** (`utils/`)
- `helpers.py` - Helper functions for test data, waits, and validations

## Common Commands

```bash
# Run tests with verbose output
pytest -v

# Run tests with output capture disabled (shows print statements)
pytest -s

# Run specific test method
pytest tests/api/test_api.py::TestPublicAPI::test_get_posts

# Run tests matching pattern
pytest -k "test_get"

# Run tests and stop on first failure
pytest -x

# Run tests with parallel execution (requires pytest-xdist)
pytest -n 4

# Generate HTML report
pytest --html=reports/pytest_report.html --self-contained-html

# Run only smoke tests
pytest -m smoke

# Run only regression tests
pytest -m regression
```

## Extending the Framework

### Add a New Page Object
1. Create a new file in `framework/pages/` (e.g., `dashboard_page.py`)
2. Inherit from `BasePage`
3. Define CSS selectors and methods

### Add a New Test Suite
1. Create a new file in `tests/ui/` or `tests/api/`
2. Import required fixtures and page objects
3. Write test methods with @pytest.mark decorators

### Add a New Helper
1. Add method to `utils/helpers.py`
2. Import and use in test files

## Troubleshooting

### Playwright Browsers Not Installed
```bash
playwright install
```

### Timeout Issues
Increase `TIMEOUT` in `.env`:
```env
TIMEOUT=60000
```

### Module Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Port Already in Use
Change the port in `.env` or kill the process using the port

## Next Steps
1. Add your own page objects for your application
2. Write UI tests for your workflows
3. Add API tests for your backend endpoints
4. Configure CI/CD pipeline to run tests automatically
