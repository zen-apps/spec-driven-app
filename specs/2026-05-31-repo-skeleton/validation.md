# Validation — Repo skeleton & docker-compose (Phase 1)

## Automated

No pytest suite exists yet (introduced in Phase 3), so Phase 1 has no automated
test command. The build itself is the automated gate:

- [ ] `docker-compose build` completes without error for both `backend` and
      `frontend`.
- [ ] Both images install only their pinned dependencies (no LangChain/Gemini in
      backend yet).

## Manual

Bring the stack up and exercise both services:

- [ ] `docker-compose up` starts both services with no crash loop.
- [ ] `curl http://localhost:8001/health` returns HTTP `200` and body
      `{"status": "ok"}`.
- [ ] Backend is published on host `8001` (container port `8000`), frontend on
      host `8501`, both reachable from the host.
- [ ] `http://localhost:8501` loads the minimal Streamlit placeholder page in a
      browser.
- [ ] Both services share a compose network (verify the `backend` service name
      resolves from the `frontend` container, e.g.
      `docker-compose exec frontend python -c "import socket; print(socket.gethostbyname('backend'))"`).
- [ ] `docker-compose down` stops and removes both containers cleanly.

### Edge cases

- [ ] Re-running `docker-compose up` after `down` works without manual cleanup.
- [ ] No credential files or `./credentials` contents are tracked by git
      (`git status` clean; `git check-ignore credentials/` matches).

## Definition of done

- All automated (build) and manual checks above pass.
- The skeleton contains **no** agent logic, LangChain, or Gemini wiring — scope is
  limited to the two-service shell.
- Files follow the existing repo layout and `examples/` style; dependencies are
  pinned; no new dependencies beyond FastAPI/uvicorn and Streamlit.
- `specs/roadmap.md` Phase 1 is ready to be marked `[x] COMPLETE` (with date) once
  these checks pass — done in the implement step, not here.
