"""Example page object for home page."""

from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for Home page."""

    def __init__(self, page: Page, base_url: str):
        """Initialize home page."""
        super().__init__(page)
        self.base_url = base_url
        
        # Locators
        self.header = "h1"
        self.logo = "h1"
        self.navigation_menu = "footer"
        self.search_input = "input.new-todo"
        self.search_button = "button"  # Assuming there's a button, but TodoMVC doesn't have search
        self.user_profile = ".user-profile"  # Not on TodoMVC
        self.logout_button = "button:has-text('Logout')"  # Not on TodoMVC
        self.welcome_message = ".welcome-message"  # Not on TodoMVC

    def navigate_to_home(self) -> None:
        """Navigate to home page."""
        self.navigate(self.base_url)
        self.wait_for_load_state()

    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        return self.is_visible(self.user_profile, timeout=5000)

    def get_welcome_message(self) -> str:
        """Get welcome message text."""
        return self.get_text(self.welcome_message)

    def search(self, query: str) -> None:
        """Perform search."""
        self.fill(self.search_input, query)
        self.click(self.search_button)

    def logout(self) -> None:
        """Logout user."""
        self.click(self.user_profile)
        self.click(self.logout_button)

    def click_logo(self) -> None:
        """Click on logo and wait for home page to load."""
        self.navigate(self.base_url)

    def expect_home_page_loaded(self) -> None:
        """Assert home page is loaded."""
        self.expect_visible(self.header)
        self.expect_visible(self.navigation_menu)
