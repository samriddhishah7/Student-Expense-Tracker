"""Database access layer for Student Expense Tracker.

Responsibilities:
- Provide simple SQLite-based CRUD operations for the documented `expenses` table.
- Manage connections and transactions safely.

Design notes:
- Functions accept an optional `db_path` parameter. If omitted the module uses
  the configured DATABASE_PATH from backend.config. Tests should pass an
  explicit `db_path` to avoid modifying the development DB.
- The database layer stores monetary values as integer paise (amount_paise).
  Helper conversion utilities are provided but NOT implicitly applied by CRUD
  functions; callers should provide amount_paise integers. This keeps API
  validation and conversion responsibility at the API boundary (later
  milestone) while still making conversion utilities available for reuse.

This module intentionally keeps Flask and HTTP concerns out of the code.
"""
from __future__ import annotations

import sqlite3
from typing import Dict, List, Optional
from decimal import Decimal

from .config import DATABASE_PATH


def _get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Open a sqlite3 connection to the given path (or configured path).

    The caller is responsible for closing the connection. Connections created
    here use the default sqlite3 settings; row_factory is set where rows are
    returned to simplify conversion to dict.
    """
    path = db_path or DATABASE_PATH
    conn = sqlite3.connect(path)
    return conn


def _row_to_dict(row: sqlite3.Row) -> Dict:
    return {k: row[k] for k in row.keys()}


# ----- Helper conversion utilities -----

def rupees_to_paise(value: Decimal) -> int:
    """Convert a Decimal rupees amount to integer paise.

    Precision: raises ValueError if `value` has more than 2 fractional
    decimal places. This function does not perform any rounding.

    Example: Decimal('99.50') -> 9950
    """
    if not isinstance(value, Decimal):
        value = Decimal(str(value))

    # Normalize and check fractional digits
    quantized = value.quantize(Decimal('0.01'))
    if quantized != value:
        raise ValueError("Amount has more than 2 decimal places")

    paise = int((value * 100).to_integral_value())
    return paise


def paise_to_rupees(paise: int) -> Decimal:
    """Convert integer paise to Decimal rupees.

    Example: 9950 -> Decimal('99.50')
    """
    return (Decimal(paise) / Decimal(100)).quantize(Decimal('0.01'))


# ----- CRUD operations -----

def create_expense(amount_paise: int, category: str, date: str, description: Optional[str] = None,
                   db_path: Optional[str] = None) -> int:
    """Insert a new expense and return the generated id.

    Parameters are expected to conform to the documented schema. The
    database layer requires amount_paise to already be an integer number of
    paise; it will not perform rupee<->paise conversion automatically.
    """
    conn = _get_connection(db_path)
    try:
        cur = conn.execute(
            "INSERT INTO expenses (amount_paise, category, date, description) VALUES (?, ?, ?, ?)",
            (amount_paise, category, date, description),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_expense(expense_id: int, db_path: Optional[str] = None) -> Optional[Dict]:
    """Return a single expense record as a dict, or None if not found."""
    conn = _get_connection(db_path)
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT id, amount_paise, category, date, description FROM expenses WHERE id = ?", (expense_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return _row_to_dict(row)
    finally:
        conn.close()


def get_all_expenses(db_path: Optional[str] = None) -> List[Dict]:
    """Return all expenses ordered by date DESC, id DESC as documented."""
    conn = _get_connection(db_path)
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT id, amount_paise, category, date, description FROM expenses ORDER BY date DESC, id DESC")
        rows = cur.fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()


def update_expense(expense_id: int, amount_paise: int, category: str, date: str,
                   description: Optional[str] = None, db_path: Optional[str] = None) -> bool:
    """Update an existing expense. Returns True if a row was updated.

    The function will not create a new row if the id does not exist; it will
    return False in that case.
    """
    conn = _get_connection(db_path)
    try:
        cur = conn.execute(
            "UPDATE expenses SET amount_paise = ?, category = ?, date = ?, description = ? WHERE id = ?",
            (amount_paise, category, date, description, expense_id),
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def delete_expense(expense_id: int, db_path: Optional[str] = None) -> bool:
    """Delete the requested expense. Returns True if a row was deleted."""
    conn = _get_connection(db_path)
    try:
        cur = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
