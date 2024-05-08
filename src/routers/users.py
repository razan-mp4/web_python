from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import user_schema
from ..crud import user_crud
from ..dependencies import get_db, get_current_user, is_admin, is_super_admin

router = APIRouter()

@router.post("/", response_model=user_schema.User)
def create_user(user_data: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db, user_data)

@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    if is_super_admin(current_user):
        return user_crud.get_user(db, user_id)
    elif current_user.id == user_id:
        return user_crud.get_user(db, user_id)
    else:
        raise HTTPException(status_code=403, detail="User not authorized to access this user")

@router.put("/{user_id}", response_model=user_schema.User)
def update_user(user_id: int, user_data: user_schema.UserCreate, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    if is_super_admin(current_user):
        return user_crud.update_user(db, user_id, user_data)
    elif current_user.id == user_id:
        return user_crud.update_user(db, user_id, user_data)
    else:
        raise HTTPException(status_code=403, detail="User not authorized to update this user")

@router.delete("/{user_id}", response_model=user_schema.User)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    if is_super_admin(current_user):
        return user_crud.delete_user(db, user_id)
    elif current_user.id == user_id:
        return user_crud.delete_user(db, user_id)
    else:
        raise HTTPException(status_code=403, detail="User not authorized to delete this user")

# Endpoint accessible only to super admins to get all users
@router.get("/", response_model=list[user_schema.User])
def read_users(db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    if is_super_admin(current_user):
        return user_crud.get_all_users(db)
    else:
        raise HTTPException(status_code=403, detail="User not authorized to access all users")