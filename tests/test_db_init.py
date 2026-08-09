import sqlite3
from backend.app import init_db_file

def test_init_creates_schema(tmp_path):
    db_path = str(tmp_path / "test.db")
    # Initialize DB file with schema
    init_db_file(db_path)

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses'")
        assert cur.fetchone() is not None, "expenses table was not created"

        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_expenses_date'")
        assert cur.fetchone() is not None, "idx_expenses_date index was not created"
    finally:
        conn.close()
