# Student Expense Tracker — Database Specification

**Document:** `DATABASE.md`
**Project:** Student Expense Tracker
**Version:** 1.0
**Status:** Initial Database Specification
**Last Updated:** 2026-08-09

---

# 1. Purpose

This document defines the database structure and data rules for the Student Expense Tracker.

It specifies:

* database technology
* database location
* tables
* columns
* data types
* required/optional fields
* constraints
* relationships
* indexes
* CRUD behavior
* calculation rules
* validation rules
* database initialization
* database access boundaries
* rules for AI coding agents

The database must implement only the data requirements defined in:

```text
docs/REQUIREMENTS.md
```

The database architecture must remain consistent with:

```text
docs/ARCHITECTURE.md
```

---

# 2. Database Technology

The initial project uses:

```text
SQLite
```

SQLite is selected because:

* the project is intended for personal/student use
* the application has a relatively small dataset
* it requires minimal setup
* it is easy to develop and test locally
* it does not require a separate database server

The project does not require a cloud database.

---

# 3. Database File

The initial database file should be stored inside the project in:

```text
database/expenses.db
```

The exact location may be changed only if the project configuration explicitly requires it.

The database file must not be committed to Git if the project later adopts a policy that excludes generated/local database files.

The `.gitignore` should be used appropriately.

---

# 4. Database Responsibility

The database is responsible for:

* persistent storage of expense records
* retrieving expense records
* updating expense records
* deleting expense records
* maintaining data integrity

The database is NOT responsible for:

* rendering the frontend
* handling HTTP requests
* deciding UI behavior
* authentication
* financial advice
* AI processing
* payment processing

Those responsibilities belong to other application layers or are outside the current scope.

---

# 5. Database Architecture

The data flow must follow:

```text
Frontend
   ↓
HTTP/API
   ↓
Flask Backend
   ↓
Database Layer
   ↓
SQLite
```

The frontend must never directly access SQLite.

---

# 6. Current Database Entities

The initial database contains the following primary entity:

```text
Expense
```

The database should remain intentionally small.

The initial schema does NOT require separate tables for:

* users
* accounts
* payments
* banks
* transactions
* notifications
* AI recommendations
* authentication
* categories
* currencies

unless a future requirement explicitly introduces them.

---

# 7. Database Schema Overview

The initial database contains:

```text
expenses
```

Conceptually:

```text
┌──────────────────────────────────────┐
│              expenses                │
├──────────────────────────────────────┤
│ id                                   │
│ amount_paise                          │
│ category                             │
│ date                                 │
│ description                          │
└──────────────────────────────────────┘
```

There are no foreign-key relationships in the initial schema.

---

# 8. `expenses` Table

The `expenses` table stores individual expense records.

Each row represents **one manually recorded expense**.

---

# 9. `expenses.id`

## Purpose

Uniquely identifies an expense.

## Type

SQLite:

```text
INTEGER
```

## Required

Yes.

## Null

Not allowed.

## Primary Key

Yes.

## Generation

The ID should be generated automatically by the database.
The application should not ask the user to enter an expense ID.

Example:

```text
1
2
3
4
```

The exact SQLite primary-key declaration may be determined by the implementation.

---

# 10. `expenses.amount_paise`

## Purpose

Stores the amount of money spent in paise (integer).

## Type

```text
INTEGER
```

## Required

Yes.

## Null

Not allowed.

## Rules

The value must:

* represent the amount in paise (1 rupee = 100 paise)
* correspond to an API-provided rupee value that is numeric, greater than zero, and has at most two decimal places

Examples of valid API inputs and stored values:

```text
API: 50      -> amount_paise = 5000
API: 99.50   -> amount_paise = 9950
API: 250     -> amount_paise = 25000
```

Invalid API inputs include:

```text
0
-50
"abc"
99.555  (more than 2 decimal places)
```

The backend MUST reject any API request with an amount that has more than two decimal places and return HTTP 400 using the canonical error response. The backend MUST NOT round incoming amounts.

