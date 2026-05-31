# Plan — Frontend Chat UI (Phase 4)

The plan systematically transitions the frontend from a static placeholder page to a fully operational, responsive chat interface communicating with our FastAPI + LangChain agent.

## 1. Environment & Dependency Setup (`frontend/requirements.txt`)

1. Update `frontend/requirements.txt` to append:
   - `requests==2.31.0`
2. Run local install of dependencies if needed or prepare Docker configurations.

## 2. Session State & Basic Layout Structure (`frontend/app.py`)

1. Initialize `st.session_state` keys:
   - `messages`: a list of dictionary items representing past turns. Each turn should contain:
     - `role`: either `"user"` or `"assistant"`.
     - `content`: the message content string (or full API dictionary response for the assistant).
2. Set up page configuration:
   - Page Title: `"Spec-Driven App — Agent Chat"`
   - Layout: `"centered"` or as per standard style.
3. Add a clear, brief header explaining the app.
4. Add a "Clear History" button in the sidebar or page to allow resetting `st.session_state["messages"]`.

## 3. Backend Communication Client (`frontend/app.py`)

1. Add a helper function `send_chat_request(prompt: str) -> dict` that:
   - Resolves the API URL using `os.getenv("BACKEND_URL", "http://localhost:8001")`.
   - Sends a `POST` request to `{BACKEND_URL}/chat` with payload `{"message": prompt}`.
   - Sets a reasonable timeout (e.g., 60 seconds) because agent loops can take some time.
   - Checks the response status code:
     - If `200 OK`, returns the JSON dictionary directly.
     - If `500` or other error code, returns the fallback JSON payload provided by the backend.
   - Implements a robust `try-except` block for connection failures (e.g. backend is completely down):
     - Catches `requests.exceptions.RequestException`.
     - Returns a simulated error JSON matching the backend's fallback structure (setting `task_completed=False`, `confidence=0.0`, and explaining in `reasoning_summary` or `recommended_next_steps` that the backend service might be offline or starting up).

## 4. Chat Interface and Diagnostics Expander (`frontend/app.py`)

1. **History Rendering Loop**:
   - Loop through `st.session_state["messages"]`.
   - Render user messages cleanly using `st.chat_message("user")`.
   - Render assistant messages using `st.chat_message("assistant")`:
     - Display the `final_answer` content at the top.
     - Add a collapsible `st.expander("Agent Diagnostics")`.
     - Inside the expander, render structured metadata:
       - Status Indicators: "Success: Yes" (or green emoji) / "No" (red emoji), and "Confidence: XX%".
       - Reasoning Summary.
       - Key Findings (bulleted).
       - Limitations (bulleted) and Recommended Next Steps (bulleted).
       - Execution Metrics: Iterations count, tool sequence (e.g., joined by arrows or bulleted list), and token usage (Input, Output, Total).
2. **Chat Input Handling**:
   - Capture user input via `st.chat_input("Ask the agent anything...")`.
   - When input is submitted:
     - Immediately append user turn to `st.session_state["messages"]` and display it in the chat container.
     - Show a loading spinner (`st.spinner("Agent is thinking and executing tools...")`) while calling `send_chat_request`.
     - Invoke the API client.
     - Append the API response dictionary as the assistant's turn in `st.session_state["messages"]`.
     - Force a Streamlit rerun/refresh (`st.rerun()`) to render the updated conversation.

## 5. Verification & Container Build

1. Rebuild the frontend and backend container images via `docker-compose build`.
2. Spin up the containers: `docker-compose up`.
3. Check the Streamlit URL (usually `http://localhost:8501`) to verify the interface comes up.
4. Interact with the chat interface to verify that:
   - Real Gemini/LangChain agent responses return and render properly.
   - Token counts, iteration metrics, and tool logs match the actual background run.
   - Robust error scenarios can be gracefully visualized (e.g., by temporarily shutting down the backend container and verifying the frontend displays the simulated unreachable state nicely).
