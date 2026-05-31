# Validation — Frontend Chat UI (Phase 4)

Detailed checklist to verify that the Streamlit frontend chat UI meets all acceptance criteria and works flawlessly against the backend container before considering Phase 4 complete.

## Automated & Dependency Checks

### 1. Dependency Alignment
Verify that packages are correctly specified.

- [ ] Check `frontend/requirements.txt` contains `requests==2.31.0`.
- [ ] Check `frontend/requirements.txt` contains `streamlit==1.58.0`.

### 2. Streamlit Run Test (Syntactic Correctness)
Ensure no syntax or immediate import errors prevent the Streamlit application from initializing.

- [ ] Run `python -m py_compile frontend/app.py` or `streamlit hello --help` to ensure standard Streamlit libraries are available.

---

## Manual Walkthrough & Interaction Checks

Verify the user experience end-to-end through manual UI exercises.

### 1. Container Boot & Initial Display
- [ ] Spin up the containers using `docker-compose up --build`.
- [ ] Wait for both services to show healthy logs.
- [ ] Open a browser and navigate to `http://localhost:8501`.
- [ ] Confirm that the page loads with a standard Streamlit theme, featuring a clean chat interface input at the bottom and a header.

### 2. Interactive Chat Flow (Success Case)
- [ ] Submit a query that requires a simple answer (e.g., "Hello, who are you?").
- [ ] Confirm a spinner displays during the network request.
- [ ] Verify that the assistant's reply contains:
  - The final answer text displayed at the top.
  - A collapsible expander titled **"Agent Diagnostics"**.
- [ ] Open the expander and verify that:
  - Task completed status is visible.
  - Confidence is shown.
  - Reasoning summary is readable.
  - Iterations and tool sequence details are populated (even if zero for non-tool queries).
  - Input, output, and total token metrics are displayed.

### 3. Tool Usage & Complex Execution Trace
- [ ] Submit a query that triggers a tool (e.g., "What is the weather in Delano?").
- [ ] Confirm the request completes and renders.
- [ ] Open the diagnostics expander and assert:
  - Tools Used contains `"weather"` or the corresponding tool name.
  - Iteration count is 1 or more.
  - Token totals are non-zero.

### 4. Conversation State & Session Persistence
- [ ] Submit a second distinct query (e.g., "Tell me more about that").
- [ ] Verify that the chat window now displays BOTH conversation turns (the first query/response and the second query/response).
- [ ] Expand the diagnostics for the FIRST response. Confirm that the historical metrics are still correctly retained and displayed.

### 5. Chat Reset
- [ ] Click the "Clear History" button (e.g., in the sidebar or header).
- [ ] Verify the chat window is completely cleared of all past messages and metrics.

### 6. Robust Error Handling (Backend Offline)
- [ ] Temporarily stop the backend container (`docker-compose stop backend`).
- [ ] Send another query in the chat UI.
- [ ] Confirm that the frontend does NOT crash with a standard Streamlit traceback stack trace.
- [ ] Verify that the UI displays a graceful error message indicating the backend is offline.
- [ ] Confirm that the "Agent Diagnostics" expander is still available, containing recommended next steps (e.g., check docker logs, verify port mapping).

---

## Definition of Done

- All automated/manual checks pass successfully.
- Streamlit application is free of crash-prone regressions or unhandled exceptions.
- The `requirements.txt` has pinned dependencies.
- Changes are fully integrated into `frontend/app.py`.
- No temporary/untracked files or debugging hacks are committed.
