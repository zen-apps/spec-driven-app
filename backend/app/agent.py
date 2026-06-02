"""Agent wiring.

Builds the LangChain agent exactly as in `examples/create_agent.ipynb`:
a `ChatGoogleGenerativeAI` model + the six deterministic tools + the
`AutonomousAgentResponse` structured output + the notebook's system prompt.

The agent is built lazily (on first use) so the module can be imported without
valid credentials — useful for the import smoke check in validation.md.
"""

from __future__ import annotations

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from .config import get_settings
from .schemas import AutonomousAgentResponse
from .tools import TOOLS

# System prompt — verbatim from the notebook.
SYSTEM_PROMPT = """
    You are an autonomous agent running a classroom demo.

    You may use tools repeatedly when needed. The available tools are deterministic teaching examples, not production integrations.

    Before finalizing:
    - Make sure the answer is grounded in tool results when tools were used.
    - Do not fabricate tool results.
    - Stop when the answer is complete and verified.

    Your final answer must be returned using the required structured response schema.

    In the structured response:
    - final_answer should directly answer the user's request.
    - tools_used should list the actual tools used.
    - key_findings should summarize important facts from tool outputs.
    - limitations should mention missing information or uncertainty.
    - confidence should be between 0.0 and 1.0.
    """

# Graph recursion cap (notebook value). Not exactly "max tool calls"; it bounds
# the agent loop so a runaway agent can't spin forever.
RECURSION_LIMIT = 50

# Cached agent so we build the model/graph once per process.
_agent = None


def build_agent():
    """Construct the LangChain agent from current settings (notebook pattern)."""
    settings = get_settings()

    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=settings.temperature,
        project=settings.gcp_project,
        location=settings.gcp_location,
    )

    return create_agent(
        model=llm,
        tools=TOOLS,
        response_format=AutonomousAgentResponse,
        system_prompt=SYSTEM_PROMPT,
    )


def get_agent():
    """Return the process-wide agent, building it on first use."""
    global _agent
    if _agent is None:
        _agent = build_agent()
    return _agent


def run_agent(message: str) -> dict:
    """Invoke the agent with a single user message and return the raw result dict.

    The returned dict carries both ``messages`` (the trace metrics read from)
    and ``structured_response`` (the validated business output).
    """
    agent = get_agent()
    return agent.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config={"recursion_limit": RECURSION_LIMIT},
    )
