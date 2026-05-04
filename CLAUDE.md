# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Python learning repository organized into 22 topic folders. Each folder contains runnable `.py` files that demonstrate concepts via `if __name__ == "__main__":` blocks. There are no tests, no build system, and no framework — every topic is a standalone script.

Python version: **3.13** (see `.python-version`). No external dependencies are declared.

## Running Code

**Single file:**
```bash
uv run <topic>/<file>.py
```

**Via main.py:** Uncomment the desired import(s) in `main.py`, then run `uv run main.py`.

## Project Structure

| Folder | Topic |
|--------|-------|
| `examples/` | Examples of real world apps built with python following best practices. |
| `oop/` | Classes, inheritance, encapsulation, abstraction, dunder methods, composition |
| `data_structures/` | Numbers, strings, lists, tuples, dicts, sets, stack/queue, linked list, binary tree |
| `algorithms/` | Recursion, sorting, searching, Big-O analysis |
| `design_patterns/` | Singleton, factory, observer, strategy, adapter |
| `performance/` | Profiling and optimization |
| `type_safety/` | Type hints, runtime validation, protocols |
| `testing/` | pytest basics, fixtures and mocking |
| `error_handling/` | Exceptions and recovery |
| `functional_programming/` | Pure functions and higher-order functions |
| `memory_management/` | Garbage collection |
| `metaprogramming/` | Metaclasses |
| `concurrency/` | Threading, async/await |
| `file_io/` | Reading and writing |
| `modules_packages/` | Import system |
| `context_managers/` | `with` statements |
| `iterators_generators/` | Iterators and generators |
| `decorators/` | Function/class decorators |
| `logging_debugging/` | Logging |
| `regex/` | Regular expressions |
| `database/` | SQLite |
| `packaging_cli/` | `pyproject.toml`, argparse |
| `best_practices/` | PEP 8 style |
