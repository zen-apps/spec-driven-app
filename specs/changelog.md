# Spec-Driven App Changelog

Completed roadmap phases, compressed to title, completion date, and outcome. Full
task-level detail lives in each phase's spec directory (linked where one exists) and in
git history. Open and upcoming work stays in [roadmap.md](roadmap.md).

Ordered newest phase first.

---

## Phase 2 — Backend: full LangChain agent endpoint
**Completed:** 2026-05-31 · **Spec:** [specs/2026-05-31-backend-agent/](2026-05-31-backend-agent/)

Implemented the complete autonomous LangChain agent using Google Gemini (`gemini-3.5-flash`) with structured output and six demo tools, exposing a robust `POST /chat` endpoint with run metrics; implementation complete, manual QA pending.

## Phase 1 — Repo skeleton & docker-compose
**Completed:** 2026-05-31 · **Spec:** [specs/2026-05-31-repo-skeleton/](2026-05-31-repo-skeleton/)

Stood up the two-service shell — FastAPI backend and Streamlit frontend, each with a
`Dockerfile` and pinned requirements, wired together by `docker-compose.yml` on a shared
network so `docker-compose up` brings both up with responding `/health` endpoints;
implementation complete, manual QA pending.
