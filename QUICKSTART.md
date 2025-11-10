# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Prerequisites
- Python 3.10+
- pip
- Git

### 2. Clone and Setup

```bash
# Clone repository
git clone <repo-url>
cd py-playwright

# Run setup script (Linux/macOS)
chmod +x setup.sh
./setup.sh

# Or manual setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install
cp .env.example .env
```

### 3. Run Your First Test

```bash
# Run smoke tests
pytest -m smoke -v

# Or using Make
make smoke
```

### 4. View Results

```bash
# Open HTML report
open reports/report.html

# Generate Allure report
make report
```

---

## 📚 Common Commands

### Run Tests

```bash
# All tests
pytest

# Smoke tests only
pytest -m smoke

# Regression tests
pytest -m regression

# Mobile tests
pytest -m mobile --device=iPhone_13

# Specific browser
pytest --browser=firefox

# Parallel execution
pytest -n 4
```

### Using Make

```bash
make smoke          # Run smoke tests
make regression     # Run regression tests
make mobile         # Run mobile tests
make all-browsers   # Run on all browsers
make parallel       # Run in parallel
make report         # Generate Allure report
```

### Docker

```bash
# Build image
docker build -t ui-automation .

# Run tests
docker-compose up test-runner

# Run specific browser
docker-compose up test-chromium
```

---

## 🎯 Quick Examples

### Example 1: Basic Login Test

```python
import pytest
from pages import LoginPage

@pytest.mark.smoke
def test_login(page, base_url, test_user):
    login_page = LoginPage(page)
    login_page.navigate_to_login(base_url)
    login_page.login(test_user["email"], test_user["password"])
    assert "dashboard" in page.url
```

### Example 2: Mobile Test

```python
import pytest

@pytest.mark.mobile
def test_mobile_ui(page, base_url):
    page.goto(base_url)
    assert page.viewport_size["width"] <= 500
```

### Example 3: Data-Driven Test

```python
import pytest
from tools import DataGenerator

def test_with_generated_data(page, base_url):
    data_gen = DataGenerator()
    user = data_gen.generate_user()
    # Use generated data in test
```

---

## 🔧 Configuration

### Environment Variables (.env)

```env
ENV=dev
BASE_URL=https://example.com
BROWSER=chromium
HEADLESS=true
PARALLEL_WORKERS=4
```

### CLI Options

```bash
pytest \
  --browser=chromium \
  --env=staging \
  --device=iPhone_13 \
  --parallel=4 \
  --report=allure
```

---

## 📊 Understanding Reports

### Allure Report Features
- Test execution timeline
- Test categories and suites
- Screenshots and videos
- Trace files
- Failed test analysis
- Test history

### Artifacts Location
- Screenshots: `artifacts/screenshots/`
- Videos: `artifacts/videos/`
- Traces: `artifacts/traces/`
- Logs: `artifacts/logs/`

---

## 🐛 Debugging

```bash
# Run with Playwright inspector
PWDEBUG=1 pytest tests/test_smoke.py

# View trace file
playwright show-trace artifacts/traces/trace.zip

# Check logs
cat artifacts/logs/test_execution_*.jsonl | jq
```

---

## 📞 Need Help?

- Check `README.md` for full documentation
- Review test examples in `tests/`
- Check page objects in `pages/`
- Review fixtures in `fixtures/`

---

## 🎓 Next Steps

1. ✅ Run smoke tests: `make smoke`
2. ✅ View report: `make report`
3. ✅ Customize `.env` for your environment
4. ✅ Create your first page object
5. ✅ Write your first test
6. ✅ Set up CI/CD pipeline
7. ✅ Run tests in Docker

---

**Happy Testing! 🎉**
