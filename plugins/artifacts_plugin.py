"""Pytest plugin for artifact management and collection."""

import pytest
from pathlib import Path
from datetime import datetime
from typing import Optional

from configs import get_settings


class ArtifactManager:
    """Manage test artifacts (screenshots, videos, traces)."""

    def __init__(self, artifacts_path: Path):
        """Initialize artifact manager."""
        self.artifacts_path = artifacts_path
        self.artifacts_path.mkdir(parents=True, exist_ok=True)
        
        self.screenshots_path = self.artifacts_path / "screenshots"
        self.screenshots_path.mkdir(parents=True, exist_ok=True)
        
        self.videos_path = self.artifacts_path / "videos"
        self.videos_path.mkdir(parents=True, exist_ok=True)
        
        self.traces_path = self.artifacts_path / "traces"
        self.traces_path.mkdir(parents=True, exist_ok=True)

    def save_screenshot(self, page, test_name: str, suffix: str = "") -> Path:
        """Save screenshot for a test."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}{suffix}.png"
        screenshot_path = self.screenshots_path / filename
        
        try:
            page.screenshot(path=str(screenshot_path), full_page=True)
            return screenshot_path
        except Exception as e:
            print(f"Failed to save screenshot: {e}")
            return None

    def get_test_artifacts(self, test_name: str) -> dict:
        """Get all artifacts for a specific test."""
        artifacts = {
            "screenshots": [],
            "videos": [],
            "traces": []
        }
        
        # Find screenshots
        for screenshot in self.screenshots_path.glob(f"{test_name}_*.png"):
            artifacts["screenshots"].append(str(screenshot))
        
        # Find videos
        for video in self.videos_path.glob(f"{test_name}_*.webm"):
            artifacts["videos"].append(str(video))
        
        # Find traces
        for trace in self.traces_path.glob(f"{test_name}_*.zip"):
            artifacts["traces"].append(str(trace))
        
        return artifacts


@pytest.fixture(scope="session")
def artifact_manager() -> ArtifactManager:
    """Get artifact manager instance."""
    settings = get_settings()
    artifacts_path = Path(settings.artifacts_path)
    return ArtifactManager(artifacts_path)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result and save artifacts on failure."""
    outcome = yield
    report = outcome.get_result()
    
    # Only process test call (not setup or teardown)
    if report.when == "call":
        # Store test result for later use
        setattr(item, f"report_{report.when}", report)
        
        # Save screenshot on failure
        if report.failed:
            settings = get_settings()
            if settings.screenshot_on_failure:
                try:
                    # Get page fixture if available
                    page = item.funcargs.get("page")
                    if page:
                        artifact_manager = item.funcargs.get("artifact_manager")
                        if artifact_manager:
                            test_name = item.nodeid.replace("::", "_").replace("/", "_")
                            screenshot_path = artifact_manager.save_screenshot(
                                page, test_name, "_failure"
                            )
                            if screenshot_path:
                                # Attach to Allure report
                                try:
                                    import allure
                                    allure.attach.file(
                                        str(screenshot_path),
                                        name="Failure Screenshot",
                                        attachment_type=allure.attachment_type.PNG
                                    )
                                except ImportError:
                                    pass
                except Exception as e:
                    print(f"Failed to capture failure screenshot: {e}")


def pytest_configure(config):
    """Configure plugin."""
    config.addinivalue_line(
        "markers", "artifacts: mark test to collect specific artifacts"
    )
