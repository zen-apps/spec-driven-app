# Validation — Phase 5: Tools-centric agent backend

This document specifies the validation criteria to ensure the new tools-centric backend functions correctly and matches the classroom notebook references.

## 1. Automated Validation

### Unit Tests
- Execute the test suite using `pytest backend/tests`.
- **Expected Outcome**: All tests pass successfully without any deprecation or runtime errors caused by modified signatures.

### Mock Agent Loop Checks
- Ensure test cases in `backend/tests/test_main.py` explicitly mock the updated tool signature:
  - `save_artifact` must be verified using a two-argument tool call schema (e.g. `name` and `content`).

---

## 2. Manual Validation

### Walkthrough & Behavior
1. Run `make build` and `make up` to spin up both Streamlit and FastAPI containers.
2. Navigate to Streamlit in the browser (default `http://localhost:8501`).
3. Send a request designed to exercise the agent's autonomous planning and tool calls (derived from `create_agent_tools.ipynb`):
   > "Use internal docs to explain SDD, check whether Delano is hotter than 50 degrees, search the web for latest on AI if it is, use the sales tool to identify the top revenue product, validate the answer, and save a simulated artifact named sdd-demo-summary.md."
4. Verify that:
   - The final answer is displayed correctly in Streamlit.
   - Expand the **Agent Diagnostics** expander.
   - Verify that **Tools Triggered** lists the sequence of tools called.
   - Verify that **Token Usage** is recorded and non-zero.
   - Verify that the **Confidence Score** is displayed.

### Edge Cases
- Test a query with no tools (e.g., "Hello, what is your name?"):
  - Expected: The agent responds directly without triggering any tools, and diagnostics show `Tools Triggered: None`.
- Test query with incorrect SQL commands:
  - Expected: `run_sql` rejects commands with write operations like `INSERT` or `DROP`.

---

## 3. Tone and Copy Check
- Ensure that the agent does not output raw JSON as its main response unless requested.
- Ensure the diagnostics expander copy is clean and readable, matching the design of the Phase 4 Streamlit layout.

---

## 4. Definition of Done
1. Re-implemented all 6 tools in `backend/app/tools.py` matching the reference notebook.
2. Updated agent configuration in `backend/app/agent.py` matching the reference notebook.
3. Updated and verified pytest unit test suite runs and passes.
4. Streamlit frontend runs and communicates successfully with the updated backend.
5. All feature spec documents are completed and stored in the dated spec directory.
