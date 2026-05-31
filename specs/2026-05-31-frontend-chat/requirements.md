# Requirements — Frontend Chat UI (Phase 4)

Build the real Streamlit experience on top of the working backend, allowing students to interact with the LangChain agent end to end and observe its inner workings (tool calls, token counts, and reasoning process) directly in the UI.

Traces to: `specs/roadmap.md` → *Phase 4 — Frontend: chat UI against the real backend*.

## Scope

### In scope (roadmap baseline)

- **Streamlit Chat Interface**:
  - A clean, standard chat interface utilizing `st.chat_input` and `st.chat_message`.
  - Maintain persistent session history in `st.session_state` so past conversation turns remain visible across user interactions.
  
- **Structured Fields & Run Metrics Rendering**:
  - In each assistant reply bubble, display the `final_answer` at the top as primary content.
  - Directly beneath the `final_answer` in the bubble, render an expander labeled **"Agent Diagnostics"** to inspect:
    - **Task Success & Confidence**: Display `task_completed` (using a visual indicator or emoji) and `confidence` (rendered as a percentage or progress bar).
    - **Reasoning Summary**: Render the high-level `reasoning_summary` explaining the agent's path.
    - **Key Findings**: Render `key_findings` as a bulleted list.
    - **Limitations**: Render `limitations` as a bulleted list if any are returned.
    - **Recommended Next Steps**: Render `recommended_next_steps` as a bulleted list.
    - **Tool Loop Sequence**: Display the count of `iterations` and a chronological list of `tools_used` / tool calls that were executed in the autonomous loop.
    - **Token Usage**: Display `input_tokens`, `output_tokens`, and `total_tokens` formatted nicely.

- **Backend Integration (`requests`)**:
  - Add `requests==2.31.0` to `frontend/requirements.txt`.
  - Perform `POST` requests to `BACKEND_URL + "/chat"` sending `{"message": user_message}`.
  - Retrieve the backend address via the `BACKEND_URL` environment variable, falling back gracefully to `http://localhost:8001` or `http://backend:8000` (within the Docker network).

- **Robust Error Handling & Fallback Rendering**:
  - Handle communication timeouts, connection issues, or HTTP 500 error responses from the backend.
  - If the backend returns a 500 with the detailed fallback schema, render that fallback data nicely (retaining the "Agent Diagnostics" expander to show recommendations like credentials mounting).
  - If the backend is completely unreachable, generate an in-app fallback schema describing the failure and showing instructions on how to start the backend container.

### Out of scope

- **Persistent Database Chat History**: There is no database; historical messages live only in memory via `st.session_state` and are lost when the browser tab is refreshed.
- **User Authentication**: Anyone who can reach the Streamlit port can chat.
- **Streaming Responses**: Due to the structured JSON output requirement from the agent, we render responses synchronously once the backend completes its full execution loop.

---

### Data / interface shape

The frontend communicates with the backend `/chat` endpoint.

#### API Request (sent by frontend):
- **Method**: `POST`
- **URL**: `${BACKEND_URL}/chat`
- **Body**:
```json
{
  "message": "User's query"
}
```

#### Successful API Response (received by frontend):
Refer to the schema returned by the backend:
```json
{
  "response": {
    "final_answer": "...",
    "task_completed": true,
    "reasoning_summary": "...",
    "tools_used": ["..."],
    "key_findings": ["..."],
    "limitations": [],
    "recommended_next_steps": [],
    "confidence": 0.95
  },
  "metrics": {
    "tool_calls": [...],
    "token_totals": {
      "input_tokens": 120,
      "output_tokens": 80,
      "total_tokens": 200
    },
    "iterations": 1
  }
}
```

---

## Decisions

| Decision | Choice | Why |
|:---|:---|:---|
| **API Client** | `requests==2.31.0` | Standard, lightweight, highly readable HTTP library in Python for making synchronous REST calls from Streamlit to FastAPI. |
| **Diagnostics Placement** | Collapsible `st.expander` under each response | Direct result of user interview feedback (Q1). Keeps the chat window clean and uncluttered while ensuring detailed agent telemetry is immediately inspectable. |
| **History Schema** | Store full JSON payloads in `st.session_state["messages"]` | User interview feedback (Q2). Allows Streamlit to reconstruct the detailed "Agent Diagnostics" expander for historical messages when the app re-renders. |
| **UI Aesthetics** | Minimal, clean standard Streamlit chat theme | User interview feedback (Q3). Emphasizes raw metrics readability and structured agent telemetry without ad-hoc clutter or distraction. |

---

## Context

- **Statelessness**: Remind users that reloading the page resets the session history.
- **Docker Compose Networking**: The Streamlit container uses `http://backend:8000` because they reside on the same docker-compose network, while local host debugging uses `http://localhost:8001`.
- **Educational Value**: Visualizing the token totals and tool list helps learners understand that autonomous agents run multiple background loops before returning.
