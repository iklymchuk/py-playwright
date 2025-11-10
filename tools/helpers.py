"""Utility functions and helpers."""

import os
import json
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(file_path: Path) -> Dict[str, Any]:
    """Read JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)


def write_json(file_path: Path, data: Dict[str, Any], indent: int = 2) -> None:
    """Write JSON file."""
    ensure_dir(file_path.parent)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=indent)


def get_timestamp(format: str = "%Y%m%d_%H%M%S") -> str:
    """Get formatted timestamp."""
    return datetime.now().strftime(format)


def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
    """Mask sensitive data, showing only last N characters."""
    if len(data) <= visible_chars:
        return "*" * len(data)
    return "*" * (len(data) - visible_chars) + data[-visible_chars:]


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename


def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable with optional default."""
    return os.getenv(key, default)


def parse_bool(value: Any) -> bool:
    """Parse boolean value from string."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "on")
    return bool(value)


class Timer:
    """Context manager for timing code execution."""

    def __init__(self, name: str = ""):
        """Initialize timer."""
        self.name = name
        self.start_time = None
        self.end_time = None
        self.duration = None

    def __enter__(self):
        """Start timer."""
        self.start_time = datetime.now()
        return self

    def __exit__(self, *args):
        """Stop timer and calculate duration."""
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        
        if self.name:
            print(f"{self.name} took {self.duration:.2f} seconds")

    def get_duration(self) -> float:
        """Get duration in seconds."""
        return self.duration if self.duration else 0.0
