from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from pymongo.collection import Collection

from .schemas.user_schema import User
from .database import mongo_db


# Get the MongoDB collection for users
users_collection: Collection = mongo_db['users']

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)

# Secret key to sign JWT tokens
SECRET_KEY = "a3cbnM0yaxO5Syeqbsmc0NxdyaLxpn5p0KpfGbhaRUY" 
ALGORITHM = "HS256"

# Dependency to get the current user from JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = users_collection.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return user

# Function to check if user is an admin
def is_admin(user: User = Depends(get_current_user)):
    if user["role"] == "admin" or user["role"] == "super_admin":
        return True
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to perform this action.")

# Function to check if user is a super admin
def is_super_admin(user: User = Depends(get_current_user)):
    if user["role"] == "super_admin":
        return True
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to perform this action.")

# Function to check if user is a patient
def is_user(user: User = Depends(get_current_user)):
    if user["role"] == "user":
        return True
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to perform this action.")

# Function to check if user is authenticated
def is_authenticated(user: User = Depends(get_current_user)):
    pass
