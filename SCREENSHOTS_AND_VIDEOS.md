# Screenshot and Video Capture Documentation

## Overview

The test framework now automatically captures **screenshots and videos** for all tests. This provides visual evidence of test execution and helps with debugging failures.

### Features

✅ **Automatic Video Recording** - Every test execution is recorded as a video  
✅ **Manual Screenshot Capture** - Take screenshots at critical test points  
✅ **Timestamp-Based Organization** - Files are named with timestamps for easy tracking  
✅ **Organized Output** - Screenshots and videos saved to `reports/` directory  

---

## Video Recording (Automatic)

### How It Works

Videos are **automatically recorded** for every test execution. The browser context captures the entire test:

```python
@pytest.fixture
def context(browser: Browser, request) -> BrowserContext:
    """Create browser context for each test with video recording"""
    os.makedirs(settings.VIDEO_PATH, exist_ok=True)
    context = browser.new_context(
        record_video_dir=settings.VIDEO_PATH  # ← Video recording enabled
    )
    yield context
    context.close()
```

### Video Files Location

- **Path**: `reports/videos/`
- **Format**: WebM (.webm)
- **Naming**: `{unique_id}.webm`
- **Size**: Typically 500KB - 5MB per test
- **Duration**: ~10-30 seconds per test (depending on test length)

### View Videos

Videos are saved in WebM format. You can play them using:

