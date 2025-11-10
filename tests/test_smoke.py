"""Smoke tests - critical path scenarios."""

import pytest
from playwright.sync_api import Page, expect

from pages import LoginPage, HomePage


@pytest.mark.skip(reason="Login functionality not available on TodoMVC demo site")
@pytest.mark.smoke
@pytest.mark.chromium
class TestLoginSmoke:
    """Smoke tests for login functionality."""

    def test_successful_login(self, page: Page, base_url: str, test_user: dict):
        """Test successful login with valid credentials."""
        # Arrange
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        login_page.expect_login_page_loaded()
        
        # Act
        login_page.login(test_user["email"], test_user["password"])
        
        # Assert
        home_page = HomePage(page, base_url)
        home_page.expect_home_page_loaded()
        assert home_page.is_logged_in(), "User should be logged in"

    def test_login_with_invalid_credentials(self, page: Page, base_url: str):
        """Test login with invalid credentials shows error."""
        # Arrange
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        
        # Act
        login_page.login("invalid@example.com", "wrongpassword")
        
        # Assert
        error_message = login_page.get_error_message()
        assert error_message is not None, "Error message should be displayed"
        assert "invalid" in error_message.lower() or "incorrect" in error_message.lower()

    def test_login_page_elements_visible(self, page: Page, base_url: str):
        """Test all login page elements are visible."""
        # Arrange
        login_page = LoginPage(page)
        
        # Act
        login_page.navigate_to_login(base_url)
        
        # Assert
        login_page.expect_visible(login_page.email_input)
        login_page.expect_visible(login_page.password_input)
        login_page.expect_visible(login_page.login_button)
        login_page.expect_visible(login_page.forgot_password_link)


@pytest.mark.smoke
@pytest.mark.chromium
class TestNavigationSmoke:
    """Smoke tests for basic navigation."""

    def test_home_page_loads(self, page: Page, base_url: str):
        """Test home page loads successfully."""
        # Arrange
        home_page = HomePage(page, base_url)
        
        # Act
        home_page.navigate_to_home()
        
        # Assert
        home_page.expect_home_page_loaded()
        assert base_url in home_page.get_url()

    def test_logo_click_returns_home(self, page: Page, base_url: str):
        """Test clicking logo returns to home page."""
        # Arrange
        home_page = HomePage(page, base_url)
        home_page.navigate_to_home()
        
        # Navigate away
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        
        # Act
        home_page.click_logo()
        
        # Assert
        assert home_page.get_url().startswith(base_url)
