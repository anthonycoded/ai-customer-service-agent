import os

os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://postgres:postgres@localhost:5433/"
    "ai_customer_service_test"
)


from app.database import Base, engine
from app.models import Customer, Conversation, Message


def pytest_configure():
    Base.metadata.create_all(bind=engine)