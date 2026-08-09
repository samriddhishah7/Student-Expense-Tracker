import pytest
from backend.app import init_db_file, create_app

@pytest.fixture
def temp_db_path(tmp_path):
    """
    Create a temporary SQLite database file, initialize the documented schema
    in that file, and return the filesystem path. This file persists for the
    duration of the test and avoids in-memory connection lifetime issues.
    """
    db_file = tmp_path / "test_expenses.db"
    init_db_file(str(db_file))
    return str(db_file)

@pytest.fixture
def app(temp_db_path, monkeypatch):
    """
    Create the Flask application configured to use the temporary DB file.
    Set DATABASE_PATH so backend.config reads the correct path when create_app()
    is invoked.
    """
    monkeypatch.setenv("DATABASE_PATH", temp_db_path)
    return create_app()

@pytest.fixture
def client(app):
    """Flask test client using the app fixture configured with a temp DB."""
    return app.test_client()
