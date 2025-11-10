"""Shared fixtures - imported by conftest.py."""

from fixtures.browser_fixtures import (
    browser_type_launch_args,
    browser_context_args,
    context,
    page,
    authenticated_page,
    base_url,
    api_url,
)

from fixtures.data_fixtures import (
    test_data_dir,
    test_user,
    admin_user,
    load_test_data,
    sample_todos,
)

__all__ = [
    "browser_type_launch_args",
    "browser_context_args",
    "context",
    "page",
    "authenticated_page",
    "base_url",
    "api_url",
    "test_data_dir",
    "test_user",
    "admin_user",
    "load_test_data",
    "sample_todos",
]
