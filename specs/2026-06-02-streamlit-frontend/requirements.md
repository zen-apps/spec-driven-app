# Requirements — Streamlit Frontend (Phase 2)

Build the chat UI that talks to the Phase 1 backend. This is a **frontend-only**
phase: it consumes the existing `POST /chat` contract and adds no backend code.

## Scope

### In scope

- A Streamlit app in `./frontend` with a single chat interface.
- Calls the backend's `POST /chat` endpoint with `{ "message": <user text> }`.
- Renders, per turn:
  - the agent's **final answer** as a chat bubble in the conversation thread;
  - a **tool calls view** for that turn, shown in a collapsible `st.expander`
    beneath the answer.
- Conversation history held in **Streamlit session state** for the life of the
  browser session (no server-side persistence).
- A **frontend `Dockerfile`** (build only — wiring into `docker-compose` is
  Phase 3, not this phase).

### Out of scope

- **Structured output view** (`AutonomousAgentResponse` fields) — explicitly
  dropped for this phase.
- **Run-metrics panel** (token usage, iterations) as a standalone view — not
  surfaced this phase beyond the tool-call data described below.
- **Per-call tool arguments and tool outputs** — the current `/chat` response
  does not expose them (see Decisions). Not shown this phase.
- Adding the frontend service to `docker-compose.yml` or pointing at the
  backend by compose service name — that is **Phase 3**.
- Multi-turn server-side context, auth, persistence, automated tests.

### Data available from `POST /chat`

The backend returns `ChatResponse` (`backend/app/schemas.py`):

| Field | Type | Used this phase? | Notes |
|-------|------|------------------|-------|
| `final_answer` | `str` | ✅ | Rendered as the assistant chat bubble. |
| `structured_response` | `dict` | ❌ | `AutonomousAgentResponse` dump — out of scope. |
| `metrics` | `dict` | ✅ (subset) | Source for the tool-calls view. |

The tool-calls view is built **only** from fields the API actually exposes in
`metrics` (`backend/app/metrics.py` → `build_api_metrics`):

| `metrics` field | Type | Meaning |
|-----------------|------|---------|
| `tool_call_sequence` | `list[str]` | Ordered tool names as invoked. |
| `tool_name_counts` | `dict[str,int]` | Per-tool invocation counts. |
| `tool_call_count` | `int` | Total tool invocations. |
| `unique_tools_used` | `int` | Distinct tools used. |

`metrics` also carries iteration/token fields; they are **not** displayed this
phase (out of scope above), though they remain available for Phase 3+.

## Decisions

- **Backend URL is hardcoded to `http://localhost:8001`** (the Phase 1 host-port
  mapping → container `8000`). Rationale: keeps Phase 2 dead-simple to read in
  class; the configurable/compose-service-name wiring is deliberately a Phase 3
  concern. Define it as a single named module-level constant so Phase 3 has one
  obvious line to change.
- **Tool-calls view uses only exposed metrics** (sequence, per-tool counts,
  totals). Per-call args + tool outputs are intentionally not shown because the
  `/chat` contract does not return them; surfacing those would require a backend
  change, which is out of scope for a frontend-only phase. (The backend already
  computes `tool_calls` + `get_tool_outputs` internally — a future backend phase
  can expose them without frontend rework.)
- **Layout: expanders under each answer.** Each assistant turn renders the final
  answer, then an `st.expander` (e.g. "🔧 Tool calls (N)") containing the
  ordered sequence and per-tool counts for that turn. Keeps the reasoning trail
  inline and per-response, which reads clearly for students.
- **Conversation state in `st.session_state`.** Each entry stores the user
  message, the assistant `final_answer`, and the tool-call data for that turn so
  history re-renders correctly on rerun.
- **No new dependencies beyond Streamlit + an HTTP client.** `requests` (or
  `httpx`) for the backend call; both are standard and teachable. Pin in
  `frontend/requirements.txt`.

## Context

- **Audience:** students learning AI agents across the stack. Code must be
  walk-through-simple with no hidden magic — favor obvious, linear Streamlit code
  over abstractions.
- **Tone of user-facing copy:** plain, friendly, instructional. Labels like
  "Ask the agent…", "🔧 Tool calls (N)" — clear over clever. No emoji overload.
- **Stack pointers:** `specs/tech-stack.md` (Frontend = Streamlit; backend host
  port `8001`); `backend/app/schemas.py` (`ChatResponse`); `backend/app/metrics.py`
  (`build_api_metrics`). Tool names the agent may call: `run_sql`,
  `validate_answer`, `search_docs`, `save_artifact`, `weather`, `web_search`.
- **Error handling:** if the backend is unreachable or returns a non-200, show a
  friendly inline error (e.g. "Couldn't reach the backend at <url> — is it
  running on port 8001?") rather than a stack trace, and keep the chat usable.
- **Repo convention:** mirror the backend's layout discipline — keep the app
  small and readable; one `frontend/app.py` plus `requirements.txt` and
  `Dockerfile` is enough.
