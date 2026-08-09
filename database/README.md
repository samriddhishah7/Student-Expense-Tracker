Student Expense Tracker — database directory

- The application uses SQLite for persistent storage.
- The database file path is configured by the environment variable DATABASE_PATH (see .env.example).
- On startup the backend initializes the database non-destructively:
  - It will create the database file if missing.
  - It will create the required schema using CREATE TABLE IF NOT EXISTS and CREATE INDEX IF NOT EXISTS.
  - It will not delete or overwrite an existing database.
