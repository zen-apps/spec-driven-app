# Roadmap

High-level implementation order, broken into small sequential phases. Each phase
becomes a feature branch in later SDD steps. The strategy is **backend-first,
vertical**: scaffold the repo, get the agent working end to end on the backend,
test it, then build the frontend on top, and finish with docs.

Mark a phase `[x] COMPLETE` (with a date) when it ships.

---

## Phase 1 — Repo skeleton & docker-compose [x] COMPLETE (implementation; manual QA pending) — 2026-05-31

Stand up the two-service shell. **Repo skeleton only — no agent logic yet.**

- `./backend`: FastAPI app with a `/health` endpoint, `Dockerfile`,
  pinned `requirements.txt`.
- `./frontend`: Streamlit app with a minimal page, `Dockerfile`,
  pinned `requirements.txt`.
- `docker-compose.yml`: builds both services, each on its own port, on a shared
  compose network so the frontend can reach the backend.
- Outcome: `docker-compose up` brings both services up; each `/health` responds.

## Phase 2 — Backend: full LangChain agent endpoint

Bring up the complete agent in one pass, matching
[`examples/create_agent.ipynb`](../examples/create_agent.ipynb) — **structured
output AND all demo tools at once.**

- Wire `ChatGoogleGenerativeAI` (`gemini-3.5-flash`) using credentials mounted
  from `./credentials`, configured (`project`/`location`) as in the example.
- Build the agent with `create_agent`, including:
  - the `AutonomousAgentResponse` Pydantic `response_format` (final_answer,
    task_completed, reasoning_summary, tools_used, key_findings, limitations,
    recommended_next_steps, confidence);
  - all `@tool` functions from the example (`run_sql`, `validate_answer`,
    `search_docs`, `save_artifact`, `weather`, `web_search`);
  - the system prompt and `recursion_limit` from the notebook.
- Expose a `POST /chat` endpoint returning the structured response plus run
  metrics (tool-call counts/sequence, agent iterations, token usage) via the
  notebook's metrics helpers.
- Outcome: a request to `/chat` runs the agent end to end — tool calls,
  structured JSON, and metrics all returned.

## Phase 3 — Backend tests (pytest)

Lock in backend behavior with the LLM mocked.

- pytest covering `/health`, the `/chat` request/response shape,
  structured-output validation, and tool-call handling — **Gemini mocked**, no
  live LLM calls.
- Outcome: `pytest` passes locally and in the backend container.

## Phase 4 — Frontend: chat UI against the real backend

Build the real Streamlit experience on top of the working backend.

- Streamlit chat interface that posts to `/chat` and renders the agent reply.
- Display the structured fields and run metrics (tools used, key findings,
  reasoning summary, confidence, token usage) so the agent's work is visible.
- Conversation state held in the Streamlit session.
- Outcome: a user can chat with the agent through the UI end to end via
  `docker-compose up`.

## Phase 5 — Polish & docs

Make the project reproducible by a student from a clean clone.

- Update `README.md` / `AGENTS.md` with run instructions, ports, the
  `docker-compose up` flow, and where credentials go.
- A short walkthrough tying the running app back to these specs (the SDD story).
- Outcome: clone → add credentials → `docker-compose up` → working demo, with
  the spec trail legible.
