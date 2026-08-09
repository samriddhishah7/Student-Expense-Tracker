import sqlite3
from decimal import Decimal

import pytest

from backend import database
from backend.app import init_db_file

def test_rupees_to_paise_valid_and_invalid():
    assert database.rupees_to_paise(Decimal('99.50')) == 9950
    with pytest.raises(ValueError):
        database.rupees_to_paise(Decimal('1.005'))  # more than two decimal places

def test_create_and_get_expense(temp_db_path):
    eid = database.create_expense(9950, "Food", "2026-08-09", "Lunch", db_path=temp_db_path)
    rec = database.get_expense(eid, db_path=temp_db_path)
    assert rec is not None
    assert rec["id"] == eid
    assert rec["amount_paise"] == 9950
    assert rec["category"] == "Food"
    assert rec["date"] == "2026-08-09"
    assert rec["description"] == "Lunch"

def test_get_nonexistent_expense(temp_db_path):
    assert database.get_expense(999999, db_path=temp_db_path) is None

def test_update_expense(temp_db_path):
    eid = database.create_expense(500, "Transport", "2026-01-01", "Bus", db_path=temp_db_path)
    updated = database.update_expense(eid, 700, "Transport", "2026-01-02", "Train", db_path=temp_db_path)
    assert updated is True
    rec = database.get_expense(eid, db_path=temp_db_path)
    assert rec["amount_paise"] == 700
    assert rec["date"] == "2026-01-02"
    assert rec["description"] == "Train"

def test_delete_expense(temp_db_path):
    eid = database.create_expense(200, "Snack", "2026-02-02", "Samosa", db_path=temp_db_path)
    deleted = database.delete_expense(eid, db_path=temp_db_path)
    assert deleted is True
    assert database.get_expense(eid, db_path=temp_db_path) is None

def test_get_all_ordering(temp_db_path):
    # Create two expenses with distinct dates and ids
    id1 = database.create_expense(100, "A", "2026-03-01", None, db_path=temp_db_path)  # older date
    id2 = database.create_expense(200, "B", "2026-04-01", None, db_path=temp_db_path)  # newer date
    id3 = database.create_expense(150, "C", "2026-04-01", None, db_path=temp_db_path)  # same date as id2, higher id will come first
    all_exp = database.get_all_expenses(db_path=temp_db_path)
    # Expect ordering: date DESC, id DESC -> entries with 2026-04-01 first, with higher id first
    assert all_exp[0]["id"] == id3  # newest id among newest date
    assert all_exp[1]["id"] == id2
    assert all_exp[2]["id"] == id1

def test_amount_stored_as_integer_paise(temp_db_path):
    eid = database.create_expense(12345, "Test", "2026-05-05", "Amount test", db_path=temp_db_path)
    rec = database.get_expense(eid, db_path=temp_db_path)
    assert isinstance(rec["amount_paise"], int)
    assert rec["amount_paise"] == 12345

def test_reinit_does_not_destroy_data(tmp_path):
    db_file = str(tmp_path / "persist.db")
    init_db_file(db_file)
    eid = database.create_expense(999, "Persist", "2026-06-06", "Preserve", db_path=db_file)
    # Re-initialize the DB non-destructively
    init_db_file(db_file)
    rec = database.get_expense(eid, db_path=db_file)
    assert rec is not None
    assert rec["id"] == eid
