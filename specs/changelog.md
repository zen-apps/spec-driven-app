# Spec-Driven App Changelog

Completed roadmap phases, compressed to title, completion date, and outcome. Full
task-level detail lives in each phase's spec directory (linked where one exists) and in
git history. Open and upcoming work stays in [roadmap.md](roadmap.md).

Ordered newest phase first.

---

## Phase 1 — Repo skeleton & docker-compose
**Completed:** 2026-05-31 · **Spec:** [2026-05-31-repo-skeleton/](2026-05-31-repo-skeleton/)

Stood up the two-service shell — FastAPI backend and Streamlit frontend, each with a
`Dockerfile` and pinned requirements, wired together by `docker-compose.yml` on a shared
network so `docker-compose up` brings both up with responding `/health` endpoints;
implementation complete, manual QA pending.
