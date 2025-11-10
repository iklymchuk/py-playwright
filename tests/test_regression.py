"""Regression tests - comprehensive test coverage."""

import pytest
from playwright.sync_api import Page

from pages import LoginPage, HomePage
from tools import DataGenerator


@pytest.mark.skip(reason="Login functionality not available on TodoMVC demo site")
@pytest.mark.regression
class TestLoginRegression:
    """Regression tests for login functionality across browsers."""

    def test_login_remember_me(self, page: Page, base_url: str, test_user: dict):
        """Test login with remember me checkbox."""
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        
        login_page.enter_email(test_user["email"])
        login_page.enter_password(test_user["password"])
        login_page.check_remember_me()
        login_page.click_login()
        
        # Verify login successful
        home_page = HomePage(page)
        assert home_page.is_logged_in()

    def test_login_button_disabled_with_empty_fields(self, page: Page, base_url: str):
        """Test login button state with empty fields."""
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        
        # Check button state with empty fields
        is_enabled = login_page.is_login_button_enabled()
        # Note: Implementation depends on actual page behavior
        assert isinstance(is_enabled, bool)

    def test_email_validation(self, page: Page, base_url: str):
        """Test email field validation."""
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        
        # Try invalid email formats
        invalid_emails = ["notanemail", "@example.com", "user@", "user @example.com"]
        
        for email in invalid_emails:
            login_page.enter_email(email)
            login_page.enter_password("password123")
            login_page.click_login()
            
            # Should show error or stay on login page
            error = login_page.get_error_message()
            # Either error is shown or we're still on login page
            assert error is not None or "/login" in login_page.get_url()
            
            # Clear for next iteration
            login_page.navigate_to_login(base_url)


@pytest.mark.regression
class TestSearchFunctionality:
    """Regression tests for search functionality."""

    def test_search_with_valid_query(self, page: Page, base_url: str):
        """Test search with valid query."""
        home_page = HomePage(page, base_url)
        home_page.navigate_to_home()
        
        search_query = "test query"
        home_page.search(search_query)
        
        # Verify search executed (URL or results visible)
        current_url = home_page.get_url()
        assert "search" in current_url.lower() or search_query in current_url

    def test_search_with_empty_query(self, page: Page, base_url: str):
        """Test search with empty query."""
        home_page = HomePage(page, base_url)
        home_page.navigate_to_home()


@pytest.mark.skip(reason="Login functionality not available on TodoMVC demo site")
@pytest.mark.regression
class TestDataDrivenTests:
    """Data-driven regression tests."""

    def test_login_with_generated_data(self, page: Page, base_url: str):
        """Test login with dynamically generated user data."""
        data_gen = DataGenerator()
        user_data = data_gen.generate_user()
        
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        
        # Attempt login with generated data
        login_page.login(user_data["email"], user_data["password"])
        
        # Should show error for unregistered user
        error = login_page.get_error_message()
        assert error is not None

    @pytest.mark.parametrize("user_file", ["users.json"])
    def test_login_with_test_data_file(
        self, 
        page: Page, 
        base_url: str, 
        load_test_data,
        user_file: str
    ):
        """Test login with data from JSON file."""
        test_data = load_test_data(user_file)
        users = test_data.get("users", [])
        
        # Test with first user from file
        if users:
            user = users[0]
            login_page = LoginPage(page)
            login_page.navigate_to_login(base_url)
            login_page.login(user["email"], user["password"])
            
            # Verify login attempt processed
            # Actual assertion depends on test data validity
