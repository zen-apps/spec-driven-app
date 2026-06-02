# Validation — Phase 3: Compose integration + structured-output view

Per `tech-stack.md`, this project uses **manual validation only**. Do not mark
the phase complete unless these steps were actually exercised (`AGENTS.md`
Testing Expectations).

## Automated / sanity gates

- [ ] **Frontend image builds:** `docker build ./frontend` succeeds (the
      carried-over Phase 2 check).
- [ ] **Whole stack builds:** `make build` (`docker compose build`) succeeds for
      both `backend` and `frontend` services.
- [ ] **Compose config is valid:** `docker compose config` parses without error
      and shows the `frontend` service with `BACKEND_URL=http://backend:8000`,
      port `8501:8501`, and `depends_on: backend`.
- [ ] **Frontend imports cleanly:** `python -c "import ast; ast.parse(open('frontend/app.py').read())"`
      (no syntax errors). `os` import is present.

## Manual end-to-end walkthrough

Requires a valid Gemini service-account key in `./credentials` (as in Phase 1).

- [ ] **Both services come up:** `make run` (or `docker compose up`) starts
      `backend` and `frontend`; no crash loops in `make logs`.
- [ ] **Frontend is reachable** at `http://localhost:8501` in a browser.
- [ ] **End-to-end chat works:** send a prompt that exercises tools (e.g. one
      that triggers `run_sql` / `search_docs`). The final answer renders as a
      chat bubble.
- [ ] **Tool-calls view still works:** the `🔧 Tool calls (N)` expander shows the
      ordered sequence and per-tool counts (unchanged from Phase 2).
- [ ] **Structured-output view works:** the `🧩 Structured output` expander
      renders `task_completed`, `confidence`, `reasoning_summary`, and the
      `tools_used` / `key_findings` / `limitations` / `recommended_next_steps`
      lists. `final_answer` is **not** duplicated inside the expander.
- [ ] **Service-name wiring proven:** the frontend reaches the backend via
      `http://backend:8000` (it works inside compose with NO host `8001` mapping
      relied on for service-to-service traffic). Confirm by chatting
      successfully from the containerized frontend.

## Edge cases

- [ ] **Backend down:** stop the backend; the frontend shows the friendly
      `BackendError` message (referencing `BACKEND_URL`), not a raw traceback.
- [ ] **Empty lists:** a turn whose `structured_response` has empty
      `limitations` / `recommended_next_steps` shows a muted "none" caption, not
      a crash or blank bullet.
- [ ] **Missing structured_response:** if `structured_response` is absent/empty,
      the expander shows a caption rather than erroring.
- [ ] **Standalone still works:** running `streamlit run frontend/app.py`
      directly (no compose, no `BACKEND_URL` set) still targets
      `http://localhost:8001` and works against a locally-run backend.
- [ ] **History re-render:** after several turns, scrolling shows each stored
      turn re-rendering both the tool-calls and structured-output views from
      session state.

## Tone check

- [ ] New copy matches the existing frontend voice: short, student-facing, with
      a light emoji header (`🧩 Structured output`) consistent with
      `🔧 Tool calls`. No jargon, no raw chain-of-thought exposed.

## Definition of done

- [ ] All sanity gates pass.
- [ ] The end-to-end walkthrough passes: `docker compose up` brings up both
      services and a user chats and sees **tool calls + structured output** —
      satisfying `mission.md` success criterion #1.
- [ ] No backend code changed; `/chat` contract untouched.
- [ ] Phase 3 marked `[x] COMPLETE` in `specs/roadmap.md`.
