"""Regression tests for TodoMVC application."""

import pytest
from pages.todo_page import TodoPage


@pytest.mark.regression
class TestTodoRegression:
    """Regression tests for todo functionality."""

    def test_add_multiple_todos(self, page, base_url):
        """Test adding multiple todo items."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Add multiple todos
        todos = ["Task 1", "Task 2", "Task 3"]
        todo_page.add_multiple_todos(todos)
        
        # Verify all todos are added
        assert todo_page.get_todo_count() == 3
        for todo in todos:
            assert todo_page.is_todo_visible(todo)

    def test_edit_todo(self, page, base_url):
        """Test editing a todo item."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Add and edit a todo
        todo_page.add_todo("Old task name")
        todo_page.edit_todo("Old task name", "New task name")
        
        # Verify todo is edited
        assert todo_page.is_todo_visible("New task name")
        assert not todo_page.is_todo_visible("Old task name")

    def test_toggle_all_todos(self, page, base_url):
        """Test toggling all todos at once."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Add multiple todos
        todo_page.add_multiple_todos(["Task 1", "Task 2", "Task 3"])
        
        # Toggle all
        todo_page.toggle_all()
        
        # Verify all are completed
        assert todo_page.is_todo_completed("Task 1")
        assert todo_page.is_todo_completed("Task 2")
        assert todo_page.is_todo_completed("Task 3")

    def test_clear_completed_todos(self, page, base_url):
        """Test clearing completed todos."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Add todos and complete some
        todo_page.add_multiple_todos(["Task 1", "Task 2", "Task 3"])
        todo_page.complete_todo("Task 1")
        todo_page.complete_todo("Task 2")
        
        # Clear completed
        todo_page.clear_completed()
        
        # Verify only active todo remains
        assert todo_page.get_todo_count() == 1
        assert todo_page.is_todo_visible("Task 3")
        assert not todo_page.is_todo_visible("Task 1")

    def test_filter_active_todos(self, page, base_url):
        """Test filtering active todos."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Add todos and complete one
        todo_page.add_multiple_todos(["Active task", "Completed task"])
        todo_page.complete_todo("Completed task")
        
        # Filter active
        todo_page.filter_active()
        
        # Verify only active todo is visible
        assert todo_page.is_todo_visible("Active task")

    def test_filter_completed_todos(self, page, base_url):
        """Test filtering completed todos."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Add todos and complete one
        todo_page.add_multiple_todos(["Active task", "Completed task"])
        todo_page.complete_todo("Completed task")
        
        # Filter completed
        todo_page.filter_completed()
        
        # Verify only completed todo is visible
        assert todo_page.is_todo_visible("Completed task")

    def test_todo_counter(self, page, base_url):
        """Test todo counter accuracy."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Add todos
        todo_page.add_multiple_todos(["Task 1", "Task 2", "Task 3"])
        assert todo_page.get_active_count() == 3
        
        # Complete one
        todo_page.complete_todo("Task 1")
        assert todo_page.get_active_count() == 2
        
        # Complete another
        todo_page.complete_todo("Task 2")
        assert todo_page.get_active_count() == 1
