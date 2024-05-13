from pymongo.collection import Collection
from bson.objectid import ObjectId
from ..schemas import user_schema
from ..dependencies import mongo_db

# MongoDB users collection
users_collection: Collection = mongo_db['users']

def initialize_user_collection(collection):
    global users_collection
    users_collection = collection

def create_user(user_data: user_schema.UserCreate):
    # Insert user_data into MongoDB users collection
    inserted_user = users_collection.insert_one(user_data.dict())
    return str(inserted_user.inserted_id)

def get_user_by_username(username: str):
    # Query MongoDB users collection for a user by username
    user = users_collection.find_one({"username": username})
    return user

def get_user_by_email(email: str):
    # Query MongoDB users collection for a user by email
    user = users_collection.find_one({"email": email})
    return user

def get_user_by_id(user_id: str):
    # Query MongoDB users collection for a user by ID
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    return user

def update_user(user_id: str, user_data: user_schema.UserUpdate):
    # Update user_data in MongoDB users collection
    updated_user = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_data.dict()})
    return updated_user.modified_count > 0

def delete_user(user_id: str):
    # Delete user from MongoDB users collection
    deleted_user = users_collection.delete_one({"_id": ObjectId(user_id)})
    return deleted_user.deleted_count > 0

def get_all_users():
    # Retrieve all users from MongoDB users collection
    all_users = users_collection.find()
    return list(all_users)

def check_super_admin_exists():
    # Check if super admin exists in MongoDB users collection
    super_admin = users_collection.find_one({"role": "super_admin"})
    return super_admin is not None

def create_super_admin():
    # Create super admin in MongoDB users collection if not exists
    if not check_super_admin_exists():
        super_admin_data = {
            "username": "super_admin",
            "email": "super_admin@example.com",
            "password": "$2b$12$86QXFH/oGwyPdl07a4QzjuchN5B.PKxNLErQbrUbzPnW63KZwEFTK",  # 'superadminpassword'
            "role": "super_admin",
            "is_active": True
        }
        inserted_super_admin = users_collection.insert_one(super_admin_data)
        return str(inserted_super_admin.inserted_id)
    else:
        return None
