"""Pydantic models.

`AutonomousAgentResponse` is ported verbatim from
`examples/create_agent.ipynb` — it is the agent's validated final business
output. The `ChatRequest` / `ChatResponse` models define the thin HTTP contract
for `POST /chat`.
"""

from typing import List

from pydantic import BaseModel, Field


# ============================================================
# Agent structured final response (from the notebook — do not redesign)
# ============================================================

class AutonomousAgentResponse(BaseModel):
    """
    This is the final structured response returned by the agent.

    Important:
    - This does not replace result["messages"].
    - Tool-call metrics still come from result["messages"].
    - This is your validated final business output.
    """

    final_answer: str = Field(
        description="The final response to the user's request."
    )

    task_completed: bool = Field(
        description="Whether the agent completed the user's request."
    )

    reasoning_summary: str = Field(
        description="Brief user-facing summary of the steps the agent took. Do not include hidden chain-of-thought."
    )

    tools_used: List[str] = Field(
        description="Names of tools used by the agent during the run."
    )

    key_findings: List[str] = Field(
        description="Important facts, observations, or tool outputs used to support the final answer."
    )

    limitations: List[str] = Field(
        description="Any limitations, missing information, or uncertainty."
    )

    recommended_next_steps: List[str] = Field(
        description="Suggested next steps for the user, if any."
    )

    confidence: float = Field(
        description="Confidence score from 0.0 to 1.0."
    )


# ============================================================
# HTTP API contract for POST /chat
# ============================================================

class ChatRequest(BaseModel):
    """A single-message chat request. Phase 1 is stateless — no history."""

    message: str = Field(description="The user's message to the agent.")


class ChatResponse(BaseModel):
    """The agent's answer plus its run metrics.

    - final_answer: convenience accessor (structured_response.final_answer with
      a fallback to the last AIMessage).
    - structured_response: the AutonomousAgentResponse, serialized to a dict.
    - metrics: a JSON-safe subset of the run metrics (counts, tool names,
      iterations, token totals).
    """

    final_answer: str
    structured_response: dict
    metrics: dict
