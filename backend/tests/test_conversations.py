from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_conversation(auth_headers):
    # Create customer
    customer_response = client.post(
        "/customers/",
        json={
            "name": "Conversation Customer",
            "email": "conversation@example.com",
        },
        headers=auth_headers
    )

    assert customer_response.status_code in [200, 201]

    customer = customer_response.json()

    # Create conversation
    response = client.post(
        "/conversations/",
        json={
            "customer_id": customer["id"],
        },
        headers=auth_headers
    )

    assert response.status_code in [200, 201]

    data = response.json()

    assert "id" in data
    assert data["customer_id"] == customer["id"]