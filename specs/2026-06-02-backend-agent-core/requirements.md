# Requirements — Backend Agent Core (Phase 1)

Stand up the FastAPI backend that wraps the LangChain agent so it is testable
over HTTP **before any UI exists**. This is the inside-out first slice from
[`roadmap.md`](../roadmap.md) Phase 1.

## Scope

### In scope

| Area | What it includes |
|------|------------------|
| **Chat endpoint** | A single `POST /chat` route that accepts a user message and returns the agent's structured answer plus run metrics. |
| **Agent** | LangChain `create_agent` wired to Google Gemini (`ChatGoogleGenerativeAI`), mirroring [`examples/create_agent.ipynb`](../../examples/create_agent.ipynb) exactly. |
| **Tools** | All **six** deterministic teaching tools, ported verbatim from the notebook: `run_sql`, `search_docs`, `web_search`, `weather`, `validate_answer`, `save_artifact`. No real I/O or arbitrary code execution. |
| **Structured output** | The `AutonomousAgentResponse` Pydantic model from the notebook is the agent's validated final business output. |
| **Run metrics** | Tool-call counts, `tool_name_counts`, agent iterations, and token usage (input/output/total) extracted from `result["messages"]` via the notebook's `summarize_agent_metrics` helper, returned in the API response. |
| **Credentials** | Backend reads the GCP service-account JSON from the gitignored `./credentials` directory and project/location/model from config; never logged, never committed. |
| **Backend Dockerfile** | A Dockerfile that builds and runs the FastAPI app (image is built/run for real in Phase 3, but authored here). |

### Out of scope (deferred)

- **Conversation history / multi-turn.** `POST /chat` is single-message and
  stateless for Phase 1 (matches the stateless data model in
  [`tech-stack.md`](../tech-stack.md)). Multi-turn is a frontend concern.
- **Full tool-call trace in the response.** Metrics include tool-call *counts*
  and the tool-name sequence, but rendering the detailed per-call trace is a
  **Phase 2** UI concern; the response stays focused for now.
- **Streamlit frontend** (Phase 2), **docker-compose wiring** (Phase 3).
- **Health-check endpoint** — deferred to Phase 3 when compose needs a readiness
  probe (not selected for Phase 1 scope).
- Persistence, auth, automated test suite, CI/CD (post-roadmap, per roadmap).

### `AutonomousAgentResponse` shape (from the notebook — do not redesign)

| Field | Type | Meaning |
|-------|------|---------|
| `final_answer` | `str` | Direct answer to the user's request. |
| `task_completed` | `bool` | Whether the agent completed the request. |
| `reasoning_summary` | `str` | User-facing summary of steps (no hidden chain-of-thought). |
| `tools_used` | `List[str]` | Names of tools actually used. |
| `key_findings` | `List[str]` | Facts/observations supporting the answer. |
| `limitations` | `List[str]` | Missing info or uncertainty. |
| `recommended_next_steps` | `List[str]` | Suggested next steps. |
| `confidence` | `float` | 0.0–1.0. |

## Decisions

- **Follow the notebook exactly.** The agent, tools, system prompt,
  `AutonomousAgentResponse`, and the metrics helpers
  (`normalize_content`, `get_final_answer`, `summarize_agent_metrics`,
  `get_tool_outputs`) are ported from `examples/create_agent.ipynb` with minimal
  edits. The notebook is the source of truth; the API is a thin HTTP wrapper
  around it. *(User answer: "Follow notebook exactly".)*
- **All six tools, full metrics in the response.** The endpoint returns both the
  structured `AutonomousAgentResponse` and the run-metrics summary (tool-call
  counts, iterations, token totals) so the agent's behaviour is inspectable over
  HTTP before the UI exists. *(User answers: "All 6 example tools", "Full metrics
  in response".)*
- **Single `POST /chat` route.** Minimal API surface for Phase 1 — request takes
  a user message string; response carries `final_answer`, the structured
  response object, and the metrics summary.
- **Config, not hardcoding.** Model name, GCP `project`, `location`, and the
  credentials file path are read from environment / config rather than baked into
  the agent module, so the same code runs in the notebook's project and in
  compose later. Defaults match the notebook (`gemini-3.5-flash`,
  `project="zen-general-377713"`, `location="global"`).

## Context

- **Teaching-first clarity.** Code is a lesson artifact: readable, commented, and
  walk-through-able over cleverness. Keep the module structure obvious (e.g.
  `tools.py`, `agent.py`, `metrics.py`, `main.py`) so a class can trace the
  request → agent → tools → structured output → metrics path live.
  *(User answer: "Teaching-first clarity".)*
- **No new dependencies beyond the agreed stack.** Reuse the pinned libraries in
  [`examples/requirements.txt`](../../examples/requirements.txt) (`langchain`,
  `langchain-google-genai`, etc.; `pydantic` comes via langchain). The **only**
  additions are the web-serving layer already mandated by `tech-stack.md` and the
  roadmap — **`fastapi`** and an ASGI server (**`uvicorn`**). These are the agreed
  backend framework, not net-new scope; pin them in `backend/requirements.txt`.
  Anything beyond this set needs explicit user approval. *(User answer: "No new
  dependencies".)*
- **Patterns to follow:** the notebook's helper functions and tool definitions
  verbatim; `tech-stack.md` repository layout (`backend/`); `AGENTS.md` testing
  expectations (manual validation, don't claim validated unless exercised).
- **Credentials safety** (`AGENTS.md` Safety & Boundaries): the
  service-account JSON lives only in the gitignored `./credentials` dir; the
  backend must not log it or echo it in any response or error.
