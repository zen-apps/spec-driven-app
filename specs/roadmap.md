# Roadmap

High-level implementation order, broken into small sequential phases. Each phase
becomes a feature branch in later SDD steps. The strategy is **backend-first,
vertical**: scaffold the repo, get the agent working end to end on the backend,
test it, then build the frontend on top, and finish with docs.

Mark a phase `[x] COMPLETE` (with a date) when it ships.

Completed phases have moved to [changelog.md](changelog.md) — this file tracks only open and upcoming work.

---

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
