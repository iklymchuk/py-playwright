"""Example page object for login functionality."""

from typing import Optional
from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for Login page."""

    def __init__(self, page: Page):
        """Initialize login page."""
        super().__init__(page)
        
        # Locators
        self.email_input = "input.new-todo"
        self.password_input = "input.new-todo"
        self.login_button = "input.new-todo"
        self.error_message = ".error-message"
        self.forgot_password_link = "a[href*='forgot-password']"
        self.signup_link = "a[href*='signup']"
        self.remember_me_checkbox = "#remember-me"

    def navigate_to_login(self, base_url: str) -> None:
        """Navigate to login page."""
        self.navigate(f"{base_url}/login")
        self.wait_for_load_state()

    def enter_email(self, email: str) -> None:
        """Enter email address."""
        self.fill(self.email_input, email)

    def enter_password(self, password: str) -> None:
        """Enter password."""
        self.fill(self.password_input, password)

    def click_login(self) -> None:
        """Click login button."""
        self.click(self.login_button)

    def check_remember_me(self) -> None:
        """Check remember me checkbox."""
        self.check(self.remember_me_checkbox)

    def login(self, email: str, password: str, remember_me: bool = False) -> None:
        """Perform login with credentials."""
        self.enter_email(email)
        self.enter_password(password)
        
        if remember_me:
            self.check_remember_me()
        
        self.click_login()

    def get_error_message(self) -> Optional[str]:
        """Get error message text."""
        if self.is_visible(self.error_message, timeout=5000):
            return self.get_text(self.error_message)
        return None

    def click_forgot_password(self) -> None:
        """Click forgot password link."""
        self.click(self.forgot_password_link)

    def click_signup(self) -> None:
        """Click signup link."""
        self.click(self.signup_link)

    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled."""
        return self.is_enabled(self.login_button)

    def expect_login_page_loaded(self) -> None:
        """Assert login page is loaded."""
        self.expect_visible(self.email_input)
        self.expect_visible(self.password_input)
        self.expect_visible(self.login_button)
