from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import mongo_db
from ..crud import user_crud
from ..schemas import user_schema
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.post("/", response_model=user_schema.User)
def signup(user_data: user_schema.UserCreate):
    # Check if the email already exists
    existing_user = mongo_db['users'].find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Hash the password
    hashed_password = pwd_context.hash(user_data.password)

    # Create the new user document
    new_user = {
        "username": user_data.username,
        "email": user_data.email,
        "password": hashed_password,
        "is_active": True,
        "role": user_data.role  
    }
    
    # Insert the new user document into the MongoDB collection
    result = mongo_db['users'].insert_one(new_user)
    
    # Retrieve the inserted user document
    inserted_user = mongo_db['users'].find_one({"_id": result.inserted_id})
    
    # Return the inserted user document as the response
    return inserted_user
