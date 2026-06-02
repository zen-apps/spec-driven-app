# Spec-Driven Agent App Changelog

Completed roadmap phases, compressed to title, completion date, and outcome. Full
task-level detail lives in each phase's spec directory (linked where one exists) and in
git history. Open and upcoming work stays in [roadmap.md](roadmap.md).

Ordered newest phase first.

---

## Phase 1 — Backend agent core
**Completed:** 2026-06-02 · **Spec:** [specs/2026-06-02-backend-agent-core/](2026-06-02-backend-agent-core/)

Stood up the FastAPI backend wrapping a LangChain agent on Google Gemini, with deterministic teaching tools, Pydantic structured output and run metrics, and a backend Dockerfile — making the agent API-testable over HTTP before any UI exists.
