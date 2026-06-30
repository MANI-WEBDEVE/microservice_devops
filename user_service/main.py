from fastapi import FastAPI
import datetime



app=FastAPI()


@app.get("/")
def get_user():
    return {
        "service": "user-service",
        "message": "User data fetched successfully",
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat()
    }


@app.get("/health")
def health_check():
    return {"status": "UP"}