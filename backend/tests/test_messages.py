from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_message():
    # Create customer
    customer_response = client.post(
        "/customers/",
        json={
            "name": "Message Customer",
            "email": "message@example.com",
        },
    )

    assert customer_response.status_code in [200, 201]

    customer = customer_response.json()

    # Create conversation
    conversation_response = client.post(
        "/conversations/",
        json={
            "customer_id": customer["id"],
        },
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
    )

    assert response.status_code in [200, 201]

    message = response.json()

    assert "id" in message
    assert message["conversation_id"] == conversation["id"]
    assert message["role"] == "user"
    assert message["content"] == "I need help with my order."

def test_get_conversation_messages():
    customer_response = client.post(
        "/customers/",
        json={
            "name": "History Customer",
            "email": "history@example.com",
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

    # Add first message
    client.post(
        f"/conversations/{conversation_id}/messages",
        json={
            "role": "user",
            "content": "Hello",
        },
    )

    # Add second message
    client.post(
        f"/conversations/{conversation_id}/messages",
        json={
            "role": "assistant",
            "content": "Hello! How can I help?",
        },
    )

    # Retrieve history
    response = client.get(
        f"/conversations/{conversation_id}/messages"
    )

    assert response.status_code == 200

    messages = response.json()

    assert len(messages) == 2
    assert messages[0]["content"] == "Hello"
    assert messages[1]["content"] == "Hello! How can I help?"

def test_get_conversation_messages():
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

    client.post(
        f"/conversations/{conversation_id}/messages",
        json={
            "role": "user",
            "content": "Hello",
        },
    )

    client.post(
        f"/conversations/{conversation_id}/messages",
        json={
            "role": "assistant",
            "content": "Hello! How can I help?",
        },
    )

    response = client.get(
        f"/conversations/{conversation_id}/messages"
    )

    assert response.status_code == 200

    messages = response.json()

    assert len(messages) == 2
    assert messages[0]["content"] == "Hello"
    assert messages[1]["content"] == "Hello! How can I help?"