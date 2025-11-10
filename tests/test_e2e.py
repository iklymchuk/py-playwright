"""End-to-end test scenarios."""

import pytest
from playwright.sync_api import Page

from pages import LoginPage, HomePage
from tools import DataGenerator


@pytest.mark.skip(reason="Login functionality not available on TodoMVC demo site")
@pytest.mark.e2e
@pytest.mark.slow
class TestUserJourney:
    """End-to-end user journey tests."""

    def test_complete_user_registration_and_login_flow(
        self, 
        page: Page, 
        base_url: str
    ):
        """Test complete user journey from registration to login."""
        # Generate test user data
        data_gen = DataGenerator()
        user_data = data_gen.generate_user()
        
        # Step 1: Navigate to home page
        home_page = HomePage(page, base_url)
        home_page.navigate_to_home()
        home_page.expect_home_page_loaded()
        
        # Step 2: Navigate to login page
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        login_page.expect_login_page_loaded()
        
        # Step 3: Click signup link
        login_page.click_signup()
        
        # Note: Would continue with registration flow
        # This is a demonstration of E2E test structure

    def test_user_login_search_logout_flow(
        self, 
        page: Page, 
        base_url: str,
        test_user: dict
    ):
        """Test complete user flow: login -> search -> logout."""
        # Step 1: Login
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        login_page.login(test_user["email"], test_user["password"])
        
        # Step 2: Verify logged in
        home_page = HomePage(page, base_url)
        assert home_page.is_logged_in()
        
        # Step 3: Perform search
        home_page.search("test product")
        
        # Step 4: Navigate back to home
        home_page.navigate_to_home()
        
        # Step 5: Logout
        home_page.logout()
        
        # Step 6: Verify logged out
        assert not home_page.is_logged_in()


@pytest.mark.skip(reason="Login functionality not available on TodoMVC demo site")
@pytest.mark.e2e
class TestCrossBrowserE2E:
    """Cross-browser end-to-end tests."""

    def test_login_flow_all_browsers(
        self, 
        page: Page, 
        base_url: str,
        test_user: dict
    ):
        """Test login flow across all browsers."""
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        login_page.login(test_user["email"], test_user["password"])
        
        home_page = HomePage(page)
        home_page.expect_home_page_loaded()
        assert home_page.is_logged_in()


@pytest.mark.skip(reason="Login functionality not available on TodoMVC demo site")
@pytest.mark.e2e
@pytest.mark.slow
class TestMultiStepWorkflow:
    """Multi-step workflow tests."""

    def test_complex_workflow_with_multiple_pages(
        self,
        page: Page,
        base_url: str,
        test_user: dict
    ):
        """Test complex workflow spanning multiple pages."""
        from tools import Timer
        
        with Timer("E2E workflow") as timer:
            # Step 1: Home page
            home_page = HomePage(page, base_url)
            home_page.navigate_to_home()
            
            # Step 2: Login
            login_page = LoginPage(page)
            login_page.navigate_to_login(base_url)
            login_page.login(test_user["email"], test_user["password"])
            
            # Step 3: Return to home
            home_page.navigate_to_home()
            assert home_page.is_logged_in()
            
            # Step 4: Perform actions
            home_page.search("test query")
            
            # Step 5: Logout
            home_page.logout()
        
        print(f"Complete E2E workflow took {timer.get_duration():.2f} seconds")
        assert timer.get_duration() < 30.0, "E2E flow should complete within 30 seconds"
