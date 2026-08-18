import os

from app.database import Base, engine
from app.models import Customer, Conversation, Message
from app.models.user import User


def pytest_configure():
    Base.metadata.create_all(bind=engine)


def pytest_runtest_teardown(item, nextitem):
    with engine.begin() as connection:
        # Delete dependent records first
        connection.execute(Message.__table__.delete())
        connection.execute(Conversation.__table__.delete())
        connection.execute(Customer.__table__.delete())
        connection.execute(User.__table__.delete())