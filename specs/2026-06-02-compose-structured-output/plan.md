# Plan — Phase 3: Compose integration + structured-output view

Task groups are independently implementable. Group 1 (backend URL) and Group 2
(structured-output view) are frontend code; Group 3 is compose wiring; Group 4
validates. Suggested order is 1 → 2 → 3 → 4.

## 1. Backend URL via env var (`frontend/app.py`)

1.1 Add `import os` at the top of `frontend/app.py`.
1.2 Replace the hardcoded `BACKEND_URL = "http://localhost:8001"` with
    `BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8001")`.
1.3 Update the surrounding comment to explain: defaults to the local host port
    for standalone runs; compose sets `BACKEND_URL=http://backend:8000`.
1.4 Leave `CHAT_ENDPOINT`, `BackendError`, and the connection-error message
    referencing `BACKEND_URL` as-is (they already interpolate the variable).

## 2. Structured-output view (`frontend/app.py`)

2.1 Add `render_structured_output(structured: dict) -> None`, modeled on
    `render_tool_calls`:
    - Guard: `structured = structured or {}`; if empty, show a caption inside
      the expander and return.
    - Use `st.expander("🧩 Structured output")`.
    - Render fields with bold labels, **skipping `final_answer`** (already the
      chat bubble):
      - `task_completed` → ✓/✗ line
      - `confidence` → numeric (e.g. `Confidence: 0.82`)
      - `reasoning_summary` → paragraph
      - `tools_used`, `key_findings`, `limitations`,
        `recommended_next_steps` → bulleted lists, each defensively defaulting
        to `[]` and showing a muted "none" caption when empty.
2.2 Call `render_structured_output(...)` in `render_turn(...)` right after
    `render_tool_calls(...)`, reading `turn.get("structured_response", {})`.
2.3 Call `render_structured_output(...)` in `main()` in the live-turn block,
    right after the `render_tool_calls(metrics)` call, using the
    `structured_response` from the result.
2.4 Extract `structured_response = result.get("structured_response", {})` in
    `main()` and include it when appending the completed turn to
    `st.session_state.messages` (alongside `final_answer` and `metrics`).
2.5 Update the module docstring's "Scope notes" — structured output is now
    **in** scope; remove it from the "out of scope" line.

## 3. Compose wiring (`docker-compose.yml`)

3.1 Add a `frontend` service under `services:`:
    - `build: ./frontend`
    - `ports: ["8501:8501"]`
    - `environment: { BACKEND_URL: http://backend:8000 }`
    - `depends_on: [backend]`
3.2 Update the top-of-file comment: the frontend service now exists and reaches
    the backend by compose service name; remove the "Phase 3 will add…" framing.
3.3 Confirm the backend service is reachable as `backend:8000` inside the
    compose network (it already exposes container port `8000`; no host remap
    needed for service-to-service traffic).

## 4. Validation pass

4.1 Sanity-build the frontend image (`docker build ./frontend`) and the whole
    stack via `make build`.
4.2 Bring the stack up with `make run` (or `docker compose up`) and exercise the
    end-to-end flow per `validation.md`.
4.3 When validation passes, mark **Phase 3** `[x] COMPLETE` in
    `specs/roadmap.md` (done in the implement step, not here).
