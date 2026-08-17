from fastapi.testclient import TestClient

from app.main import app
from app.services.ai_service import AIService


client = TestClient(app)


def test_ai_generates_response(monkeypatch):

    customer_response = client.post(
        "/customers/",
        json={
            "name": "Test Customer",
            "email": "test.customer@example.com",
        },
    )

    assert customer_response.status_code in [200, 201]

    customer = customer_response.json()

    conversation_response = client.post(
        "/conversations/",
        json={
            "customer_id": customer["id"],
        },
    )

    assert conversation_response.status_code in [200, 201]

    conversation = conversation_response.json()

    conversation_id = conversation["id"]

    # Add a user message
    message_response = client.post(
        f"/conversations/{conversation_id}/messages",
        json={
            "role": "user",
            "content": "I need help with my order.",
        },
    )

    assert message_response.status_code in [200, 201]

    # Fake Ollama response
    def mock_generate_response(self, messages):
        return "I'd be happy to help with your order."

    monkeypatch.setattr(
        "app.ai.ollama_service.OllamaService.generate_response",
        mock_generate_response,
    )

    # Call AI endpoint
    response = client.post(
        f"/conversations/{conversation_id}/messages/ai"
    )

    assert response.status_code in [200, 201]

    data = response.json()

    assert data["role"] == "assistant"
    assert data["content"] == (
        "I'd be happy to help with your order."
    )
    assert data["conversation_id"] == conversation_id

def mock_generate_response(self, messages):
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"

    return "Mock response"

def test_ai_uses_conversation_history(monkeypatch):
    customer_response = client.post(
        "/customers/",
        json={
            "name": "Test Customer",
            "email": "test.customer@example.com",
        },
    )

    assert customer_response.status_code in [200, 201]

    customer = customer_response.json()

    conversation_response = client.post(
        "/conversations/",
        json={
            "customer_id": customer["id"],
        },
    )

    assert conversation_response.status_code in [200, 201]

    conversation = conversation_response.json()
    conversation_id = conversation["id"]

    # First message
    client.post(
        f"/conversations/{conversation_id}/messages",
        json={
            "role": "user",
            "content": "My order number is 12345.",
        },
    )

    # Second message
    client.post(
        f"/conversations/{conversation_id}/messages",
        json={
            "role": "assistant",
            "content": "Thank you. I have your order number.",
        },
    )

    # New user message
    client.post(
        f"/conversations/{conversation_id}/messages",
        json={
            "role": "user",
            "content": "Can you check its status?",
        },
    )

    captured_messages = []

    def mock_generate_response(self, messages):
        captured_messages.extend(messages)

        return "Your order status is being checked."

    monkeypatch.setattr(
        "app.ai.ollama_service.OllamaService.generate_response",
        mock_generate_response,
    )

    response = client.post(
        f"/conversations/{conversation_id}/messages/ai"
    )

    assert response.status_code in [200, 201]

    # Verify system prompt exists
    assert captured_messages[0]["role"] == "system"

    # Verify conversation history was sent to the AI
    assert captured_messages[1]["role"] == "user"
    assert captured_messages[1]["content"] == (
        "My order number is 12345."
    )

    assert captured_messages[2]["role"] == "assistant"
    assert captured_messages[2]["content"] == (
        "Thank you. I have your order number."
    )

    assert captured_messages[3]["role"] == "user"
    assert captured_messages[3]["content"] == (
        "Can you check its status?"
    )

    # Verify AI response
    data = response.json()

    assert data["role"] == "assistant"
    assert data["content"] == (
        "Your order status is being checked."
    )