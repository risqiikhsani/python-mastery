"""
Error Handling: Error recovery patterns
"""

from typing import Callable, TypeVar, Optional, Any
from functools import wraps
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


# Retry pattern with exponential backoff
def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """Decorator that retries a function on failure."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1} failed: {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        import time
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"All {max_attempts} attempts failed")

            raise last_exception
        return wrapper
    return decorator


# Result type pattern (no exceptions)
from dataclasses import dataclass


@dataclass
class Result:
    success: bool
    data: Any = None
    error: Optional[str] = None


def safe_divide(a: float, b: float) -> Result:
    try:
        return Result(success=True, data=a / b)
    except ZeroDivisionError:
        return Result(success=False, error="Division by zero")
    except Exception as e:
        return Result(success=False, error=str(e))


# Circuit breaker pattern
from datetime import datetime, timedelta


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "closed"  # closed, open, half-open

    def call(self, func: Callable, *args, **kwargs):
        if self.state == "open":
            if self._should_attempt_reset():
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        self.failures = 0
        self.state = "closed"

    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = datetime.now()
        if self.failures >= self.failure_threshold:
            self.state = "open"

    def _should_attempt_reset(self) -> bool:
        if self.last_failure_time is None:
            return True
        return datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout)


# Usage examples
@retry(max_attempts=3, delay=0.1)
def unstable_function():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network error")
    return "Success!"


# Result pattern
result = safe_divide(10, 0)
if result.success:
    print(f"Result: {result.data}")
else:
    print(f"Error: {result.error}")