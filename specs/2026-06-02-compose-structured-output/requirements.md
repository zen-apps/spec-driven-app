# Requirements — Phase 3: Compose integration + structured-output view

Roadmap phase: **Phase 3 — Compose integration + structured-output view**
(`specs/roadmap.md`). This is the final core-build phase: it wires both services
into one `docker-compose up`, points the frontend at the backend by compose
service name, and completes the frontend's reasoning views by rendering the
agent's structured output. Completing it satisfies the **"runs end-to-end"**
success criterion in `mission.md` (#1) and the structured-output teaching goal.

## Scope

### In scope

1. **Add the frontend service to `docker-compose.yml`** alongside the existing
   backend service, on its own port, with a `depends_on` on the backend.
2. **Reach the backend by compose service name.** Replace the Phase 2 hardcoded
   `http://localhost:8001` in `frontend/app.py` with an env-driven `BACKEND_URL`
   that defaults to the local value, so the frontend still runs standalone.
3. **Structured-output view in the frontend.** Render the agent's
   `AutonomousAgentResponse` (the `structured_response` dict the `/chat` API
   already returns) in a collapsible expander beneath each answer, alongside the
   existing tool-calls view.
4. **Validate the frontend image builds** via `make build` once the frontend
   service is in compose — the carried-over check from Phase 2.

### Out of scope (explicitly)

- **No backend changes.** The `/chat` contract is unchanged; this phase only
  consumes `structured_response`, which the backend already returns.
- **Per-call tool arguments / outputs** stay out — `build_api_metrics` does not
  expose them and surfacing them needs a backend change (see `tech-stack.md`
  Frontend). The tool-calls view remains names / sequence / counts.
- **Standalone run-metrics panel** (token counts, iterations as their own view) —
  not part of this phase.
- **Persistence, automated tests, CI/CD, auth, cloud deploy** — post-roadmap
  (see `roadmap.md` "Out of scope").

### Data shape consumed

The `structured_response` dict (from `backend/app/schemas.py`
`AutonomousAgentResponse`) has these fields:

| Field | Type | Render note |
|---|---|---|
| `final_answer` | str | **Skip in the view** — already shown as the chat bubble; avoid duplication |
| `task_completed` | bool | Show as ✓/✗ or true/false |
| `reasoning_summary` | str | Short paragraph |
| `tools_used` | list[str] | List |
| `key_findings` | list[str] | List |
| `limitations` | list[str] | List (may be empty) |
| `recommended_next_steps` | list[str] | List (may be empty) |
| `confidence` | float (0.0–1.0) | Show the number |

The view must be defensive: `structured_response` may be missing or partial
(treat as empty / show a caption), and list fields may be empty.

## Decisions

- **Structured-output presentation: collapsible expander, raw-ish.** A
  `st.expander("🧩 Structured output")` mirroring the existing
  `render_tool_calls` expander pattern, rendering each field with a bold label.
  Chosen for **consistency** with the current UI and so students can read the
  shape of `AutonomousAgentResponse` without a wall of always-on text.
  *(Rejected: always-visible labeled fields — too noisy per turn; raw `st.json`
  dump — less teachable than labeled fields.)*
- **Compose wiring: frontend on host `8501` → container `8501`,
  `depends_on: backend`.** Matches `tech-stack.md` (Streamlit's default port)
  and the existing `frontend/Dockerfile` `EXPOSE 8501`.
- **Backend URL: env var with localhost fallback.**
  `BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8001")`. The
  compose frontend service sets `BACKEND_URL: http://backend:8000`. This keeps
  the standalone `streamlit run app.py` path working (most teachable / flexible)
  while compose overrides it. *(Rejected: hardcoding `http://backend:8000` —
  breaks running the frontend outside Docker.)*
- **No new dependencies.** `os` is stdlib; `streamlit` / `requests` already
  pinned. The backend port stays `8000` inside the compose network (the `8001`
  host mapping is only for host access; service-to-service uses container port).

## Context

- **Tone / copy:** match the existing frontend voice — short, student-facing,
  light emoji headers (`🔧 Tool calls`, mirror with `🧩 Structured output`). The
  app is a teaching reference; copy should be plain and walk-through-able.
- **Patterns to follow:** model the new `render_structured_output(...)` function
  on `render_tool_calls(...)` in `frontend/app.py` — same defensive `.get(...)`
  style, same expander idiom, same numbered/bulleted markdown. Persist the
  structured response into the per-turn session-state dict the same way
  `metrics` is persisted, and re-render it in `render_turn(...)`.
- **Stack limits:** stateless, no DB; conversation lives only in Streamlit
  session state (`tech-stack.md` Data model). Backend is unchanged.
- **Open question / watch-out:** `final_answer` appears both at the top level of
  the response and inside `structured_response`; the view intentionally does not
  re-render it to avoid duplicating the chat bubble.
