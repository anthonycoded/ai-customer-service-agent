from fastapi.testclient import TestClient

from app.main import app
from tests.conftest import auth_headers

client = TestClient(app)



def test_create_customer(auth_headers):

    response = client.post(
        "/customers",
        json={
            "name": "Tested Customer",
            "email": "tested.customer@example.com",
        },
        headers=auth_headers,
    )

    assert response.status_code in [200, 201]


def test_get_customer(auth_headers):

    create_response = client.post(
        "/customers",
        json={
            "name": "Retrieval Customer",
            "email": "retrieval@example.com",
        },
        headers=auth_headers,
    )

    assert create_response.status_code in [200, 201]

    customer_id = create_response.json()["id"]

    response = client.get(
        f"/customers/{customer_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == customer_id
    assert data["email"] == "retrieval@example.com"


def test_get_customer_requires_authentication():
    response = client.get("/customers/1")

    assert response.status_code == 401