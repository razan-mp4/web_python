from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

from .patient_schema import PatientCreate

class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool
    role: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None

class User(UserBase):
    _id: ObjectId

    class Config:
        orm_mode = True

class UserSignIn(BaseModel):
    pass
class UserSignUp(UserCreate, PatientCreate):
    pass