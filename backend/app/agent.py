import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from app.helpers import AutonomousAgentResponse
from app.tools import run_sql, validate_answer, search_docs, save_artifact, weather, web_search

# Load environment variables with defaults matching the reference notebook
GEMINI_PROJECT = os.environ.get("GEMINI_PROJECT", "zen-general-377713")
GEMINI_LOCATION = os.environ.get("GEMINI_LOCATION", "global")

# Initialize ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=1.0,
    project=GEMINI_PROJECT,
    location=GEMINI_LOCATION,
)

# Assemble the Agent with the required tools, system prompt, and structured schema
agent = create_agent(
    model=llm,
    tools=[
        run_sql,
        validate_answer,
        search_docs,
        save_artifact,
        weather,
        web_search,
    ],
    response_format=AutonomousAgentResponse,
    system_prompt="""
    You are an autonomous agent.

    You may use tools repeatedly when needed.

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
)


def run_agent(prompt: str) -> dict:
    """Invokes the LangChain agent with a given prompt.

    Enforces recursion limit of 50 for the graph.
    Returns the raw LangChain invoke output dictionary.
    """
    return agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        },
        config={
            "recursion_limit": 50
        },
    )
