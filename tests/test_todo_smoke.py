"""Smoke tests for TodoMVC application."""

import pytest
from pages.todo_page import TodoPage


@pytest.mark.smoke
class TestTodoSmoke:
    """Smoke tests for basic todo functionality."""

    def test_add_single_todo(self, page, base_url):
        """Test adding a single todo item."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Add a todo
        todo_page.add_todo("Buy groceries")
        
        # Verify todo is added
        assert todo_page.is_todo_visible("Buy groceries")
        assert todo_page.get_todo_count() == 1

    def test_complete_todo(self, page, base_url):
        """Test completing a todo item."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Add and complete a todo
        todo_page.add_todo("Read a book")
        todo_page.complete_todo("Read a book")
        
        # Verify todo is completed
        assert todo_page.is_todo_completed("Read a book")

    def test_delete_todo(self, page, base_url):
        """Test deleting a todo item."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Add and delete a todo
        todo_page.add_todo("Temporary task")
        todo_page.delete_todo("Temporary task")
        
        # Verify todo is deleted
        assert not todo_page.is_todo_visible("Temporary task")
        assert todo_page.get_todo_count() == 0
