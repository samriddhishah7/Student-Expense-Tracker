import sqlite3
from flask import Flask, jsonify
import os
from .config import DATABASE_PATH, API_PORT


DDL_SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    amount_paise INTEGER NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT
);

CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date);
"""


def create_app():
    app = Flask(__name__)
    app.config['DATABASE_PATH'] = DATABASE_PATH

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "ok"}), 200

    return app


def init_db_file(path=None):
    """Ensure the database file and required schema exist.

    Behavior:
    - If path is ':memory:', create an in-memory SQLite database and initialize the required schema.
    - Otherwise, create parent directories if needed, create the database file if missing, and ensure the required tables and indexes exist using CREATE TABLE IF NOT EXISTS / CREATE INDEX IF NOT EXISTS.

    This function is non-destructive and will not overwrite existing data.
    Returns the path provided or ':memory:' for in-memory.
    """
    p = path or DATABASE_PATH

    if p == ':memory:':
        conn = sqlite3.connect(':memory:')
        conn.executescript(DDL_SCHEMA)
        conn.commit()
        conn.close()
        return ':memory:'

    parent = os.path.dirname(p)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

    # Connect to the database (will create file if missing) and ensure schema exists
    conn = sqlite3.connect(p)
    try:
        conn.executescript(DDL_SCHEMA)
        conn.commit()
    finally:
        conn.close()

    return p


if __name__ == '__main__':
    init_db_file()
    app = create_app()
    app.run(host='0.0.0.0', port=API_PORT)
