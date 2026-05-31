# Plan — Backend tests (pytest) (Phase 3)

The plan proceeds from updating dependencies and files layout, to helper/metrics unit testing, endpoint integration testing, and local/containerized validation.

## 1. Environment & Dependency Setup (`requirements.txt`, `Makefile`)

1. Update `backend/requirements.txt` to append:
   - `pytest==8.1.1`
   - `httpx==0.27.0` (required for FastAPI TestClient)
2. Add the following targets to the root `./Makefile` to streamline execution:
   - `test-local`: runs `pytest` in the local backend environment (e.g. within `./backend` directory).
   - `test-container`: runs `pytest` inside the backend Docker container via Docker Compose (e.g. `docker-compose run --rm backend pytest`).

## 2. Directory Layout & Test Client Hook (`backend/tests/`)

1. Create a `tests/` subdirectory under `./backend/` to separate production code from test code.
2. Create an empty `backend/tests/__init__.py` to make the directory a package.
3. Create `backend/tests/conftest.py` containing:
   - Reusable fixtures (e.g., an `app_client` fixture that instantiates and returns `TestClient(app)` from `app.main`).

## 3. Helper & Utility Unit Tests (`backend/tests/test_helpers.py`)

1. Write unit tests for `normalize_content`:
   - Verify it handles a plain string correctly.
   - Verify it handles a list of string blocks or dictionary blocks (with keys `text`, `content`, or generic dictionaries) correctly.
   - Verify it handles a `None` input cleanly by returning an empty string.
2. Write unit tests for accessors:
   - `get_final_answer_from_messages`: test extraction of the last non-empty `AIMessage` content.
   - `get_structured_response`: test extraction of `AutonomousAgentResponse` from results.
   - `get_final_answer`: test happy-path (retrieval from structured response) and fallback (retrieval from raw AIMessages).
3. Write comprehensive unit tests for `summarize_agent_metrics`:
   - Construct dummy LangChain message lists (including `HumanMessage`, `AIMessage` with `tool_calls` and `usage_metadata`, and `ToolMessage`).
   - Call `summarize_agent_metrics` with these structures.
   - Assert `tool_call_count`, `tool_call_sequence`, individual tool call lists (verifying `message_index` and `ai_step` logic), and aggregated `input_tokens`, `output_tokens`, and `total_tokens`.

## 4. FastAPI Endpoints Integration Tests (`backend/tests/test_main.py`)

1. **Liveness test (`GET /health`)**:
   - Send `GET /health` via the `TestClient`.
   - Assert response status is `200 OK` and body is exactly `{"status": "ok"}`.
2. **Chat Success path test (`POST /chat`)**:
   - Use `unittest.mock.patch` to intercept `app.main.run_agent`.
   - Make the mock return a representative LangChain result dict (comprising a mock list of messages, token metadata, and a populated `AutonomousAgentResponse` object under `"structured_response"`).
   - Send a `POST /chat` request with a sample prompt.
   - Assert response status is `200 OK`.
   - Assert response body contains correct keys `"response"` and `"metrics"`, matching the required structured schema and data.
3. **Chat Failure path test (`POST /chat` Exceptions)**:
   - Patch `app.main.run_agent` to raise a descriptive exception (e.g., `ValueError("API key invalid")`).
   - Send `POST /chat`.
   - Assert response status is `500 Internal Server Error`.
   - Assert response body matches the error schema: `"detail"` is populated, `"response"` fallback is correctly initialized (e.g. `task_completed=False`, `confidence=0.0`), and `"metrics"` are appropriately zeroed.

## 5. Verification & Final Validation

1. Run local tests: `make test-local` or `pytest backend/tests` directly to verify all tests pass.
2. Re-build Docker containers to pull in the new `requirements.txt` dependencies: `docker-compose build`.
3. Run containerized tests: `make test-container` or `docker-compose run --rm backend pytest` to verify the suite passes inside the Python container.
