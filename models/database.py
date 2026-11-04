import os
import sqlite3

class DatabaseModel:

    def __init__(self, db_path):
        self.db_path = db_path
        folder = os.path.dirname(db_path)

        if folder:
            os.makedirs(folder, exist_ok=True)   # makes data if missing
        self._create_tables()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _create_tables(self):
        with self._connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS user (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email    TEXT NOT NULL UNIQUE,
                points   INTERGER NOT NULL DEFAULT 0
            )""")

            conn.execute("""CREATE TABLE IF NOT EXISTS clues (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                riddle      TEXT NOT NULL,
                cipher_text TEXT,
                key         TEXT NOT NULL,
                created_by  INTEGER,
                created_on  TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
            )""")

# USERS
def get_user(self):
    """The current user as (id, username, email, points), or None."""
    with self._connect() as conn:
        return conn.execute(
            "SELECT id, username, email, points FROM users ORDER BY id LIMIT 1"
        ).fetchone()

def add_user(self):
    """Create a user; returns the new id, or None if the name/email is already taken."""
    try:
        with self.connect() as conn:
            cur = conn.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)", (username, email)
            )
            return cur.lastrowid
    except sqlite3.IntegrityError:
        return None

def update_user(self, user_id, username, email):
    """Change username/email; returns False on a duplicate."""
    try:
        with self._connect() as conn:
            conn.execute(
                "UPDATE users SET username = ?, email = ? WHERE id = ?", (username, email, user_id)
            )
        return True
    except sqlite3.IntegrityError:
        return False

def add_points(self, user_id, amount):
    with self._connect() as conn:
        conn.execute("UPDATE users SET points = points + ? WHERE id = ?", (amount, user_id))

# CLUES
def add_clue(self, riddle, cipher_text, key, created_by = None):
    """Inserts clues, and returns its new id."""
    with self._connect() as conn:
        cur = conn.execute(
            "INSERT INTO clues (riddle, chipher_text, key, created_by) VALUES (?, ?, ?, ?)",
            (riddle, cipher_text, key, created_by)
        )
        return cur.lastrowid

def get_all_clues(self):
    with self._connect() as conn:
        return conn.execute(
            "SELECT id, riddle, cipher_text, key, created_by, created_on FROM clues"
        ).fetchall()

def get_random_clue(self):
    with self._connect() as conn:
        return conn.execute(
            "SELECT id, riddle, cipher_text, key, created_by, created_on FROM clues ORDER BY RANDOM() LIMIT 1"
        ).fetchone()


# DELETES
def wipe_user_data(self, user_id):
    """Delete the user and every clue they created."""
    with self._connect() as conn:
        conn.execute("DELETE FROM clues WHERE created_by = ?", (user_id,))
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))