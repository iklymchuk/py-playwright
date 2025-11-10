"""Main conftest.py for pytest configuration."""

import pytest
from pathlib import Path

# Import fixtures
from fixtures import *
from plugins import *

# Import custom CLI options
from configs.pytest_cli import pytest_addoption, pytest_configure


# Hook imports are handled by the plugin modules
pytest_plugins = [
    "plugins.artifacts_plugin",
    "plugins.logging_plugin",
]


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment(request):
    """Setup test environment before all tests."""
    from configs import get_settings
    
    settings = get_settings()
    
    # Create required directories
    artifacts_path = Path(settings.artifacts_path)
    artifacts_path.mkdir(parents=True, exist_ok=True)
    
    reports_path = Path(settings.reports_path)
    reports_path.mkdir(parents=True, exist_ok=True)
    
    # Print configuration
    print("\n" + "="*80)
    print("Test Execution Configuration")
    print("="*80)
    print(f"Environment: {settings.env}")
    print(f"Browser: {request.config.option.browser_name}")
    print(f"Headless: {request.config.option.headless_mode}")
    print(f"Base URL: {settings.base_url}")
    print(f"Artifacts Path: {settings.artifacts_path}")
    print(f"Reports Path: {settings.reports_path}")
    print("="*80 + "\n")
    
    yield
    
    # Cleanup after all tests
    print("\n" + "="*80)
    print("Test Execution Complete")
    print("="*80)
