# Plan — Backend Agent Core (Phase 1)

Task groups are ordered to keep the agent runnable end-to-end as early as
possible. Each group is independently implementable. All Python lives under
`./backend`. Mirror [`examples/create_agent.ipynb`](../../examples/create_agent.ipynb)
verbatim where noted — do not redesign the agent.

## 1. Project skeleton & dependencies

1. Create the `backend/` package layout:
   ```text
   backend/
   ├── app/
   │   ├── __init__.py
   │   ├── config.py        # settings: model, project, location, creds path
   │   ├── tools.py         # the 6 deterministic tools + demo constants
   │   ├── agent.py         # LLM + create_agent wiring + invoke helper
   │   ├── metrics.py       # notebook metrics/content helpers
   │   ├── schemas.py       # AutonomousAgentResponse + API request/response models
   │   └── main.py          # FastAPI app + POST /chat
   ├── requirements.txt
   └── Dockerfile
   ```
2. Write `backend/requirements.txt`: pin the agent libs from
   `examples/requirements.txt` that are actually imported (`langchain`,
   `langchain-google-genai`, and their needed peers) plus `fastapi` and
   `uvicorn[standard]`. No other additions.
3. Confirm `credentials/` is gitignored at the repo root; add an entry if
   missing. Never commit key material.

## 2. Config

1. In `app/config.py`, read from environment with notebook-matching defaults:
   `GEMINI_MODEL` (`gemini-3.5-flash`), `GCP_PROJECT` (`zen-general-377713`),
   `GCP_LOCATION` (`global`), and `GOOGLE_APPLICATION_CREDENTIALS` /
   credentials file path pointing into `./credentials`.
2. Keep it simple and typed (plain module constants or a small dataclass) — no
   new dependency. Document each setting with a one-line comment.

## 3. Tools (port from notebook)

1. Copy the demo data constants verbatim into `app/tools.py`:
   `DEMO_SALES_SCHEMA`, `DEMO_TOP_REVENUE_PRODUCTS`, `DEMO_TOTAL_REVENUE`,
   `SDD_DOC_SUMMARY`, `WEB_SEARCH_RESULTS`.
2. Port all six `@tool` functions unchanged: `run_sql`, `validate_answer`,
   `search_docs`, `save_artifact`, `weather`, `web_search`. Keep docstrings —
   they are the lesson and the tool descriptions the model sees.
3. Export a `TOOLS` list in notebook order.

## 4. Structured output & metrics

1. In `app/schemas.py`, define `AutonomousAgentResponse` exactly as the notebook
   (all 8 fields, same descriptions).
2. In `app/metrics.py`, port the helpers verbatim: `normalize_content`,
   `get_final_answer_from_messages`, `get_structured_response`,
   `get_final_answer`, `summarize_agent_metrics`, `get_tool_outputs`.
3. Decide the JSON-serializable metrics subset returned by the API (counts,
   `tool_name_counts`, `tool_call_sequence`, `agent_iterations`, token totals,
   `token_usage_by_step`) — exclude non-serializable objects like the raw
   `structured_response` instance (return its `model_dump()` instead).

## 5. Agent wiring

1. In `app/agent.py`, build the `ChatGoogleGenerativeAI` LLM from `config`
   (model/project/location, `temperature=1.0` as in the notebook).
2. Build the agent with `create_agent(model=llm, tools=TOOLS,
   response_format=AutonomousAgentResponse, system_prompt=...)` using the
   notebook's system prompt verbatim.
3. Provide a `run_agent(message: str) -> dict` helper that invokes the agent
   with `recursion_limit=50` and returns the raw `result` dict.

## 6. API: `POST /chat`

1. In `app/schemas.py`, add API models: `ChatRequest { message: str }` and
   `ChatResponse { final_answer: str, structured_response: dict, metrics: dict }`.
2. In `app/main.py`, create the FastAPI app and the `POST /chat` handler:
   call `run_agent`, run `summarize_agent_metrics`, assemble the JSON-safe
   response (structured response via `model_dump()`, metrics subset from group 4).
3. Handle the no-credentials / agent-error case with a clear HTTP error that
   does **not** leak credential contents or paths beyond what's safe.

## 7. Dockerfile

1. Write `backend/Dockerfile`: slim Python base, install
   `backend/requirements.txt`, copy `app/`, expose the backend port, run
   `uvicorn app.main:app`. (Built/run for real in Phase 3; authored now.)
2. Document the expectation that `./credentials` is mounted at runtime (not
   baked into the image).

## 8. Manual validation

1. Work through [`validation.md`](./validation.md): run the backend locally,
   `POST /chat` with the notebook's multi-tool prompt, confirm tools fire,
   structured output is well-formed, and metrics come back.
2. Mark Phase 1 `[x] COMPLETE` in [`roadmap.md`](../roadmap.md) only after the
   manual validation passes.
