"""Test data fixtures and utilities."""

import pytest
from typing import Dict, Any, Optional
from pathlib import Path
import json


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Get test data directory path."""
    return Path(__file__).parent.parent / "tests" / "data"


@pytest.fixture(scope="function")
def test_user(load_test_data) -> Dict[str, Any]:
    """Provide a test user data from JSON."""
    data = load_test_data("users.json")
    users = data.get("users", [])
    if not users:
        raise ValueError("No users found in users.json")
    # Return the first user
    return users[0]


@pytest.fixture(scope="function")
def admin_user(load_test_data) -> Dict[str, Any]:
    """Provide an admin user data from JSON."""
    data = load_test_data("users.json")
    users = data.get("users", [])
    admin_users = [u for u in users if u.get("role") == "admin"]
    if not admin_users:
        raise ValueError("No admin users found in users.json")
    return admin_users[0]


@pytest.fixture(scope="function")
def load_test_data(test_data_dir: Path):
    """Factory fixture to load test data from JSON files."""
    def _load(filename: str) -> Dict[str, Any]:
        """Load test data from JSON file."""
        file_path = test_data_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Test data file not found: {file_path}")
        
        with open(file_path, "r") as f:
            return json.load(f)
    
    return _load


@pytest.fixture(scope="function")
def sample_todos(load_test_data) -> list:
    """Provide sample todo data from JSON."""
    data = load_test_data("todos.json")
    return data.get("todos", [])
