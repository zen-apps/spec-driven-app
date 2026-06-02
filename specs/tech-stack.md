# Tech Stack

Decisions here favor **simplicity and teachability** over production rigor, in
line with [`mission.md`](./mission.md). The goal is a reference agent app a class
can stand up, read, and extend.

## Overview

Two services, each in its own Docker container, wired together with
`docker-compose`. Each runs on its own port.

```text
frontend (Streamlit)  ──HTTP──▶  backend (FastAPI)  ──▶  LangChain agent  ──▶  Google Gemini
```

## Frontend

- **Streamlit** — a single chat UI (`frontend/app.py`) that talks to the backend
  over HTTP. Dependencies pinned in `frontend/requirements.txt`:
  `streamlit==1.54.0`, `requests==2.32.3`. No agent libraries live here — the
  frontend only calls the backend's `POST /chat`.
- **As built (through Phase 3):** renders the agent's **final answer** as a chat
  bubble, a collapsible **tool-calls view** (the ordered tool-call sequence and
  per-tool counts, drawn from the `metrics` the API exposes), and a collapsible
  **structured-output view** — the `🧩 Structured output` expander rendering the
  agent's `AutonomousAgentResponse` fields (`task_completed`, `confidence`,
  `reasoning_summary`, and the `tools_used` / `key_findings` / `limitations` /
  `recommended_next_steps` lists; `final_answer` is intentionally skipped to
  avoid duplicating the chat bubble). Conversation is held in Streamlit's
  per-session state (see Data model).
- **Still not surfaced (deferred teaching goals):**
  - **Run metrics** (token counts, iterations) as a standalone view.
  - **Per-call tool arguments and outputs** — the backend `/chat` response does
    not expose them today (`build_api_metrics` returns only counts, the tool-name
    sequence, and totals); surfacing them needs a backend change first.
- **Backend URL** is env-driven:
  `BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8001")`. It
  defaults to the Phase 1 host mapping for a standalone `streamlit run`, and is
  overridden to the compose service name (`http://backend:8000`) by the frontend
  service in `docker-compose.yml`.

## Backend

- **Python** with **FastAPI**, exposing a JSON API the frontend calls.
- Wraps a **LangChain agent** built with `create_agent`, following the pattern in
  [`examples/create_agent.ipynb`](../examples/create_agent.ipynb):
  - **Tools** — deterministic classroom stand-ins (e.g. `run_sql`,
    `search_docs`, `web_search`, `weather`, `validate_answer`, `save_artifact`).
    No real I/O or arbitrary code execution.
  - **Structured output** — a Pydantic response model (e.g.
    `AutonomousAgentResponse`) is the agent's validated final business output.
  - **Run metrics** — tool-call counts, agent iterations, and token usage are
    extracted from the message trace and returned to the frontend.

## LLM / AI

- **Google Gemini** via `langchain-google-genai` (`ChatGoogleGenerativeAI`),
  matching the notebook (model e.g. `gemini-3.5-flash`).
- **Auth: GCP service-account JSON.** The key file is mounted from the
  gitignored `./credentials` directory; the backend reads project/location from
  config. Credentials are never committed and never logged.
- Key libraries (pinned in `backend/requirements.txt` to match
  `examples/requirements.txt`): `langchain==1.3.0`,
  `langchain-google-genai==4.2.4`, plus `pydantic` for structured output, and the
  serving layer `fastapi` + `uvicorn[standard]`.
- **Configuration** is via environment variables, with notebook-matching defaults
  in `backend/app/config.py`: `GEMINI_MODEL` (`gemini-3.5-flash`), `GCP_PROJECT`
  (`zen-general-377713`), `GCP_LOCATION` (`global`), `GEMINI_TEMPERATURE` (`1.0`),
  and `GOOGLE_APPLICATION_CREDENTIALS` (path to the mounted key). Nothing is
  hardcoded into the agent module.

## Data model

**Stateless — no database.** This is deliberate: a real DB would add infra that
distracts from the lesson.

- The "data" the agent reasons over is the **deterministic tool stand-ins** in
  the backend (curated sales facts, doc summaries, fake web results). These are
  Python constants, not a queried store.
- **Conversation state** is held only in the frontend's Streamlit session for
  the life of the browser session. Nothing is persisted server-side; restarting
  a service clears state.
- If persistence is ever wanted, it is a future roadmap item, not part of the
  core build.

## Testing

- **Manual validation only.** No automated test suite for the core build.
- Each feature's `validation.md` documents the **manual steps** to verify it
  (e.g. "run `docker-compose up`, send prompt X, confirm tool Y is called and
  structured output includes Z").
- Per `AGENTS.md`: do not claim something is validated unless it was actually
  exercised through these manual steps.

## Deployment & CI/CD

- **Local `docker-compose` only.** Target environment is a developer's machine in
  the classroom.
- `docker-compose.yml` defines **both services** (Phase 3): `backend`
  (host `8001` → container `8000`, `./credentials` mounted read-only) and
  `frontend` (host `8501` → container `8501`, `BACKEND_URL=http://backend:8000`,
  `depends_on: backend`). The frontend reaches the backend by compose service
  name over the internal network — no host port is used for service-to-service
  traffic. **Manual QA still owed:** Phase 3 is implementation-complete, but the
  frontend image build and the end-to-end walkthrough (`make build` /
  `docker compose up`, browser chat) have **not yet been exercised**; the
  sanity/QA gates in
  [`specs/2026-06-02-compose-structured-output/validation.md`](./2026-06-02-compose-structured-output/validation.md)
  remain unchecked.
- The backend is published on **host port `8001`** (→ container `8000`) because
  host `8000` is taken by another local service. Adjust the mapping in
  `docker-compose.yml` if your machine differs.
- A root **`Makefile`** wraps the common commands: `make build` / `make run`
  (build + `up`) / `make down`. (It also has a `copy-skills` target unrelated to
  the app.)
- **No CI/CD pipeline.** Keep the setup transparent and dependency-free.

## Repository layout

```text
.
├── backend/            # FastAPI + LangChain agent (Python)
├── frontend/           # Streamlit UI
├── credentials/        # Gemini service-account JSON (gitignored)
├── examples/           # reference notebooks (agent + RAG)
├── specs/              # SDD docs (this directory)
└── docker-compose.yml
```
