from langchain.tools import tool

DEMO_SALES_SCHEMA = """Demo sales CSV: examples/demo_data/sales.csv
Rows: 10,000
Columns:
- SalesOrderNumber: order id
- SalesOrderLineNumber: line item number
- OrderDate: order date
- CustomerName: customer name
- EmailAddress: customer email
- Item: product name
- Quantity: units sold
- UnitPrice: price per unit
- TaxAmount: tax charged
"""

DEMO_TOP_REVENUE_PRODUCTS = """Top products by estimated revenue in the demo sales CSV:
1. Road-150 Red, 48 — 337 units — $1,205,876.99
2. Road-150 Red, 62 — 336 units — $1,202,298.72
3. Road-150 Red, 52 — 302 units — $1,080,637.54
4. Road-150 Red, 56 — 295 units — $1,055,589.65
5. Road-150 Red, 44 — 281 units — $1,005,493.87
"""

DEMO_TOTAL_REVENUE = """Demo sales CSV summary:
- Rows: 10,000
- Estimated total revenue: $14,432,081.12
- Highest revenue product variant: Road-150 Red, 48
"""

SDD_DOC_SUMMARY = """Spec-Driven Development means steering AI coding agents with durable markdown specs instead of relying only on vibe coding and long chat history.
In this workflow, the constitution, feature specs, validation files, roadmap, and changelog keep the agent focused, reduce drift, and make the project easier to explain and reproduce.
SDD is part of harness engineering: the developer directs intent, boundaries, acceptance criteria, and validation while the agent handles more of the implementation work.
"""

WEB_SEARCH_RESULTS = {
    "latest on ai": "Search result: OpenCode is being discussed as a free alternative to Claude Code. Demo takeaway: the AI coding tool space is moving quickly, so durable specs help teams avoid rebuilding around every new tool trend.",
    "langchain tools": "Search result: LangChain tools let agents call Python functions with typed inputs. Demo takeaway: tools give an agent controlled ways to use external context, calculations, and actions.",
    "spec driven development": "Search result: Spec-driven workflows use written requirements, plans, and validation criteria to guide AI-assisted software delivery. Demo takeaway: specs help reduce drift and make agent work reviewable.",
    "streamlit fastapi demo": "Search result: Streamlit is commonly used for quick Python UIs, while FastAPI is used for JSON APIs. Demo takeaway: this repo separates the teaching UI from the agent backend.",
}


@tool
def run_sql(query: str) -> str:
    """Simulate a read-only SQL tool over the demo sales CSV.

    This classroom version does not execute SQL. It returns curated sales-data
    facts so students can see how an agent might call a database tool without
    adding a real database or arbitrary code execution to the notebook.
    """
    normalized = query.lower().strip()
    blocked_terms = ["insert", "update", "delete", "drop", "alter", "create", "attach"]

    if any(term in normalized for term in blocked_terms):
        return "Rejected: this demo SQL tool is read-only and does not run write or schema-changing statements."

    if "schema" in normalized or "column" in normalized or "table" in normalized:
        return DEMO_SALES_SCHEMA

    if "top" in normalized and "revenue" in normalized:
        return DEMO_TOP_REVENUE_PRODUCTS

    if "total" in normalized and "revenue" in normalized:
        return DEMO_TOTAL_REVENUE

    return (
        "Demo SQL tool received the query but did not execute it. "
        "Try asking for the sales schema, total revenue, or top products by revenue.\n\n"
        f"Query received: {query}"
    )


@tool
def validate_answer(answer: str, evidence: str) -> str:
    """Critique the answer for missing evidence, bad assumptions, or calculation errors."""
    if not answer.strip():
        return "Validation failed: answer is empty."

    if not evidence.strip():
        return "Validation warning: evidence is empty or limited."

    answer_terms = set(answer.lower().split())
    evidence_terms = set(evidence.lower().split())
    overlap = answer_terms.intersection(evidence_terms)

    if len(overlap) < 3:
        return "Validation warning: the answer has limited overlap with the provided evidence."

    return "Validation passed: the answer is supported by the provided evidence."


@tool
def search_docs(query: str) -> str:
    """Search internal documents for relevant context about SDD.

    This classroom version returns one concise SDD knowledge-base passage when
    the query asks about SDD. It intentionally avoids embeddings or file IO.
    """
    if "sdd" not in query.lower() and "spec" not in query.lower():
        return f"No internal documents found for query: {query}"

    return SDD_DOC_SUMMARY


@tool
def save_artifact(name: str, content: str) -> str:
    """Simulate saving an artifact and return a receipt without writing files."""
    safe_name = name.strip() or "untitled-artifact.md"
    preview = content.strip().replace("\n", " ")[:160]

    return (
        f"Artifact save simulated: {safe_name}\n"
        f"Characters: {len(content)}\n"
        f"Preview: {preview}"
    )


@tool
def weather(location: str) -> str:
    """Get deterministic demo weather for a location."""
    normalized = location.lower().strip()

    weather_by_location = {
        "new york": "The current weather in New York is sunny, 75°F.",
        "delano": "The current weather in Delano is foggy, 60°F.",
        "minneapolis": "The current weather in Minneapolis is cloudy, 48°F.",
        "phoenix": "The current weather in Phoenix is hot, 98°F.",
    }

    if normalized in weather_by_location:
        return weather_by_location[normalized]

    return f"Sorry, I don't have weather data for {location}."


@tool
def web_search(query: str) -> str:
    """Search a curated fake web index for classroom-safe demo results."""
    normalized = query.lower().strip()

    if normalized in WEB_SEARCH_RESULTS:
        return WEB_SEARCH_RESULTS[normalized]

    for topic, result in WEB_SEARCH_RESULTS.items():
        if topic in normalized or normalized in topic:
            return result

    return f"Sorry, I don't have web search capabilities for the query: {query}"
