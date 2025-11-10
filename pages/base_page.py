"""Base Page Object class with common methods."""

from typing import Optional, List
from playwright.sync_api import Page, Locator, expect
from pathlib import Path


class BasePage:
    """Base class for all Page Objects."""

    def __init__(self, page: Page):
        """Initialize base page."""
        self.page = page
        self.timeout = 30000

    def navigate(self, url: str) -> None:
        """Navigate to URL."""
        self.page.goto(url, timeout=self.timeout)

    def wait_for_load_state(self, state: str = "load") -> None:
        """Wait for page load state."""
        self.page.wait_for_load_state(state)

    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Get current URL."""
        return self.page.url

    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """Click element by selector."""
        timeout = timeout or self.timeout
        self.page.click(selector, timeout=timeout)

    def fill(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """Fill input field."""
        timeout = timeout or self.timeout
        self.page.fill(selector, value, timeout=timeout)

    def type(self, selector: str, text: str, delay: int = 0) -> None:
        """Type text into element."""
        self.page.type(selector, text, delay=delay)

    def select_option(self, selector: str, value: str) -> None:
        """Select option from dropdown."""
        self.page.select_option(selector, value)

    def check(self, selector: str) -> None:
        """Check checkbox or radio button."""
        self.page.check(selector)

    def uncheck(self, selector: str) -> None:
        """Uncheck checkbox."""
        self.page.uncheck(selector)

    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Check if element is visible."""
        timeout = timeout or self.timeout
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def is_hidden(self, selector: str) -> bool:
        """Check if element is hidden."""
        return self.page.is_hidden(selector)

    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled."""
        return self.page.is_enabled(selector)

    def is_checked(self, selector: str) -> bool:
        """Check if checkbox/radio is checked."""
        return self.page.is_checked(selector)

    def get_text(self, selector: str) -> str:
        """Get element text content."""
        return self.page.text_content(selector)

    def get_inner_text(self, selector: str) -> str:
        """Get element inner text."""
        return self.page.inner_text(selector)

    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """Get element attribute value."""
        return self.page.get_attribute(selector, attribute)

    def get_element(self, selector: str) -> Locator:
        """Get element locator."""
        return self.page.locator(selector)

    def get_elements(self, selector: str) -> List[Locator]:
        """Get all matching elements."""
        return self.page.locator(selector).all()

    def wait_for_selector(
        self, 
        selector: str, 
        state: str = "visible",
        timeout: Optional[int] = None
    ) -> None:
        """Wait for selector to be in specific state."""
        timeout = timeout or self.timeout
        self.page.wait_for_selector(selector, state=state, timeout=timeout)

    def wait_for_url(self, url: str, timeout: Optional[int] = None) -> None:
        """Wait for URL to match."""
        timeout = timeout or self.timeout
        self.page.wait_for_url(url, timeout=timeout)

    def wait_for_timeout(self, timeout: int) -> None:
        """Wait for specific timeout."""
        self.page.wait_for_timeout(timeout)

    def screenshot(self, path: Optional[Path] = None, full_page: bool = True) -> bytes:
        """Take screenshot."""
        if path:
            return self.page.screenshot(path=str(path), full_page=full_page)
        return self.page.screenshot(full_page=full_page)

    def press_key(self, selector: str, key: str) -> None:
        """Press keyboard key on element."""
        self.page.press(selector, key)

    def hover(self, selector: str) -> None:
        """Hover over element."""
        self.page.hover(selector)

    def scroll_to(self, selector: str) -> None:
        """Scroll to element."""
        self.page.locator(selector).scroll_into_view_if_needed()

    def execute_script(self, script: str, *args) -> any:
        """Execute JavaScript."""
        return self.page.evaluate(script, *args)

    def reload(self) -> None:
        """Reload page."""
        self.page.reload()

    def go_back(self) -> None:
        """Navigate back."""
        self.page.go_back()

    def go_forward(self) -> None:
        """Navigate forward."""
        self.page.go_forward()

    def expect_visible(self, selector: str) -> None:
        """Assert element is visible."""
        expect(self.page.locator(selector)).to_be_visible()

    def expect_hidden(self, selector: str) -> None:
        """Assert element is hidden."""
        expect(self.page.locator(selector)).to_be_hidden()

    def expect_enabled(self, selector: str) -> None:
        """Assert element is enabled."""
        expect(self.page.locator(selector)).to_be_enabled()

    def expect_text(self, selector: str, text: str) -> None:
        """Assert element has text."""
        expect(self.page.locator(selector)).to_have_text(text)

    def expect_url(self, url: str) -> None:
        """Assert page URL."""
        expect(self.page).to_have_url(url)

    def expect_title(self, title: str) -> None:
        """Assert page title."""
        expect(self.page).to_have_title(title)
