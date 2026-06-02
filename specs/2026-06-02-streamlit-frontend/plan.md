# Plan — Streamlit Frontend (Phase 2)

Frontend-only. Task groups are ordered but each is independently implementable
and verifiable. Target layout in `./frontend`:

```text
frontend/
├── app.py
├── requirements.txt
└── Dockerfile
```

## 1. Project scaffolding

1.1. Create the `./frontend` directory.
1.2. Add `frontend/requirements.txt` pinning `streamlit` and an HTTP client
     (`requests`). Pin explicit versions for reproducibility.
1.3. Add a module-level constant `BACKEND_URL = "http://localhost:8001"` at the
     top of `app.py` with a comment that Phase 3 swaps this for the compose
     service name. Derive the endpoint as `f"{BACKEND_URL}/chat"`.

## 2. Backend client

2.1. Write a small `call_agent(message: str) -> dict` helper that POSTs
     `{ "message": message }` to `{BACKEND_URL}/chat` with a sensible timeout.
2.2. Return the parsed JSON (`final_answer`, `structured_response`, `metrics`).
2.3. Raise/return a clear error signal on connection failure or non-200 so the
     UI layer can render a friendly message (no raw traceback to the user).

## 3. Tool-calls rendering

3.1. Write a helper that, given a turn's `metrics` dict, renders an
     `st.expander` titled e.g. `🔧 Tool calls ({tool_call_count})`.
3.2. Inside it, show the **ordered** `tool_call_sequence` (e.g. a numbered list
     or `1. run_sql → 2. validate_answer`) and the per-tool `tool_name_counts`.
3.3. Handle the **no-tools** case gracefully (count 0 → "No tools were called
     for this answer.").
3.4. Use only fields guaranteed by `build_api_metrics`; do not assume per-call
     args or tool outputs exist.

## 4. Chat UI + session state

4.1. Initialize `st.session_state` with a `messages` list on first load.
4.2. Render existing history on each rerun: for each turn, the user message,
     the assistant `final_answer` bubble, then the tool-calls expander.
4.3. Add a `st.chat_input` ("Ask the agent…"); on submit, append the user
     message, call `call_agent`, append the assistant turn (storing
     `final_answer` + the `metrics` needed for the expander), and rerun.
4.4. Render a `st.spinner` while the agent call is in flight.
4.5. On backend error, append/show a friendly inline error message and keep the
     input usable.

## 5. Page polish

5.1. Set page title/header and a one-line description of what the app does.
5.2. Apply plain, instructional copy per the tone rules in `requirements.md`.

## 6. Dockerfile

6.1. Add `frontend/Dockerfile`: a slim Python base, install
     `requirements.txt`, copy `app.py`, expose the Streamlit port, and run
     `streamlit run app.py` bound to `0.0.0.0`.
6.2. Confirm the image **builds** (`docker build ./frontend`). Wiring it into
     `docker-compose.yml` and connecting by compose service name is **Phase 3**,
     not this phase.

## 7. Sanity validation

7.1. Run the manual + automated gates in `validation.md` against a running
     backend on port `8001`.
