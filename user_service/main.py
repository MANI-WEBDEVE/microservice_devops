from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import datetime
import httpx
from database import USER, get_db
GREETING_URI='http://greeting-service:80'


app=FastAPI()


@app.get("/")
async def get_user(db :Session = Depends(get_db)):

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
        
    first_user=db.query(USER).first()
    return {
        "service": "user-service",
        "message": "User data fetched successfully",
        "greeting_from_other_service": greeting_message,
        "first_user_in_db": {
            "id": first_user.id,
            "name": first_user.name,
            "email": first_user.email
        } if first_user else None,
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.post("/users/")
async def user_create(name:str , email:str,db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(USER).filter(USER.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # New user create karna
    new_user = USER(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }


@app.get("/health")
def health_check():
    return {"status": "UP"}