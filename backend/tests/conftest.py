import os

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.models import Customer, Conversation, Message
from app.models.user import User
from app.main import app


def pytest_configure():
    Base.metadata.create_all(bind=engine)


def pytest_runtest_teardown(item, nextitem):
    with engine.begin() as connection:
        # Delete dependent records first
        connection.execute(Message.__table__.delete())
        connection.execute(Conversation.__table__.delete())
        connection.execute(Customer.__table__.delete())
        connection.execute(User.__table__.delete())


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    payload = {
        "email": "test.auth@example.com",
        "password": "TestPassword123!",
    }

    register_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert register_response.status_code in [201, 400]

    login_response = client.post(
        "/auth/login",
        json=payload,
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }