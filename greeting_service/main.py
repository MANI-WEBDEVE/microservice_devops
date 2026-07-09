from fastapi import FastAPI
import datetime

app = FastAPI()

@app.get("/")
def get_greeting():
    return {
        "service": "greeting-service",
        "message": "Hello! Welcome to our greeting service.",
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.get("/health")
def health_check():
    return {"status": "UP"}