"""
Testing: Fixtures and mocking
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Generator


# Fixture examples
@pytest.fixture
def sample_data() -> list[int]:
    """Provide sample data for tests."""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def mock_database():
    """Create a mock database for testing."""
    db = Mock()
    db.query.return_value = [{"id": 1, "name": "Test"}]
    db.connect.return_value = True
    return db


# Tests using fixtures
class TestWithFixtures:
    def test_sum(self, sample_data):
        assert sum(sample_data) == 15

    def test_max(self, sample_data):
        assert max(sample_data) == 5

    def test_mock_db(self, mock_database):
        mock_database.query("SELECT * FROM users")
        mock_database.query.assert_called_once()


# Mock examples
class TestMocking:
    def test_mock_function(self):
        mock_func = Mock(return_value=42)
        assert mock_func() == 42
        mock_func.assert_called_once()

    def test_mock_with_args(self):
        mock_calc = Mock(return_value=100)
        result = mock_calc(10, 90)
        mock_calc.assert_called_with(10, 90)

    def test_spy_on_function(self):
        original_func = len
        spy = Mock(wraps=original_func)

        spy([1, 2, 3])
        assert spy.call_count == 1
        assert spy([1, 2, 3, 4]) == 4


# Patch example
class UserService:
    def __init__(self, db):
        self.db = db

    def get_user(self, user_id: int):
        return self.db.fetch_one(f"SELECT * FROM users WHERE id = {user_id}")


def test_get_user():
    mock_db = Mock()
    mock_db.fetch_one.return_value = {"id": 1, "name": "Alice"}

    service = UserService(mock_db)
    user = service.get_user(1)

    assert user["name"] == "Alice"
    mock_db.fetch_one.assert_called_once()


# MagicMock for context managers
def test_context_manager():
    with MagicMock() as mock_cm:
        mock_cm.__enter__ = Mock(return_value="context")
        mock_cm.__exit__ = Mock(return_value=False)
        with mock_cm as ctx:
            assert ctx == "context"