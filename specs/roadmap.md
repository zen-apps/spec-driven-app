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

## Phase 3 — Compose integration + structured-output view [x] COMPLETE (implementation; manual QA pending)

Wire both services together for a one-command classroom setup, and complete the
frontend's reasoning views.

- **Already in place from Phase 1:** `docker-compose.yml` with the **backend**
  service (host `8001` → container `8000`, `./credentials` mounted read-only) and
  a root `Makefile` (`make build` / `run` / `down`). Phase 3 builds on these
  rather than starting from scratch.
- Add the **frontend** service to `docker-compose.yml`, on its own port.
- Configure the frontend to reach the backend by its compose service name
  (`http://backend:8000`).
- **Folded in from Phase 2 (replan 2026-06-02):** add the **structured-output
  view** to the frontend — render the agent's `AutonomousAgentResponse` (the
  `structured_response` the `/chat` API already returns) so the end-to-end demo
  shows it, satisfying `mission.md` success criterion #1. Phase 2 intentionally
  shipped final answer + tool calls only; this completes the promised reasoning
  views. (The tool-calls view stays names/sequence/counts — exposing per-call
  args/outputs is explicitly **not** scheduled; see `tech-stack.md` Frontend.)
- **Carried over from Phase 2:** the `frontend/Dockerfile` exists but its image
  build was not validated in Phase 2 (the Makefile builds only compose services,
  and the frontend wasn't in compose yet). Validate the frontend image builds
  here, via `make build` once the service is added.
- Validation: manual — `docker-compose up` (or `make run`) brings up both
  services; a user chats with the agent end-to-end and sees tool calls +
  structured output. This satisfies the "runs end-to-end" success criterion in
  `mission.md`.

## Status — core build complete (manual QA pending)

The inside-out core build (Phase 1 backend → Phase 2 frontend → Phase 3 compose
integration + structured-output view) is **implementation-complete**. The agent
runs as an API, the Streamlit UI renders final answer + tool calls + structured
output, and `docker-compose.yml` wires both services for a one-command setup.

**One item is still owed before this is truly done:** the Phase 3 **manual QA**
walkthrough — `make build` / `docker compose up`, a browser chat end-to-end, and
the frontend image build — has not been exercised yet (its
[`validation.md`](2026-06-02-compose-structured-output/validation.md) gates are
unchecked). Until that passes, `mission.md` success criterion #1 ("runs
end-to-end") is met only in code, not demonstrated.

No further core-build phases are planned. The next candidates, if prioritized,
come from the deferred list below.

## Out of scope (post-roadmap)

Deferred unless explicitly prioritized later: persistence/database, automated
test suite, CI/CD, authentication, and any cloud deployment.
