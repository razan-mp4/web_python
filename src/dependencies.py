from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .crud.user_crud import get_user_by_username
from .schemas.user_schema import User
from .database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
    )

# Secret key (randomly genarated with python library "secrets") to sign JWT tokens
SECRET_KEY = "a3cbnM0yaxO5Syeqbsmc0NxdyaLxpn5p0KpfGbhaRUY" 
ALGORITHM = "HS256"

def get_session_local():
    yield SessionLocal()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to verify JWT token and get user details
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Function to check if user is an admin
def is_admin(user: User = Depends(get_current_user)):
    if user.role == "admin" or user.role == "super_admin":
        return True




# Function to check if user is an admin
def is_super_admin(user: User = Depends(get_current_user)):
    if user.role == "super_admin":
        return True
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to perform this action.")


# Function to check if user is patient
def is_user(user: User = Depends(get_current_user)):
    if user.role == "user":
        return True
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to perform this action.")

# Function to check if user is authenticated
def is_authenticated(user: User = Depends(get_current_user)):
    pass
