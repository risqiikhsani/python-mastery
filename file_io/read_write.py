"""
File I/O: Reading and writing files
"""

import os
from pathlib import Path

# Path handling (recommended way)
base_path = Path(__file__).parent


# Read entire file
def read_entire_file(path: Path) -> str:
    return path.read_text()


# Write entire file
def write_file(path: Path, content: str) -> None:
    path.write_text(content)


# Read line by line (memory efficient)
def process_lines(path: Path):
    with open(path, 'r') as f:
        for line in f:
            print(line.strip())


# JSON handling
import json


def write_json(path: Path, data: dict) -> None:
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def read_json(path: Path) -> dict:
    with open(path, 'r') as f:
        return json.load(f)


# CSV handling
import csv


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict]:
    with open(path, 'r') as f:
        return list(csv.DictReader(f))


# Binary files
def read_binary(path: Path) -> bytes:
    return path.read_bytes()


def write_binary(path: Path, data: bytes) -> None:
    path.write_bytes(data)


# File existence and metadata
def file_info(path: Path) -> dict:
    return {
        "exists": path.exists(),
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
        "size": path.stat().st_size if path.exists() else 0,
        "modified": path.stat().st_mtime if path.exists() else 0,
    }


# Temp file handling
import tempfile


def temp_file_demo():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Temporary content")
        temp_path = f.name

    # Read temp file
    content = Path(temp_path).read_text()
    print(f"Temp file content: {content}")

    # Clean up
    os.unlink(temp_path)


# Walk directory tree
def walk_directory(root: Path):
    for path in root.rglob("*.py"):
        print(f"{path.relative_to(root)}")


# Example usage
demo_file = base_path / "demo.txt"
write_file(demo_file, "Hello, Python!")
print(read_entire_file(demo_file))
os.remove(demo_file)