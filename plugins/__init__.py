"""Custom pytest plugins for the framework."""

from plugins.artifacts_plugin import artifact_manager, pytest_runtest_makereport
from plugins.logging_plugin import structured_logger, console_logger

__all__ = [
    "artifact_manager",
    "pytest_runtest_makereport",
    "structured_logger",
    "console_logger",
]
