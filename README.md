# UI Test Automation Framework
## Python + pytest + Playwright

[![Test Automation](https://github.com/yourusername/ui-automation/actions/workflows/test-automation.yml/badge.svg)](https://github.com/yourusername/ui-automation/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.40+-green.svg)](https://playwright.dev/python/)

A robust, scalable, and maintainable test automation framework for **UI and mobile browser testing** built with Python, pytest, and Playwright.

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Reporting](#reporting)
- [CI/CD Integration](#cicd-integration)
- [Docker Support](#docker-support)
- [Best Practices](#best-practices)

---

## ✨ Features

- **Multi-Browser Support**: Chromium, Firefox, WebKit
- **Mobile Testing**: Device emulation for iOS and Android
- **Parallel Execution**: Run tests in parallel with pytest-xdist
- **Page Object Model**: Maintainable and reusable page objects
- **Rich Reporting**: Allure reports with screenshots, videos, and traces
- **Artifact Management**: Auto-capture screenshots/videos on failure
- **Structured Logging**: JSON logs with full traceability
- **Test Data Service**: Synthetic data generation and management
- **Configuration Management**: Environment-based YAML configs
- **CI/CD Ready**: GitHub Actions workflows with cross-platform support
- **Docker Support**: Containerized execution for reproducibility

---

## 🏗️ Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Execution Layer                      │
│                    (pytest + CLI)                            │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────────┐
│              Configuration Management                        │
│        (YAML configs, env vars, CLI options)                │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────────┐
│                    Fixtures Layer                            │
│      (Browser, Context, Page, Auth, Data)                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────────┐
│                  Page Object Layer                           │
│           (BasePage, LoginPage, etc.)                        │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────────┐
│                 Playwright Engine                            │
│            (Browser automation)                              │
└──────────────────────────────────────────────────────────────┘

         Plugins: Artifacts | Logging | Reporting
         Tools: TDS Client | Helpers | Utilities
```

---

## 📁 Project Structure

```
.
├── configs/                 # Configuration files
│   ├── __init__.py         # Config loader and settings
│   ├── config.yaml         # Environment configurations
│   └── pytest_cli.py       # Custom CLI options
│
├── fixtures/               # pytest fixtures
│   ├── __init__.py
│   ├── browser_fixtures.py # Browser, context, page fixtures
│   └── data_fixtures.py    # Test data fixtures
│
├── pages/                  # Page Object Model
│   ├── __init__.py
│   ├── base_page.py        # Base page class
│   ├── login_page.py       # Login page object
│   └── home_page.py        # Home page object
│
├── plugins/                # Custom pytest plugins
│   ├── __init__.py
│   ├── artifacts_plugin.py # Artifact management
│   └── logging_plugin.py   # Structured logging
│
├── tools/                  # Utilities and helpers
│   ├── __init__.py
│   ├── test_data_service.py # TDS client
│   └── helpers.py          # Helper functions
│
├── tests/                  # Test suites
│   ├── data/              # Test data files
│   │   └── users.json
│   ├── test_smoke.py      # Smoke tests
│   ├── test_regression.py # Regression tests
│   ├── test_mobile.py     # Mobile tests
│   └── test_e2e.py        # E2E tests
│
├── artifacts/              # Test artifacts (generated)
│   ├── screenshots/
│   ├── videos/
│   ├── traces/
│   └── logs/
│
├── reports/                # Test reports (generated)
│   ├── allure-results/
│   └── report.html
│
├── .github/
│   └── workflows/
│       └── test-automation.yml  # CI/CD workflow
│
├── conftest.py             # pytest configuration
├── pytest.ini              # pytest settings
├── pyproject.toml          # Project metadata
├── requirements.txt        # Dependencies
├── Dockerfile              # Docker image
├── docker-compose.yml      # Docker services
├── .env.example            # Environment variables template
├── .gitignore
└── README.md
```

---

## 📦 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git
- Docker (optional, for containerized execution)

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd py-playwright
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install
playwright install-deps  # Install system dependencies
```

### 5. Setup environment variables

```bash
cp .env.example .env
# Edit .env file with your configuration
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
ENV=dev                      # Environment: dev, staging, prod
BASE_URL=https://demo.playwright.dev/todomvc  # Base URL for tests
BROWSER=chromium             # Browser: chromium, firefox, webkit
HEADLESS=true                # Headless mode
PARALLEL_WORKERS=4           # Number of parallel workers
SCREENSHOT_ON_FAILURE=true   # Capture screenshots on failure
VIDEO_ON_FAILURE=true        # Record videos on failure
TRACE_ON_FAILURE=true        # Capture traces on failure
```

### YAML Configuration (configs/config.yaml)

Environment-specific settings, browser configurations, and device profiles.

### CLI Options

```bash
pytest \
  --browser=chromium \        # Browser selection
  --headless=true \           # Headless mode
  --device=iPhone_13 \        # Device emulation
  --env=staging \             # Environment
  --suite=smoke \             # Test suite
  --parallel=4 \              # Parallel workers
  --report=allure             # Report type
```

---

## 🎯 Usage

### Running Tests

#### Run all tests

```bash
pytest
```

#### Run specific test suite

```bash
# Smoke tests
pytest -m smoke

# Regression tests
pytest -m regression

# Mobile tests
pytest -m mobile

# E2E tests
pytest -m e2e
```

#### Run with specific browser

```bash
pytest --browser=chromium
pytest --browser=firefox
pytest --browser=webkit
```

#### Run in headless mode

```bash
pytest --headless=true
```

#### Run with device emulation

```bash
pytest --device=iPhone_13 -m mobile
pytest --device=Pixel_5 -m mobile
```

#### Run specific environment

```bash
pytest --env=staging
pytest --env=prod
```

#### Parallel execution

```bash
# Using pytest-xdist
pytest -n 4

# Using framework CLI option
pytest --parallel=4
```

#### Run specific test file

```bash
pytest tests/test_smoke.py
pytest tests/test_regression.py -v
```

#### Run specific test

```bash
pytest tests/test_smoke.py::TestLoginSmoke::test_successful_login
```

---

## 📊 Reporting

### Allure Reports

#### Generate and view Allure report

```bash
# Run tests with Allure
pytest --alluredir=reports/allure-results

# Generate report
allure generate reports/allure-results -o reports/allure-report --clean

# Open report
allure open reports/allure-report
```

### HTML Reports

HTML reports are generated automatically in `reports/report.html`

```bash
pytest --html=reports/report.html --self-contained-html
```

### Artifacts

Test artifacts are automatically saved in the `artifacts/` directory:

- **Screenshots**: Captured on test failure
- **Videos**: Recorded for failed tests
- **Traces**: Playwright traces for debugging
- **Logs**: Structured JSON logs

---

## 🔄 CI/CD Integration

### GitHub Actions

The framework includes a comprehensive GitHub Actions workflow (`.github/workflows/test-automation.yml`) that:

- Runs smoke tests on multiple OS (Ubuntu, Windows, macOS)
- Executes regression and mobile tests
- Generates and publishes Allure reports
- Uploads artifacts for each run
- Supports manual workflow dispatch with parameters

#### Trigger manually

```bash
# Via GitHub UI: Actions → UI Test Automation → Run workflow
# Select browser and suite
```

#### Scheduled runs

Tests run automatically daily at 2 AM UTC (configurable in workflow file)

---

## 🐳 Docker Support

### Build Docker image

```bash
docker build -t ui-automation-framework .
```

### Run tests in Docker

```bash
docker run --rm \
  -v $(pwd)/artifacts:/app/artifacts \
  -v $(pwd)/reports:/app/reports \
  ui-automation-framework
```

### Using Docker Compose

```bash
# Run all tests
docker-compose up test-runner

# Run specific browser tests
docker-compose up test-chromium
docker-compose up test-firefox
docker-compose up test-webkit

# Run mobile tests
docker-compose up test-mobile

# Start Allure report server
docker-compose up allure-report
# Access at http://localhost:5050
```

---

## 📝 Writing Tests

### Example Test

```python
import pytest
from pages.todo_page import TodoPage

@pytest.mark.smoke
def test_add_todo(page, base_url):
    """Test adding a single todo item."""
    todo_page = TodoPage(page)
    todo_page.navigate_to_todo_app(base_url)
    
    # Add a todo
    todo_page.add_todo("Buy groceries")
    
    # Verify todo is added
    assert todo_page.is_todo_visible("Buy groceries")
    assert todo_page.get_todo_count() == 1
```

### Test Coverage

The framework includes **comprehensive test coverage** for the **TodoMVC demo application**:

#### Smoke Tests (`test_todo_smoke.py`)
- ✅ Add single todo
- ✅ Complete todo
- ✅ Delete todo

#### Regression Tests (`test_todo_regression.py`)
- ✅ Add multiple todos
- ✅ Edit todo
- ✅ Toggle all todos
- ✅ Clear completed todos
- ✅ Filter active todos
- ✅ Filter completed todos
- ✅ Todo counter accuracy

#### E2E Tests (`test_todo_e2e.py`)
- ✅ Complete workflow (add, edit, complete, filter, delete)
- ✅ Empty state workflow
- ✅ Bulk operations workflow
- ✅ Edge cases (empty todos, long text, special characters)

### Creating Page Objects

```python
from pages.base_page import BasePage

class MyPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.my_element = "#my-selector"
    
    def click_element(self):
        self.click(self.my_element)
```

---

## 🎨 Best Practices

1. **Use Page Objects**: Encapsulate page interactions in page objects
2. **Meaningful Test Names**: Use descriptive test names
3. **Test Independence**: Each test should be independent
4. **Proper Markers**: Tag tests with appropriate markers (@pytest.mark.smoke)
5. **Fixtures for Setup**: Use fixtures for common setup/teardown
6. **Explicit Waits**: Use explicit waits instead of sleep
7. **Error Handling**: Handle expected errors gracefully
8. **Clean Test Data**: Use data fixtures or TDS for test data
9. **Assertions**: Use Playwright's built-in assertions
10. **Documentation**: Document complex test scenarios

---

## 🐛 Debugging

### Run tests with verbose output

```bash
pytest -v -s
```

### Run with Playwright inspector

```bash
PWDEBUG=1 pytest tests/test_smoke.py::test_name
```

### View traces

```bash
playwright show-trace artifacts/traces/trace.zip
```

### Check logs

```bash
cat artifacts/logs/test_execution_*.jsonl | jq
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Contact the test automation team
- Check documentation in `/docs`

---

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) - Browser automation
- [pytest](https://pytest.org/) - Testing framework
- [Allure](https://docs.qameta.io/allure/) - Test reporting

---

**Built with ❤️ by the Ivan Klymchuk**