- **Windows**: Windows Media Player, VLC, Edge Browser
- **Mac**: Safari, VLC
- **Linux**: VLC, Firefox
- **Online**: Upload to [webmdemux.appspot.com](https://webmdemux.appspot.com/)

---

## Screenshot Capture (Manual)

### How It Works

You can manually capture screenshots at any point in your test using the screenshot methods:

#### Method 1: Using Page Object

```python
def test_practice_login_complete_scenario(page):
    login_page = PracticeLoginPage(page)
    login_page.navigate("https://practice.expandtesting.com/login")
    
    # Capture screenshot
    login_page.take_screenshot("login_page_loaded")
    
    # ... rest of test
```

#### Method 2: Using Base Page Fixture

```python
def test_example(page):
    page.goto("https://example.com")
    
    # Take screenshot using fixture utility
    screenshot_path = page.screenshot_path("page_loaded")
```

### Screenshot Files Location

- **Path**: `reports/screenshots/`
- **Format**: PNG (.png)
- **Naming**: `{name}_{YYYYMMDD}_{HHMMSS}.png`
- **Example**: `login_page_20260406_205638.png`

### Screenshot Storage

```
reports/screenshots/
├── 01_login_page_20260406_205638.png
├── 02_after_login_click_20260406_205642.png
├── 03_secure_dashboard_20260406_205646.png
├── 04_success_message_20260406_205647.png
├── test_1_login_page_20260406_210115.png
├── test_1_after_login_click_20260406_210119.png
├── test_1_secure_dashboard_20260406_210123.png
└── ... more screenshots
```

---

## Usage Examples

### Example 1: Simple Test with Screenshots

```python
@pytest.mark.ui
def test_practice_login_complete_scenario(page):
    """Complete test scenario with screenshots"""
    
    # Step 1: Navigate
    login_page = PracticeLoginPage(page)
    login_page.navigate("https://practice.expandtesting.com/login")
    login_page.take_screenshot("01_login_page")  # Screenshot 1
    
    # Step 2: Login
    login_page.login(
        username="practice",
        password="SuperSecretPassword!"
    )
    login_page.take_screenshot("02_after_login_click")  # Screenshot 2
    
    # Step 3: Verify
    page.wait_for_timeout(3000)
    dashboard_page = PracticeDashboardPage(page)
    dashboard_page.take_screenshot("03_secure_dashboard")  # Screenshot 3
    
    # Assertions
    assert "/secure" in dashboard_page.get_url()
    dashboard_page.take_screenshot("04_verification_passed")  # Screenshot 4
```

### Example 2: Screenshot on Failure

```python
def test_error_scenario(page):
    page.goto("https://practice.expandtesting.com/login")
    
    try:
        # Attempt login
        page.fill("#username", "wrong_user")
        page.fill("#password", "wrong_pass")
        page.click("button[type='submit']")
        
        # Wait for response
        page.wait_for_timeout(2000)
        
    except Exception as e:
        # Capture screenshot on error
        page.screenshot_path("error_state")
        raise e
```

### Example 3: Multiple Verification Points

```python
def test_multi_step_process(page):
    login_page = PracticeLoginPage(page)
    
    # Step 1
    login_page.navigate("https://practice.expandtesting.com/login")
    login_page.take_screenshot("step_1_login_page")
    
    # Step 2
    login_page.enter_username("practice")
    login_page.take_screenshot("step_2_username_entered")
    
    # Step 3
    login_page.enter_password("SuperSecretPassword!")
    login_page.take_screenshot("step_3_password_entered")
    
    # Step 4
    login_page.click_login_button()
    login_page.take_screenshot("step_4_login_clicked")
    
    # Step 5
    page.wait_for_timeout(3000)
    dashboard = PracticeDashboardPage(page)
    dashboard.take_screenshot("step_5_dashboard_loaded")
```

---

## Running Tests with Screenshots

### Run a Single Test

```bash
python -m pytest tests/ui/test_practice_login_simple.py -v -s
```

**Output:**
```
📸 Screenshot saved: reports/screenshots\01_login_page_20260406_205638.png
📸 Screenshot saved: reports/screenshots\02_after_login_click_20260406_205642.png
📸 Screenshot saved: reports/screenshots\03_secure_dashboard_20260406_205646.png
📸 Screenshot saved: reports/screenshots\04_success_message_20260406_205647.png
✅ ALL TESTS PASSED!
📸 SCREENSHOTS saved to: reports/screenshots/
🎥 VIDEO saved to: reports/videos/
```

### Run All Practice Login Tests

```bash
python -m pytest tests/ui/test_practice_login.py -v
```

**Result:** 10 tests passed, 10 videos recorded, 10+ screenshots captured

### Run Specific Test with Detailed Output

```bash
python -m pytest tests/ui/test_practice_login.py::TestPracticeLoginFlow::test_successful_login_with_all_verifications -v -s
```

---

## Configuration

### Environment Variables (.env)

```ini
# Screenshot Configuration
SCREENSHOTS_PATH=reports/screenshots

# Video Configuration
VIDEO_PATH=reports/videos
```

### Modifying Paths

To change where screenshots and videos are saved, edit `.env`:

```ini
# Save to custom location
SCREENSHOTS_PATH=test_artifacts/screenshots
VIDEO_PATH=test_artifacts/videos
```

Then create the directories:
```bash
mkdir -p test_artifacts/screenshots
mkdir -p test_artifacts/videos
```

---

## Screenshot API

### Take Screenshot (Page Object Method)

```python
# Basic usage
login_page.take_screenshot("login_page")

# Returns filepath
filepath = login_page.take_screenshot("login_page")
print(filepath)
# Output: reports/screenshots\login_page_20260406_205638.png
```

### Screenshot Properties

| Property | Value |
|----------|-------|
| Format | PNG |
| Quality | Full page |
| Size | Variable (typically 1280x720+) |
| Timestamp | Automatic (YYYYMMDD_HHMMSS) |
| Location | Configurable via settings.SCREENSHOTS_PATH |

---

## Video API

### Video Recording (Automatic)

```python
# No code needed - videos are captured automatically
# Just run your tests normally

@pytest.mark.ui
def test_example(page):
    # ... test code ...
    # Video will be automatically saved
```

### Video Properties

| Property | Value |
|----------|-------|
| Format | WebM (.webm) |
| Codec | VP9 video, Opus audio |
| Frame Rate | ~30 fps |
| Duration | Entire test execution |
| Location | Configurable via settings.VIDEO_PATH |
| File Size | 500KB - 5MB per test |

---

## Troubleshooting

### Screenshots Not Being Saved

**Issue**: Screenshots directory not created

**Solution**:
```python
import os
from framework.config.settings import settings

# Ensure directory exists
os.makedirs(settings.SCREENSHOTS_PATH, exist_ok=True)
os.makedirs(settings.VIDEO_PATH, exist_ok=True)
```

### Videos Not Recording

**Issue**: Video files not created

**Solution**:
1. Ensure `browser.new_context(record_video_dir=...)` is set in fixtures
2. Check that `settings.VIDEO_PATH` directory exists
3. Verify Playwright is properly installed: `python -m playwright install`

### Large File Sizes

**Issue**: Videos taking up too much disk space

**Solution**: Delete old videos periodically
```bash
# Remove videos older than 7 days
# On Windows PowerShell:
Get-ChildItem reports/videos/ -Filter *.webm | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-7)} | Remove-Item
```

### Viewing WebM Videos

**Issue**: Can't open WebM files

**Solution**: Install a player
- **Windows**: [VLC Media Player](https://www.videolan.org/)
- **Online**: Upload to [webmdemux.appspot.com](https://webmdemux.appspot.com/)
- **Convert**: Use FFmpeg to convert to MP4:
  ```bash
  ffmpeg -i video.webm video.mp4
  ```

---

## Best Practices

### 1. Strategic Screenshot Placement

```python
# Good: Screenshots at key verification points
login_page.navigate("...")
login_page.take_screenshot("initial_state")

login_page.login(...)
dashboard.take_screenshot("after_login")  # Key point

assert verification
dashboard.take_screenshot("verification_passed")  # Evidence
```

### 2. Meaningful Names

```python
# Good
page.take_screenshot("login_page_loaded")
page.take_screenshot("credentials_entered")
page.take_screenshot("error_message_displayed")

# Avoid
page.take_screenshot("screenshot1")
page.take_screenshot("img")
page.take_screenshot("temp")
```

### 3. Limit Screenshot Volume

```python
# Good: 3-5 screenshots per test
def test_workflow(page):
    page.take_screenshot("step_1")
    # ... action ...
    page.take_screenshot("step_2")
    # ... action ...
    page.take_screenshot("step_3")

# Avoid: Screenshot every line
for i in range(100):
    page.take_screenshot(f"step_{i}")
```

### 4. Use Videos for Complex Flows

Videos are great for:
- Debugging timing issues
- Understanding user flows
- Demonstrating test execution
- Identifying when failures occur

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
- name: Run Tests
  run: python -m pytest tests/ui/ -v

- name: Upload Screenshots
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: screenshots
    path: reports/screenshots/

- name: Upload Videos
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: videos
    path: reports/videos/
```

### Jenkins Example

```groovy
stage('Run Tests') {
    steps {
        sh 'python -m pytest tests/ui/ -v'
    }
}

stage('Archive Artifacts') {
    steps {
        archiveArtifacts artifacts: 'reports/screenshots/**/*.png'
        archiveArtifacts artifacts: 'reports/videos/**/*.webm'
    }
}
```

---

## Summary

| Feature | Auto | Manual | Location | Format |
|---------|------|--------|----------|--------|
| **Video Recording** | ✅ Yes | N/A | reports/videos/ | WebM |
| **Screenshots** | N/A | ✅ Yes | reports/screenshots/ | PNG |
| **Timestamps** | ✅ Auto | ✅ Auto | Filename | YYYYMMDD_HHMMSS |
| **All Tests** | ✅ Recorded | Configure | reports/ | WebM + PNG |

---

## Quick Reference

```python
# Take a screenshot
page_object.take_screenshot("meaningful_name")

# Or using fixture
page.screenshot_path("meaningful_name")

# Videos are automatic - no code needed!

# Results
# 📸 Screenshots: reports/screenshots/*.png
# 🎥 Videos: reports/videos/*.webm
```

---

**Last Updated**: 2026-04-06  
**Framework**: Playwright + Pytest  
**Python Version**: 3.11+
