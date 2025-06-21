import os
import sqlite3
from loguru import logger

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "database.db")
print(f"Database path: {DATABASE_PATH}")

def create_database():
    try:
        # Ensure the directory exists and is writable
        db_dir = os.path.dirname(DATABASE_PATH)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        # Remove existing database if it exists and is empty/corrupted
        if os.path.exists(DATABASE_PATH) and os.path.getsize(DATABASE_PATH) == 0:
            os.remove(DATABASE_PATH)
            logger.info(f"Removed empty database file at {DATABASE_PATH}")
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        logger.info(f"Creating database at {DATABASE_PATH}...")
        
        # Create users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL
            )
        """
        )
        logger.info("Created 'users' table.")

        # Create todos table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """
        )
        logger.info("Created 'todos' table.")

        # Insert dummy users (ignore if they already exist)
        dummy_users = [
            ("alice", "alice@example.com"),
            ("bob", "bob@example.com"),
            ("charlie", "charlie@example.com"),
        ]
        cursor.executemany(
            "INSERT OR IGNORE INTO users (username, email) VALUES (?, ?)", dummy_users
        )
        logger.info(f"Inserted {len(dummy_users)} dummy users (ignoring duplicates).")

        # Clear existing todos to avoid duplicates
        cursor.execute("DELETE FROM todos")
        logger.info("Cleared existing todos.")

        # Insert dummy todos
        dummy_todos = [
            (1, "Buy groceries", 0),
            (1, "Read a book", 1),
            (2, "Finish project report", 0),
            (2, "Go for a run", 0),
            (3, "Plan weekend trip", 1),
        ]
        cursor.executemany(
            "INSERT INTO todos (user_id, task, completed) VALUES (?, ?, ?)", dummy_todos
        )
        logger.info(f"Inserted {len(dummy_todos)} dummy todos.")

        conn.commit()
        logger.info("Database created and populated successfully.")
        conn.close()

    except sqlite3.Error as e:
        logger.error(f"SQLite error: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if 'conn' in locals():
            conn.close()
        raise


if __name__ == "__main__":
    create_database()