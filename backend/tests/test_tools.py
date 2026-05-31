import pytest
from app.tools import run_sql, validate_answer, search_docs, save_artifact, weather, web_search, DEMO_SALES_SCHEMA, DEMO_TOP_REVENUE_PRODUCTS, DEMO_TOTAL_REVENUE, SDD_DOC_SUMMARY


def test_run_sql():
    # Schema check
    assert run_sql.func("SELECT * FROM schema") == DEMO_SALES_SCHEMA
    assert "columns" in run_sql.func("what is the columns?").lower()

    # Revenue checks
    assert run_sql.func("top revenue products") == DEMO_TOP_REVENUE_PRODUCTS
    assert run_sql.func("total estimated revenue") == DEMO_TOTAL_REVENUE

    # Blocked terms
    assert "Rejected" in run_sql.func("DROP TABLE sales")
    assert "Rejected" in run_sql.func("INSERT INTO sales VALUES (1)")

    # Fallback
    assert "Demo SQL tool received" in run_sql.func("SELECT * FROM users")


def test_validate_answer():
    # Empty cases
    assert "failed" in validate_answer.func("", "some evidence").lower()
    assert "warning" in validate_answer.func("some answer", "").lower()

    # High overlap
    ans = "The weather is sunny and hot in phoenix today."
    ev = "Phoenix is hot today with sunny conditions."
    assert "passed" in validate_answer.func(ans, ev).lower()

    # Low overlap
    ans_low = "banana apple grape"
    ev_low = "phoenix hot weather"
    assert "warning" in validate_answer.func(ans_low, ev_low).lower()


def test_search_docs():
    assert search_docs.func("What is SDD?") == SDD_DOC_SUMMARY
    assert "No internal documents found" in search_docs.func("weather in New York")


def test_save_artifact():
    result = save_artifact.func("test.md", "Hello World\nLine 2")
    assert "Artifact save simulated: test.md" in result
    assert "Characters: 18" in result
    assert "Preview: Hello World Line 2" in result


def test_weather():
    assert "75°F" in weather.func("New York")
    assert "60°F" in weather.func("delano")
    assert "Sorry, I don't have weather data" in weather.func("Chicago")


def test_web_search():
    assert "OpenCode" in web_search.func("latest on ai")
    assert "LangChain tools let agents" in web_search.func("langchain tools")
    assert "Sorry, I don't have web search" in web_search.func("cooking recipes")
