from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine
from app.models import Customer, Conversation, Message


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Customer Service Agent",
    description="AI-powered customer service API",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-customer-service-agent",
    }


@app.get("/health/database")
def database_health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }