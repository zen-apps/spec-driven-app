# Validation — Backend: full LangChain agent endpoint (Phase 2)

## Automated

No pytest unit testing is introduced in this phase (mocked tests arrive in Phase 3). The automated validation is the build compilation itself:

- [ ] `docker-compose build` completes with exit code 0.
- [ ] No installation or import errors are generated in the backend container log.
- [ ] Requirements.txt successfully installs langchain modules without dependency conflicts.

## Manual

Launch the stack (`docker-compose up`) and perform the following verifications using `curl` or an API client (like Postman):

### 1. Minimal Smoke Request (No Tools Needed)

Send a generic conversational request that should not trigger any tool calls:
`curl -i -X POST http://localhost:8001/chat -H "Content-Type: application/json" -d '{"message": "State your name and say hello."}'`

Verify:
- [ ] Returns HTTP `200 OK`.
- [ ] Response contains `"response"` and `"metrics"` keys.
- [ ] `"response.final_answer"` contains a friendly greeting.
- [ ] `"response.task_completed"` is `true`.
- [ ] `"response.confidence"` is a float between 0.0 and 1.0.
- [ ] `"metrics.tool_calls"` is empty `[]`.
- [ ] `"metrics.token_totals.total_tokens"` is greater than 0.
- [ ] `"metrics.iterations"` is exactly 1 (only the final model call).

### 2. Multi-Tool Executing Request

Send a request designed to exercise the agent's autonomous planning and tool calls (derived from `create_agent.ipynb`):
`curl -i -X POST http://localhost:8001/chat -H "Content-Type: application/json" -d '{"message": "Search the web for \"latest on ai\" if it is hotter than 50 degrees in Delano."}'`

Verify:
- [ ] Returns HTTP `200 OK`.
- [ ] `"metrics.tool_calls"` contains at least two entries: one for `weather` (location "Delano") and one for `web_search` (query "latest on ai").
- [ ] `"response.tools_used"` contains `"weather"` and `"web_search"`.
- [ ] `"response.key_findings"` contains facts summarizing that Delano's weather is 60°F and that the latest on AI is OpenCode.
- [ ] `"metrics.iterations"` matches the reasoning loop steps (typically 3 steps).
- [ ] `"response.final_answer"` correctly answers the request using both tool results.

### 3. Graceful Downstream Error Handling (Mocking down state)

To verify the robust API-level error fallback, stop the compose stack, temporarily rename your local `credentials` folder or credentials JSON file, restart, and fire a chat request:
`curl -i -X POST http://localhost:8001/chat -H "Content-Type: application/json" -d '{"message": "Hello"}'`

Verify:
- [ ] Returns HTTP `500 Internal Server Error`.
- [ ] Response is valid JSON.
- [ ] `"detail"` contains a descriptive message indicating the authentication/connection error.
- [ ] `"response.final_answer"` contains a friendly error message starting with `"Error:"`.
- [ ] `"response.task_completed"` is `false`.
- [ ] `"response.confidence"` is exactly `0.0`.
- [ ] `"response.recommended_next_steps"` lists actionable troubleshooting tasks (e.g. checking credentials or env configuration).
- [ ] `"metrics.tool_calls"` is `[]` and token counts/iterations are `0`.

---

## Definition of Done

- All automated and manual verification checks above pass successfully.
- Code is fully integrated into the FastAPI backend service inside the `feature/backend-agent` branch.
- No dummy/placeholder files are left behind, and no unapproved libraries are introduced.
- The `specs/roadmap.md` Phase 2 entry remains untouched (it will be marked complete when this branch is implemented).
