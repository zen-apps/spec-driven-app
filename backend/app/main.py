"""FastAPI app exposing the agent over HTTP.

Phase 1 surface is intentionally minimal: a single ``POST /chat`` route that
runs the agent on one user message and returns the structured answer plus a
JSON-safe metrics summary. This makes the agent inspectable over HTTP before
any UI exists.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException

from .agent import run_agent
from .metrics import build_api_metrics, get_final_answer, get_structured_response
from .schemas import ChatRequest, ChatResponse

logger = logging.getLogger("backend.agent")

app = FastAPI(
    title="Reference Agent Backend",
    description="FastAPI wrapper around the LangChain teaching agent (Phase 1).",
    version="0.1.0",
)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Run the agent on a single message and return its structured answer + metrics."""
    message = request.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="message must not be empty.")

    try:
        result = run_agent(message)
    except Exception as exc:  # noqa: BLE001 - surface a safe, generic error
        # Never echo credential material or file contents. Log the exception
        # type only; the full traceback stays in server logs, not the response.
        logger.exception("Agent run failed")
        raise HTTPException(
            status_code=502,
            detail=f"Agent run failed: {type(exc).__name__}. Check backend logs and credentials configuration.",
        ) from exc

    structured = get_structured_response(result)
    structured_dict = structured.model_dump() if structured is not None else {}

    return ChatResponse(
        final_answer=get_final_answer(result),
        structured_response=structured_dict,
        metrics=build_api_metrics(result),
    )
