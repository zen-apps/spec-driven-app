# Validation — Streamlit Frontend (Phase 2)

Per `specs/tech-stack.md`, validation for the core build is **manual**. Do not
claim a check passed unless it was actually exercised.

## Automated / sanity gates

- [ ] `python -c "import ast; ast.parse(open('frontend/app.py').read())"` — the
      app parses (no syntax errors). (No project typecheck/test suite exists.)
- [ ] `docker build ./frontend` succeeds and produces an image (per
      `prefers-docker-compose` — validate the container builds, not just a local
      run).
- [ ] `frontend/requirements.txt` pins explicit versions for Streamlit and the
      HTTP client; no unpinned/extra dependencies.

## Manual walkthrough

Prereq: the Phase 1 backend is running and reachable on host port `8001`
(`make run`, or `uvicorn app.main:app --port 8000` from `./backend` with the
host mapping). Confirm `POST http://localhost:8001/chat` responds before testing
the UI.

1. [ ] Start the frontend (`streamlit run frontend/app.py`, or the built Docker
       image) and open it in the browser.
2. [ ] The page shows a title/header and a one-line description; a chat input
       ("Ask the agent…") is visible.
3. [ ] Send a prompt that exercises a tool (e.g. something that triggers
       `run_sql` or `search_docs`). Confirm:
   - [ ] the agent's **final answer** renders as a chat bubble;
   - [ ] a **"🔧 Tool calls (N)"** expander appears beneath the answer;
   - [ ] expanding it shows the **ordered tool-call sequence** and **per-tool
         counts**, matching the backend `metrics` for that turn.
4. [ ] Send a second prompt. Confirm the first turn's answer **and** its
       tool-calls expander remain in the thread (session-state history works).
5. [ ] Send a prompt unlikely to call any tool. Confirm the tool-calls view
       handles the **zero-tools** case gracefully ("No tools were called…").

## Edge cases

- [ ] **Backend down:** stop the backend, send a prompt. A friendly inline error
      names the URL/port (`http://localhost:8001`) — no raw stack trace — and the
      input stays usable.
- [ ] **Non-200 from backend** (e.g. empty message rejected with 400): the UI
      surfaces a readable message rather than crashing.
- [ ] **Page refresh** clears conversation (session-state-only, as designed).

## Tone check

- [ ] User-facing copy is plain, friendly, and instructional (labels, error
      messages). Clear over clever; no emoji overload.

## Out-of-scope confirmation (must NOT appear this phase)

- [ ] No structured-output (`AutonomousAgentResponse`) view.
- [ ] No standalone run-metrics/token panel.
- [ ] No per-call tool **arguments** or tool **outputs** shown (not exposed by
      the current `/chat` contract).
- [ ] Frontend is **not** wired into `docker-compose.yml` and does **not** reach
      the backend by compose service name (those are Phase 3).

## Definition of done

- All automated/sanity gates pass.
- The full manual walkthrough passes against a live backend on port `8001`.
- Conversation history persists across turns within a session.
- Backend-down and non-200 paths degrade gracefully.
- Tone check passes.
- Out-of-scope items confirmed absent.
- `frontend/` contains `app.py`, `requirements.txt`, and a building `Dockerfile`.
