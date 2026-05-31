"""FastAPI backend entrypoint.

Phase 1 (repo skeleton): exposes a single health-check endpoint so the service
shell is reachable via docker-compose. The LangChain agent and the /chat
endpoint arrive in Phase 2.
"""

from fastapi import FastAPI

app = FastAPI(title="Spec-Driven App — Backend")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe used by docker-compose and the frontend."""
    return {"status": "ok"}
