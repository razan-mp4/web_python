from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from bson.objectid import ObjectId
from ..schemas import user_schema
from ..dependencies import get_current_user, mongo_db

router = APIRouter()

# Get the MongoDB collection for users
users_collection: Collection = mongo_db['users']

# Endpoint to return information about the current user
@router.get("/", response_model=user_schema.User)
async def get_user(current_user: str = Depends(get_current_user)):
    user = users_collection.find_one({"_id": ObjectId(current_user["_id"])})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
