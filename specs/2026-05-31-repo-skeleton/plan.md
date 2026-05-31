# Plan — Repo skeleton & docker-compose (Phase 1)

Task groups are ordered backend → frontend → compose → hygiene, matching the
roadmap's backend-first strategy. Each group is independently implementable and
verifiable on its own.

## 1. Backend service (`./backend`)

1. Create `backend/requirements.txt` with pinned `fastapi` and `uvicorn[standard]`
   (no LangChain/Gemini yet).
2. Create `backend/app/main.py` (or `backend/main.py`) defining a FastAPI app with
   `GET /health` returning JSON `{"status": "ok"}`.
3. Create `backend/Dockerfile`: `python:3.12-slim` base, install
   `requirements.txt`, copy the app, expose `8000`, run
   `uvicorn ... --host 0.0.0.0 --port 8000`.

## 2. Frontend service (`./frontend`)

1. Create `frontend/requirements.txt` with a pinned `streamlit`.
2. Create `frontend/app.py` — a minimal Streamlit page (a title and one line of
   placeholder text). No backend call yet.
3. Create `frontend/Dockerfile`: `python:3.12-slim` base, install
   `requirements.txt`, copy the app, expose `8501`, run
   `streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true`.

## 3. Compose wiring (`./docker-compose.yml`)

1. Define a `backend` service: build `./backend`, publish `8001:8000` (container
   stays on `8000`; host `8000` is occupied on the dev machine).
2. Define a `frontend` service: build `./frontend`, publish `8501:8501`,
   `depends_on: [backend]`.
3. Put both on a shared network (the default compose network is sufficient) so the
   frontend can resolve `backend` by service name in later phases. Optionally set a
   `BACKEND_URL=http://backend:8000` env var on the frontend for Phase 4 to use.

## 4. Repo hygiene

1. Confirm `.gitignore` already covers `./credentials` and Python artifacts
   (`__pycache__/`, `*.pyc`); add any missing entries.
2. Confirm no secrets or credential files are staged.

## 5. Smoke verification (manual, this phase)

1. `docker-compose build` succeeds for both services.
2. `docker-compose up` brings both up; backend reachable at
   `http://localhost:8000/health` returning `{"status": "ok"}`.
3. Frontend page loads at `http://localhost:8501`.
4. `docker-compose down` cleans up.
