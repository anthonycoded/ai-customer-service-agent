from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_message(auth_headers):
    # Create customer
    customer_response = client.post(
        "/customers/",
        json={
            "name": "Message Customer",
            "email": "message@example.com",
        },
        headers=auth_headers
    )

    assert customer_response.status_code in [200, 201]

    customer = customer_response.json()

    # Create conversation
    conversation_response = client.post(
        "/conversations/",
        json={
            "customer_id": customer["id"],
        },
        headers=auth_headers
    )

    assert conversation_response.status_code in [200, 201]

    conversation = conversation_response.json()

    # Create message
    response = client.post(
        f"/conversations/{conversation['id']}/messages",
        json={
            "role": "user",
            "content": "I need help with my order.",
        },
        headers=auth_headers
    )

    assert response.status_code in [200, 201]

    message = response.json()

    assert "id" in message
    assert message["conversation_id"] == conversation["id"]
    assert message["role"] == "user"
    assert message["content"] == "I need help with my order."

def test_get_conversation_messages(auth_headers):
    customer_response = client.post(
        "/customers/",
        json={
            "name": "History Customer",
            "email": "history@example.com",
        },
        headers=auth_headers
    )

    assert customer_response.status_code in [200, 201]

    customer = customer_response.json()

    conversation_response = client.post(
        "/conversations/",
        json={
            "customer_id": customer["id"],
        },
        headers=auth_headers
    )

    assert conversation_response.status_code in [200, 201]

    conversation = conversation_response.json()

    conversation_id = conversation["id"]

    # Add first message
    client.post(
        f"/conversations/{conversation_id}/messages",
        json={
            "role": "user",
            "content": "Hello",
        },
        headers=auth_headers
    )

    # Add second message
    client.post(
        f"/conversations/{conversation_id}/messages",
        json={
            "role": "assistant",
            "content": "Hello! How can I help?",
        },
        headers=auth_headers
    )

    # Retrieve history
    response = client.get(
        f"/conversations/{conversation_id}/messages",
        headers=auth_headers
    )

    assert response.status_code == 200

    messages = response.json()

    assert len(messages) == 2
    assert messages[0]["content"] == "Hello"
    assert messages[1]["content"] == "Hello! How can I help?"

