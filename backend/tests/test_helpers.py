import pytest
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from app.helpers import (
    normalize_content,
    get_final_answer_from_messages,
    get_structured_response,
    get_final_answer,
    summarize_agent_metrics,
    AutonomousAgentResponse,
)


def test_normalize_content_string():
    """Verify normalize_content handles plain string content."""
    assert normalize_content("hello") == "hello"
    assert normalize_content("") == ""


def test_normalize_content_none():
    """Verify normalize_content handles None cleanly."""
    assert normalize_content(None) == ""


def test_normalize_content_list_blocks():
    """Verify normalize_content handles lists of blocks/dicts/strings."""
    content_list = [
        "plain string block",
        {"text": "block with text"},
        {"content": "block with content"},
        {"other": "generic block"},
    ]
    expected = (
        "plain string block\n"
        "block with text\n"
        "block with content\n"
        "{'other': 'generic block'}"
    )
    assert normalize_content(content_list) == expected


def test_get_final_answer_from_messages():
    """Verify extraction of the last non-empty AIMessage content."""
    messages = [
        HumanMessage(content="Hello"),
        AIMessage(content="First response"),
        ToolMessage(content="Tool output", tool_call_id="call_1"),
        AIMessage(content=""),  # Empty content, should skip
        AIMessage(content="Final response"),
    ]
    result = {"messages": messages}
    assert get_final_answer_from_messages(result) == "Final response"


def test_get_final_answer_from_messages_empty():
    """Verify empty behavior when no valid messages exist."""
    assert get_final_answer_from_messages({}) == ""
    assert get_final_answer_from_messages({"messages": []}) == ""
    assert get_final_answer_from_messages({"messages": [HumanMessage(content="Hello")]}) == ""


def test_get_structured_response():
    """Verify extraction of AutonomousAgentResponse from result dict."""
    response_obj = AutonomousAgentResponse(
        final_answer="The answer",
        task_completed=True,
        reasoning_summary="Reasoned",
        tools_used=["weather"],
        key_findings=["Finding"],
        limitations=[],
        recommended_next_steps=[],
        confidence=0.9,
    )
    result = {"structured_response": response_obj}
    assert get_structured_response(result) == response_obj
    assert get_structured_response({}) is None


def test_get_final_answer():
    """Verify get_final_answer prioritizes structured_response and falls back to messages."""
    response_obj = AutonomousAgentResponse(
        final_answer="Structured answer",
        task_completed=True,
        reasoning_summary="Reasoned",
        tools_used=[],
        key_findings=[],
        limitations=[],
        recommended_next_steps=[],
        confidence=0.9,
    )
    messages = [AIMessage(content="Message answer")]
    
    # Priority 1: structured_response
    assert get_final_answer({"structured_response": response_obj, "messages": messages}) == "Structured answer"
    
    # Priority 2: message fallback
    assert get_final_answer({"messages": messages}) == "Message answer"
    
    # Priority 3: empty fallback
    assert get_final_answer({}) == ""


def test_summarize_agent_metrics_comprehensive():
    """Verify metrics summary with custom message sequence, tool calls, and token usage."""
    messages = [
        HumanMessage(content="Tell me the weather in Delano and search for local news."),
        AIMessage(
            content="",
            tool_calls=[
                {"name": "weather", "args": {"location": "Delano"}, "id": "call_1"},
            ],
            usage_metadata={"input_tokens": 100, "output_tokens": 10, "total_tokens": 110},
        ),
        ToolMessage(content="Weather is fog, 60F", tool_call_id="call_1"),
        AIMessage(
            content="",
            tool_calls=[
                {"name": "web_search", "args": {"query": "Delano news"}, "id": "call_2"},
            ],
            usage_metadata={"input_tokens": 200, "output_tokens": 15, "total_tokens": 215},
        ),
        ToolMessage(content="No news today", tool_call_id="call_2"),
        AIMessage(
            content="Final output",
            usage_metadata={"input_tokens": 300, "output_tokens": 20, "total_tokens": 320},
        ),
    ]

    structured = AutonomousAgentResponse(
        final_answer="Fog, 60F and no news.",
        task_completed=True,
        reasoning_summary="Checked weather and news.",
        tools_used=["weather", "web_search"],
        key_findings=["60F in Delano", "no news today"],
        limitations=[],
        recommended_next_steps=[],
        confidence=0.85,
    )

    result = {
        "messages": messages,
        "structured_response": structured,
    }

    metrics = summarize_agent_metrics(result)

    # Basic counts
    assert metrics["message_count"] == 6
    assert metrics["human_message_count"] == 1
    assert metrics["ai_message_count"] == 3
    assert metrics["tool_message_count"] == 2
    assert metrics["agent_iterations"] == 3

    # Token aggregations
    assert metrics["input_tokens"] == 100 + 200 + 300
    assert metrics["output_tokens"] == 10 + 15 + 20
    assert metrics["total_tokens"] == 110 + 215 + 320
    assert metrics["model_calls_with_usage"] == 3

    # Tool calls & structure
    assert metrics["tool_call_count"] == 2
    assert metrics["tool_call_sequence"] == ["weather", "web_search"]
    assert metrics["tool_name_counts"] == {"weather": 1, "web_search": 1}
    assert metrics["unique_tools_used"] == 2

    # Verify message index and step assignment
    assert metrics["tool_calls"][0] == {
        "name": "weather",
        "args": {"location": "Delano"},
        "id": "call_1",
        "message_index": 1,
        "ai_step": 1,
    }
    assert metrics["tool_calls"][1] == {
        "name": "web_search",
        "args": {"query": "Delano news"},
        "id": "call_2",
        "message_index": 3,
        "ai_step": 2,
    }

    # Verify structured output fields extraction
    assert metrics["has_structured_response"] is True
    assert metrics["structured_response_type"] == "AutonomousAgentResponse"
    assert metrics["structured_response"] == structured
    assert metrics["structured_response_dict"]["final_answer"] == "Fog, 60F and no news."
    assert metrics["final_answer"] == "Fog, 60F and no news."

