"""End-to-end tests for TodoMVC application."""

import pytest
from pages.todo_page import TodoPage


@pytest.mark.e2e
class TestTodoE2E:
    """End-to-end tests for complete user workflows."""

    def test_complete_todo_workflow(self, page, base_url, sample_todos):
        """Test complete workflow: add, edit, complete, filter, and delete todos."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Use sample todos from data
        todos = [todo["text"] for todo in sample_todos[:4]]
        todo_page.add_multiple_todos(todos)
        assert todo_page.get_todo_count() == 4
        
        # Step 2: Edit a todo
        todo_page.edit_todo("Morning exercise", "Evening exercise")
        assert todo_page.is_todo_visible("Evening exercise")
        
        # Step 3: Complete some todos
        todo_page.complete_todo("Buy groceries")
        todo_page.complete_todo("Call dentist")
        assert todo_page.get_active_count() == 2
        
        # Step 4: Filter completed
        todo_page.filter_completed()
        assert todo_page.is_todo_visible("Buy groceries")
        assert todo_page.is_todo_visible("Call dentist")
        
        # Step 5: Filter active
        todo_page.filter_active()
        assert todo_page.is_todo_visible("Evening exercise")
        assert todo_page.is_todo_visible("Finish report")
        
        # Step 6: Clear completed
        todo_page.filter_all()
        todo_page.clear_completed()
        assert todo_page.get_todo_count() == 2
        
        # Step 7: Complete remaining and verify
        todo_page.toggle_all()
        assert todo_page.is_todo_completed("Evening exercise")
        assert todo_page.is_todo_completed("Finish report")

    def test_empty_state_workflow(self, page, base_url):
        """Test workflow starting from empty state."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Verify empty state
        assert todo_page.get_todo_count() == 0
        
        # Add first todo
        todo_page.add_todo("First task ever")
        assert todo_page.get_todo_count() == 1
        
        # Delete it
        todo_page.delete_todo("First task ever")
        assert todo_page.get_todo_count() == 0

    def test_bulk_operations_workflow(self, page, base_url):
        """Test workflow with bulk operations."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Add many todos
        todos = [f"Task {i}" for i in range(1, 11)]
        todo_page.add_multiple_todos(todos)
        assert todo_page.get_todo_count() == 10
        
        # Complete all
        todo_page.toggle_all()
        for todo in todos:
            assert todo_page.is_todo_completed(todo)
        
        # Uncomplete all
        todo_page.toggle_all()
        assert todo_page.get_active_count() == 10
        
        # Complete half
        for i in range(1, 6):
            todo_page.complete_todo(f"Task {i}")
        assert todo_page.get_active_count() == 5
        
        # Clear completed
        todo_page.clear_completed()
        assert todo_page.get_todo_count() == 5


@pytest.mark.e2e
@pytest.mark.slow
class TestTodoEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_add_empty_todo(self, page, base_url):
        """Test that empty todos cannot be added."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Try to add empty todo
        todo_page.fill(todo_page.new_todo_input, "")
        todo_page.press_key(todo_page.new_todo_input, "Enter")
        
        # Verify no todo is added
        assert todo_page.get_todo_count() == 0

    def test_add_very_long_todo(self, page, base_url):
        """Test adding a very long todo item."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Add a very long todo
        long_text = "A" * 500
        todo_page.add_todo(long_text)
        
        # Verify todo is added
        assert todo_page.get_todo_count() == 1

    def test_special_characters_in_todo(self, page, base_url):
        """Test adding todos with special characters."""
        todo_page = TodoPage(page)
        todo_page.navigate_to_todo_app(base_url)
        
        # Add todos with special characters
        special_todos = [
            "Task with <HTML> tags",
            "Task with 'quotes'",
            "Task with \"double quotes\"",
            "Task with & symbols",
        ]
        
        todo_page.add_multiple_todos(special_todos)
        assert todo_page.get_todo_count() == 4
