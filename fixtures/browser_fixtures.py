"""Core pytest fixtures for browser and context management."""

import pytest
from pathlib import Path
from typing import Generator, Dict, Any
from playwright.sync_api import Browser, BrowserContext, Page, Playwright

from configs import get_settings, get_config_loader


@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig: pytest.Config) -> Dict[str, Any]:
    """Get browser launch arguments based on configuration."""
    settings = get_settings()
    config_loader = get_config_loader()
    
    browser_name = pytestconfig.option.browser_name
    browser_config = config_loader.get_browser_config(browser_name)
    
    launch_args = {
        "headless": pytestconfig.option.headless_mode,
        "slow_mo": settings.slow_mo,
    }
    
    if browser_config.get("args"):
        launch_args["args"] = browser_config["args"]
    
    return launch_args


@pytest.fixture(scope="session")
def browser_context_args(pytestconfig: pytest.Config) -> Dict[str, Any]:
    """Get browser context arguments based on configuration."""
    settings = get_settings()
    config_loader = get_config_loader()
    
    context_args = {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": None,
        "record_har_path": None,
    }
    
    # Device emulation
    device_name = pytestconfig.option.device_name
    if device_name:
        device_config = config_loader.get_device_config(device_name)
        if device_config:
            if "viewport" in device_config:
                context_args["viewport"] = device_config["viewport"]
            if "user_agent" in device_config:
                context_args["user_agent"] = device_config["user_agent"]
            if "device_scale_factor" in device_config:
                context_args["device_scale_factor"] = device_config["device_scale_factor"]
            if "is_mobile" in device_config:
                context_args["is_mobile"] = device_config["is_mobile"]
            if "has_touch" in device_config:
                context_args["has_touch"] = device_config["has_touch"]
    else:
        # Browser-specific viewport
        browser_name = pytestconfig.option.browser_name
        browser_config = config_loader.get_browser_config(browser_name)
        if "viewport" in browser_config:
            context_args["viewport"] = browser_config["viewport"]
    
    # Video recording on failure
    if settings.video_on_failure:
        artifacts_path = Path(settings.artifacts_path)
        artifacts_path.mkdir(parents=True, exist_ok=True)
        context_args["record_video_dir"] = str(artifacts_path / "videos")
    
    return context_args


@pytest.fixture(scope="function")
def context(
    browser: Browser,
    browser_context_args: Dict[str, Any],
    pytestconfig: pytest.Config
) -> Generator[BrowserContext, None, None]:
    """Create a new browser context for each test."""
    settings = get_settings()
    
    # Add tracing if enabled
    ctx = browser.new_context(**browser_context_args)
    
    if settings.trace_on_failure:
        ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    yield ctx
    
    # Save trace on failure
    if settings.trace_on_failure:
        artifacts_path = Path(settings.artifacts_path)
        artifacts_path.mkdir(parents=True, exist_ok=True)
        trace_path = artifacts_path / "traces" / f"{pytestconfig.option.run_id}_trace.zip"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        ctx.tracing.stop(path=str(trace_path))
    
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Create a new page for each test."""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def authenticated_page(page: Page) -> Generator[Page, None, None]:
    """Create an authenticated page session."""
    # This is a placeholder - implement your authentication logic
    # Example: navigate to login page, fill credentials, submit
    # For demo purposes, we'll just return the page
    yield page


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    """Get base URL for the current environment."""
    from configs import get_base_url
    env = pytestconfig.option.environment
    return get_base_url(env)


@pytest.fixture(scope="session")
def api_url(pytestconfig: pytest.Config) -> str:
    """Get API URL for the current environment."""
    from configs import get_api_url
    env = pytestconfig.option.environment
    return get_api_url(env)
