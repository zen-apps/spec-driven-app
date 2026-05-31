from langchain.tools import tool


@tool
def run_sql(query: str) -> str:
    """Run a read-only SQL query and return results.

    Demo placeholder:
    Replace this with your actual SQL execution logic.
    """
    return f"SQL tool received query: {query}"


@tool
def validate_answer(answer: str, evidence: str) -> str:
    """Critique the answer for missing evidence, bad assumptions, or calculation errors."""
    if not answer.strip():
        return "Validation failed: answer is empty."

    if not evidence.strip():
        return "Validation warning: evidence is empty or limited."

    return "Validation passed: the answer is supported by the provided evidence."


@tool
def search_docs(query: str) -> str:
    """Search internal documents for relevant context.

    Demo placeholder:
    Replace this with your vector DB / RAG search.
    """
    return f"No internal documents found for query: {query}"


@tool
def save_artifact(content: str) -> str:
    """Save the final output to a file or database.

    Demo placeholder:
    Replace this with actual file/database persistence.
    """
    return f"Artifact save simulated. Content length: {len(content)} characters."


@tool
def weather(location: str) -> str:
    """Get the current weather for a location."""
    normalized = location.lower().strip()

    if normalized == "new york":
        return "The current weather in New York is sunny, 75°F."

    if normalized == "delano":
        return "The current weather in Delano is foggy, 60°F."

    return f"Sorry, I don't have weather data for {location}."


@tool
def web_search(query: str) -> str:
    """Search the web for information.

    Demo placeholder:
    Replace this with Tavily, SerpAPI, Google Custom Search, Exa, etc.
    """
    normalized = query.lower().strip()

    if normalized == "latest on ai":
        return "The latest news on AI is about OpenCode, an alternative to Claude Code, and it is free."

    return f"Sorry, I don't have web search capabilities for the query: {query}"
