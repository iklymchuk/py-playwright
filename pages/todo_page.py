"""Page Object for TodoMVC application."""

from typing import List
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class TodoPage(BasePage):
    """Page Object for TodoMVC application."""

    def __init__(self, page: Page):
        """Initialize TodoMVC page."""
        super().__init__(page)
        
        # Locators
        self.new_todo_input = ".new-todo"
        self.todo_list = ".todo-list"
        self.todo_items = ".todo-list li"
        self.todo_item = lambda text: f".todo-list li:has-text('{text}')"
        self.todo_checkbox = lambda text: f".todo-list li:has-text('{text}') .toggle"
        self.todo_delete_button = lambda text: f".todo-list li:has-text('{text}') .destroy"
        self.todo_edit_input = ".todo-list li.editing .edit"
        self.todo_count = ".todo-count"
        self.clear_completed_button = ".clear-completed"
        self.toggle_all_checkbox = ".toggle-all"
        
        # Filters
        self.filter_all = "a[href='#/']"
        self.filter_active = "a[href='#/active']"
        self.filter_completed = "a[href='#/completed']"

    def navigate_to_todo_app(self, base_url: str = None) -> None:
        """Navigate to TodoMVC page."""
        url = base_url if base_url else "https://demo.playwright.dev/todomvc"
        self.navigate(url)
        self.wait_for_load_state("networkidle")

    def add_todo(self, text: str) -> None:
        """Add a new todo item."""
        self.fill(self.new_todo_input, text)
        self.press_key(self.new_todo_input, "Enter")

    def add_multiple_todos(self, todos: List[str]) -> None:
        """Add multiple todo items."""
        for todo in todos:
            self.add_todo(todo)

    def get_todo_count(self) -> int:
        """Get count of todo items."""
        items = self.page.locator(self.todo_items).all()
        return len(items)

    def get_active_count(self) -> int:
        """Get count of active todo items from the counter."""
        if self.is_visible(self.todo_count, timeout=2000):
            count_text = self.get_text(self.todo_count)
            # Extract number from "X item(s) left"
            import re
            match = re.search(r'(\d+)', count_text)
            return int(match.group(1)) if match else 0
        return 0

    def complete_todo(self, text: str) -> None:
        """Mark a todo as completed."""
        self.click(self.todo_checkbox(text))

    def delete_todo(self, text: str) -> None:
        """Delete a todo item."""
        # Hover to make delete button visible
        self.hover(self.todo_item(text))
        self.click(self.todo_delete_button(text))

    def edit_todo(self, old_text: str, new_text: str) -> None:
        """Edit a todo item."""
        # Double click to enter edit mode
        self.page.locator(self.todo_item(old_text)).dblclick()
        self.wait_for_selector(self.todo_edit_input)
        
        # Clear and enter new text
        self.page.locator(self.todo_edit_input).fill("")
        self.page.locator(self.todo_edit_input).fill(new_text)
        self.press_key(self.todo_edit_input, "Enter")

    def toggle_all(self) -> None:
        """Toggle all todos."""
        self.click(self.toggle_all_checkbox)

    def clear_completed(self) -> None:
        """Clear completed todos."""
        if self.is_visible(self.clear_completed_button, timeout=2000):
            self.click(self.clear_completed_button)

    def filter_all(self) -> None:
        """Show all todos."""
        self.click(self.filter_all)

    def filter_active(self) -> None:
        """Show only active todos."""
        self.click(self.filter_active)

    def filter_completed(self) -> None:
        """Show only completed todos."""
        self.click(self.filter_completed)

    def is_todo_visible(self, text: str) -> bool:
        """Check if todo is visible."""
        return self.is_visible(self.todo_item(text), timeout=2000)

    def is_todo_completed(self, text: str) -> bool:
        """Check if todo is marked as completed."""
        locator = self.page.locator(f".todo-list li:has-text('{text}')")
        class_attr = locator.get_attribute("class")
        return "completed" in class_attr if class_attr else False

    def get_all_todos(self) -> List[str]:
        """Get all todo item texts."""
        todos = []
        items = self.page.locator(self.todo_items).all()
        for item in items:
            label = item.locator("label")
            todos.append(label.inner_text())
        return todos

    def expect_todo_count(self, count: int) -> None:
        """Assert todo count."""
        self.page.locator(self.todo_items).nth(count - 1).wait_for() if count > 0 else None

    def expect_todo_visible(self, text: str) -> None:
        """Assert todo is visible."""
        self.expect_visible(self.todo_item(text))

    def expect_todo_completed(self, text: str) -> None:
        """Assert todo is completed."""
        from playwright.sync_api import expect
        expect(self.page.locator(f".todo-list li:has-text('{text}')")
        ).to_have_class(lambda c: "completed" in c)

    def expect_active_count(self, count: int) -> None:
        """Assert active todo count."""
        if count == 1:
            self.expect_text(self.todo_count, f"{count} item left")
        else:
            self.expect_text(self.todo_count, f"{count} items left")
