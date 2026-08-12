from fastapi import FastAPI

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