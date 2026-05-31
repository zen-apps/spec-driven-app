# Plan — Phase 5: Tools-centric agent backend

This document outlines the phased step-by-step implementation plan for the Tools-centric agent backend feature.

## Task Group 1: Tool Definitions
Re-implement backend tools to match `examples/create_agent_tools.ipynb`.

1. **Update `backend/app/tools.py`**:
   - Define SQL schema, summaries, and search mock databases.
   - Update `run_sql(query: str) -> str` tool to return schema/total revenue/top products based on string content.
   - Update `validate_answer(answer: str, evidence: str) -> str` with the exact word-set comparison logic.
   - Update `search_docs(query: str) -> str` to return the `SDD_DOC_SUMMARY` when queried about SDD.
   - Update `save_artifact(name: str, content: str) -> str` to take both name and content parameters and return the simulated receipt.
   - Update `weather(location: str) -> str` to return the deterministic weather dictionary values.
   - Update `web_search(query: str) -> str` to search the dictionary of curated fake web index results.

## Task Group 2: Agent Configuration
Update the LangChain agent setup.

1. **Update `backend/app/agent.py`**:
   - Set LLM temperature to `1.0`.
   - Update `tools` array to include all 6 updated tools.
   - Update `system_prompt` to match the exact teaching assistant prompt from the notebook.
   - Confirm recursion limit is set to `50` in `run_agent`.

## Task Group 3: Test Adaptation
Update backend tests to support the new implementations and signatures.

1. **Update `backend/tests/test_helpers.py`**:
   - Ensure the helpers tests reflect any changes in `AutonomousAgentResponse` parsing or token/tool metrics tracking.
2. **Update `backend/tests/test_main.py`**:
   - Adjust mock metrics and tool calling structures (such as `save_artifact` taking 2 arguments) so they align with the updated tool signatures.
   - Verify `POST /chat` and error fallback schemas handle mock payloads correctly.

## Task Group 4: Local Validation
Execute and verify the application end to end.

1. **Run Unit Tests**:
   - Execute `pytest backend/tests` to confirm all test suites pass with zero failures.
2. **Docker Build & Run**:
   - Run `docker-compose build` and `docker-compose up` to launch the backend and Streamlit services locally.
3. **Manual Flow Check**:
   - Open Streamlit UI, send a complex autonomous request exercising the new tools (e.g., asking for the top product by revenue or SDD details), and verify the diagnostics and output metrics.
