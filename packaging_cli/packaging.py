"""
Packaging and CLI: pyproject.toml and argparse
"""

# pyproject.toml structure
"""
[project]
name = "my-package"
version = "0.1.0"
description = "A sample package"
requires-python = ">=3.10"
dependencies = ["requests>=2.28", "click>=8.0"]

[project.optional-dependencies]
dev = ["pytest>=7.0", "black", "mypy"]
docs = ["sphinx", "sphinx-rtd-theme"]

[project.scripts]
myapp = "my_package.main:main"

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
target-version = ["py310", "py311"]

[tool.mypy]
python_version = "3.10"
strict = true
"""

# CLI with argparse
import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="A sample CLI application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --name Alice --count 5
  %(prog)s list --filter recent
  %(prog)s process --verbose --input data.csv
        """
    )

    # Positional arguments
    parser.add_argument("action", choices=["list", "create", "delete"])

    # Optional arguments
    parser.add_argument("-n", "--name", help="Name of the item")
    parser.add_argument("-c", "--count", type=int, default=1, help="Count")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("--config", default="config.json", help="Config file path")

    # Flag with choices
    parser.add_argument(
        "--level",
        choices=["debug", "info", "warning", "error"],
        default="info"
    )

    # Boolean flag
    parser.add_argument("--dry-run", action="store_true")

    # Store values as list
    parser.add_argument("--exclude", action="append", default=[])

    return parser


# Alternative: click library (more user-friendly)
"""
import click

@click.command()
@click.option("-n", "--name", prompt="Enter name")
@click.option("-c", "--count", default=1, type=int)
@click.argument("action", type=click.Choice(["start", "stop"]))
def cli(action, name, count):
    click.echo(f"{action}: {name} x {count}")

if __name__ == "__main__":
    cli()
"""

# Setup.py (legacy but still used)
"""
from setuptools import setup, find_packages

setup(
    name="my-package",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=["requests"],
)
"""


# __init__.py exports
"""
from .module import MyClass
from .utils import helper_function

__all__ = ["MyClass", "helper_function"]
"""


# Entry point example
"""
# my_package/__main__.py
from .main import main

if __name__ == "__main__":
    main()
"""


# Version info (dynamic)
def get_version() -> str:
    try:
        from importlib.metadata import version
        return version("my-package")
    except Exception:
        return "0.0.0"


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    print(f"Action: {args.action}")
    print(f"Name: {args.name}")
    print(f"Count: {args.count}")
    print(f"Verbose: {args.verbose}")
    print(f"Config: {args.config}")
    print(f"Level: {args.level}")
    print(f"Dry run: {args.dry_run}")
    print(f"Exclude: {args.exclude}")