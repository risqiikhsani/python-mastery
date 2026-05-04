"""
Testing: Unit tests with pytest
"""

import pytest


# Simple function to test
def add(a: int, b: int) -> int:
    return a + b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def find_user(users: list[dict], user_id: int) -> dict | None:
    for user in users:
        if user["id"] == user_id:
            return user
    return None


# Test cases
class TestAdd:
    def test_positive_numbers(self):
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        assert add(-1, -1) == -2

    def test_zero(self):
        assert add(0, 5) == 5

    def test_large_numbers(self):
        assert add(1_000_000, 1_000_000) == 2_000_000


class TestDivide:
    def test_normal_division(self):
        assert divide(10, 2) == 5.0

    def test_decimal_result(self):
        assert divide(7, 2) == 3.5

    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            divide(1, 0)


class TestFindUser:
    def test_found(self):
        users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        result = find_user(users, 2)
        assert result == {"id": 2, "name": "Bob"}

    def test_not_found(self):
        users = [{"id": 1, "name": "Alice"}]
        result = find_user(users, 999)
        assert result is None


# Run tests: pytest testing_01_pytest.py -v