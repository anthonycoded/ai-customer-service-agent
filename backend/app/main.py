from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine
from app.models import Customer, Conversation, Message
from app.api.customers import router as customers_router
from app.api.conversations import router as conversations_router
from app.api.messages import router as messages_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Customer Service Agent",
    description="AI-powered customer service API",
    version="0.1.0",
)
app.include_router(customers_router)
app.include_router(conversations_router)
app.include_router(messages_router)


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