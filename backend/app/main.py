"""FastAPI backend entrypoint.

Phase 2 (full LangChain agent): exposes GET /health and POST /chat endpoints,
integrating with the ChatGoogleGenerativeAI model and running autonomous tool loops.
"""

import logging
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.agent import run_agent
from app.helpers import AutonomousAgentResponse, summarize_agent_metrics

# Set up simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")

app = FastAPI(title="Spec-Driven App — Backend")


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe used by docker-compose and the frontend."""
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest) -> JSONResponse:
    """Invokes the LangChain agent and returns the structured final answer and run metrics.

    Includes a robust error handler returning HTTP 500 with a detailed fallback schema on downstream failure.
    """
    try:
        logger.info(f"Received chat request: {request.message}")
        
        # Invoke LangChain agent run
        raw_result = run_agent(request.message)
        
        # Summarize agent metrics
        metrics = summarize_agent_metrics(raw_result)
        
        # Extract the structured response object
        structured_response = metrics.get("structured_response")
        
        # If structured response is missing, fabricate a default from the final answer
        if structured_response is None:
            logger.warning("Agent execution did not produce a structured response; constructing fallback.")
            structured_response = AutonomousAgentResponse(
                final_answer=metrics.get("final_answer", ""),
                task_completed=True,
                reasoning_summary="Completed request but response was not structured.",
                tools_used=metrics.get("tool_call_sequence", []),
                key_findings=[],
                limitations=["No structured output produced by LLM."],
                recommended_next_steps=[],
                confidence=0.5,
            )
            
        # Serialize structured response to dict
        response_dict = structured_response.model_dump()
        
        # Clean metrics dictionary of non-serializable fields before returning
        metrics_serializable = {
            "tool_calls": metrics.get("tool_calls", []),
            "token_totals": {
                "input_tokens": metrics.get("input_tokens", 0),
                "output_tokens": metrics.get("output_tokens", 0),
                "total_tokens": metrics.get("total_tokens", 0),
            },
            "iterations": metrics.get("agent_iterations", 0),
        }
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "response": response_dict,
                "metrics": metrics_serializable,
            }
        )
        
    except Exception as e:
        logger.error(f"Downstream/API Exception encountered: {str(e)}", exc_info=True)
        
        # Construct fallback schema for error
        fallback_response = {
            "final_answer": "Error: Failed to process the request due to a downstream API failure.",
            "task_completed": False,
            "reasoning_summary": f"Attempted to initialize or run the Gemini model, but an error occurred during setup: {str(e)}",
            "tools_used": [],
            "key_findings": [],
            "limitations": ["Downstream API is unavailable or misconfigured."],
            "recommended_next_steps": [
                "Check your credentials mount in ./credentials",
                "Verify GOOGLE_APPLICATION_CREDENTIALS in your environment.",
                "Check GEMINI_PROJECT and GEMINI_LOCATION values.",
            ],
            "confidence": 0.0,
        }
        
        fallback_metrics = {
            "tool_calls": [],
            "token_totals": {
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
            },
            "iterations": 0,
        }
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": f"Failed to call Google Gemini API: {str(e)}",
                "response": fallback_response,
                "metrics": fallback_metrics,
            }
        )
