"""
Database: SQLite with Python
"""

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional


# Connection context manager
@contextmanager
def get_connection(db_path: str = ":memory:"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# Create tables
def create_schema(conn: sqlite3.Connection):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)


# CRUD operations
def create_user(conn: sqlite3.Connection, name: str, email: str) -> int:
    cursor = conn.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email)
    )
    return cursor.lastrowid


def get_user_by_id(conn: sqlite3.Connection, user_id: int) -> Optional[dict]:
    cursor = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    return dict(row) if row else None


def get_all_users(conn: sqlite3.Connection) -> list[dict]:
    cursor = conn.execute("SELECT * FROM users ORDER BY created_at DESC")
    return [dict(row) for row in cursor.fetchall()]


def update_user_email(conn: sqlite3.Connection, user_id: int, new_email: str):
    conn.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )


def delete_user(conn: sqlite3.Connection, user_id: int):
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))


# Query with join
def get_user_posts(conn: sqlite3.Connection, user_id: int) -> list[dict]:
    cursor = conn.execute("""
        SELECT p.*, u.name as author
        FROM posts p
        JOIN users u ON p.user_id = u.id
        WHERE u.id = ?
    """, (user_id,))
    return [dict(row) for row in cursor.fetchall()]


# Transaction example
def transfer_posts(conn: sqlite3.Connection, from_user: int, to_user: int):
    try:
        cursor = conn.execute(
            "UPDATE posts SET user_id = ? WHERE user_id = ?",
            (to_user, from_user)
        )
        if cursor.rowcount > 0:
            print(f"Transferred {cursor.rowcount} posts")
    except sqlite3.IntegrityError as e:
        print(f"Transfer failed: {e}")


# Usage
with get_connection() as conn:
    create_schema(conn)

    # Create users
    alice_id = create_user(conn, "Alice", "alice@example.com")
    bob_id = create_user(conn, "Bob", "bob@example.com")

    # Create posts
    conn.execute(
        "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
        (alice_id, "Hello World", "My first post!")
    )
    conn.execute(
        "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
        (bob_id, "Another Post", "Bob's content")
    )

    # Query
    print(f"Users: {get_all_users(conn)}")
    print(f"Alice's posts: {get_user_posts(conn, alice_id)}")
    print(f"User 1: {get_user_by_id(conn, alice_id)}")