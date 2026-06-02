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

## Open follow-ups

- **Phase 3 manual QA** (owed) — the now-archived Phase 3 shipped its
  implementation but its end-to-end walkthrough and frontend image build have
  **not been exercised**; the gates in
  [`validation.md`](2026-06-02-compose-structured-output/validation.md) remain
  unchecked. Until they pass, `mission.md` success criterion #1 ("runs
  end-to-end") is met only in code, not demonstrated. See
  [changelog.md](changelog.md) → Phase 3.

## Status — core build complete

The inside-out core build (Phase 1 backend → Phase 2 frontend → Phase 3 compose
integration + structured-output view) is **implementation-complete**: the agent
runs as an API, the Streamlit UI renders final answer + tool calls + structured
output, and `docker-compose.yml` wires both services for a one-command setup.
No further core-build phases are planned; the next candidates, if prioritized,
come from the deferred list below. (The one item still owed is the Phase 3
manual QA — see "Open follow-ups" above.)

## Out of scope (post-roadmap)

Deferred unless explicitly prioritized later: persistence/database, automated
test suite, CI/CD, authentication, and any cloud deployment.
