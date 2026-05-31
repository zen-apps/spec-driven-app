# Roadmap

High-level implementation order, broken into small sequential phases. Each phase
becomes a feature branch in later SDD steps. The strategy is **backend-first,
vertical**: scaffold the repo, get the agent working end to end on the backend,
test it, then build the frontend on top, and finish with docs.

Mark a phase `[x] COMPLETE` (with a date) when it ships.

Completed phases have moved to [changelog.md](changelog.md) — this file tracks only open and upcoming work.

---

## Phase 5 — Tools-centric agent backend

Implement the new tools-centric agent backend based on `create_agent_tools.ipynb`, keeping existing tests and frontend integration intact (with necessary minimal adjustments).

> **TODO:** implement examples/create_agent_tools.ipynb in the backend for the demo instead of what is currently there. It’s more straightforward and better illustrates the tool chain concept.

- Re-implement the FastAPI backend agent to match the tool definition and calling patterns in `examples/create_agent_tools.ipynb`.
- Ensure all agent outputs still conform to the expected Pydantic structured schema.
- Keep the existing Streamlit frontend integration intact with minimal, clean adjustments.
- Update/adjust existing backend unit tests to ensure they continue to pass under the new implementation.
- Outcome: FastAPI backend updated with the new `create_agent_tools.ipynb` pattern, with passing tests and working frontend integration.

## Phase 6 — Polish & docs

Make the project reproducible by a student from a clean clone.

- Update `README.md` / `AGENTS.md` with run instructions, ports, the
  `docker-compose up` flow, and where credentials go.
- A short walkthrough tying the running app back to these specs (the SDD story).
- Outcome: clone → add credentials → `docker-compose up` → working demo, with
  the spec trail legible.