Maximum amount
- The API must enforce a maximum allowed amount of ₹10,000,000.00 (10,000,000 rupees). Amounts above this limit must be rejected with HTTP 400.

---

# 11. Monetary Precision

The backend converts rupees (API numeric) to integer paise for storage. All calculations and aggregates must be performed using integer paise and converted back to rupees only for API responses and display.

This avoids floating-point rounding errors in storage and calculation.

---

# 12. `expenses.category`

## Purpose

Identifies the category of the expense.

## Type

```text
TEXT
```

## Required

Yes.

## Null

Not allowed.

## Allowed Values

The initial application supports exactly:

```text
Food
Travel
Education
Shopping
Entertainment
Other
```

The application must not silently introduce additional categories.

Leading/trailing whitespace will be trimmed before validation.

---

# 13. `expenses.date`

## Purpose

Stores the date on which the expense occurred.

## Type

```text
TEXT
```

## Required

Yes.

## Null

Not allowed.

## Representation

The application uses `YYYY-MM-DD` text format for the `date` column (example: `2026-08-09`).

## Date rules
- The backend must validate that the `date` field represents a valid calendar date.

---

# 14. `expenses.description`

## Purpose

Stores an optional human-readable description of the expense.

## Type

```text
TEXT
```

## Required

No.

## Null

Allowed.

## Rules

- Description is optional and may be empty.
- Leading/trailing whitespace will be trimmed before storage.
- Maximum length: 500 characters. Requests with descriptions longer than 500 characters must return HTTP 400.

---

# 15. Example Records

Example data (for understanding only):

| id | amount_paise | category      | date       | description |
| -: | ----------: | ------------- | ---------- | ----------- |
|  1 |       25000 | Food          | 2026-08-01 | Lunch       |
|  2 |        8000 | Travel        | 2026-08-02 | Bus fare    |

These are examples for understanding the schema only. They must NOT automatically be inserted into the production database.

---

# 16. Database CRUD Operations

The database must support the operations required by the application.

## Create

Insert a new expense.

## Read

Retrieve:

* all expenses
* an individual expense
* expenses relevant to calculations

## Update

Modify an existing expense.

## Delete

Remove an existing expense.

---

# 17. Read / Ordering

When retrieving all expenses for API responses, the backend should use a default ordering of `date` descending (newest first). To provide deterministic results, when several rows share the same `date`, order by `id` descending.

---

# 18. Indexes

The initial database should create an index on the `date` column to optimize ordering and monthly aggregation queries:

CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date);

Additional indexes should only be added when justified by performance needs.

---

# 19. Null Handling and Constraints

- `id` — NOT NULL
- `amount_paise` — NOT NULL
- `category` — NOT NULL
- `date` — NOT NULL
- `description` — may be NULL or empty

---

# 20. SQL Safety

All database operations involving user-provided values must use parameterized queries. Do NOT build SQL by concatenating user input.

---

# 21. Database Initialization and Migrations

On application startup, the backend should check whether the database file exists at `DATABASE_PATH` and create the required tables/indexes if missing using non-destructive statements (e.g., `CREATE TABLE IF NOT EXISTS ...`). Do NOT delete or overwrite existing databases.

If schema changes are later required, handle migrations carefully and preserve existing data.

---

# 22. Testing

Tests should use an isolated test database (preferably in-memory) and must not modify the development database. Test code should initialize the required schema in the test database before running test cases.

---

# 23. Explicitly Forbidden Additions

Unless requirements are explicitly changed, do NOT create:

```
users
accounts
profiles
transactions
payments
bank_accounts
cards
notifications
messages
analytics
reports
audit_logs
expense_history
expense_versions
currencies
exchange_rates
ai_recommendations
ai_predictions
```

---

# 24. Final Database Principle

Store the minimum structured data necessary to satisfy the documented requirements. The initial database is intentionally simple and uses integer paise for monetary values.
