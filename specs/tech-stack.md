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

- **Streamlit** — a single chat UI that talks to the backend over HTTP.
- Renders the agent's final answer plus a view of its **tool calls** and
  **structured output** / run metrics (token counts, iterations), since making
  the agent's reasoning visible is a teaching goal.
- Conversation state lives in Streamlit's per-session state (see Data model).

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
- Key libraries (see `examples/requirements.txt`): `langchain`,
  `langchain-google-genai`, plus `pydantic` for structured output.

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
- `docker-compose.yml` builds and runs `./backend` and `./frontend`, each on its
  own port, with `./credentials` mounted into the backend.
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
