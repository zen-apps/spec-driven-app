# Roadmap

High-level build order for the reference agent app. Phases are **coarse and
sequential** — each becomes a feature branch in later SDD steps and gets its own
`specs/YYYY-MM-DD-<feature>/` with `requirements.md`, `plan.md`, and
`validation.md`. The build goes **inside-out**: a working, API-testable agent
first, then the UI, then full container integration.

Mark a phase `[x] COMPLETE` when its validation passes. This done-marker is read
and written by the other SDD skills (`sdd-feature-spec`, `sdd-implement-feature`,
`sdd-changelog`).

Completed phases have moved to [changelog.md](changelog.md) — this file tracks
only open and upcoming work.

## Phase 2 — Streamlit frontend [ ]

Build the chat UI that talks to the backend.

- Streamlit app in `./frontend` with a chat interface calling the backend's
  endpoint.
- Render the agent's final answer plus a view of its **tool calls** and
  **structured output / metrics**, since visible reasoning is a teaching goal.
- Conversation held in Streamlit session state.
- Frontend Dockerfile.
- Validation: manual — run frontend against a running backend, send a prompt,
  confirm the answer and tool/metric views display correctly.

## Phase 3 — Compose integration [ ]

Wire both services together for a one-command classroom setup.

- **Already in place from Phase 1:** `docker-compose.yml` with the **backend**
  service (host `8001` → container `8000`, `./credentials` mounted read-only) and
  a root `Makefile` (`make build` / `run` / `down`). Phase 3 builds on these
  rather than starting from scratch.
- Add the **frontend** service to `docker-compose.yml`, on its own port.
- Configure the frontend to reach the backend by its compose service name
  (`http://backend:8000`).
- Validation: manual — `docker-compose up` (or `make run`) brings up both
  services; a user chats with the agent end-to-end and sees tool calls +
  structured output. This satisfies the "runs end-to-end" success criterion in
  `mission.md`.

## Out of scope (post-roadmap)

Deferred unless explicitly prioritized later: persistence/database, automated
test suite, CI/CD, authentication, and any cloud deployment.
