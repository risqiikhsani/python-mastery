"""
Best Practices: PEP 8, type hints, docstrings, naming
"""

from typing import Optional


# Clear naming conventions
# Classes: CamelCase
# Functions/variables: snake_case
# Constants: UPPER_SNAKE_CASE
# Private: _leading_underscore


# Good vs bad function names
class UserService:
    # Bad: unclear, generic
    def process(x, y):
        return x + y

    # Good: descriptive, clear intent
    def calculate_total_price(base_price: float, tax_rate: float) -> float:
        return base_price * (1 + tax_rate)


# Type hints everywhere
def greet_user(user_id: int, name: Optional[str] = None) -> str:
    """Return a greeting message.

    Args:
        user_id: The unique identifier for the user
        name: Optional name override

    Returns:
        A formatted greeting string

    Example:
        >>> greet_user(1, "Alice")
        'Hello, Alice!'
    """
    return f"Hello, {name or 'User ' + str(user_id)}!"


# Docstring styles
class DataProcessor:
    """Process and transform data according to configured rules.

    This class provides functionality for cleaning, validating,
    and transforming input data into standardized formats.

    Attributes:
        verbose: Enable detailed logging output
        strict: Raise exceptions on validation failures

    Example:
        >>> processor = DataProcessor(verbose=True)
        >>> processor.process([1, 2, 3])
        [2, 4, 6]
    """

    def __init__(self, verbose: bool = False, strict: bool = False):
        self.verbose = verbose
        self.strict = strict
        self._processed_count = 0

    def process(self, data: list[int]) -> list[int]:
        """Process a list of integers by doubling them.

        Args:
            data: List of integers to process

        Returns:
            New list with each value doubled

        Raises:
            ValueError: If strict mode and data is empty
        """
        if not data:
            if self.strict:
                raise ValueError("Cannot process empty data")
            return []

        result = [x * 2 for x in data]
        self._processed_count += len(result)

        if self.verbose:
            print(f"Processed {len(result)} items")

        return result


# Error handling best practices
def robust_division(a: float, b: float) -> float:
    """Divide two numbers with proper error handling."""
    if not isinstance(a, (int, float)):
        raise TypeError(f"Expected number, got {type(a).__name__}")
    if not isinstance(b, (int, float)):
        raise TypeError(f"Expected number, got {type(b).__name__}")
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


# Constants at module level
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".doc"}


# Avoid globals, use classes or passing state
def process_with_config(data: list, config: dict) -> list:
    """Process data according to configuration."""
    threshold = config.get("threshold", 0)
    return [x for x in data if x > threshold]


# Use dataclasses for data containers
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    name: str
    email: str
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)


# Chain exceptions appropriately
def read_config(path: str) -> dict:
    """Read configuration from file."""
    try:
        import json
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise RuntimeError(f"Config file not found: {path}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON in config: {path}") from e


# Avoid long parameter lists
@dataclass
class PaginationParams:
    page: int = 1
    per_page: int = 20
    max_per_page: int = 100


@dataclass
class SearchParams:
    query: str
    pagination: PaginationParams
    filters: Optional[dict] = None