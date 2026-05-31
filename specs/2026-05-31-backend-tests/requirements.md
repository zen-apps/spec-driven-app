# Requirements — Backend tests (pytest) (Phase 3)

Lock in backend behavior by building a comprehensive pytest test suite that covers the FastAPI endpoints, agent invocation patterns, error handling, and helper/metric utility functions with Gemini and LangChain fully mocked.

Traces to: `specs/roadmap.md` → *Phase 3 — Backend tests (pytest)*.

## Scope

### In scope (roadmap baseline)

- **FastAPI Endpoint Testing (`FastAPI TestClient`)**:
  - **GET `/health`**: Assert it returns HTTP `200 OK` and json `{"status": "ok"}`.
  - **POST `/chat` (Success Path)**: Mock the agent execution to return a standard successful response, asserting that the endpoint returns HTTP `200 OK`, serialize and validate the response against the expected structure (Pydantic model under `"response"` and performance metrics under `"metrics"`).
  - **POST `/chat` (Error Path)**: Mock the agent/model call to raise an exception (e.g., authentication, API timeout, down state). Assert it returns HTTP `500 Internal Server Error`, contains a descriptive `detail` error message, a fully populated fallback `"response"` (with `task_completed=False`, `confidence=0.0`), and zeroed `"metrics"`.

- **Unit Testing for Helpers & Metrics**:
  - **Content Normalization**: Test `normalize_content` with various structures (strings, list of blocks, dictionaries, empty / None values).
  - **Accessors**: Test `get_final_answer_from_messages`, `get_structured_response`, and `get_final_answer` under successful and fallback scenarios.
  - **Metrics Summarization**: Test `summarize_agent_metrics` against mock message structures. Verify it correctly counts iterations, parses tool calls (names, arguments, message indices, steps), and aggregates token totals.

- **Mocking Strategy**:
  - Enforce zero external API calls or credentials dependency. Intercept at the agent execution level (`agent.invoke` or `run_agent`) to simulate complete agent runs with message lists, tool-call events, token usage metadata, and structured output.

- **Local and Container Executability**:
  - Add `pytest` and `httpx` to `backend/requirements.txt`.
  - Add convenient test targets to the root `Makefile` to run tests both locally and inside the backend Docker container (e.g. `docker-compose run`).

### Out of scope

- **Live Google Gemini Calls**: No live model/API calls are allowed in tests.
- **Frontend / UI Tests**: Testing the Streamlit UI or web browser logic is deferred.
- **Stateful Integration Tests**: Multi-turn history or persistence is out of scope since the backend remains stateless.

---

### Data / interface shape

The endpoints are expected to maintain the exact contract established in Phase 2.

#### `/health` Output:
```json
{"status": "ok"}
```

#### `/chat` Mock Input:
```json
{"message": "Test message"}
```

#### `/chat` Successful Mock Output Structure (HTTP 200):
```json
{
  "response": {
    "final_answer": "Mocked answer",
    "task_completed": true,
    "reasoning_summary": "Mocked reasoning",
    "tools_used": ["weather"],
    "key_findings": ["Fact 1"],
    "limitations": [],
    "recommended_next_steps": [],
    "confidence": 0.9
  },
  "metrics": {
    "tool_calls": [
      {
        "name": "weather",
        "args": {"location": "Delano"},
        "id": "call_1",
        "message_index": 1,
        "ai_step": 1
      }
    ],
    "token_totals": {
      "input_tokens": 100,
      "output_tokens": 50,
      "total_tokens": 150
    },
    "iterations": 1
  }
}
```

---

## Decisions

| Decision | Choice | Why |
|:---|:---|:---|
| **Test Client** | `fastapi.testclient.TestClient` powered by `httpx` | Canonical framework-approved client for writing clean, readable synchronous endpoint tests in FastAPI. |
| **Mocking Layer** | Mock `run_agent` directly in endpoint tests | Direct result of user interview feedback (Q2). Allows us to explicitly control and verify different agent execution trajectories (e.g., success, fallback, multi-step tool calls) at the boundary without loading Gemini. |
| **Test Directory** | `./backend/tests/` with standard `test_*.py` files | User interview feedback (Q3). Standard Python/pytest convention, cleanly separating testing assets from production runtime codebase in `./backend/app/`. |
| **Makefile targets** | Add `test-local` and `test-container` | Provides dual pathways for executing tests, ensuring seamless local developer testing as well as verification inside the identical container environment. |

---

## Context

- **Hermeticity**: Tests must run quickly, in isolation, and never require internet connectivity or Google credentials.
- **No Side Effects**: Ensure test execution does not write persistent artifacts to git-tracked folders.
- **Lint & Types**: Code style should align with the clean, well-commented style used in `backend/app/`.
