from fastapi import FastAPI
import datetime
import httpx

GREETING_URI='http://greeting_service:8000'


app=FastAPI()


@app.get("/")
async def get_user():

    async with httpx.AsyncClient() as client:
        try:
            
            greeting_response = await client.get(f"{GREETING_URI}/")
            print(f"first response : {greeting_response}")
            greeting_data = greeting_response.json()
            print(f"second response : {greeting_data}")
            greeting_message = greeting_data.get("message", "No greeting available")
            print(f"third response : {greeting_message}")

        except Exception as e:
            greeting_message = f"Error calling greeting service: {str(e)}"
    return {
        "service": "user-service",
        "message": "User data fetched successfully",
        "greeting_from_other_service": greeting_message,
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat()
    }


@app.get("/health")
def health_check():
    return {"status": "UP"}