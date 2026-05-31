# Requirements — Phase 5: Tools-centric agent backend

This document defines the requirements for transitioning the current placeholder backend agent tools and configuration to a more fully realized, tools-centric agent backend matching the pattern in `examples/create_agent_tools.ipynb`.

## 1. Scope

### In Scope
- **Re-implement All 6 Tools**: Replace placeholder tool definitions in `backend/app/tools.py` with the classroom-demo implementations defined in `examples/create_agent_tools.ipynb`:
  - `run_sql(query: str) -> str`: Simulates a read-only SQL tool over the demo sales CSV with mock schemas and responses.
  - `validate_answer(answer: str, evidence: str) -> str`: Critiques an answer for missing evidence or errors with full string logic.
  - `search_docs(query: str) -> str`: Searches internal documents for relevant context about Spec-Driven Development (returns `SDD_DOC_SUMMARY`).
  - `save_artifact(name: str, content: str) -> str`: Simulates saving an artifact with an explicit `name` and `content` parameter, returning a receipt.
  - `weather(location: str) -> str`: Gets deterministic demo weather for selected locations (New York, Delano, Minneapolis, Phoenix).
  - `web_search(query: str) -> str`: Searches a curated mock web index dictionary for classroom-safe demo results.
- **Update Tool Signatures**: Specifically, change `save_artifact` to take both `name` and `content` as inputs (instead of just `content`), and update any relevant backend models, agent calls, or tests that depend on it.
- **Agent Configuration Alignment**: Update the agent instantiation in `backend/app/agent.py` to use:
  - The exact system prompt matching `examples/create_agent_tools.ipynb`.
  - A temperature of `1.0`.
  - Proper mapping of all 6 tools.
  - Recursion limit set to `50`.
- **Backend Schema Verification**: Ensure `AutonomousAgentResponse` and metrics helper functions in `backend/app/helpers.py` perfectly parse and summarize the new tool calling patterns.
- **Streamlit Frontend Compatibility**: The Streamlit frontend should function perfectly with the updated tools and their outputs without needing major UI layout rewrites.

### Out of Scope
- Introducing actual database persistence, SQL execution, or vector search indexing (the tools must remain deterministic Python mock/teaching tools as defined in the notebook).
- Changing the Streamlit frontend layout structure or adding non-agent pages.
- Installing new external dependencies or libraries.

---

## 2. Decisions

### Tool Signature and Implementation Alignment
- **Decision**: Port the exact implementation and signatures from the notebook, including the 2-argument signature for `save_artifact(name: str, content: str)`.
- **Rationale**: This provides a 1:1 match with the classroom notebook `create_agent_tools.ipynb`, ensuring that students transitioning from the Jupyter environment to the full-stack app experience no friction or API mismatch.

### Test Strategy Adaptation
- **Decision**: Fully update the pytest unit test suite (`test_main.py` and `test_helpers.py`) to align with the new tool behaviors, ensuring that mock data, schemas, and assertions match the upgraded tool definitions.
- **Rationale**: Keeps the codebase's verification suite high-fidelity, preventing test rot and verifying that the backend integration is robust against future tool-centric changes.

### Agent System Prompt and Parameter Match
- **Decision**: Adopt the exact system prompt, temperature, and configuration from `create_agent_tools.ipynb`.
- **Rationale**: Preserves the precise classroom teaching context, ensuring the LLM is instructed identically to how it performs in the Jupyter notebook.

---

## 3. Context

### Stack Pointers and Existing Patterns
- The backend relies on `langchain-google-genai` and `langchain` with a structured response format.
- The model used is `gemini-3.5-flash` with a recursion limit of 50.
- All core agent execution happens via `run_agent(prompt: str)` defined in `backend/app/agent.py`.

### Tone Rules and Copy Style
- The agent acts as an autonomous classroom teaching assistant.
- Output text and final answers should be informative, technical, clear, and perfectly grounded in tool outputs. No ad-hoc assumptions should be fabricated.
