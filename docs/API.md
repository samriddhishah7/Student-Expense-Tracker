# API — Student Expense Tracker

This document defines the backend HTTP/JSON API contract for the Student Expense Tracker.

This file is part of the authoritative documentation. Follow docs/REQUIREMENTS.md and docs/DATABASE.md when implementing or changing API behavior.

---

## Canonical error response

Errors MUST use the following JSON structure:

{
  "error": "Human-readable error message",
  "details": {}
}

- `error`: a concise human-readable message describing the problem.
- `details`: an object with field-specific errors (optional). When no details are necessary, `details` may be an empty object.

Example validation error:

HTTP 400 Bad Request

{
  "error": "Validation failed",
  "details": {
    "amount": "Amount must be a positive number with at most two decimal places and ≤ 10000000.00",
    "description": "Description must be at most 500 characters"
  }
}

---

## General rules

Content type
- Requests with structured data MUST use `Content-Type: application/json`.
- If a request body is expected to be JSON but is missing or malformed, return HTTP 400 using the canonical error response.

Unknown fields
- The API rejects requests that contain unknown JSON properties. If a request body contains any fields not defined in this contract, the server MUST return HTTP 400 and include the unknown field names in the `details` object.

ID validation
- The path parameter `<id>` MUST be a positive integer (>= 1).
- If the client supplies a non-integer, zero, negative, or decimal value for `<id>`, return HTTP 400 with the canonical error response.
- If the `<id>` is syntactically valid but no expense exists with that ID, return HTTP 404 with:

{
  "error": "Expense not found",
  "details": {}
}

---

## Expense object

Standard expense representation (API-level):

{
  "id": 1,
  "amount": 250.00,
  "category": "Food",
  "date": "2026-08-09",
  "description": "Lunch"
}

Field meanings and rules
- `id`: integer, system-generated, present in responses.
- `amount`: JSON numeric value in rupees. The API accepts numeric rupees values with at most two decimal places (e.g., 99, 99.5, 99.50). The backend stores amounts as integer paise internally and converts to rupees for API responses.
  - Validation rules:
    - Must be present for POST and PUT.
    - Must be numeric (JSON number) — string numeric values such as "99.50" are not accepted.
    - Must be greater than 0.
    - Must have at most two decimal places. Values with more than two decimal places are invalid and must return HTTP 400.
    - Must be ≤ 10,000,000.00 (₹1,00,00,000). Values above this limit must return HTTP 400.
- `category`: string. Must be one of the approved categories: `Food`, `Travel`, `Education`, `Shopping`, `Entertainment`, `Other`.
  - Leading and trailing whitespace will be trimmed before validation.
- `date`: string in `YYYY-MM-DD` format. The server must validate the date is a real calendar date.
  - Stored in database as `YYYY-MM-DD` text.
- `description`: optional string. Leading and trailing whitespace will be trimmed. Maximum length 500 characters. If omitted in PUT, it is treated as an empty string.

---

## Endpoints

### POST /expenses

Purpose: Create a new expense.

Request
- Method: POST
- Path: /expenses
- Content-Type: application/json
- Body (example):

{
  "amount": 250.00,
  "category": "Food",
  "date": "2026-08-09",
  "description": "Lunch"
}

Validation and behavior
- `amount`, `category`, and `date` are required. `description` is optional.
- Reject unknown fields with HTTP 400.
- If the request is valid, the backend converts the amount into paise (amount_paise = amount_in_rupees * 100) and stores the record.

Successful response
- HTTP 201 Created
- Response body: the created expense object (including generated `id`), with `amount` shown in rupees (converted back from paise).

Validation error
- HTTP 400 Bad Request with canonical error structure.

---

### GET /expenses

Purpose: Retrieve all expenses.

Request
- Method: GET
- Path: /expenses
- No request body required.

Successful response
- HTTP 200 OK
- Response body: a JSON array of expense objects ordered by `date` descending (newest first). Where multiple records share the same `date`, order by `id` descending as a tie-breaker.

Empty database
- Returns HTTP 200 with an empty array `[]`.

Notes
- The initial implementation does not provide server-side analytics endpoints. The frontend may compute totals and category breakdowns from the GET /expenses response.

---

### GET /expenses/<id>

Purpose: Retrieve one expense.

Request
- Method: GET
- Path: /expenses/<id>

Successful response
- If found: HTTP 200 OK and the expense object.
- If `<id>` is malformed: HTTP 400 with canonical error.
- If `<id>` is valid but not found: HTTP 404 with { "error": "Expense not found", "details": {} }.

---

### PUT /expenses/<id>

Purpose: Update an existing expense (full replacement semantics).

Request
- Method: PUT
- Path: /expenses/<id>
- Content-Type: application/json
- Body must include `amount`, `category`, and `date`. `description` is optional; if omitted it is set to an empty string.
- Unknown fields cause HTTP 400.

Successful response
- HTTP 200 OK and the updated expense object in the response body.

Errors
- Malformed JSON → HTTP 400
- Invalid data → HTTP 400 with canonical error
- Valid id but no record → HTTP 404

---

### DELETE /expenses/<id>

Purpose: Delete an existing expense.

Request
- Method: DELETE
- Path: /expenses/<id>

Responses
- If deleted successfully: HTTP 204 No Content
- If `<id>` malformed: HTTP 400
- If `<id>` syntactically valid but no record: HTTP 404 with { "error": "Expense not found", "details": {} }

---

## Status codes

Use the following HTTP status codes consistently:
- 200 OK — successful operation with a response body
- 201 Created — resource successfully created
- 204 No Content — successful deletion
- 400 Bad Request — invalid request or validation error
- 404 Not Found — requested resource does not exist
- 500 Internal Server Error — unexpected server error (do not expose internal details)

---

## Examples

Create example (POST):
Request
{
  "amount": 99.50,
  "category": "Food",
  "date": "2026-08-09",
  "description": "Lunch"
}

If valid, server stores amount_paise = 9950 and returns:
HTTP 201 Created
{
  "id": 1,
  "amount": 99.50,
  "category": "Food",
  "date": "2026-08-09",
  "description": "Lunch"
}

---

## Notes for implementers
- Trim leading/trailing whitespace from string inputs (category, description) before validation and storage.
- For monthly calculations, use the `YYYY-MM` prefix of the `date` field (e.g., `2026-08-09` → month `2026-08`).
- Do not accept numeric strings for `amount`. Accept only JSON numbers.
- Do not return monetary amounts as strings in responses.
