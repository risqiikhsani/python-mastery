"""
Logging and Debugging
"""

import logging
import pdb
import traceback
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Create a configured logger."""
    log = logging.getLogger(name)
    log.setLevel(level)

    # Console handler
    handler = logging.StreamHandler()
    handler.setLevel(level)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log


# Log levels
def log_levels_demo():
    log = logging.getLogger("demo")

    log.debug("Debug message - detailed info")
    log.info("Info message - normal operation")
    log.warning("Warning message - something might be wrong")
    log.error("Error message - something failed")
    log.critical("Critical - system may be unusable")


# Debug decorator
def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        try:
            result = func(*args, **kwargs)
            print(f"{func.__name__} returned {result!r}")
            return result
        except Exception as e:
            print(f"{func.__name__} raised {type(e).__name__}: {e}")
            raise
    return wrapper


# PDB debugging
def pdb_demo():
    """Example showing pdb commands."""
    pdb.set_trace()
    # Commands: n(ext), s(tep), c(ontinue), p(rint), pp, l(ist), w(here)
    x = 42
    y = 10
    result = x + y
    return result


# Post-mortem debugging
def post_mortem():
    try:
        1 / 0
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()


# Breakpoint convenience
def smart_breakpoint():
    """Breakpoint that only triggers in debug mode."""
    import os
    if os.environ.get("DEBUG"):
        pdb.set_trace()


# Logging configuration with dictConfig
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s %(name)s:%(lineno)d %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "DEBUG",
        }
    },
    "loggers": {
        "myapp": {"level": "DEBUG", "handlers": ["console"]}
    }
}


# Usage examples
@debug
def calculate(a, b):
    return a ** b


@log_levels_demo.__func__() if hasattr(log_levels_demo, '__func__') else None
log_levels_demo()