from unittest.mock import patch
import pytest
from app.helpers import AutonomousAgentResponse
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


def test_health_endpoint(app_client):
    """Verify that GET /health returns 200 OK and {"status": "ok"}."""
    response = app_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint_success(app_client):
    """Verify that POST /chat handles successful agent runs with structured response."""
    mock_response_obj = AutonomousAgentResponse(
        final_answer="The local weather in Delano is foggy and 60°F.",
        task_completed=True,
        reasoning_summary="Checked the weather for Delano using the weather tool.",
        tools_used=["weather"],
        key_findings=["Delano is 60°F.", "Conditions: foggy."],
        limitations=[],
        recommended_next_steps=[],
        confidence=0.95,
    )

    mock_messages = [
        HumanMessage(content="What is the weather in Delano?"),
        AIMessage(
            content="",
            tool_calls=[
                {"name": "weather", "args": {"location": "Delano"}, "id": "call_1"},
            ],
            usage_metadata={"input_tokens": 100, "output_tokens": 10, "total_tokens": 110},
        ),
        ToolMessage(content="Weather in Delano is foggy and 60°F.", tool_call_id="call_1"),
        AIMessage(
            content="The local weather in Delano is foggy and 60°F.",
            usage_metadata={"input_tokens": 150, "output_tokens": 20, "total_tokens": 170},
        ),
    ]

    mock_result = {
        "messages": mock_messages,
        "structured_response": mock_response_obj,
    }

    # Patch the run_agent call imported in app.main
    with patch("app.main.run_agent", return_value=mock_result) as mock_run:
        response = app_client.post("/chat", json={"message": "What is the weather in Delano?"})
        
        # Verify call arguments
        mock_run.assert_called_once_with("What is the weather in Delano?")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify the structure and values of response
        assert "response" in data
        assert "metrics" in data
        
        resp_data = data["response"]
        assert resp_data["final_answer"] == "The local weather in Delano is foggy and 60°F."
        assert resp_data["task_completed"] is True
        assert resp_data["reasoning_summary"] == "Checked the weather for Delano using the weather tool."
        assert resp_data["tools_used"] == ["weather"]
        assert resp_data["key_findings"] == ["Delano is 60°F.", "Conditions: foggy."]
        assert resp_data["limitations"] == []
        assert resp_data["recommended_next_steps"] == []
        assert resp_data["confidence"] == 0.95
        
        # Verify the structure and values of metrics
        metrics_data = data["metrics"]
        assert metrics_data["iterations"] == 2
        assert metrics_data["token_totals"] == {
            "input_tokens": 250,
            "output_tokens": 30,
            "total_tokens": 280,
        }
        assert len(metrics_data["tool_calls"]) == 1
        assert metrics_data["tool_calls"][0]["name"] == "weather"
        assert metrics_data["tool_calls"][0]["args"] == {"location": "Delano"}
        assert metrics_data["tool_calls"][0]["ai_step"] == 1


def test_chat_endpoint_error_handling(app_client):
    """Verify that POST /chat handles downstream errors gracefully with HTTP 500."""
    with patch("app.main.run_agent", side_effect=ValueError("API key invalid or expired")) as mock_run:
        response = app_client.post("/chat", json={"message": "Hello"})
        
        mock_run.assert_called_once_with("Hello")
        
        assert response.status_code == 500
        data = response.json()
        
        # Verify general error structure
        assert "detail" in data
        assert "Failed to call Google Gemini API: API key invalid or expired" in data["detail"]
        
        # Verify fallback response
        assert "response" in data
        resp_data = data["response"]
        assert resp_data["final_answer"] == "Error: Failed to process the request due to a downstream API failure."
        assert resp_data["task_completed"] is False
        assert "API key invalid or expired" in resp_data["reasoning_summary"]
        assert resp_data["tools_used"] == []
        assert resp_data["confidence"] == 0.0
        assert len(resp_data["recommended_next_steps"]) > 0
        
        # Verify zeroed metrics
        assert "metrics" in data
        metrics_data = data["metrics"]
        assert metrics_data["iterations"] == 0
        assert metrics_data["tool_calls"] == []
        assert metrics_data["token_totals"] == {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
        }
