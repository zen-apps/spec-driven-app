"""Streamlit chat UI for the reference agent app (Phase 2).

A deliberately small, walk-through-able chat interface that talks to the Phase 1
backend over HTTP. For each turn it shows the agent's final answer as a chat
bubble, and a collapsible "Tool calls" panel built from the run metrics the
backend exposes.

Scope notes (see specs/2026-06-02-streamlit-frontend/requirements.md):
- This is frontend-only. It consumes the existing ``POST /chat`` contract and
  adds no backend code.
- The tool-calls view uses ONLY the metrics the API returns today
  (tool-call sequence, per-tool counts, totals). Per-call arguments and tool
  outputs are not exposed by ``/chat`` yet, so they are not shown here.
- Structured output and a standalone token/metrics panel are out of scope.
"""

import requests
import streamlit as st

# Backend location. Phase 1 publishes the backend on host port 8001 (-> container
# 8000). This is hardcoded on purpose to keep Phase 2 simple to read; Phase 3
# swaps this single line for the docker-compose service name (http://backend:8000).
BACKEND_URL = "http://localhost:8001"
CHAT_ENDPOINT = f"{BACKEND_URL}/chat"

# How long to wait on the backend before giving up. Agent runs can take a few
# seconds (model + tool calls), so allow generous headroom.
REQUEST_TIMEOUT_SECONDS = 120


class BackendError(Exception):
    """Raised when the backend is unreachable or returns a non-200 response.

    Carries a user-friendly message that is safe to show in the UI (no raw
    tracebacks).
    """


# ============================================================
# Backend client
# ============================================================

def call_agent(message: str) -> dict:
    """POST a single message to the backend and return the parsed JSON.

    The returned dict matches the backend ``ChatResponse``:
    ``final_answer`` (str), ``structured_response`` (dict), ``metrics`` (dict).

    Raises ``BackendError`` with a friendly message on connection failure or a
    non-200 status, so the UI can render it inline.
    """
    try:
        response = requests.post(
            CHAT_ENDPOINT,
            json={"message": message},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except requests.exceptions.RequestException:
        raise BackendError(
            f"Couldn't reach the backend at {BACKEND_URL} — is it running on "
            f"port 8001? (Try `make run`.)"
        )

    if response.status_code != 200:
        # Surface the backend's detail message if there is one, otherwise the code.
        detail = ""
        try:
            detail = response.json().get("detail", "")
        except ValueError:
            detail = response.text
        raise BackendError(
            f"The backend returned an error ({response.status_code})."
            + (f" {detail}" if detail else "")
        )

    return response.json()


# ============================================================
# Tool-calls rendering
# ============================================================

def render_tool_calls(metrics: dict) -> None:
    """Render a turn's tool activity in a collapsible expander.

    Uses only fields guaranteed by the backend's ``build_api_metrics``:
    ``tool_call_count``, ``tool_call_sequence`` (ordered names), and
    ``tool_name_counts`` (per-tool counts).
    """
    metrics = metrics or {}
    sequence = metrics.get("tool_call_sequence", []) or []
    counts = metrics.get("tool_name_counts", {}) or {}
    total = metrics.get("tool_call_count", len(sequence))

    with st.expander(f"🔧 Tool calls ({total})"):
        if total == 0:
            st.caption("No tools were called for this answer.")
            return

        st.markdown("**Order of calls**")
        # A simple numbered trail reads clearly for students: 1. run_sql ...
        for step, name in enumerate(sequence, start=1):
            st.markdown(f"{step}. `{name}`")

        if counts:
            st.markdown("**Per-tool counts**")
            for name, count in counts.items():
                st.markdown(f"- `{name}` × {count}")


# ============================================================
# Chat UI
# ============================================================

def render_turn(turn: dict) -> None:
    """Re-render a single stored turn (user message + assistant reply)."""
    with st.chat_message("user"):
        st.markdown(turn["user"])

    with st.chat_message("assistant"):
        if turn.get("error"):
            st.error(turn["error"])
        else:
            st.markdown(turn["final_answer"])
            render_tool_calls(turn.get("metrics", {}))


def main() -> None:
    st.set_page_config(page_title="Reference Agent", page_icon="🤖")
    st.title("🤖 Reference Agent")
    st.caption(
        "Chat with the teaching agent. Each answer shows the tools the agent "
        "called to get there."
    )

    # Conversation history lives only in this browser session.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Redraw the whole conversation on each rerun.
    for turn in st.session_state.messages:
        render_turn(turn)

    prompt = st.chat_input("Ask the agent…")
    if not prompt:
        return

    # Show the user's message immediately.
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call the backend and show the assistant's reply.
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                result = call_agent(prompt)
            except BackendError as exc:
                error_message = str(exc)
                st.error(error_message)
                st.session_state.messages.append(
                    {"user": prompt, "error": error_message}
                )
                return

        final_answer = result.get("final_answer", "")
        metrics = result.get("metrics", {})
        st.markdown(final_answer)
        render_tool_calls(metrics)

    # Persist the completed turn so it re-renders on the next run.
    st.session_state.messages.append(
        {"user": prompt, "final_answer": final_answer, "metrics": metrics}
    )


if __name__ == "__main__":
    main()
