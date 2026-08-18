from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "email": "test.user@example.com",
            "password": "TestPassword123!",
        },
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test.user@example.com"
    assert "id" in data

    assert "password" not in data
    assert "hashed_password" not in data

def test_login():
    payload = {
        "email": "login.test@example.com",
        "password": "TestPassword123!",
    }

    register_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json=payload,
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0

def test_get_current_user():
    payload = {
        "email": "me.test@example.com",
        "password": "TestPassword123!",
    }

    register_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json=payload,
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == payload["email"]
    assert "hashed_password" not in data

def test_get_current_user_without_token():
    response = client.get("/auth/me")

    assert response.status_code == 401

def test_get_current_user_invalid_token():
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401