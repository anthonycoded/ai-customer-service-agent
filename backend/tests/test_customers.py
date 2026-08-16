from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_customer():
    response = client.post(
        "/customers/",
        json={
            "name": "Ttested Customer",
            "email": "ttested.customer@example.com",
        },
    )

    assert response.status_code in [200, 201]

    data = response.json()

    assert data["name"] == "Ttested Customer"
    assert data["email"] == "ttested.customer@example.com"
    assert "id" in data


def test_get_customer():
    response = client.post(
        "/customers/",
        json={
            "name": "Retrievalss Customer",
            "email": "retrievalss@example.com",
        },
    )

    assert response.status_code in [200, 201]

    customer = response.json()

    customer_id = customer["id"]

    response = client.get(
        f"/customers/{customer_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == customer_id
    assert data["name"] == "Retrievalss Customer"
    assert data["email"] == "retrievalss@example.com"