"""Run-metrics helpers, ported verbatim from `examples/create_agent.ipynb`.

These read from ``result["messages"]`` (the message trace), NOT from the
structured response — that is deliberate, because tool-call and token metrics
only live in the trace. The notebook's comment is preserved: do not switch the
metrics source to ``structured_response`` or you lose tool-call visibility.

``build_api_metrics`` is the one addition: it selects a JSON-serializable subset
of the metrics for the HTTP response (the raw ``structured_response`` instance
is not JSON-safe, so the API returns its ``model_dump()`` separately).
"""

from collections import Counter
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


# ============================================================
# Content helpers
# ============================================================

def normalize_content(content: Any) -> str:
    """
    Handles plain string content and list-of-blocks content.
    LangChain message content can be a string or structured blocks.
    """
    if content is None:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for block in content:
            if isinstance(block, str):
                parts.append(block)

            elif isinstance(block, dict):
                if "text" in block:
                    parts.append(str(block["text"]))
                elif "content" in block:
                    parts.append(str(block["content"]))
                else:
                    parts.append(str(block))

            else:
                parts.append(str(block))

        return "\n".join(parts)

    return str(content)


def get_final_answer_from_messages(result: dict) -> str:
    """
    Returns the final non-empty AIMessage content.

    Note:
    When using structured output, the final AIMessage.content may sometimes
    be empty or less useful depending on provider strategy. In that case,
    prefer result["structured_response"].final_answer for the final answer.
    """
    for msg in reversed(result.get("messages", [])):
        if isinstance(msg, AIMessage):
            text = normalize_content(msg.content).strip()
            if text:
                return text

    return ""


def get_structured_response(result: dict) -> Optional[Any]:
    """
    Returns the final Pydantic structured response if LangChain produced one.
    """
    return result.get("structured_response")


def get_final_answer(result: dict) -> str:
    """
    Preferred final-answer accessor.

    Uses structured_response.final_answer when available.
    Falls back to the final AIMessage content.
    """
    structured = get_structured_response(result)

    if structured is not None and hasattr(structured, "final_answer"):
        return structured.final_answer

    return get_final_answer_from_messages(result)


# ============================================================
# Metrics helpers
# ============================================================

def summarize_agent_metrics(result: dict) -> dict:
    """
    Summarize agent run metrics while preserving tool-call visibility.

    This function intentionally reads from result["messages"].
    Do not switch this to structured_response, or you will lose tool-call metrics.
    """
    messages = result.get("messages", [])

    ai_messages = [m for m in messages if isinstance(m, AIMessage)]
    tool_messages = [m for m in messages if isinstance(m, ToolMessage)]
    human_messages = [m for m in messages if isinstance(m, HumanMessage)]

    tool_calls = []

    token_totals = {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
    }

    model_calls_with_usage = 0

    token_usage_by_step = []

    ai_step = 0

    for message_index, msg in enumerate(messages):
        if not isinstance(msg, AIMessage):
            continue

        ai_step += 1

        # ----------------------------------------------------
        # Tool calls requested by the model
        # ----------------------------------------------------
        msg_tool_calls = getattr(msg, "tool_calls", None) or []

        for call in msg_tool_calls:
            tool_calls.append({
                "name": call.get("name"),
                "args": call.get("args"),
                "id": call.get("id"),
                "message_index": message_index,
                "ai_step": ai_step,
            })

        # ----------------------------------------------------
        # Token usage
        # ----------------------------------------------------
        usage = getattr(msg, "usage_metadata", None)

        step_input_tokens = 0
        step_output_tokens = 0
        step_total_tokens = 0

        if usage:
            model_calls_with_usage += 1

            step_input_tokens = usage.get("input_tokens", 0) or 0
            step_output_tokens = usage.get("output_tokens", 0) or 0
            step_total_tokens = usage.get("total_tokens", 0) or 0

            token_totals["input_tokens"] += step_input_tokens
            token_totals["output_tokens"] += step_output_tokens
            token_totals["total_tokens"] += step_total_tokens

        token_usage_by_step.append({
            "message_index": message_index,
            "ai_step": ai_step,
            "input_tokens": step_input_tokens,
            "output_tokens": step_output_tokens,
            "total_tokens": step_total_tokens,
            "tool_call_count": len(msg_tool_calls),
            "has_tool_calls": len(msg_tool_calls) > 0,
        })

    tool_name_counts = Counter(call["name"] for call in tool_calls)

    structured = get_structured_response(result)

    if structured is not None:
        try:
            structured_response_dict = structured.model_dump()
        except Exception:
            structured_response_dict = str(structured)
    else:
        structured_response_dict = None

    return {
        # Final answer
        "final_answer": get_final_answer(result),
        "final_answer_from_messages": get_final_answer_from_messages(result),

        # Structured response
        "has_structured_response": structured is not None,
        "structured_response_type": type(structured).__name__ if structured is not None else None,
        "structured_response": structured,
        "structured_response_dict": structured_response_dict,

        # Message counts
        "message_count": len(messages),
        "human_message_count": len(human_messages),
        "ai_message_count": len(ai_messages),
        "tool_message_count": len(tool_messages),

        # Agent loop metrics
        "agent_iterations": len(ai_messages),

        # Tool metrics
        "tool_call_count": len(tool_calls),
        "tool_name_counts": dict(tool_name_counts),
        "tool_calls": tool_calls,
        "tool_call_sequence": [call["name"] for call in tool_calls],
        "unique_tools_used": len(tool_name_counts),

        # Token metrics
        "model_calls_with_usage": model_calls_with_usage,
        "token_usage_by_step": token_usage_by_step,
        **token_totals,
    }


def get_tool_outputs(result: dict) -> List[dict]:
    """
    Extract tool outputs from ToolMessage objects.
    """
    outputs = []

    for message_index, msg in enumerate(result.get("messages", [])):
        if isinstance(msg, ToolMessage):
            content = normalize_content(msg.content)

            outputs.append({
                "message_index": message_index,
                "tool_name": getattr(msg, "name", None),
                "tool_call_id": getattr(msg, "tool_call_id", None),
                "output": content,
                "output_chars": len(content),
                "is_empty": len(content.strip()) == 0,
            })

    return outputs


# ============================================================
# API-facing metrics subset (JSON-safe)
# ============================================================

def build_api_metrics(result: dict) -> Dict[str, Any]:
    """Select a JSON-serializable subset of the run metrics for the HTTP response.

    Excludes the raw ``structured_response`` instance (not JSON-safe — the API
    returns its ``model_dump()`` separately) and the verbose per-call ``tool_calls``
    list (its detailed trace is a Phase 2 UI concern). Counts, the tool-name
    sequence, iterations, and token usage are kept.
    """
    metrics = summarize_agent_metrics(result)

    return {
        "agent_iterations": metrics["agent_iterations"],
        "message_count": metrics["message_count"],
        "human_message_count": metrics["human_message_count"],
        "ai_message_count": metrics["ai_message_count"],
        "tool_message_count": metrics["tool_message_count"],
        "tool_call_count": metrics["tool_call_count"],
        "tool_name_counts": metrics["tool_name_counts"],
        "tool_call_sequence": metrics["tool_call_sequence"],
        "unique_tools_used": metrics["unique_tools_used"],
        "model_calls_with_usage": metrics["model_calls_with_usage"],
        "token_usage_by_step": metrics["token_usage_by_step"],
        "input_tokens": metrics["input_tokens"],
        "output_tokens": metrics["output_tokens"],
        "total_tokens": metrics["total_tokens"],
    }
