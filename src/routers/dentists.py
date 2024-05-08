from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import dentist_schema
from ..crud import dentist_crud
from ..dependencies import get_db, get_current_user, is_admin

router = APIRouter()

@router.post("/", response_model=dentist_schema.Dentist)
def create_dentist(dentist_data: dentist_schema.DentistCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if not is_admin(user=user):
        raise HTTPException(status_code=403, detail="Only admins can add dentists")
    db_dentist = dentist_crud.get_dentist_by_email(db, email=dentist_data.email)
    if db_dentist:
        raise HTTPException(status_code=400, detail="Email already registered")
    return dentist_crud.create_dentist(db, dentist_data)

@router.put("/{dentist_id}", response_model=dentist_schema.Dentist)
def update_dentist(dentist_id: int, dentist_data: dentist_schema.DentistCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if not is_admin(user=user):
        raise HTTPException(status_code=403, detail="Only admins can update dentists")
    db_dentist = dentist_crud.update_dentist(db, dentist_id, dentist_data)
    if db_dentist is None:
        raise HTTPException(status_code=404, detail="Dentist not found")
    return db_dentist

@router.delete("/{dentist_id}", response_model=dentist_schema.Dentist)
def delete_dentist(dentist_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if not is_admin(user=user):
        raise HTTPException(status_code=403, detail="Only admins can delete dentists")
    db_dentist = dentist_crud.delete_dentist(db, dentist_id)
    if db_dentist is None:
        raise HTTPException(status_code=404, detail="Dentist not found")
    return db_dentist

@router.get("/{dentist_id}", response_model=dentist_schema.Dentist)
def read_dentist(dentist_id: int, db: Session = Depends(get_db)):
    dentist = dentist_crud.get_dentist(db, dentist_id=dentist_id)
    if not dentist:
        raise HTTPException(status_code=404, detail="Dentist not found")
    return dentist

@router.get("/", response_model=list[dentist_schema.Dentist])
def read_dentists(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    dentists = dentist_crud.get_dentists(db, skip=skip, limit=limit)
    if not dentists:
        raise HTTPException(status_code=404, detail="Dentists not found")
    return dentists
