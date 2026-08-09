# Student Expense Tracker

A small web application to record and manage a student's expenses. The project follows a simple architecture with a Flask backend, a frontend using plain HTML/CSS/JavaScript, and a SQLite database [...]

Important docs:

- docs/REQUIREMENTS.md — functional and non-functional requirements (source of truth for behavior)
- docs/ARCHITECTURE.md  — system architecture and component responsibilities
- docs/DATABASE.md      — the database schema and rules
- docs/API.md           — the API contract between frontend and backend
- docs/DEVELOPMENT.md   — development and testing guidance
- docs/DESIGN.md        — UI/UX design guidance

Development / Configuration

The application reads configuration from environment variables. For local development you may create a `.env` file (do NOT commit it). Example variables are provided in `.env.example`.

Example environment variables:

- DATABASE_PATH=database/expenses.db
- API_PORT=5000
- API_BASE_URL=http://localhost:5000
- FRONTEND_ORIGIN=http://localhost:3000

Monetary values

- The API accepts amounts in rupees (JSON numeric). The backend stores amounts internally as integer paise (1 rupee = 100 paise) and converts to rupees in API responses.

Testing

- Tests use pytest. For isolation, tests should use a temporary SQLite database file (recommended) created with pytest's `tmp_path` fixture and initialized using the project's `init_db_file()` helper. This avoids connection-lifetime issues that can arise with in-memory `:memory:` databases when the initialization connection is closed.

  If you prefer to use `:memory:` databases for tests, ensure the test harness maintains a persistent connection for the lifetime of the test (this is more complex and error-prone). The temporary-file approach is simpler and recommended for Milestone 1 and 2.

- Tests must not modify the development database. Always pass an explicit `db_path` (or use the provided test fixtures) to database-layer functions in tests.

See the `docs/` folder for full implementation and development guidelines.
