# Requirements — Repo skeleton & docker-compose (Phase 1)

Stand up the two-service shell so `docker-compose up` brings both services up and
each `/health` responds. **Repo skeleton only — no agent logic, no LangChain, no
Gemini wiring.** Those arrive in Phase 2.

Traces to: `specs/roadmap.md` → *Phase 1 — Repo skeleton & docker-compose*.

## Scope

### In scope (roadmap baseline only)

- `./backend` — FastAPI app exposing a `GET /health` endpoint, its own
  `Dockerfile`, and a pinned `requirements.txt`.
- `./frontend` — Streamlit app with a single minimal page, its own `Dockerfile`,
  and a pinned `requirements.txt`.
- `docker-compose.yml` at the repo root — builds both services, publishes each on
  its own host port, and places both on a shared compose network so the frontend
  can reach the backend by service name in later phases.
- Repo hygiene: confirm `./credentials` and Python build artifacts are gitignored.

### Out of scope (deferred to later phases)

- Any LangChain / Gemini / agent logic, tools, or structured output (Phase 2).
- Frontend actually calling the backend `/health` or rendering agent replies — the
  Phase 1 frontend is a static placeholder page only (Phase 4 builds the real UI).
- pytest / automated tests (Phase 3).
- Helper `make` targets for the app, `.env` scaffolding, or any new dependency
  beyond FastAPI + uvicorn (backend) and Streamlit (frontend).

### Data / interface shape

| Service  | Endpoint / page | Contract |
|----------|-----------------|----------|
| backend  | `GET /health`   | `200` with JSON `{"status": "ok"}` (container `8000`, published on host `8001`) |
| frontend | root page       | Renders a minimal placeholder (title + one line of text) |

## Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Ports | backend container `8000` published on host `8001`; frontend `8501:8501` (Streamlit default) | Host `8000` is occupied by another container on the dev machine, so the backend is published on `8001`; the container port and inter-service URL stay `8000`. Confirmed by user. |
| `/health` response | JSON `{"status": "ok"}` (not plain text) | A clean contract the frontend and Phase 3 tests can assert on. |
| Dependency pinning | Pin versions in each `requirements.txt` | Matches the pinned-deps principle in `tech-stack.md` and `examples/requirements.txt`. |
| Base image | `python:3.12-slim` for both Dockerfiles | Small, legible images for a teaching repo. |
| Inter-service networking | Shared compose network; frontend reaches backend by service name (`backend`) | Wires connectivity now so Phase 4 frontend can call the API with no compose changes. |
| New dependencies | None beyond FastAPI + uvicorn and Streamlit | LangChain/Gemini deferred to Phase 2 per roadmap. |

## Context

- **Teaching repo.** Files should read cleanly and stay continuous with the
  `examples/` style; keep comments light and purposeful — the specs carry the
  narrative, not verbose inline prose.
- **Tech stack** is fixed by `specs/tech-stack.md`: Python, FastAPI (backend),
  Streamlit (frontend), per-service pinned `requirements.txt`, local
  `docker-compose up` as the only run target. No database (the app is stateless).
- **Existing conventions to follow:** repo layout in `README.md` / `tech-stack.md`
  (`backend/`, `frontend/`, `credentials/`, root `docker-compose.yml`); the root
  `Makefile` is reserved for skill-copying and is not the place for app commands in
  this phase.
- **Open question (none blocking):** Streamlit must bind to `0.0.0.0` and run
  headless inside the container to be reachable from the host — handled in the
  frontend Dockerfile/run command.
