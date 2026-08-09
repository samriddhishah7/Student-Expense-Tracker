# Student Expense Tracker

A small web application to record and manage a student's expenses. The project follows a simple architecture with a Flask backend, a frontend using plain HTML/CSS/JavaScript, and a SQLite database for persistence. Documentation is in the `docs/` directory and contains the authoritative requirements, architecture, database, API, and development guidelines.

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

- Tests use pytest. Tests should use an in-memory SQLite database for isolation using the appropriate connection configuration for the chosen backend implementation. Tests must not modify the development database.

See the `docs/` folder for full implementation and development guidelines.
