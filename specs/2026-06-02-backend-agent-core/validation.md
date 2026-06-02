# Validation — Backend Agent Core (Phase 1)

Per [`tech-stack.md`](../tech-stack.md) and `AGENTS.md`, Phase 1 is validated
**manually**. There is no automated test suite. Do not mark the phase complete
unless the steps below were actually exercised against a running backend with
real Gemini credentials.

## Prerequisites

- A GCP service-account JSON present in `./credentials` with access to the
  configured Gemini model.
- `GOOGLE_APPLICATION_CREDENTIALS` (or the configured creds path) pointing at it.
- Backend deps installed: `pip install -r backend/requirements.txt`.

## Automated checks (lightweight, no test suite)

These are sanity gates, not a test suite:

1. **Imports / app boot** — `python -c "import app.main"` from `backend/`
   succeeds with no import errors.
2. **Server starts** — `uvicorn app.main:app --port 8000` (run from `backend/`)
   starts and stays up without tracebacks.
3. **Docker build** — `docker build -t backend ./backend` completes successfully
   (image is *run* in Phase 3; here we only confirm it builds).

## Manual walkthrough

1. Start the backend: `uvicorn app.main:app --port 8000` from `backend/`.
2. Send the notebook's multi-tool prompt to `POST /chat`:
   ```bash
   curl -s localhost:8000/chat -H 'content-type: application/json' -d '{
     "message": "Use internal docs to explain SDD, check whether Delano is hotter than 50 degrees, search the web for latest on AI if it is, use the sales tool to identify the top revenue product, validate the answer, and save a simulated artifact named sdd-demo-summary.md."
   }' | jq
   ```
3. Inspect the JSON response.

### Required assertions

- **HTTP 200** with a JSON body containing `final_answer`,
  `structured_response`, and `metrics`.
- **Structured output is well-formed**: `structured_response` validates against
  `AutonomousAgentResponse` — all 8 fields present, `confidence` in `0.0–1.0`,
  `tools_used` is a list, `task_completed` is a bool.
- **Tools actually fired**: `metrics.tool_call_count >= 1` and
  `metrics.tool_name_counts` includes the tools the prompt should trigger
  (expect `search_docs`, `weather`, `web_search`, `run_sql`, `validate_answer`,
  `save_artifact` for the prompt above — the notebook run hit all six).
- **Metrics returned**: `metrics` includes `agent_iterations` and token totals
  (`input_tokens`, `output_tokens`, `total_tokens`) that are non-zero.
- **Grounding**: `final_answer` reflects tool outputs (e.g. Delano 60°F,
  top product "Road-150 Red, 48", SDD definition) rather than fabricated facts.

### Edge cases

- **Empty / whitespace message** → handled gracefully (400 or a sensible
  structured response), not a 500 traceback.
- **A prompt needing only one tool** (e.g. "What's the weather in Phoenix?") →
  fewer tool calls, still valid structured output and metrics.
- **Missing credentials** → a clear error response that does **not** print the
  credentials path contents or key material (Safety & Boundaries in `AGENTS.md`).

## Definition of done

- [ ] `POST /chat` returns 200 with `final_answer` + valid `structured_response`
      + non-empty `metrics` for the multi-tool prompt.
- [ ] All six tools are invokable and the metrics summary reflects the tools that
      fired and the token usage.
- [ ] No credential material is logged or returned in any response or error.
- [ ] `backend/Dockerfile` builds successfully.
- [ ] Code is readable and module structure matches `plan.md` (teaching-first).
- [ ] Phase 1 marked `[x] COMPLETE` in [`roadmap.md`](../roadmap.md) only after
      the above were exercised for real.
