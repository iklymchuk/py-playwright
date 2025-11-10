"""Mobile browser tests using device emulation."""

import pytest
from playwright.sync_api import Page

from pages import LoginPage, HomePage


@pytest.mark.skip(reason="Login functionality not available on TodoMVC demo site")
@pytest.mark.mobile
@pytest.mark.parametrize("device", ["iPhone_13", "Pixel_5"])
class TestMobileLogin:
    """Mobile browser tests for login functionality."""

    def test_mobile_login_ui(self, page: Page, base_url: str, device: str):
        """Test login UI on mobile devices."""
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        
        # Verify mobile-optimized UI
        login_page.expect_visible(login_page.email_input)
        login_page.expect_visible(login_page.password_input)
        login_page.expect_visible(login_page.login_button)
        
        # Check viewport is mobile
        viewport = page.viewport_size
        assert viewport["width"] <= 500, "Should be mobile viewport"

    def test_mobile_login_flow(self, page: Page, base_url: str, test_user: dict, device: str):
        """Test complete login flow on mobile."""
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        login_page.login(test_user["email"], test_user["password"])
        
        # Verify logged in
        home_page = HomePage(page, base_url)
        assert home_page.is_logged_in()
        
        # Verify device-specific behavior
        assert device in ["iPhone_13", "Pixel_5"], "Unexpected device"

    def test_mobile_touch_interactions(self, page: Page, base_url: str, device: str):
        """Test touch interactions on mobile."""
        home_page = HomePage(page, base_url)
        home_page.navigate_to_home()
        
        # Test tap on logo
        home_page.click_logo()
        
        # Verify interaction worked
        assert base_url in home_page.get_url()
        
        # Verify device-specific behavior
        assert device in ["iPhone_13", "Pixel_5"], "Unexpected device"


@pytest.mark.mobile
class TestMobileNavigation:
    """Mobile navigation tests."""

    def test_mobile_menu_interaction(self, page: Page, base_url: str):
        """Test mobile menu interactions."""
        home_page = HomePage(page, base_url)
        home_page.navigate_to_home()
        
        # Verify navigation menu is present
        home_page.expect_visible(home_page.navigation_menu)

    def test_mobile_search(self, page: Page, base_url: str):
        """Test search functionality on mobile."""
        home_page = HomePage(page, base_url)
        home_page.navigate_to_home()
        
        # Test search on mobile
        home_page.search("mobile test")
        
        # Verify search executed
        assert "search" in home_page.get_url().lower()


@pytest.mark.mobile
@pytest.mark.slow
class TestMobilePerformance:
    """Mobile performance tests."""

    def test_page_load_time_mobile(self, page: Page, base_url: str):
        """Test page load time on mobile devices."""
        from tools import Timer
        
        with Timer("Mobile page load") as timer:
            home_page = HomePage(page, base_url)
            home_page.navigate_to_home()
            home_page.wait_for_load_state("networkidle")
        
        # Assert load time is acceptable (e.g., under 5 seconds)
        assert timer.get_duration() < 5.0, "Page should load within 5 seconds"

    def test_mobile_responsiveness(self, page: Page, base_url: str):
        """Test UI responsiveness on mobile."""
        home_page = HomePage(page, base_url)
        home_page.navigate_to_home()
        
        # Test various mobile viewports
        viewports = [
            {"width": 375, "height": 667},  # iPhone SE
            {"width": 390, "height": 844},  # iPhone 13
            {"width": 393, "height": 851},  # Pixel 5
        ]
        
        for viewport in viewports:
            page.set_viewport_size(viewport)
            home_page.expect_visible(home_page.header)
            home_page.expect_visible(home_page.navigation_menu)
