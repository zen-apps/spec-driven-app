"""Streamlit frontend — Phase 4 Chat UI.

Allows users to chat with the FastAPI + LangChain agent, displaying the structured
final answer and detailed agent diagnostics (tools called, token usage, confidence, etc.).
"""

import os
import requests
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Spec-Driven App — Agent Chat",
    page_icon="🤖",
    layout="centered",
)

# 2. Session State Initialization
if "messages" not in st.session_state:
    st.session_state["messages"] = []


def clear_history():
    """Resets the chat history in the Streamlit session state."""
    st.session_state["messages"] = []
    st.rerun()


# 3. Sidebar Layout
with st.sidebar:
    st.title("🤖 Agent Workspace")
    st.markdown(
        """
        Welcome to the **Spec-Driven App**!
        
        This frontend interfaces directly with a **FastAPI + LangChain** backend service powered by **Google Gemini**.
        
        ### Diagnostics Features
        Under each response, you can expand **Agent Diagnostics** to view:
        - **Task completion & confidence**
        - **Reasoning summary**
        - **Key findings, limitations & next steps**
        - **Autonomous tool loop history**
        - **Input/Output token totals**
        """
    )
    st.markdown("---")
    st.button("🧹 Clear Chat History", on_click=clear_history, use_container_width=True)


# 4. Backend Communication Client
def send_chat_request(prompt: str) -> dict:
    """Sends a chat prompt to the backend and returns the response JSON.

    Handles connection errors and non-200 responses gracefully by generating
    or returning a matching fallback schema.
    """
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8001").rstrip("/")
    chat_endpoint = f"{backend_url}/chat"

    try:
        response = requests.post(chat_endpoint, json={"message": prompt}, timeout=60)

        # Attempt to parse JSON regardless of status code to fetch backend errors cleanly
        try:
            response_json = response.json()
        except ValueError:
            response_json = {}

        if response.status_code == 200:
            return response_json

        # If backend returned an error but provided the structured fallback, use it
        if "response" in response_json and "metrics" in response_json:
            return response_json

        # Otherwise, fabricate a descriptive fallback schema
        detail = response_json.get("detail", f"HTTP {response.status_code}")
        return {
            "response": {
                "final_answer": f"Error: Backend returned {response.status_code}",
                "task_completed": False,
                "reasoning_summary": f"FastAPI backend returned an unexpected status code. Details: {detail}",
                "tools_used": [],
                "key_findings": [],
                "limitations": ["Downstream service error."],
                "recommended_next_steps": [
                    "Check the backend container logs.",
                    "Verify backend service is running normally.",
                ],
                "confidence": 0.0,
            },
            "metrics": {
                "tool_calls": [],
                "token_totals": {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "total_tokens": 0,
                },
                "iterations": 0,
            },
        }

    except requests.exceptions.RequestException as e:
        # Gracefully handle backend connection failures
        return {
            "response": {
                "final_answer": "Error: Failed to connect to the backend.",
                "task_completed": False,
                "reasoning_summary": f"Could not establish a connection to the backend service at {backend_url}. The service might be starting up, offline, or misconfigured.",
                "tools_used": [],
                "key_findings": [],
                "limitations": ["Backend service is unreachable."],
                "recommended_next_steps": [
                    "Verify the backend container is running: `docker-compose ps`",
                    "Ensure you started the app with: `docker-compose up` or `make up`",
                    f"Check if BACKEND_URL environment variable is correct (current: {backend_url}).",
                ],
                "confidence": 0.0,
            },
            "metrics": {
                "tool_calls": [],
                "token_totals": {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "total_tokens": 0,
                },
                "iterations": 0,
            },
        }


# 5. Assistant Message Rendering Helper
def render_assistant_message(response_payload: dict):
    """Renders the assistant final answer and the collapsible diagnostics expander."""
    response_data = response_payload.get("response", {})
    metrics_data = response_payload.get("metrics", {})

    # Display final answer as primary content
    final_answer = response_data.get("final_answer", "")
    st.markdown(final_answer)

    # Render collapsible diagnostics expander
    with st.expander("🔍 Agent Diagnostics", expanded=False):
        # Header Row: Task Status & Confidence
        col1, col2 = st.columns(2)
        with col1:
            task_completed = response_data.get("task_completed", False)
            status_emoji = "✅" if task_completed else "❌"
            st.markdown(f"**Task Completed:** {status_emoji} {'Yes' if task_completed else 'No'}")
        with col2:
            confidence = response_data.get("confidence", 0.0)
            st.markdown(f"**Confidence:** {confidence * 100:.0f}%")
            st.progress(max(0.0, min(float(confidence), 1.0)))

        # Reasoning Summary
        st.markdown(f"**Reasoning Summary:**\n{response_data.get('reasoning_summary', '')}")

        # Key Findings
        findings = response_data.get("key_findings", [])
        if findings:
            st.markdown("**Key Findings:**")
            for f in findings:
                st.markdown(f"- {f}")

        # Limitations & Next Steps
        limitations = response_data.get("limitations", [])
        if limitations:
            st.markdown("**Limitations:**")
            for l in limitations:
                st.markdown(f"- {l}")

        next_steps = response_data.get("recommended_next_steps", [])
        if next_steps:
            st.markdown("**Recommended Next Steps:**")
            for s in next_steps:
                st.markdown(f"- {s}")

        st.markdown("---")
        st.markdown("**Execution & Token Metrics:**")

        # Iterations & Tools
        iterations = metrics_data.get("iterations", 0)
        st.markdown(f"- **Agent Iterations:** {iterations}")

        tools_used = response_data.get("tools_used", [])
        if tools_used:
            tools_seq = " ➔ ".join([f"`{t}`" for t in tools_used])
            st.markdown(f"- **Tools Triggered:** {tools_seq}")
        else:
            st.markdown("- **Tools Triggered:** None")

        # Token usage
        token_totals = metrics_data.get("token_totals", {})
        input_tokens = token_totals.get("input_tokens", 0)
        output_tokens = token_totals.get("output_tokens", 0)
        total_tokens = token_totals.get("total_tokens", 0)
        st.markdown(
            f"- **Token Usage:** {total_tokens:,} total (Input: {input_tokens:,} | Output: {output_tokens:,})"
        )


# 6. Main Interface Layout & Chat Thread
st.title("🤖 Gemini AI Assistant")
st.write("Interact with the autonomous LangChain agent and inspect its live execution telemetry.")

# Render existing messages from session state
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            render_assistant_message(message["content"])

# Handle new user inputs
if prompt := st.chat_input("Ask the agent anything..."):
    # Render user prompt immediately to UI
    with st.chat_message("user"):
        st.markdown(prompt)

    # Append user prompt to state
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Fetch and render assistant response
    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking and executing tools..."):
            response_payload = send_chat_request(prompt)
            render_assistant_message(response_payload)

    # Append assistant response payload to state
    st.session_state["messages"].append({"role": "assistant", "content": response_payload})

    # Rerun to lock in state and refresh the input field
    st.rerun()
