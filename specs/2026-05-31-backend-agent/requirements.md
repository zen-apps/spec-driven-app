# Requirements — Backend: full LangChain agent endpoint (Phase 2)

Bring up the complete LangChain agent on the FastAPI backend, exposing a `POST /chat` endpoint that executes the agent with standard demo tools, returns structured response data matching the notebook reference, and collects execution metrics (tokens, tool calls, and iterations).

Traces to: `specs/roadmap.md` → *Phase 2 — Backend: full LangChain agent endpoint*.

## Scope

### In scope (roadmap baseline)

- **Gemini & LangChain Integration**:
  - Add required Python packages (`langchain==1.3.0`, `langchain-google-genai==4.2.4`, etc.) to `backend/requirements.txt`.
  - Wire `ChatGoogleGenerativeAI` (`gemini-3.5-flash`) to the backend.
  - Load project credentials from the mounted `./credentials` directory and handle project/location env-var configuration with defaults.
- **Autonomous Agent Creation**:
  - Build the agent via `create_agent` from `langchain.agents` matching `create_agent.ipynb`.
  - Include the system prompt, `recursion_limit` config parameter, and support for the structured response schema.
- **Pydantic Response Model**:
  - Define `AutonomousAgentResponse` (Pydantic BaseModel) containing fields: `final_answer`, `task_completed`, `reasoning_summary`, `tools_used`, `key_findings`, `limitations`, `recommended_next_steps`, `confidence`.
- **Demo Tools**:
  - Define and decorate `@tool` helper functions matching the Jupyter notebook exactly: `run_sql`, `validate_answer`, `search_docs`, `save_artifact`, `weather`, `web_search`.
- **FastAPI Endpoints**:
  - Expose a `POST /chat` endpoint.
  - Validate and capture run metrics (token counts, tool-call details, iteration count) using helpers adapted from `create_agent.ipynb`.
- **Robust Error Handling**:
  - Catch API-level failures gracefully and return a structured fallback response with HTTP 500 to keep responses readable and parseable.

### Out of scope

- **Streamlit Chat Integration**: Frontend rendering of the structured fields and metrics is deferred to Phase 4 (Streamlit placeholder is untouched).
- **Unit Tests**: Writing pytest suites or mocking Gemini behavior is deferred to Phase 3.
- **Persistence / Chat History**: Multi-turn conversation state is handled entirely on the client-side/frontend in Phase 4. Every backend request in this phase is an independent, stateless invocation.

---

### Data / interface shape

#### `POST /chat` Request

- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "message": "Search the web for \"latest on ai\" if it is hotter than 50 degrees in Delano."
  }
  ```

#### `POST /chat` Response (Success: HTTP 200)

```json
{
  "response": {
    "final_answer": "The latest on AI is OpenCode, a free alternative to Claude Code. It is hotter than 50 degrees in Delano (foggy, 60°F).",
    "task_completed": true,
    "reasoning_summary": "Checked the weather in Delano, found it is 60°F, then searched the web for the latest on AI.",
    "tools_used": ["weather", "web_search"],
    "key_findings": [
      "Weather in Delano is 60°F (greater than 50°F).",
      "Latest on AI is OpenCode which is free."
    ],
    "limitations": [],
    "recommended_next_steps": ["Try out OpenCode on your local system."],
    "confidence": 0.95
  },
  "metrics": {
    "tool_calls": [
      {
        "name": "weather",
        "args": {"location": "Delano"},
        "id": "call_weather_1",
        "message_index": 1,
        "ai_step": 1
      },
      {
        "name": "web_search",
        "args": {"query": "latest on ai"},
        "id": "call_search_1",
        "message_index": 3,
        "ai_step": 2
      }
    ],
    "token_totals": {
      "input_tokens": 1250,
      "output_tokens": 420,
      "total_tokens": 1670
    },
    "iterations": 3
  }
}
```

#### `POST /chat` Response (Failure: HTTP 500)

When an external service call fails, we return an HTTP 500 containing a structured fallback schema:

```json
{
  "detail": "Failed to call Google Gemini API: Authentication error.",
  "response": {
    "final_answer": "Error: Failed to process the request due to a downstream API failure.",
    "task_completed": false,
    "reasoning_summary": "Attempted to initialize the Gemini model, but an error occurred during setup.",
    "tools_used": [],
    "key_findings": [],
    "limitations": ["Downstream API is unavailable or misconfigured."],
    "recommended_next_steps": [
      "Check your credentials mount in ./credentials",
      "Verify GOOGLE_APPLICATION_CREDENTIALS in your environment.",
      "Check GEMINI_PROJECT and GEMINI_LOCATION values."
    ],
    "confidence": 0.0
  },
  "metrics": {
    "tool_calls": [],
    "token_totals": {
      "input_tokens": 0,
      "output_tokens": 0,
      "total_tokens": 0
    },
    "iterations": 0
  }
}
```

---

## Decisions

| Decision | Choice | Why |
|:---|:---|:---|
| **API Contract** | Request contains `{"message": str}`. Response wraps the Pydantic model under `"response"` and performance metrics under `"metrics"`. | Direct result of user interview feedback (Q1). Isolates execution metadata from actual validated outputs, keeping UI parsers clean while exposing agent details. |
| **Credentials & Configuration** | Read `GEMINI_PROJECT` and `GEMINI_LOCATION` from environment variables, falling back to `"zen-general-377713"` and `"global"` if unset. | User interview choice (Q2). Maximizes portability: students can override values via Docker Compose/`.env`, while out-of-the-box demo setup works seamlessly. |
| **Error Format** | Return HTTP 500 containing both a descriptive `detail` message and a structured `response` fallback schema matching `AutonomousAgentResponse`. | User interview choice (Q3). Allows the Streamlit UI to display errors gracefully within the structured cards instead of crashing, offering clear debug guidance. |
| **Docker Mounts** | Mount `./credentials` from the host repository root into `/app/credentials` in the backend container. | Secures credentials outside git-tracked folders, ensuring safety while keeping deployment self-contained inside `docker-compose`. |

---

## Context

- **Continuous Style**: The backend Python files must be formatted neatly, keeping comments clear and structured. Re-use notebook utility functions (`normalize_content`, `summarize_agent_metrics`, etc.) exactly as defined to avoid subtle logical divergence.
- **Stateless Design**: Because the backend handles every request as a clean, single-turn execution, we do not need complex session tracking on the FastAPI side yet.
- **Dependencies**: The primary dependencies are `langchain==1.3.0` and `langchain-google-genai==4.2.4`. Any other transitive helper libraries from `examples/requirements.txt` should be added to ensure the container builds cleanly.
