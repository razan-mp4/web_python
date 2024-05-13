from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from bson.objectid import ObjectId
from ..schemas import user_schema
from ..crud import user_crud
from ..dependencies import get_current_user, is_super_admin, mongo_db

router = APIRouter()

# Get the MongoDB collection for users
users_collection: Collection = mongo_db['users']

@router.post("/", response_model=user_schema.User)
def create_user(user_data: user_schema.UserCreate):
    # Insert user_data into MongoDB users collection
    inserted_user = users_collection.insert_one(user_data.dict())
    return user_data

@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: str, current_user = Depends(get_current_user)):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Check if the current user is authorized to access this user
    if not is_super_admin(current_user) and str(user["_id"]) != str(user_id):
        raise HTTPException(status_code=403, detail="User not authorized to access this user")
    return user

@router.put("/{user_id}", response_model=user_schema.User)
def update_user(user_id: str, user_data: user_schema.UserCreate, current_user = Depends(get_current_user)):
    # Update user_data in MongoDB users collection
    updated_user = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_data.dict()})
    if updated_user.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

@router.delete("/{user_id}", response_model=user_schema.User)
def delete_user(user_id: str, current_user = Depends(get_current_user)):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    # Delete user from MongoDB users collection
    deleted_user = users_collection.delete_one({"_id": ObjectId(user_id)})
    if deleted_user.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[user_schema.User])
def read_users(current_user = Depends(get_current_user)):
    # Only super admins can access all users
    if not is_super_admin(current_user):
        raise HTTPException(status_code=403, detail="User not authorized to access all users")
    # Retrieve all users from MongoDB users collection
    all_users = users_collection.find()
    return list(all_users)
