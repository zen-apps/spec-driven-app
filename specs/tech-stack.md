# Tech Stack

The app is split into two services, each in its own Docker container, wired
together with docker-compose and each exposed on its own port. The guiding
principle is to keep the stack small and legible — this is a teaching project,
so every dependency should be explainable.

## Backend (`./backend`)

- **Language:** Python
- **Web framework:** FastAPI, run by **uvicorn** (`uvicorn[standard]`); serves a
  JSON API the frontend calls. The container listens on port `8000`.
- **Agent framework:** LangChain `1.3.0` — the agent is built with
  `create_agent` from `langchain.agents`, mirroring
  [`examples/create_agent.ipynb`](../examples/create_agent.ipynb) 1:1.
- **LLM:** Google **Gemini** (`gemini-3.5-flash`) via
  `langchain-google-genai` (`ChatGoogleGenerativeAI`).
  Credentials live in `./credentials` (gitignored) and are mounted into the
  backend container; `project` / `location` are configured as in the example.
- **Structured output:** the agent returns a validated **Pydantic** model
  (`response_format=...`) — `final_answer`, `task_completed`,
  `reasoning_summary`, `tools_used`, `key_findings`, `limitations`,
  `recommended_next_steps`, `confidence`.
- **Tools:** Python functions decorated with `@tool` (the example ships
  `run_sql`, `validate_answer`, `search_docs`, `save_artifact`, `weather`,
  `web_search` as demo placeholders). The backend exposes the same tool-calling
  pattern, including the run-metrics helpers (tool-call counts, token usage,
  agent iterations) from the notebook.

## Frontend (`./frontend`)

- **Framework:** Streamlit
- **Role:** a chat-style UI that sends user prompts to the backend API and
  renders the agent's response — both the `final_answer` and the structured
  fields / run metrics, so students can see the agent's tool use and reasoning
  summary.
- **State:** conversation state lives only in the Streamlit session (see
  Persistence below).

## Persistence

**None — the app is stateless.** There is no database. Each request to the
backend is independent, and any conversation history lives only in the
Streamlit session in the browser. This is a deliberate teaching choice: it keeps
the moving parts to two services and avoids a data-modeling detour.

> Database schema: N/A. If a future roadmap phase introduces persistence (e.g.
> SQLite for chat history), this section and a schema will be added then.

## Testing

- **Backend:** **pytest** — covers the FastAPI endpoints and the agent/tool
  logic with the **LLM mocked** (no live Gemini calls in tests).
- **Frontend:** validated manually by running the app and exercising the UI.

## Deployment & CI/CD

- **Run target:** **local `docker-compose up`** on a developer's machine. Each
  service builds from its own `Dockerfile`; docker-compose brings both up on
  separate ports.
- **Base image:** both services build from `python:3.12-slim`.
- **Ports:** the backend container listens on `8000` and is **published to the
  host on `8001`** — `8001` is the project's canonical backend host port (chosen
  during Phase 1 because host `8000` is commonly occupied). The frontend runs on
  `8501` (Streamlit default). The frontend reaches the backend over the compose
  network at `http://backend:8000`, supplied via the `BACKEND_URL` environment
  variable, so the host publish port is irrelevant to inter-service calls.
- **No cloud deploy and no CI/CD pipeline** for now — the teaching scope is kept
  tight. (A GitHub Actions test/lint step is a candidate for a later phase if
  the class wants it.)

## Package management

- Python dependencies per service via `requirements.txt` (pinned), matching the
  style of `examples/requirements.txt`. As of Phase 2, the pinned dependencies are:
  - **Backend (`./backend/requirements.txt`):**
    - `fastapi==0.136.3`
    - `uvicorn[standard]==0.48.0`
    - `langchain==1.3.0`
    - `langchain-community==0.4.1`
    - `langchain-google-genai==4.2.4`
    - `pydantic>=2.0`
  - **Frontend (`./frontend/requirements.txt`):**
    - `streamlit==1.58.0`

## Repository layout

```text
.
├── backend/          # FastAPI + LangChain agent (Python), own Dockerfile
├── frontend/         # Streamlit UI, own Dockerfile
├── credentials/      # Gemini credentials (gitignored), mounted into backend
├── examples/         # reference notebooks (create_agent.ipynb, sdd_rag.ipynb)
├── specs/            # spec-driven development docs
└── docker-compose.yml
```
