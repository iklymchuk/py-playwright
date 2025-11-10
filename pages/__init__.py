"""Page Objects for the application."""

from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.todo_page import TodoPage

__all__ = [
    "BasePage",
    "LoginPage",
    "HomePage",
    "TodoPage",
]
