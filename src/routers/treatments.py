from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import treatment_schema
from ..crud import treatment_crud
from ..dependencies import get_db, get_current_user, is_admin

router = APIRouter()

@router.post("/", response_model=treatment_schema.Treatment)
def create_treatment(treatment_data: treatment_schema.TreatmentCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if not is_admin(user=user):
        raise HTTPException(status_code=403, detail="Only admins can add treatments")
    return treatment_crud.create_treatment(db, treatment_data)

@router.get("/{treatment_id}", response_model=treatment_schema.Treatment)
def read_treatment(treatment_id: int, db: Session = Depends(get_db)):
    db_treatment = treatment_crud.get_treatment(db, treatment_id)
    if db_treatment is None:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return db_treatment

@router.get("/", response_model=list[treatment_schema.Treatment])
def read_treatments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    treatments = treatment_crud.get_treatments(db, skip=skip, limit=limit)
    return treatments

@router.put("/{treatment_id}", response_model=treatment_schema.Treatment)
def update_treatment(treatment_id: int, treatment_data: treatment_schema.TreatmentCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if not is_admin(user=user):
        raise HTTPException(status_code=403, detail="Only admins can update treatments")
    db_treatment = treatment_crud.update_treatment(db, treatment_id, treatment_data)
    if db_treatment is None:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return db_treatment

@router.delete("/{treatment_id}", response_model=treatment_schema.Treatment)
def delete_treatment(treatment_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if not is_admin(user=user):
        raise HTTPException(status_code=403, detail="Only admins can delete treatments")
    db_treatment = treatment_crud.delete_treatment(db, treatment_id)
    if db_treatment is None:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return db_treatment
