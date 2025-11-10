"""Pytest plugin for enhanced logging and observability."""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import pytest

from configs import get_settings


class StructuredLogger:
    """Structured JSON logger for test execution."""

    def __init__(self, log_path: Path, run_id: str):
        """Initialize structured logger."""
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.run_id = run_id
        
        # Setup file logger
        self.logger = logging.getLogger("test_framework")
        self.logger.setLevel(logging.INFO)
        
        # JSON file handler
        handler = logging.FileHandler(self.log_path)
        handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)

    def log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log a structured event."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "run_id": self.run_id,
            "event_type": event_type,
            **data
        }
        self.logger.info(json.dumps(log_entry))

    def log_test_start(self, test_id: str, test_name: str, markers: list) -> None:
        """Log test start event."""
        self.log_event("test_start", {
            "test_id": test_id,
            "test_name": test_name,
            "markers": markers
        })

    def log_test_end(self, test_id: str, test_name: str, outcome: str, duration: float) -> None:
        """Log test end event."""
        self.log_event("test_end", {
            "test_id": test_id,
            "test_name": test_name,
            "outcome": outcome,
            "duration": duration
        })

    def log_browser_console(self, test_id: str, message: Dict[str, Any]) -> None:
        """Log browser console message."""
        self.log_event("browser_console", {
            "test_id": test_id,
            **message
        })

    def log_network_event(self, test_id: str, event: Dict[str, Any]) -> None:
        """Log network event."""
        self.log_event("network_event", {
            "test_id": test_id,
            **event
        })


@pytest.fixture(scope="session")
def structured_logger() -> StructuredLogger:
    """Get structured logger instance."""
    settings = get_settings()
    artifacts_path = Path(settings.artifacts_path)
    logs_path = artifacts_path / "logs"
    logs_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_path / f"test_execution_{timestamp}.jsonl"
    
    return StructuredLogger(log_file, settings.run_id)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    """Hook to log test execution events."""
    structured_logger = None
    
    # Get structured logger if available
    if hasattr(item.config, "_structured_logger"):
        structured_logger = item.config._structured_logger
    
    # Log test start
    if structured_logger:
        test_id = item.nodeid
        test_name = item.name
        markers = [marker.name for marker in item.iter_markers()]
        structured_logger.log_test_start(test_id, test_name, markers)
    
    # Run test
    start_time = datetime.now()
    outcome = yield
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Log test end
    if structured_logger:
        # Determine outcome
        report = None
        if hasattr(item, "report_call"):
            report = item.report_call
        
        outcome_str = "passed"
        if report:
            if report.failed:
                outcome_str = "failed"
            elif report.skipped:
                outcome_str = "skipped"
        
        structured_logger.log_test_end(test_id, test_name, outcome_str, duration)


def pytest_configure(config):
    """Configure logging plugin."""
    settings = get_settings()
    artifacts_path = Path(settings.artifacts_path)
    logs_path = artifacts_path / "logs"
    logs_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_path / f"test_execution_{timestamp}.jsonl"
    
    # Store logger in config
    config._structured_logger = StructuredLogger(log_file, settings.run_id)


@pytest.fixture(scope="function")
def console_logger(page, structured_logger):
    """Fixture to capture browser console logs."""
    test_id = None
    
    def handle_console(msg):
        if test_id and structured_logger:
            structured_logger.log_browser_console(test_id, {
                "type": msg.type,
                "text": msg.text,
                "location": msg.location
            })
    
    # Attach console handler
    page.on("console", handle_console)
    
    yield
    
    # Clean up
    page.remove_listener("console", handle_console)
