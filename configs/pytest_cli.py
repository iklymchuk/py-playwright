"""Custom pytest command line options."""

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command line options."""
    parser.addoption(
        "--custom-browser",
        action="store",
        default="chromium",
        help="Browser to use: chromium, firefox, webkit",
        choices=["chromium", "firefox", "webkit"]
    )
    parser.addoption(
        "--headless",
        action="store",
        default="true",
        help="Run browser in headless mode: true, false"
    )
    parser.addoption(
        "--custom-device",
        action="store",
        default=None,
        help="Device emulation: iPhone_13, Pixel_5, etc."
    )
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment: dev, staging, prod"
    )
    parser.addoption(
        "--suite",
        action="store",
        default=None,
        help="Test suite: smoke, regression, e2e"
    )
    parser.addoption(
        "--parallel",
        action="store",
        default="1",
        help="Number of parallel workers"
    )
    parser.addoption(
        "--report",
        action="store",
        default="allure",
        help="Report type: allure, html, both"
    )
    parser.addoption(
        "--run-id",
        action="store",
        default="local-run",
        help="Unique identifier for the test run"
    )


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest based on command line options."""
    # Store config options for global access
    config.option.browser_name = config.getoption("--custom-browser")
    config.option.headless_mode = config.getoption("--headless").lower() == "true"
    config.option.device_name = config.getoption("--custom-device")
    config.option.environment = config.getoption("--env")
    config.option.test_suite = config.getoption("--suite")
    config.option.parallel_workers = int(config.getoption("--parallel"))
    config.option.report_type = config.getoption("--report")
    config.option.run_id = config.getoption("--run-id")
