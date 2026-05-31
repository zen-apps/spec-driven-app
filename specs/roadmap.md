# Roadmap

High-level implementation order, broken into small sequential phases. Each phase
becomes a feature branch in later SDD steps. The strategy is **backend-first,
vertical**: scaffold the repo, get the agent working end to end on the backend,
test it, then build the frontend on top, and finish with docs.

Mark a phase `[x] COMPLETE` (with a date) when it ships.

Completed phases have moved to [changelog.md](changelog.md) — this file tracks only open and upcoming work.

---

## Phase 5 — Polish & docs

Make the project reproducible by a student from a clean clone.

- Update `README.md` / `AGENTS.md` with run instructions, ports, the
  `docker-compose up` flow, and where credentials go.
- A short walkthrough tying the running app back to these specs (the SDD story).
- Outcome: clone → add credentials → `docker-compose up` → working demo, with
  the spec trail legible.
